/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { useService } from "@web/core/utils/hooks";

publicWidget.registry.cancel_hr_leave = publicWidget.Widget.extend({
    selector: '.cancel_leave_wizard',
    events: {
        'click .open_cancel_leave_wizard': '_onClickOpenCancelLeaveWizard',
        'click .close_cancel_leave_wizard': '_onClickCancelCloseLeaveWizard',
        'click .cancel_time_off_wizard': '_onClickCancel',
    },

    init() {
        this.orm = this.bindService("orm");
    },

    _onClickOpenCancelLeaveWizard: async function(ev) {
        var wizard = $('#cancel_leave_wizard_show');
        wizard.modal('show');
    },

    _onClickCancelCloseLeaveWizard: async function(ev){
        var wizard_close = $('#cancel_leave_wizard_show');
        wizard_close.modal('hide');
    },

    _onClickCancel: async function (ev) {
        var self = this;

        var requiredFields = [
            { field: '#cancel_reason', errorMessage: 'Please enter the Cancel Reason.' },
        ];

        var valid = true;

        requiredFields.forEach(function (field) {
            if (!$(field.field).val()) {
                valid = false;
                $(field.field).addClass('leap_required');
                alert(field.errorMessage);
            } else {
                $(field.field).removeClass('leap_required');
            }
        });

        if (!valid) {
            return false;
        }

        var result = this.orm.call('hr.leave', 'cancel_hr_leave', [{
            "cancel_reason": $('#cancel_reason').val(),
            "leave_rec_id": $('#leave_rec_id').val(),
        }]);
        setTimeout(function () {document.location.reload(true)}, 1000);
    },
});