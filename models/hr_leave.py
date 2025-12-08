# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email: sales@leap4logic.com
#################################################

import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.http import request


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    cancel_reason = fields.Char(string='Cancel Reason')
    description_name = fields.Char(string='name', store=True)

    @api.onchange('name')
    def _onchange_description_name(self):
        if self.name:
            self.description_name = self.name

    @api.model
    def create_hr_leave(self, leave_details):
        if not isinstance(leave_details, dict):
            raise ValidationError("Invalid data format. Expected a dictionary.")

        value = {
            "name": leave_details.get('name'),
            "description_name": leave_details.get('name'),
            "employee_id": leave_details.get('employee_id'),
            "holiday_status_id": leave_details.get('holiday_status_id'),
            "request_date_from": leave_details.get('date_from'),
            "date_from": leave_details.get('date_from'),
            "request_unit_half": leave_details.get('request_unit_half'),
            "request_unit_hours": leave_details.get('request_unit_hours'),
            "request_date_from_period": leave_details.get('request_date_from_period'),
            "request_hour_from": leave_details.get('request_hour_from'),
            "request_hour_to": leave_details.get('request_hour_to'),
            "request_date_to": leave_details.get('date_to'),
            "date_to": leave_details.get('date_to'),
        }

        if leave_details.get('request_unit_half'):
            value.update({
                'request_date_to': leave_details.get('date_from'),
                'date_to': leave_details.get('date_from'),
            })
        elif leave_details.get('request_unit_hours'):
            value.update({
                'request_date_to': leave_details.get('date_from'),
                'date_to': leave_details.get('date_from'),
            })
        else:
            value.update({
                "request_date_to": leave_details.get('date_to'),
                "date_to": leave_details.get('date_to'),
            })

        if 'employee_ids' in value and value['employee_ids']:
            employee = self.env['hr.employee'].sudo().browse(value['employee_ids'][0][2])
            if employee:
                value['department_id'] = employee.department_id.id

        try:
            hr_leave = self.sudo().create(value)
            hr_leave._compute_date_from_to()
            hr_leave._compute_duration_display()

            if hr_leave:
                return {
                    'success': True,
                    'message': "Leave created successfully!"
                }
        except Exception as e:
            raise ValidationError(f"Failed to create leave: {e}")

    @api.model
    def update_hr_leave(self, leave_details):
        if not isinstance(leave_details, dict):
            raise ValidationError("Invalid data format. Expected a dictionary.")
        record_id = self.sudo().search([('id', '=', leave_details.get('leave_rec_id'))])
        for record in record_id:
            if record.employee_id.name != request.env.user.name:
                raise ValidationError("You Cannot update This Time Off, Only Portal User Can Update their Time Off.")
        if not record_id:
            raise ValidationError("Leave record not found.")

        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return datetime.strptime(date_str, '%Y-%m-%d')

        date_from = leave_details.get('date_from')
        date_to = leave_details.get('date_to')
        if date_from:
            date_from = parse_date(date_from) if isinstance(date_from, str) else date_from
        if date_to:
            date_to = parse_date(date_to) if isinstance(date_to, str) else date_to

        value = {
            "name": leave_details.get('name'),
            "description_name": leave_details.get('name'),
            "employee_id": record_id.employee_id.id,
            "holiday_status_id": leave_details.get('holiday_status_id'),
            "request_date_from": date_from,
            "date_from": date_from,
            "request_unit_half": leave_details.get('request_unit_half'),
            "request_unit_hours": leave_details.get('request_unit_hours'),
            "duration_display": leave_details.get('duration_display'),
            "request_date_from_period": leave_details.get('request_date_from_period'),
            "request_hour_from": leave_details.get('request_hour_from'),
            "request_hour_to": leave_details.get('request_hour_to'),
        }

        if leave_details.get('request_unit_half') or leave_details.get('request_unit_hours'):
            value.update({
                'request_date_to': date_from,
                'date_to': date_from,
            })
        else:
            value.update({
                "request_date_to": date_to,
                "date_to": date_to,
            })

        if value.get('employee_id'):
            employee = self.env['hr.employee'].sudo().browse(value['employee_id'])
            if employee:
                value['department_id'] = employee.department_id.id

        required_fields = ['employee_id', 'holiday_status_id', 'date_from', 'date_to']
        for field in required_fields:
            if not value.get(field):
                raise ValidationError(f"The field '{field}' is required and is missing in the input data.")

        update_leave = record_id.sudo().write(value)
        if update_leave and record_id:
            record_id._compute_date_from_to()
            record_id._compute_duration_display()

        if update_leave:
            return {
                'success': True,
                'message': "Leave Updated successfully!"
            }

    @api.model
    def onchange_holiday_status_id(self, holidaystatusId):
        if holidaystatusId:
            holiday_status_id = request.env['hr.leave.type'].sudo().search([('id', '=', holidaystatusId)])
            if holiday_status_id.request_unit == 'hour':
                request_unit_condition = 'hour'
                return request_unit_condition
            if holiday_status_id.request_unit == 'half_day':
                request_unit_condition = 'half_day'
                return request_unit_condition
        return None

    @api.model
    def get_hr_leave(self, record):
        record_id = self.sudo().search([('id', '=', record)], limit=1)
        leaves = []
        for record in record_id:
            leaves.append({"id": record.id,
                           "name": record.name,
                           "employee_id": record.employee_id.id,
                           "holiday_status_id": record.holiday_status_id.id,
                           "request_unit_half": record.request_unit_half,
                           "request_unit_hours": record.request_unit_hours,
                           "duration_display": record.duration_display,
                           "request_date_from_period": record.request_date_from_period,
                           "request_hour_from": record.request_hour_from,
                           "request_hour_to": record.request_hour_to,
                           })
        return json.dumps(leaves)

    @api.model
    def cancel_hr_leave(self, cancel_leave):
        cancel_leave_reason = cancel_leave.get('cancel_reason')
        leave_rec_id = cancel_leave.get('leave_rec_id')
        record_id = self.sudo().search([('id', '=', leave_rec_id)], limit=1)
        if record_id.state in ['confirm', 'validate1']:
            record_id.cancel_reason = cancel_leave_reason
            record_id.action_refuse()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
