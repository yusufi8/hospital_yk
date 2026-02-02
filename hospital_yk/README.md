# Hospital Management System (HMS) - Odoo Module

A comprehensive Hospital Management System module for Odoo that enables healthcare facilities to efficiently manage patients, appointments, medical records, and billing operations.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Module Dependencies](#module-dependencies)
- [Core Components](#core-components)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [User Roles & Permissions](#user-roles--permissions)
- [Configuration](#configuration)
- [Reports](#reports)
- [Wizards](#wizards)
- [Usage Guide](#usage-guide)
- [Development](#development)
- [License](#license)

## ✨ Features

### Patient Management
- **Create & Manage Patient Profiles** - Store comprehensive patient information including demographics, medical history, and contact details
- **Patient Tagging System** - Categorize patients with custom tags for better organization
- **Appointment Tracking** - Track all appointments associated with each patient
- **Image Storage** - Upload and store patient photographs
- **Guardian Management** - Record guardian information for minor patients
- **Medical History** - Maintain detailed medical history, prescriptions, and dosage information

### Appointment Management
- **Appointment Scheduling** - Schedule appointments with automatic reference numbering
- **Multi-Status Workflow** - Draft → Confirmed → Ongoing → Done/Cancelled workflow
- **Doctor Assignment** - Assign appointments to specific doctors
- **Priority Levels** - Set appointment priorities (Very Low, Low, Normal, High)
- **Appointment Lines** - Add products/services to appointments with quantity and pricing
- **WhatsApp Integration** - Share appointment details via WhatsApp with one click
- **Duplicate Functionality** - Clone appointment records for quick rescheduling

### Billing & Invoicing
- **Invoice Generation** - Create invoices from appointment services
- **Appointment-Invoice Linking** - Link invoices directly to appointments
- **Product Management** - Manage medical services and products
- **Stock Integration** - Track medical inventory
- **Sale Order Integration** - Generate sales orders from appointments

### Reporting
- **Patient Report (PDF)** - Generate comprehensive patient information reports
- **Patient Card** - Create simplified patient identification cards
- **Customizable Templates** - QWeb-based PDF templates with company branding

### Advanced Features
- **Kanban View** - Visual management of patients and appointments
- **Calendar View** - Timeline visualization of appointments
- **Activity View** - Track patient and appointment activities
- **Pivot Analysis** - Analyze data by demographics and status
- **Message Threading** - Built-in communication via chatter
- **Activity Management** - Assign and track tasks and activities
- **Odoo Playground** - Execute Python code for system exploration and testing

## 📦 Installation

### Prerequisites
- Odoo 18.0 or higher
- Python 3.8+
- PostgreSQL database

### Steps

1. **Clone the module** into your Odoo addons directory:
   ```bash
   git clone <repository-url> /path/to/odoo/addons/hospital_yk
   ```

2. **Update the module list** in Odoo:
   - Navigate to Apps > Update Apps List
   - Or use the command: `./odoo-bin -d your_database -u all`

3. **Install the module**:
   - Go to Apps and search for "Hospital Management System"
   - Click Install

4. **Configure** module settings (see Configuration section below)

## 🔗 Module Dependencies

The Hospital Management System requires the following Odoo modules:

| Module | Purpose |
|--------|---------|
| `mail` | Chatter, messaging, and activity features |
| `product` | Product catalog for medical services/supplies |
| `stock` | Inventory management for medical supplies |
| `hr` | Employee/doctor management |
| `hr_holidays` | Leave management for healthcare staff |
| `sale_management` | Sales order functionality for billing |
| `account` | Invoicing and accounting integration |
| `website` | Website integration capabilities |
| `portal` | Patient portal access (future enhancement) |

## 🏗️ Core Components

### Models

#### `hospital.patient`
Main patient record model with fields for:
- Basic information (name, DOB, gender)
- Contact details (mobile, email, address)
- Guardian information
- Medical history and prescriptions
- Doctor assignment
- Tag categorization
- Image storage
- Appointment history

**Key Methods:**
- `_compute_age()` - Auto-calculate age from date of birth
- `_compute_appointment_count()` - Count total appointments
- `create()` - Generate unique patient reference

#### `hospital.appointment`
Appointment scheduling model with:
- Patient and doctor references
- Appointment date/time
- Status workflow (draft, confirmed, ongoing, done, cancelled)
- Priority levels
- Appointment line items
- Notes and other details

**Key Methods:**
- `action_confirm()` - Confirm appointment
- `action_ongoing()` - Mark as in-progress
- `action_done()` - Complete appointment
- `action_cancel()` - Cancel appointment
- `action_share_whatsapp()` - Send WhatsApp notification
- `duplicate_records()` - Clone appointment

#### `hospital.appointment.line`
Line items for appointments containing:
- Product/service reference
- Quantity and pricing
- Auto-calculated totals
- Patient tracking

#### `patient.tag`
Tags for categorizing patients with:
- Custom tag names
- Color coding
- Sequence ordering
- Active/inactive status

#### `hr.employee` (Extended)
Employee extension for doctor/staff roles:
- Employee type selection (Doctor, Nurse, Admin Staff)

#### `account.move` (Extended)
Invoice extension linking to:
- Related appointments
- Automatic reference generation

#### `sale.order` (Extended)
Sales order enhancements including:
- Lot/batch management
- Automatic splitting for multiple lots

### Transient Models

#### `odoo.playground`
A development tool for executing Python code:
- Model selection
- Code execution
- Result display
- Useful for testing and exploration

#### `cancel.appointment.wizard`
Wizard for canceling appointments with:
- Reason documentation
- Cancellation date tracking
- Validation rules

## 📡 API Endpoints

The module provides two sets of REST API endpoints for external integrations:

### API v1 (JSON POST)

**Get All Patients**
```
POST /api/v1/patients
Response: { status, data: [{ id, name, age, gender, phone }] }
```

**Create Patient**
```
POST /api/v1/patients/create
Payload: { name, age, gender, mobile }
Response: { status, data: { id, name } }
```

**Get All Appointments**
```
POST /api/v1/appointments
Response: { status, data: [{ id, patient, doctor, appointment_date, state }] }
```

**Create Appointment**
```
POST /api/v1/appointments/create
Payload: { patient_id, doctor_id, appointment_date }
Response: { status, data: { id, name } }
```

### API v2 (HTTP REST)

**List Patients**
```
GET /api/v2/patients
Response: { status: 'success', data: [...] }
```

**Get Single Patient**
```
GET /api/v2/patients/<patient_id>
Response: { status: 'success', data: { id, name, age, gender } }
```

**Create Patient**
```
POST /api/v2/patients
Body: { name, age, gender, mobile }
Response: { status: 'success', id: <patient_id> }
```

**Update Patient**
```
PUT /api/v2/patients/<patient_id>
Body: { field: value, ... }
Response: { status: 'success', message: 'Updated' }
```

**Delete Patient**
```
DELETE /api/v2/patients/<patient_id>
Response: { status: 'success', message: 'Deleted' }
```

### Authentication
All endpoints require:
- Authenticated Odoo user session
- Proper access permissions (group_user minimum)
- CSRF protection disabled for API calls

## 👥 User Roles & Permissions

The module grants permissions to `base.group_user` (standard users):

| Model | Create | Read | Write | Delete |
|-------|--------|------|-------|--------|
| Patient | ✓ | ✓ | ✓ | ✓ |
| Appointment | ✓ | ✓ | ✓ | ✓ |
| Patient Tag | ✓ | ✓ | ✓ | ✓ |
| Appointment Line | ✓ | ✓ | ✓ | ✓ |
| Cancel Appointment Wizard | ✓ | ✓ | ✓ | ✓ |
| Odoo Playground | ✓ | ✓ | ✓ | ✓ |

### Recommended User Groups
- **Doctors** - Full access to patients and appointments
- **Nurses** - View-only access to patient medical information
- **Receptionists** - Manage appointments and patient check-ins
- **Admin Staff** - Full system access and configuration

## ⚙️ Configuration

### Initial Setup

1. **Create Employee Records**
   - Go to HR > Employees
   - Add doctors and healthcare staff
   - Mark employee type as "Doctor", "Nurse", or "Admin Staff"

2. **Configure Patient Tags**
   - Go to Configuration > Patient Tags
   - Create custom tags (e.g., "VIP", "Critical", "Regular")
   - Assign colors for visual identification

3. **Set Up Products/Services**
   - Go to Inventory > Products
   - Create medical services as products
   - Set pricing and descriptions

4. **Configure Company**
   - Go to Settings > Companies
   - Upload hospital logo
   - Set contact information for report headers

### Sequences

The module automatically generates unique references:
- **Patients**: HP00001, HP00002, etc.
- **Appointments**: HP00001, HP00002, etc.

Sequences are configured in `data/sequence.xml` and can be customized via Sequences menu.

## 📊 Reports

### Patient Report
A comprehensive PDF report containing:
- Hospital header with logo and contact info
- Patient demographics (name, age, gender, DOB)
- Contact details and address
- Medical history and prescriptions
- Dosage and instructions
- Assigned doctor
- Patient photograph
- Doctor signature line
- Generated timestamp

**Access**: Patient > Print > Patient Report

### Patient Card
A simplified identification card format with:
- Hospital branding
- Key patient information
- Patient photo
- Guardian details
- Bordered table format

**Access**: Patient > Print > Patient Card

## 🧙 Wizards

### Cancel Appointment Wizard
Modal dialog for canceling appointments:
- Select appointment to cancel
- Record cancellation reason
- Set cancellation date
- Validation prevents same-day cancellations

**Access**: Appointments > Cancel (or Cancellation menu)

### Patient Reassign Wizard
(In development) For reassigning patients to different doctors:
- Select current doctor
- Choose new doctor
- Select patients to reassign
- Automatic chatter notification

## 📖 Usage Guide

### Creating a Patient

1. Go to **Front Desk > Patients**
2. Click **Create**
3. Fill in patient information:
   - Name (required)
   - Date of birth
   - Gender
   - Contact details
   - Guardian info (if minor)
4. Save

The system automatically generates a unique reference number.

### Scheduling an Appointment

1. Go to **Appointments > Appointment**
2. Click **Create**
3. Select patient
4. Choose appointment date/time
5. Assign doctor (optional)
6. Add priority level
7. Save

Workflow transitions: Draft → Confirm → Ongoing → Done

### Adding Appointment Services

1. Open appointment form
2. Go to **Prescription** tab
3. Click **Add a line**
4. Select product/service
5. Enter quantity and price
6. Total auto-calculates

### Generating Reports

1. Select patient(s) from list view
2. Click **Print > Patient Report** or **Patient Card**
3. PDF downloads automatically

### Using the Kanban Board

1. Go to **Appointments** or **Patients**
2. Switch to **Kanban** view
3. Drag cards between columns to update status
4. Click card to view details

### Calendar View

1. Go to **Appointments > Appointment** or **Patients > Patient**
2. Switch to **Calendar** view
3. See appointments/patient dates visualized
4. Click event to open record

### Using the Odoo Playground

1. Go to **Configuration > Playground**
2. Optionally select a model
3. Enter Python code (access via `self.env`)
4. Click **Execute**
5. Results display below

**Example Code:**
```python
# List all patients
self.env['hospital.patient'].search([]).mapped('name')

# Count appointments by doctor
self.env['hospital.appointment'].read_group([], ['doctor_id'], ['doctor_id'])

# Get patient with highest appointment count
self.env['hospital.patient'].search_read([], ['name', 'appointment_count'], limit=1)
```

## 🔧 Development

### Project Structure

```
hospital_yk/
├── __init__.py                 # Package initialization
├── __manifest__.py             # Module metadata and dependencies
├── controllers/
│   ├── __init__.py
│   ├── main.py                # REST API endpoints
│   └── test_controller.py      # API tests
├── models/
│   ├── __init__.py
│   ├── patient.py              # Patient model
│   ├── appointment.py          # Appointment model
│   ├── appointment_line.py     # Appointment line items
│   ├── patient_tag.py          # Patient tags
│   ├── account_move.py         # Invoice extension
│   ├── hr_employee.py          # Employee extension
│   ├── odoo_playground.py      # Development tool
│   ├── sale_res.py             # Sale order extension
│   └── sale_page.py            # Lot management
├── views/
│   ├── patient_views.xml       # Patient form, list, kanban, calendar, pivot
│   ├── patient_readonly_views.xml  # Read-only patient views
│   ├── appointment_views.xml    # Appointment views with all view types
│   ├── appointment_line_views.xml  # Line item views
│   ├── patient_tag_views.xml    # Tag views
│   ├── employee_id_views.xml    # Employee extension
│   ├── account_move_views.xml   # Invoice extension
│   ├── sale_res.xml             # Sale order extension
│   ├── sale_page.xml            # Lot visibility
│   ├── menu.xml                 # Navigation menu structure
│   └── odoo_playground_views.xml # Playground views
├── wizard/
│   ├── __init__.py
│   ├── cancel_appointment.py    # Cancellation wizard
│   ├── cancel_appointment_views.xml
│   ├── patient_reassign.py      # Reassignment wizard
│   └── patient_reassign_views.xml
├── report/
│   ├── __init__.py
│   ├── patient_report.py        # Report classes
│   └── patient_report_pdf.xml   # PDF templates
├── data/
│   └── sequence.xml             # Auto-increment sequences
├── security/
│   └── ir.model.access.csv      # Access control rules
└── .gitignore                   # Git ignore file
```

### Adding Custom Fields

To add fields to an existing model, extend it:

```python
from odoo import fields, models

class HospitalPatient(models.Model):
    _inherit = 'hospital.patient'
    
    # Your custom fields
    blood_type = fields.Selection([('O+', 'O+'), ...], string="Blood Type")
    allergies = fields.Text(string="Known Allergies")
```

### Creating Custom Views

Create a new XML file in `views/` and reference it in `__manifest__.py`:

```xml
<record id="view_hospital_patient_custom_form" model="ir.ui.view">
    <field name="name">hospital.patient.custom.form</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <form string="Custom Patient Form">
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="date_of_birth"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

### Testing the API

Use the provided test file:

```bash
# Run unit tests
python -m unittest hospital_yk.controllers.test_controller

# Or use with Odoo test runner
./odoo-bin -d your_database -m hospital_yk --test-tags=hospital_yk
```

### API Testing with cURL

```bash
# Get patients (requires session)
curl -X GET http://localhost:8018/api/v2/patients \
  -H "Cookie: session_id=YOUR_SESSION_ID"

# Create patient
curl -X POST http://localhost:8018/api/v2/patients \
  -H "Content-Type: application/json" \
  -H "Cookie: session_id=YOUR_SESSION_ID" \
  -d '{"name":"John Doe","age":30,"gender":"male","mobile":"1234567890"}'
```

## 🐛 Debugging

### Enable Logging

```python
import logging
_logger = logging.getLogger(__name__)

_logger.info("Info message")
_logger.warning("Warning message")
_logger.error("Error message")
```

### Database Queries

Use the playground to inspect data:

```python
# Show all patient data
patients = self.env['hospital.patient'].search([])
return [{'id': p.id, 'name': p.name, 'age': p.age} for p in patients]

# Debug appointment workflow
appointment = self.env['hospital.appointment'].browse(1)
print(f"State: {appointment.state}, Patient: {appointment.patient_id.name}")
```

## 📝 License

This module is licensed under the LGPL-3 License. See LICENSE file for details.

## 👤 Author

**Yusuf Khan**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team
- Check existing documentation

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 18.0.1.1 | 2024 | Initial release with patient, appointment, and billing features |

---

**Last Updated**: February 2026  
**Odoo Version**: 18.0  
**Status**: Active Development
