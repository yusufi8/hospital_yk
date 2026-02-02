from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PatientReassignWizard(models.TransientModel):
    _name = 'hospital.patient.reassign.wizard'
    _description = 'Reassign Patients to Another Doctor'

    old_doctor_id = fields.Many2one('res.users', string='Current Doctor', required=True, readonly=True)
    new_doctor_id = fields.Many2one('res.users', string='New Doctor', required=True,
                                   domain=[('is_doctor', '=', True)])
    patient_ids = fields.Many2many('hospital.patient', string='Patients to Reassign',
                                  default=lambda self: self._default_patients())
    
    @api.model
    def _default_patients(self):
        if self._context.get('active_model') == 'res.users':
            doctor_id = self._context.get('default_old_doctor_id')
            if doctor_id:
                return self.env['hospital.patient'].search([('doctor_id', '=', doctor_id)])
        return False

    @api.constrains('old_doctor_id', 'new_doctor_id')
    def _check_doctors(self):
        for wizard in self:
            if wizard.old_doctor_id == wizard.new_doctor_id:
                raise ValidationError(_("Please select a different doctor to reassign the patients to."))
            if not wizard.new_doctor_id.has_group('hospital_yk.group_hospital_doctor'):
                raise ValidationError(_("The selected user is not a doctor."))

    def action_reassign(self):
        self.ensure_one()
        if not self.patient_ids:
            raise ValidationError(_("Please select at least one patient to reassign."))

        self.patient_ids.write({
            'doctor_id': self.new_doctor_id.id
        })

        # Post a note in the chatter for each patient
        for patient in self.patient_ids:
            patient.message_post(
                body=_("Patient reassigned from Dr. %(old)s to Dr. %(new)s",
                      old=self.old_doctor_id.name,
                      new=self.new_doctor_id.name)
            )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Successfully reassigned %d patients.', len(self.patient_ids)),
                'sticky': False,
                'type': 'success',
            }
        }
