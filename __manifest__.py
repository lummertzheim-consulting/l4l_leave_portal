# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': "Employee Leave Portal",
    'category': 'Human Resources/Time Off',
    'version': '18.0.1.0',
    'sequence': 1,
    'summary': """Employee Time Off In Portal, Hr Time Off In Portal, Hr Leave Portal, Employee Leave Portal, Leave Portal, Short By, Search By, Filter By, Search Functionality, Website, Sale Order, Order, Purchase, Invoice, Bill, Receipt, Vendor, Partner, Contact, Transfer, Inventory, Shipment, Picking Portal, Picking, Portal, Delivery""",
    'description': """This Module Helps Provide Users with an Efficient and User-Friendly way to Manage Their
                            Leave Records. It Offers a Comprehensive Set of Features that Simplify The Processes of
                            Viewing, Filtering, Creating, and Updating Leave Information.""",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['mail', 'website', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/time_off_portal_template_views.xml',
        'views/hr_leave_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            "l4l_leave_portal/static/src/js/WizardOpen.js",
            "l4l_leave_portal/static/src/js/UpdateWizardOpen.js",
            "l4l_leave_portal/static/src/js/WizardLeave.js",
            "l4l_leave_portal/static/src/js/CancelLeaveWizardOpen.js",
            "l4l_leave_portal/static/src/css/leave_portal.css",
        ],
    },
    'installable': True,
    'application': True,
    'license': 'OPL-1',
    'images': ['static/description/banner.gif'],
    'price': '41.70',
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/1H4Dnk8ONks',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
