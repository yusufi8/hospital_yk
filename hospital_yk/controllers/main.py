from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class HospitalYKAPIController(http.Controller):
    """Simple REST API for Hospital YK module."""

    # ===================================================
    # 🩺 1. GET ALL PATIENTS
    # ===================================================
    @http.route('/api/v1/patients', type='json', auth='user', methods=['POST'], csrf=False)
    def get_patients(self, **kwargs):
        try:
            patients = request.env['hospital.patient'].sudo().search([])
            data = [{
                'id': p.id,
                'name': p.name,
                'age': p.age,
                'gender': p.gender,
                'phone': p.mobile,
            } for p in patients]
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # ===================================================
    # 🧍‍♂️ 2. CREATE NEW PATIENT
    # ===================================================
    @http.route('/api/v1/patients/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_patient(self, **kwargs):
        try:
            name = kwargs.get('name')
            age = kwargs.get('age')
            gender = kwargs.get('gender')
            mobile = kwargs.get('mobile')

            if not name:
                return {'status': 'error', 'message': 'Name is required'}

            patient = request.env['hospital.patient'].sudo().create({
                'name': name,
                'age': age,
                'gender': gender,
                'mobile': mobile,
            })

            return {'status': 'success', 'data': {'id': patient.id, 'name': patient.name}}
        except Exception as e:
            _logger.error("Error creating patient: %s", e)
            return {'status': 'error', 'message': str(e)}

    # ===================================================
    # 📅 3. GET ALL APPOINTMENTS
    # ===================================================
    @http.route('/api/v1/appointments', type='json', auth='user', methods=['POST'], csrf=False)
    def get_appointments(self, **kwargs):
        try:
            appointments = request.env['hospital.appointment'].sudo().search([])
            data = [{
                'id': a.id,
                'patient': a.patient_id.name,
                'doctor': a.doctor_id.name,
                'appointment_date': a.appointment_date,
                'state': a.state,
            } for a in appointments]
            return {'status': 'success', 'data': data}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # ===================================================
    # 🩹 4. CREATE NEW APPOINTMENT
    # ===================================================
    @http.route('/api/v1/appointments/create', type='json', auth='user', methods=['POST'], csrf=False)
    def create_appointment(self, **kwargs):
        try:
            patient_id = kwargs.get('patient_id')
            doctor_id = kwargs.get('doctor_id')
            appointment_date = kwargs.get('appointment_date')

            if not patient_id or not appointment_date:
                return {'status': 'error', 'message': 'Patient ID and date are required'}

            appointment = request.env['hospital.appointment'].sudo().create({
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': appointment_date,
                'state': 'draft'
            })

            return {
                'status': 'success',
                'data': {
                    'id': appointment.id,
                    'name': appointment.name
                }
            }
        except Exception as e:
            _logger.error("Error creating appointment: %s", e)
            return {'status': 'error', 'message': str(e)}


from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class HospitalYKRestAPI(http.Controller):

    # ===================================================
    # GET  →  Read all patients
    # ===================================================
    @http.route('/api/v2/patients', type='http', auth='user', methods=['GET'], csrf=False)
    def get_patients_http(self, **kwargs):
        patients = request.env['hospital.patient'].sudo().search([])
        data = [{'id': p.id, 'name': p.name, 'age': p.age, 'gender': p.gender} for p in patients]
        return request.make_json_response({'status': 'success', 'data': data})

    # ===================================================
    # GET  →  Read one patient
    # ===================================================
    @http.route('/api/v2/patients/<int:patient_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_patient_http(self, patient_id, **kwargs):
        patient = request.env['hospital.patient'].sudo().browse(patient_id)
        if not patient.exists():
            return request.make_json_response({'status': 'error', 'message': 'Patient not found'}, status=404)
        data = {'id': patient.id, 'name': patient.name, 'age': patient.age, 'gender': patient.gender}
        return request.make_json_response({'status': 'success', 'data': data})

    # ===================================================
    # POST  →  Create new patient
    # ===================================================
    @http.route('/api/v2/patients', type='http', auth='user', methods=['POST'], csrf=False)
    def create_patient_http(self, **kwargs):
        try:
            payload = request.jsonrequest  # reads JSON body
            patient = request.env['hospital.patient'].sudo().create(payload)
            return request.make_json_response({'status': 'success', 'id': patient.id})
        except Exception as e:
            _logger.error(e)
            return request.make_json_response({'status': 'error', 'message': str(e)}, status=400)

    # ===================================================
    # PUT  →  Update patient
    # ===================================================
    @http.route('/api/v2/patients/<int:patient_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_patient_http(self, patient_id, **kwargs):
        try:
            payload = request.jsonrequest
            patient = request.env['hospital.patient'].sudo().browse(patient_id)
            if not patient.exists():
                return request.make_json_response({'status': 'error', 'message': 'Not found'}, status=404)
            patient.write(payload)
            return request.make_json_response({'status': 'success', 'message': 'Updated'})
        except Exception as e:
            return request.make_json_response({'status': 'error', 'message': str(e)}, status=400)

    # ===================================================
    # DELETE  →  Delete patient
    # ===================================================
    @http.route('/api/v2/patients/<int:patient_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_patient_http(self, patient_id, **kwargs):
        patient = request.env['hospital.patient'].sudo().browse(patient_id)
        if not patient.exists():
            return request.make_json_response({'status': 'error', 'message': 'Not found'}, status=404)
        patient.unlink()
        return request.make_json_response({'status': 'success', 'message': 'Deleted'})
