# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    branch_id = fields.Many2one('res.branch', default=lambda self: self.env.user.branch_id.id)

    @api.constrains('branch_id')
    def _check_branch(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = warehouse_obj.search(
            ['|', '|', ('wh_input_stock_loc_id', '=', self.id),
             ('lot_stock_id', '=', self.id),
             ('wh_output_stock_loc_id', '=', self.id)])
        for warehouse in warehouse_id:
            if self.branch_id != warehouse.branch_id:
                raise UserError(_('Configuration error\nYou  must select same branch on a location as assigned on a warehouse configuration.'))

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        selected_brach = self.branch_id
        if selected_brach:
            user_id = self.env['res.users'].browse(self.env.uid)
            user_branch = user_id.sudo().branch_id
            if user_branch and user_branch.id != selected_brach.id:
                raise UserError("Please select active branch only. Other may create the Multi branch issue. \n\ne.g: If you wish to add other branch then Switch branch from the header and set that.")







##custommmmmmmmmmmmmmmmmmmmmmm


class StockQuant(models.Model):
    """Stock Quant Inherited."""

    _inherit = "stock.quant"

    branch_id = fields.Many2one("multi.branch", string="Branch Name")
# field----vals- {'inventory_quantity_set': True, 'location_id': 60, 
# 'product_id': 1332, 'lot_id': False, 'package_id': False, 'owner_id': False,
#  'accounting_date': False, 'inventory_quantity': 10, 
#  'inventory_date': '2022-12-31', 'user_id': False}

# allowed_fields create ['product_id', 'location_id', 'lot_id', 'package_id',
#  'owner_id', 'inventory_quantity', 'inventory_quantity_auto_apply',
#   'inventory_diff_quantity', 'inventory_date', 'user_id',
#    'inventory_quantity_set', 'is_outdated', 'accounting_date']

# field----vals- {'inventory_quantity_set': True, 'location_id': 60,
#  'product_id': 1332, 'lot_id': False, 'package_id': False,
#   'owner_id': False, 'accounting_date': False, 'inventory_quantity': 10,
#    'inventory_date': '2022-12-31', 'user_id': False}
# allowed_fields create ['product_id', 'location_id', 'lot_id',
#  'package_id', 'owner_id', 'branch_id', 'inventory_quantity',
#   'inventory_quantity_auto_apply', 'inventory_diff_quantity', 
#   'inventory_date', 'user_id', 'inventory_quantity_set', 'is_outdated',
#    'branch_id']



    # @api.model
    # def _get_inventory_fields_create(self):
    #     """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
    #     """
    #     return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id','accounting_date'] + self._get_inventory_fields_write()



    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        res = super()._get_inventory_fields_create()
        res += ['branch_id']
        #print("res====create get inv fields",res)
        return res

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
        """
        res = super()._get_inventory_fields_write()
        res += ['branch_id']
        #print("res====write get inv fields",res)
        return res


    @api.model
    def create(self, vals):
        #print("vals------StockQuant--create------",vals,self.env.context,self.env.context.get('active_model'))
        if not vals.get("branch_id",False) and  vals.get("product_id",False) and vals.get("location_id",False):
            loc_rec = self.env['stock.location'].browse(vals.get("location_id"))
            loc_branch_rec = loc_rec.branch_id
            product_rec = self.env['product.product'].browse(vals.get("product_id"))
            product_branch_rec = product_rec.branch_id
            if loc_rec.usage == "internal" and product_branch_rec.id != loc_branch_rec.id:
                raise UserError(_("Location and Product Branch do not match for %s") % (product_rec.name,))

            #print("branch_id ----------- quantttt===",loc_branch_rec)
            vals.update({'branch_id':loc_branch_rec.id})
        

        res = super(StockQuant, self).create(vals)
    
        return res

    # @api.model
    # def _get_inventory_fields_write(self):
    #     """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
    #     """
    #     fields = ['inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity',
    #               'inventory_date', 'user_id', 'inventory_quantity_set', 'is_outdated','branch_id']
    #     return fields

    def write(self, vals):
        #print("vals------StockQuant---write-----",vals,self.env.context,self.env.context.get('active_model'))
        #print("branch_id----- write stock quant ------",self.branch_id,self.location_id)
        if vals.get("inventory_quantity",False):
            loc_branch_id = self.location_id.branch_id.id
            product_branch_id  = self.product_id.product_tmpl_id.branch_id.id
            #print("loc_branch_id,product_branch_id",loc_branch_id,product_branch_id) 
            if self.location_id.usage == "internal" and loc_branch_id != product_branch_id:
                raise UserError(_("Location and Product Branch do not match for %s") % (self.product_id.name,))

        if not vals.get("branch_id",False) and not self.branch_id:
            #print("product reccc =============",self.product_id)
            branch_id = self.product_id.branch_id.id
            #print("branch_id ----------- quantttt===",branch_id)
            vals.update({'branch_id':branch_id})
        

        res = super(StockQuant, self).write(vals)
    
        return res


########## ends here
