from odoo import fields, models
from odoo.tools.safe_eval import safe_eval
from datetime import datetime


class OdooPlayGround(models.TransientModel):
    _name = 'odoo.playground'
    _description = "Odoo Playground"

    DEFAULT_ENV_VARIABLES = '''# Example: List users
self.env['res.users'].search([]).mapped('name')'''

    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code', default=DEFAULT_ENV_VARIABLES)
    result = fields.Text(string='Result', readonly=True)

    def action_execute(self):
        self.ensure_one()
        try:
            # Get target model or fallback to self
            target_model = self.model_id.model if self.model_id else self._name
            Model = self.env[target_model]

            # Prepare execution context
            local_ctx = {
                'self': Model,
                'env': self.env,
                'datetime': datetime,
                'user': self.env.user,
            }

            # Execute code and capture result
            res = safe_eval(self.code.strip(), local_ctx)

            # Format result based on type
            if isinstance(res, (list, tuple)):
                self.result = '\n'.join(str(x) for x in res)
            elif isinstance(res, dict):
                self.result = '\n'.join(f'{k}: {v}' for k, v in res.items())
            else:
                self.result = str(res) if res is not None else ''

        except Exception as e:
            self.result = str(e)
