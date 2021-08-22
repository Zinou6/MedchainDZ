# MedchainDZ
MedchainDZ is a distributed file sharing system for medical services using blockchain technology.

## Functions

### Admin
- Signup their account. Then Login (No approval Required).
- Can register/view/approve/reject/delete doctor (approve those doctor who applied for job in their hospital).
- Can admit/view/approve/reject receptionist (approve those receptionist who applied for job in their hospital).
- Can Generate/Download Invoice pdf (Generate Invoice according to medicine cost, room charge, doctor charge and other charge).

### Doctor
- Apply for job in hospital. Then Login (Approval required by hospital admin, Then only doctor can login).
- Can only view their patient details (symptoms, name, mobile ) assigned to that doctor by receptionist.
- Can view/add document for patient.
- Can view their discharged(by receptionist) patient list.
- Can view their Appointments, booked by receptionist.
- Can delete their Appointment, when doctor attended their appointment.

### Receptionist
- Apply for job in hospital. Then Login (Approval required by hospital admin, Then only receptionist can login).
- Can admit/view/approve/reject/discharge patient (discharge patient when treatment is done).
- Can view/book/approve Appointment (approve those appointments which is requested by patient).

### Patient
- Create account for admit in hospital. Then Login (Approval required by hospital receptionist, Then only patient can login).
- Can view assigned doctor's details like ( specialization, mobile, address).
- Can view their documents.
- Can view their booked appointment status (pending/confirmed by receptionist).
- Can book appointments.(approval required by receptionist)
- Can view/download Invoice pdf (Only when that patient is discharged by receptionist).

---

## HOW TO RUN THIS PROJECT

- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
source env/bin/activate 
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```
- Show blockchain list
```
http://127.0.0.1:8000/blockchain
```
