import requests
import json
import unittest
from odoo.tests.common import HttpCase

class TestHospitalAPI(HttpCase):
    """Test case for Hospital YK API endpoints."""

    def test_list_patients(self):
        """Test the /api/v1/patients endpoint."""
        response = self.url_open('/api/v1/patients', method='POST')
        self.assertEqual(response.status_code, 200, "Expected status code 200")

        data = json.loads(response.data)
        self.assertIn('status', data, "Response should contain 'status' key")
        self.assertEqual(data['status'], 'success', "Status should be 'success'")
        self.assertIn('data', data, "Response should contain 'data' key")
        self.assertIsInstance(data['data'], list, "'data' should be a list of patients")
        if data['data']:
            patient = data['data'][0]
            self.assertIn('id', patient, "Patient record should contain 'id'")
            self.assertIn('name', patient, "Patient record should contain 'name'")
            self.assertIn('age', patient, "Patient record should contain 'age'")
            self.assertIn('gender', patient, "Patient record should contain 'gender'")
    def url_open(self, url, method='POST', data=None):
        """Helper method to open a URL and return the response."""
        headers = {'Content-Type': 'application/json'}
        if method == 'GET':
            response = requests.get(self.base_url + url, headers=headers)
        elif method == 'POST':
            response = requests.post(self.base_url + url, headers=headers, data=json.dumps(data))
        else:
            raise ValueError("Unsupported HTTP method: {}".format(method))
        return response
    @property
    def base_url(self):
        """Base URL for the Odoo instance."""
        return 'http://localhost:8018'  # Adjust the port if necessary

import requests
import json
import logging

_logger = logging.getLogger(__name__)

class HospitalYKAPITest:
    """
    Simple tester for Hospital YK REST API (v2).
    Run this manually or use it in Odoo shell for debugging.
    """

    BASE_URL = "http://localhost:8018/api/v2"
    SESSION_ID = "PASTE_YOUR_SESSION_ID_HERE"  # 👈 Replace with your real session ID from Postman

    @classmethod
    def _headers(cls):
        """Return the standard headers with cookie."""
        return {
            "Content-Type": "application/json",
            "Cookie": f"session_id={cls.SESSION_ID}"
        }

    # ===================================================
    # 1️⃣ TEST GET ALL PATIENTS
    # ===================================================
    @classmethod
    def test_get_patients(cls):
        url = f"{cls.BASE_URL}/patients"
        res = requests.get(url, headers=cls._headers())
        print("GET ALL PATIENTS:", res.status_code, res.text)

    # ===================================================
    # 2️⃣ TEST CREATE PATIENT
    # ===================================================
    @classmethod
    def test_create_patient(cls):
        url = f"{cls.BASE_URL}/patients"
        payload = {
            "name": "Test User",
            "age": 30,
            "gender": "male",
            "mobile": "9999999999"
        }
        res = requests.post(url, headers=cls._headers(), data=json.dumps(payload))
        print("CREATE PATIENT:", res.status_code, res.text)

    # ===================================================
    # 3️⃣ TEST UPDATE PATIENT
    # ===================================================
    @classmethod
    def test_update_patient(cls, patient_id):
        url = f"{cls.BASE_URL}/patients/{patient_id}"
        payload = {"age": 31, "mobile": "8888888888"}
        res = requests.put(url, headers=cls._headers(), data=json.dumps(payload))
        print("UPDATE PATIENT:", res.status_code, res.text)

    # ===================================================
    # 4️⃣ TEST DELETE PATIENT
    # ===================================================
    @classmethod
    def test_delete_patient(cls, patient_id):
        url = f"{cls.BASE_URL}/patients/{patient_id}"
        res = requests.delete(url, headers=cls._headers())
        print("DELETE PATIENT:", res.status_code, res.text)

    # ===================================================
    # 5️⃣ TEST APPOINTMENTS (OPTIONAL)
    # ===================================================
    @classmethod
    def test_get_appointments(cls):
        url = f"{cls.BASE_URL}/appointments"
        res = requests.get(url, headers=cls._headers())
        print("GET APPOINTMENTS:", res.status_code, res.text)


# ============================
# 🧪 Quick run section
# ============================
if __name__ == "__main__":
    tester = HospitalYKAPITest
    tester.test_get_patients()
    tester.test_create_patient()
    # After creating, manually check Odoo for the new patient’s ID,
    # then test update/delete:
    # tester.test_update_patient(1)
    # tester.test_delete_patient(1)
