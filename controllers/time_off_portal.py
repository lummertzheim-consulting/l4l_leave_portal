# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import http, _, SUPERUSER_ID, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.addons.portal.controllers import portal
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'leave_count' in counters:
            values['leave_count'] = request.env['hr.leave'].sudo().search_count([])
        return values

    def get_leave_searchbar_sortings(self):
        return {
            'date_from': {'label': _('Start Date'), 'order': 'date_from desc'},
            'date_to': {'label': _('End Date'), 'order': 'date_to desc'},
            'stage': {'label': _('Status'), 'order': 'state'},
        }

    def get_leave_searchbar_filters(self):
        today = datetime.now().today()
        yesterday = today - relativedelta(days=1)
        today_date_str = today.strftime('%Y-%m-%d')
        last_month_end = today - relativedelta(day=1)
        last_month_start = last_month_end - relativedelta(months=1)
        last_week_start = today - relativedelta(weeks=1)
        first_day_current_year = datetime(datetime.now().year, 1, 1)
        first_day_last_year = first_day_current_year - relativedelta(years=1)
        next_month_start = (today + relativedelta(months=1)).replace(day=1)
        this_month_end = next_month_start - relativedelta(days=1)
        this_week_start = today - relativedelta(days=today.weekday())
        this_week_end = this_week_start + relativedelta(days=6)
        this_year_start = today.replace(day=1, month=1)
        this_year_end = this_year_start + relativedelta(years=1)

        domain_last_month = [
            ('date_from', '>=', last_month_start.strftime('%Y-%m-%d')),
            ('date_from', '<', last_month_end.strftime('%Y-%m-%d'))]
        domain_last_week = [
            ('date_from', '>=', last_week_start.strftime('%Y-%m-%d')),
            ('date_from', '<', today.strftime('%Y-%m-%d'))]
        domain_last_year = [
            ('date_from', '>=', first_day_last_year.strftime('%Y-%m-%d')),
            ('date_from', '<', first_day_current_year.strftime('%Y-%m-%d'))]
        domain_this_month = [
            ('date_from', '>=', today.replace(day=1).strftime('%Y-%m-%d')),
            ('date_from', '<=', this_month_end.strftime('%Y-%m-%d'))]
        domain_today = [('date_from', '>', yesterday.strftime('%Y-%m-%d')),
                        ('date_from', '<=', today_date_str)]
        domain_this_week = [
            ('date_from', '>=', this_week_start.strftime('%Y-%m-%d')),
            ('date_from', '<=', this_week_end.strftime('%Y-%m-%d'))]
        domain_this_year = [
            ('date_from', '>=', this_year_start.strftime('%Y-%m-%d')),
            ('date_from', '<=', this_year_end.strftime('%Y-%m-%d'))]
        return {
            'All': {'label': _('All'), 'domain': []},
            'Old Date': {'label': _('Last Month'), 'domain': domain_last_month},
            'Last Week': {'label': _('Last Week'), 'domain': domain_last_week},
            'Last Year': {'label': _('Last Year'), 'domain': domain_last_year},
            'This Month': {'label': _('This Month'), 'domain': domain_this_month},
            'Today': {'label': _('Today'), 'domain': domain_today},
            'This Week': {'label': _('This Week'), 'domain': domain_this_week},
            'This Year': {'label': _('This Year'), 'domain': domain_this_year},
        }

    def get_leave_searchbar_groupby(self):
        return {
            'none': {'input': 'none', 'label': _('None'), "order": 1},
            'holiday_status_id': {'input': 'holiday_status_id', 'label': _('Time Off Type'), "order": 1},
            'description_name': {'input': 'description_name', 'label': _('Description'), "order": 1},
            'state': {'input': 'state', 'label': _('State'), "order": 1},
        }

    @http.route(['/employee/leave', '/employee/leave/page/<int:page>'], type='http', auth='user', website=True)
    def portal_employee_leave_list(self, sortby='date_from', filterby='All', search="", search_in="all", groupby="none",
                                   **kw):
        searchbar_sortings = self.get_leave_searchbar_sortings()
        if not sortby:
            sortby = 'date_from'
        order = searchbar_sortings[sortby]['order']

        search_list = {
            'All': {'label': _('All'), 'input': 'All', 'domain': []},
            'Description': {'label': _('Description'), 'input': 'Description', 'domain': [('description_name', 'ilike', search)]},
            'Duration': {'label': _('Duration'), 'input': 'Duration',
                         'domain': [('duration_display', 'ilike', search)]},
            'Time Off Type': {'label': _('Time Off Type'), 'input': 'Time Off Type',
                              'domain': [('holiday_status_id', 'ilike', search)]},
        }

        employees = request.env['hr.employee'].sudo().search([('id', 'in', request.env.user.partner_id.employee_ids.ids)])
        
        allocation_types = request.env['hr.leave.type'].sudo().search([])
        allocation_ids = []
        for type in allocation_types:
            allocations = request.env['hr.leave.allocation'].sudo().search([
                ('holiday_status_id', '=', type.id),
                ('employee_id', 'in', request.env.user.partner_id.employee_ids.ids),
                ('state', '=', 'validate')
            ])
            allocation_ids.extend(allocations.mapped('holiday_status_id.id'))

        types = request.env['hr.leave.type'].sudo().search([
            '|', ('id', 'in', allocation_ids), ('requires_allocation', '=', 'no'), ('virtual_remaining_leaves', '>', 0)
        ])

        if search_in not in search_list:
            search_in = 'All'
        search_domain = search_list[search_in]['domain']

        searchbar_filters = self.get_leave_searchbar_filters()
        if filterby == 'All':
            domain = []
        else:
            domain = searchbar_filters[filterby]['domain']

        if not groupby:
            groupby = 'none'
        searchbar_groupby = self.get_leave_searchbar_groupby()
        leave_group_by = searchbar_groupby.get(groupby, {})

        if groupby in ('holiday_status_id', 'description_name', 'state'):
            group_by_for_leave = leave_group_by.get('input')
        else:
            group_by_for_leave = ''

        leave_obj = request.env['hr.leave']
        leave_detail = request.env['hr.leave'].sudo().search([('employee_id', 'in', request.env.user.partner_id.employee_ids.ids)] + domain + search_domain, order=order)

        if group_by_for_leave:
            leave_group_list = [{group_by_for_leave: key, 'leave': leave_obj.concat(*group)} for key, group in
                                groupbyelem(leave_detail, itemgetter(group_by_for_leave))]
        else:
            leave_group_list = [{'leave': leave_detail}]

        return request.render('l4l_leave_portal.l4l_portal_employee_leave_list', {
            'employees': employees,
            'types': types,
            'leave': leave_detail,
            'page_name': 'list_employee_leave',
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'search': search,
            'searchbar_inputs': search_list,
            'filterby': filterby,
            'searchbar_filters': searchbar_filters,
            'groupby': groupby,
            'leave_group': leave_group_list,
            'searchbar_groupby': searchbar_groupby,
            'default_url': '/employee/leave',
        })

    @http.route(["/employee/leave/<int:record_id>"], type='http', auth="public", website=True)
    def leave_record_details(self, record_id):
        leave_details_rec = request.env['hr.leave'].sudo().browse(record_id)

        allocation_types = request.env['hr.leave.type'].sudo().search([])
        allocation_ids = []
        for type in allocation_types:
            allocations = request.env['hr.leave.allocation'].sudo().search([
                ('holiday_status_id', '=', type.id),
                ('employee_id', 'in', request.env.user.partner_id.employee_ids.ids),
                ('state', '=', 'validate')
            ])
            allocation_ids.extend(allocations.mapped('holiday_status_id.id'))

        types = request.env['hr.leave.type'].sudo().search([
            '|', ('id', 'in', allocation_ids), ('requires_allocation', '=', 'no'), ('virtual_remaining_leaves', '>', 0)
        ])
        request_unit_condition = leave_details_rec.holiday_status_id.request_unit == 'hour'

        formatted_date_to = None
        formatted_date_from = None

        request_hour_from = leave_details_rec.request_hour_from
        request_hour_to = leave_details_rec.request_hour_to
        request_date_from_period = leave_details_rec.request_date_from_period

        if leave_details_rec.date_to and isinstance(leave_details_rec.date_to, datetime):
            formatted_date_to = leave_details_rec.date_to.strftime('%Y-%m-%d')

        if leave_details_rec.date_from and isinstance(leave_details_rec.date_from, datetime):
            formatted_date_from = leave_details_rec.date_from.strftime('%Y-%m-%d')

        page_name = 'list_employee_leave_rec'

        leave_records = request.env['hr.leave'].sudo().search([])

        return request.render(
            'l4l_leave_portal.l4l_portal_employee_leave_detail_rec',
            {
                'leave_records': leave_records,
                'leave_details_rec': leave_details_rec,
                'date_to': formatted_date_to,
                'request_unit_condition': request_unit_condition,
                'request_hour_from': request_hour_from,
                'request_hour_to': request_hour_to,
                'request_date_from_period': request_date_from_period,
                'date_from': formatted_date_from,
                'page_name': page_name,
                'types': types
            }
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
