/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { useService } from "@web/core/utils/hooks";

publicWidget.registry.hr_leave = publicWidget.Widget.extend({
    selector: '.search-bar',
    events: {
        'click .open_leave_wizard': '_onClickOpenLeaveWizard',
    },

    _onClickOpenLeaveWizard: async function(ev){
        ev.preventDefault();
        this._PopulateRequestToTimeOptions();
        this._PopulateRequestFromTimeOptions();
        this._populateRequestPeriodTimeOptions();
        var wizard = $('#leave_wizard_show');
        wizard.modal('show');
    },

    _PopulateRequestToTimeOptions: function() {
        const selectTo = document.getElementById('request_hour_to');
        const times = [
            '12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM',
            '3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM',
            '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM',
            '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
            '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
            '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM',
            '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM',
            '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM'
        ];

        times.forEach((time, index) => {
            const option = document.createElement('option');
            option.value = index * 0.5;
            option.textContent = time;
            selectTo.appendChild(option);
        });
    },

    _PopulateRequestFromTimeOptions: function() {
        const selectTo = document.getElementById('request_hour_from');
        const times = [
            '12:00 AM', '12:30 AM', '1:00 AM', '1:30 AM', '2:00 AM', '2:30 AM',
            '3:00 AM', '3:30 AM', '4:00 AM', '4:30 AM', '5:00 AM', '5:30 AM',
            '6:00 AM', '6:30 AM', '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM',
            '9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM',
            '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
            '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM',
            '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM',
            '9:00 PM', '9:30 PM', '10:00 PM', '10:30 PM', '11:00 PM', '11:30 PM'
        ];

        times.forEach((time, index) => {
            const option = document.createElement('option');
            option.value = index * 0.5;
            option.textContent = time;
            selectTo.appendChild(option);
        });
    },

    _populateRequestPeriodTimeOptions: function() {
        const selectPeriod = document.getElementById('request_date_from_period');
        const periods = [
            { value: 'am', text: 'Morning' },
            { value: 'pm', text: 'Afternoon' }
        ];

        periods.forEach(period => {
            const option = document.createElement('option');
            option.value = period.value;
            option.textContent = period.text;
            selectPeriod.appendChild(option);
        });
    },
});