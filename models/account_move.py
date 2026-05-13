from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    product_ids = fields.Many2many(
        'product.product',
        compute='_compute_product_ids',
        string='Productos',
    )

    @api.depends('invoice_line_ids.product_id')
    def _compute_product_ids(self):
        for move in self:
            move.product_ids = move.invoice_line_ids.product_id

    @api.model
    def _create_demo_invoices(self):
        journal = self.env['account.journal'].search(
            [('type', '=', 'sale'), ('company_id', '=', self.env.company.id)],
            limit=1,
        )
        if not journal:
            return

        def ref(xmlid):
            return self.env.ref(xmlid, raise_if_not_found=False)

        guitar = ref('insight_graph_account_partner.demo_product_guitar')
        mic = ref('insight_graph_account_partner.demo_product_mic')

        invoices = [
            {
                'partner': ref('insight_graph_account_partner.demo_partner_piazzolla'),
                'date': '2024-01-15',
                'lines': [(guitar, 'Guitarra Fender Stratocaster', 1500.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_ginastera'),
                'date': '2024-02-20',
                'lines': [(guitar, 'Guitarra Fender Stratocaster', 1500.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_lara'),
                'date': '2024-02-20',
                'lines': [(guitar, 'Guitarra Fender Stratocaster', 1500.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_yupanqui'),
                'date': '2024-03-10',
                'lines': [(guitar, 'Guitarra Fender Stratocaster', 1500.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_sosa'),
                'date': '2024-04-05',
                'lines': [(mic, 'Micrófono Shure SM58', 250.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_downs'),
                'date': '2024-04-05',
                'lines': [(mic, 'Micrófono Shure SM58', 250.0)],
            },
            {
                'partner': ref('insight_graph_account_partner.demo_partner_zitarrosa'),
                'date': '2024-03-10',
                'lines': [
                    (guitar, 'Guitarra Fender Stratocaster', 1500.0),
                    (mic, 'Micrófono Shure SM58', 250.0),
                ],
            },
        ]

        for inv in invoices:
            partner = inv['partner']
            if not partner:
                continue
            self.create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'journal_id': journal.id,
                'invoice_date': inv['date'],
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': product.id,
                        'name': name,
                        'quantity': 1.0,
                        'price_unit': price,
                    })
                    for product, name, price in inv['lines']
                    if product
                ],
            })
