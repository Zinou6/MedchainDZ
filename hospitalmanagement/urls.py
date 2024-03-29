from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('blockchain/', views.blockchain_view,name='blockchain'),
    path('aboutus/', views.aboutus_view),
    path('contactus/', views.contactus_view),


    path('adminclick/', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('receptionistclick', views.receptionistclick_view),

    path('adminsignup/', views.admin_signup_view),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view),
    path('receptionistsignup/',views.receptionist_signup_view),
    
    path('adminlogin/', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin/', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('receptionistlogin/', LoginView.as_view(template_name='hospital/receptionistlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-receptionist', views.admin_receptionist_view,name='admin-receptionist'),
    path('admin-view-receptionist', views.admin_view_receptionist_view,name='admin-view-receptionist'),
    path('delete-receptionist-from-hospital/<int:pk>', views.delete_receptionist_from_hospital_view,name='delete-receptionist-from-hospital'),
    path('update-receptionist/<int:pk>', views.update_receptionist_view,name='update-receptionist'),
    path('admin-add-receptionist', views.admin_add_receptionist_view,name='admin-add-receptionist'),
    path('admin-approve-receptionist', views.admin_approve_receptionist_view,name='admin-approve-receptionist'),
    path('approve-receptionist/<int:pk>', views.approve_receptionist_view,name='approve-receptionist'),
    path('reject-receptionist/<int:pk>', views.reject_receptionist_view,name='reject-receptionist'),
    
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),

    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('doctor-view-document', views.doctor_view_document,name='doctor-view-document'),
    path('doctor-add-prescription/<int:patieniID>',views.doctor_add_prescription,name='doctor-add-prescription'),
    path('doctor-add-radio/<int:patieniID>',views.doctor_add_radio,name='doctor-add-radio'),
    path('doctor-add-analyse/<int:patieniID>',views.doctor_add_analyse,name='doctor-add-analyse'),
    path('doctor-add-comment/<int:patieniID>',views.doctor_add_comment,name='doctor-add-comment'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]


#---------FOR RECEPTIONIST RELATED URLS--------------------------------
urlpatterns +=[

    path('receptionist-dashboard', views.receptionist_dashboard_view,name='receptionist-dashboard'),
    
    path('receptionist-view-doctor', views.receptionist_view_doctor_view,name='receptionist-view-doctor'),
    
    path('receptionist-patient', views.receptionist_patient_view,name='receptionist-patient'),
    path('receptionist-view-patient', views.receptionist_view_patient_view,name='receptionist-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('receptionist-add-patient', views.receptionist_add_patient_view,name='receptionist-add-patient'),
    path('receptionist-approve-patient', views.receptionist_approve_patient_view,name='receptionist-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('receptionist-discharge-patient', views.receptionist_discharge_patient_view,name='receptionist-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

    path('receptionist-appointment', views.receptionist_appointment_view,name='receptionist-appointment'),
    path('receptionist-view-appointment', views.receptionist_view_appointment_view,name='receptionist-view-appointment'),
    path('receptionist-add-appointment', views.receptionist_add_appointment_view,name='receptionist-add-appointment'),
    path('receptionist-approve-appointment', views.receptionist_approve_appointment_view,name='receptionist-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]
