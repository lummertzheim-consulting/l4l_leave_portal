/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { useService } from "@web/core/utils/hooks";

publicWidget.registry.wizard_leave = publicWidget.Widget.extend({
    selector: '.leave-container',
    events: {
        'click .close_leave_wizard': '_onClickCloseLeaveWizard',
        'click #request_unit_half': '_onChangeRequestUnitHalf',
        'click #request_unit_hours': '_onChangeRequestUnitHours',
        'change input[name="date_from"], input[name="date_to"], input[name="request_unit_half"], input[name="request_unit_hours"], select[name="request_hour_from"], select[name="request_hour_to"]': '_calculateDuration',
        'change #holiday_status_id': '_onChangeHolidayStatusId',
        'click .submit_leave_wizard': '_onClickSubmit',
    },

    init() {
        this.orm = this.bindService("orm");
    },

    start: function() {
        this._super.apply(this, arguments);
        var holidaystatusid = $('select[name="holiday_status_id"]').val();
        this.orm.call('hr.leave', 'onchange_holiday_status_id', [holidaystatusid]).then(function(result) {
           if (result) {
               var requestUnitCondition = result;
               var request_unit_half = $("#request_unit_half").is(':checked');
               var request_unit_hours = $("#request_unit_hours").is(':checked');
               if (request_unit_hours) {
                    $("#from_hours_div").show();
                    $("#to_hours_div").show();
               }
               if (request_unit_half) {
                    $("#shifting_div").show();
               }
                if (requestUnitCondition == 'hour') {
                    $('#l4l_request_unit_half, #l4l_request_unit_hours').toggle(true);
                }
                else {
                    $('#l4l_request_unit_half').toggle(true);
                    $("#l4l_request_unit_hours").hide();
                }
           } else {
               $("#from_hours_div").hide();
               $("#to_hours_div").hide();
               $("#shifting_div").hide();
               $("#l4l_request_unit_half").hide();
               $("#l4l_request_unit_hours").hide();
               if ($("#request_unit_hours").is(':checked')) {
                    $('#request_unit_hours').prop('checked', false);
                    $("#date_to").show();
               } if ($("#request_unit_half").is(':checked')){
                    $('#request_unit_half').prop('checked', false);
                    $("#date_to").show();
               }
           }
        }).catch(function(error) {
            console.error('Error:', error);
        });
    },

    _onChangeHolidayStatusId: function(ev) {
        var holidaystatusId = $(ev.target).val();
        this.orm.call('hr.leave', 'onchange_holiday_status_id', [holidaystatusId]).then(function(result) {
           if (result) {
               var requestUnitCondition = result;
               var request_unit_half = $("#request_unit_half").is(':checked');
               var request_unit_hours = $("#request_unit_hours").is(':checked');
               if (request_unit_hours) {
                    $("#from_hours_div").show();
                    $("#to_hours_div").show();
               }
               if (request_unit_half) {
                    $("#shifting_div").show();
               }
                if (requestUnitCondition == 'hour') {
                    $('#l4l_request_unit_half, #l4l_request_unit_hours').toggle(true);
                }
                else {
                    $('#l4l_request_unit_half').toggle(true);
                    $("#l4l_request_unit_hours").hide();
                }
           } else {
               $("#from_hours_div").hide();
               $("#to_hours_div").hide();
               $("#shifting_div").hide();
               $("#l4l_request_unit_half").hide();
               $("#l4l_request_unit_hours").hide();
               if ($("#request_unit_hours").is(':checked')) {
                    $('#request_unit_hours').prop('checked', false);
                    $("#date_to").show();
               } if ($("#request_unit_half").is(':checked')){
                    $('#request_unit_half').prop('checked', false);
                    $("#date_to").show();
               }
           }
        }).catch(function(error) {
            console.error('Error:', error);
        });
    },


    _calculateDuration: function (ev) {
        var dateFrom = new Date($('input[name="date_from"]').val());
        var dateTo = new Date($('input[name="date_to"]').val());
        var HoursFrom = parseInt($('select[name="request_hour_from"]').val());
        var HoursTo = parseInt($('select[name="request_hour_to"]').val());

        var durationText = '';

        function isWeekend(date) {
            var day = date.getDay();
            return (day === 6 || day === 0);
        }

        function getWeekdayDuration(startDate, endDate) {
            var currentDate = new Date(startDate);
            var weekdayDuration = 0;
            var totalDurationInMillis = 0;

            while (currentDate <= endDate) {
                if (!isWeekend(currentDate)) {
                    weekdayDuration++;
                }
                currentDate.setDate(currentDate.getDate() + 1);
            }

            return weekdayDuration;
        }

        if ($('#request_unit_half').is(':checked')) {
            durationText = '4 hours';
        } else if ($('#request_unit_hours').is(':checked')) {
            var selectedHours = HoursTo - HoursFrom;

            if (selectedHours < 0) {
                durationText = "Invalid Inputs";
            } else if (selectedHours >= 0) {
                durationText = selectedHours + ' hour';
            }

            if (selectedHours !== 1) {
                durationText += 's';
            }
        } else {
            var weekdayCount = getWeekdayDuration(dateFrom, dateTo);

            var durationInMillis = dateTo - dateFrom;
            var totalDays = Math.floor(durationInMillis / (1000 * 60 * 60 * 24));
            var totalHours = Math.floor((durationInMillis % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

            var days = weekdayCount;
            if (days === 0) {
                durationText = "0";
            } else {
                durationText = days + ' day';
                if (days > 1) {
                    durationText += 's';
                }
            }

            if (totalHours > 0) {
                if (days > 0) {
                    durationText += ' ';
                }
                durationText += totalHours + ' hour';
                if (totalHours > 1) {
                    durationText += 's';
                }
            }
        }

        $('input[name="duration_display"]').val(durationText);
    },

    _onClickCloseLeaveWizard: async function(ev){
        var wizard_close = $('#leave_wizard_show');
        wizard_close.modal('hide');
    },

    _onChangeRequestUnitHalf: function(ev) {
        var isChecked = $(ev.currentTarget).is(':checked');
        var isNone = !isChecked;
        $('#shifting_div').toggle(isChecked);
        $('#date_to').toggle(isNone);

        if (isChecked) {
            $('#request_unit_hours').prop('disabled', true);
        } else {
            $('#request_unit_hours').prop('disabled', false);
        }
    },

    _onChangeRequestUnitHours: function(ev) {
        var isChecked = $(ev.currentTarget).is(':checked');
        var isNone = !isChecked;
        $('#from_hours_div').toggle(isChecked);
        $('#to_hours_div').toggle(isChecked);
        $('#date_to').toggle(isNone);

        if (isChecked) {
            $('#request_unit_half').prop('disabled', true);
        } else {
            $('#request_unit_half').prop('disabled', false);
        }
    },

    formatDate: function(dateString) {
       var date = new Date(dateString);
       var year = date.getFullYear();
       var month = ('0' + (date.getMonth() + 1)).slice(-2);
       var day = ('0' + date.getDate()).slice(-2);
       return year + '-' + month + '-' + day;
    },

    _onClickSubmit: async function(ev) {
        var self = this;

        var name = $('#name').val();
        var employee_id = parseInt($("#employee_id").val());
        var holiday_status_id = parseInt($("#holiday_status_id").val());
        var date_from = self.formatDate($("#date_from").val());
        var date_to = self.formatDate($("#leave_date_to").val());
        var request_unit_half = $("#request_unit_half").is(':checked');
        var request_unit_hours = $("#request_unit_hours").is(':checked');
        var duration_display = parseInt($("#duration_display").val());
        var request_date_from_period = $("#request_date_from_period").val();
        var request_hour_from = $("#request_hour_from").val();
        var request_hour_to = $("#request_hour_to").val();

        var requiredFields = [
            { field: '#name', errorMessage: 'Please enter the Description.' },
            { field: '#employee_id', errorMessage: 'Please select an employee.' },
            { field: '#holiday_status_id', errorMessage: 'Please select the holiday status.' },
            { field: '#date_from', errorMessage: 'Please select the Start Date.' },
        ];

        if (!(request_unit_half || request_unit_hours)) {
            requiredFields.push({ field: '#leave_date_to', errorMessage: 'Please select the End Date.' });
        }

        if (date_from > date_to) {
            alert('End Date cannot be Earlier than the Start Date.');
            return false;
        }

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

        if (isNaN(duration_display)) {
            alert('Please enter a valid Duration.');
            $("#duration_display").addClass('leap_required');
            return false;
        } else {
            $("#duration_display").removeClass('leap_required');
        }

        var leave_details = {
            "name": name,
            "employee_id": employee_id,
            "holiday_status_id": holiday_status_id,
            "date_from": date_from,
            "date_to": date_to,
            "request_unit_half": request_unit_half,
            "request_unit_hours": request_unit_hours,
            "duration_display": duration_display,
            "request_date_from_period": request_date_from_period,
            "request_hour_from": request_hour_from,
            "request_hour_to": request_hour_to,
        };

        var result = this.orm.call('hr.leave', 'create_hr_leave', [leave_details]);

        setTimeout(function () {document.location.reload(true)}, 1000);
    },
});