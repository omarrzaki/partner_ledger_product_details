/** @odoo-module */

import { AccountReport } from "@account_reports/components/account_report/account_report";
import { AccountReportLine } from "@account_reports/components/account_report/line/line";

/**
 * Custom line component for Partner Ledger that renders product details as a table.
 * When a line has product_data field, it renders an HTML table instead of the standard line.
 */
export class ProductDetailsLine extends AccountReportLine {
    static template = "partner_ledger_product_details.ProductDetailsLine";
    
    /**
     * Check if this line should display a product details table
     */
    get hasProductData() {
        return this.props.line.product_data && this.props.line.product_data.length > 0;
    }
    
    /**
     * Get the product data for rendering
     */
    get productData() {
        return this.props.line.product_data || [];
    }
    
    /**
     * Get the currency symbol
     */
    get currencySymbol() {
        return this.props.line.currency_symbol || '';
    }
    
    /**
     * Calculate total amount
     */
    get totalAmount() {
        if (!this.productData.length) return 0;
        return this.productData.reduce((sum, p) => sum + (p.subtotal || 0), 0);
    }
    
    /**
     * Format number with commas
     */
    formatNumber(value) {
        if (value === null || value === undefined) return '';
        return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
}

// Register the custom component
AccountReport.registerCustomComponent(ProductDetailsLine);
