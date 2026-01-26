# -*- coding: utf-8 -*-
# Copyright (C) 2026 Omar Zaki
# License OPL-1
{
    'name': 'Partner Ledger Product Details',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Show product details table in Partner Ledger report',
    'description': """
        Extends the Partner Ledger report to display product details 
        for each invoice/bill transaction as a beautiful table.
        
        Features:
        - Expandable invoice/bill lines
        - Product table with: Name, Quantity, Unit Price, Subtotal
        - Arabic column headers
        - Total row at bottom
        - Custom JavaScript component for web view
        - Custom PDF template for printing
    """,
    'author': "Omar Zaki",
    'website': "http://www.softprimes.com",
    'license': 'OPL-1',
    'depends': ['account_reports'],
    'data': [
        'data/pdf_export_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'partner_ledger_product_details/static/src/scss/partner_ledger_product_details.scss',
            'partner_ledger_product_details/static/src/components/product_details/product_details_line.js',
            'partner_ledger_product_details/static/src/components/product_details/product_details_line.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
