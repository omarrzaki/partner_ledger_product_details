# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (C) 2026 Omar Zaki
# License LGPL-2.1


from odoo import api, models, _
from odoo.tools import SQL


class PartnerLedgerProductDetails(models.AbstractModel):
    """
    Extend Partner Ledger report to show product details for each transaction.
    When a user expands a journal entry line, they will see the product lines
    from the related invoice/bill in a table format rendered by JavaScript.
    """
    _inherit = 'account.partner.ledger.report.handler'

    def _get_custom_display_config(self):
        """
        Override to register our custom ProductDetailsLine component.
        """
        config = super()._get_custom_display_config()
        # Add our custom component
        if 'components' not in config:
            config['components'] = {}
        config['components']['AccountReportLine'] = 'partner_ledger_product_details.ProductDetailsLine'
        return config

    def _get_report_line_move_line(self, options, aml_query_result, partner_line_id, init_bal_by_col_group, level_shift=0):
        """
        Override to make move lines expandable if they have product details.
        """
        # Get the base line from parent
        line = super()._get_report_line_move_line(
            options, aml_query_result, partner_line_id, init_bal_by_col_group, level_shift=level_shift
        )
        
        # Check if this move has product lines that can be shown
        move_line = self.env['account.move.line'].browse(aml_query_result['id'])
        move = move_line.move_id
        
        # Only make expandable if it's an invoice/bill with product lines
        if move and move.is_invoice(include_receipts=True):
            product_lines = move.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product' and l.product_id
            )
            if product_lines:
                line['unfoldable'] = True
                line['unfolded'] = line['id'] in options.get('unfolded_lines', []) or options.get('unfold_all', False)
                line['expand_function'] = '_report_expand_unfoldable_line_product_details'
        
        return line

    def _report_expand_unfoldable_line_product_details(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        """
        Expand function to show product details when a move line is expanded.
        Returns a single line with product_data that JavaScript will render as a table.
        """
        report = self.env['account.report'].browse(options['report_id'])
        
        # Parse the line ID to get the move line ID
        parsed = report._parse_line_id(line_dict_id)
        aml_id = None
        for markup, model, record_id in parsed:
            if model == 'account.move.line':
                aml_id = record_id
                break
        
        if not aml_id:
            return {'lines': [], 'offset_increment': 0, 'has_more': False}
        
        # Get the move line and its move
        move_line = self.env['account.move.line'].browse(aml_id)
        move = move_line.move_id
        
        if not move or not move.is_invoice(include_receipts=True):
            return {'lines': [], 'offset_increment': 0, 'has_more': False}
        
        # Get product lines from the invoice
        product_lines = move.invoice_line_ids.filtered(
            lambda l: l.display_type == 'product' and l.product_id
        )
        
        if not product_lines:
            return {'lines': [], 'offset_increment': 0, 'has_more': False}
        
        # Build product data for JavaScript
        product_data = []
        for pline in product_lines:
            product_data.append({
                'id': pline.id,
                'name': pline.product_id.display_name or pline.name or '',
                'quantity': pline.quantity,
                'uom': pline.product_uom_id.name if pline.product_uom_id else '',
                'price_unit': pline.price_unit,
                'subtotal': pline.price_subtotal,
            })
        
        # Create columns (empty for table row)
        columns = []
        for column in options['columns']:
            columns.append(report._build_column_dict(None, column, options=options))
        
        # Create the line with product_data for JavaScript to render
        table_line = {
            'id': report._get_generic_line_id(
                None, None,
                parent_line_id=line_dict_id,
                markup='product_table'
            ),
            'parent_id': line_dict_id,
            'name': '',
            'columns': columns,
            'level': 4,
            'product_data': product_data,
            'currency_symbol': move.currency_id.symbol,
        }
        
        return {
            'lines': [table_line],
            'offset_increment': 1,
            'has_more': False,
            'progress': progress,
        }
