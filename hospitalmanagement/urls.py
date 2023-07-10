from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView
from hospital.views import (
    DoctorLoginView,
    ParamedicLoginView,
    PatientLoginView,
    DoctorAddReview,
)


# -------------FOR ADMIN RELATED URLS
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name=""),
    path("aboutus", views.aboutus_view),
    path("contactus", views.contactus_view),
    path("adminclick", views.adminclick_view),
    path("doctorclick", views.doctorclick_view),
    path("paramedicclick", views.paramedicclick_view),
    path("patientclick", views.patientclick_view),
    path("adminsignup", views.admin_signup_view),
    path("doctorsignup", views.doctor_signup_view, name="doctorsignup"),
    path("paramedicsignup", views.paramedic_signup_view, name="paramedicsignup"),
    path("patientsignup", views.patient_signup_view, name="patientsignup"),
    path("adminlogin", LoginView.as_view(template_name="hospital/adminlogin.html")),
    # path('doctorlogin/', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    # path('paramediclogin/', LoginView.as_view(template_name='hospital/paramediclogin.html')),
    # path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path("patientlogin", PatientLoginView.as_view(), name="patientlogin"),
    path("doctorlogin", DoctorLoginView.as_view(), name="doctorlogin"),
    path("paramediclogin", ParamedicLoginView.as_view(), name="paramediclogin"),
    path("afterlogin", views.afterlogin_view, name="afterlogin"),
    path(
        "logout", LogoutView.as_view(template_name="hospital/index.html"), name="logout"
    ),
    path("admin-dashboard", views.admin_dashboard_view, name="admin-dashboard"),
    path("admin-doctor", views.admin_doctor_view, name="admin-doctor"),
    path("admin-view-doctor", views.admin_view_doctor_view, name="admin-view-doctor"),
    path(
        "delete-doctor-from-hospital/<int:pk>",
        views.delete_doctor_from_hospital_view,
        name="delete-doctor-from-hospital",
    ),
    path("update-doctor/<int:pk>", views.update_doctor_view, name="update-doctor"),
    path("admin-add-doctor", views.admin_add_doctor_view, name="admin-add-doctor"),
    path(
        "admin-approve-doctor",
        views.admin_approve_doctor_view,
        name="admin-approve-doctor",
    ),
    path("approve-doctor/<int:pk>", views.approve_doctor_view, name="approve-doctor"),
    path("reject-doctor/<int:pk>", views.reject_doctor_view, name="reject-doctor"),
    path(
        "admin-view-doctor-specialisation",
        views.admin_view_doctor_specialisation_view,
        name="admin-view-doctor-specialisation",
    ),
    path("admin-paramedic", views.admin_paramedic_view, name="admin-paramedic"),
    path(
        "admin-view-paramedic",
        views.admin_view_paramedic_view,
        name="admin-view-paramedic",
    ),
    path(
        "delete-paramedic-from-hospital/<int:pk>",
        views.delete_paramedic_from_hospital_view,
        name="delete-paramedic-from-hospital",
    ),
    path(
        "update-paramedic/<int:pk>",
        views.update_paramedic_view,
        name="update-paramedic",
    ),
    path(
        "admin-add-paramedic",
        views.admin_add_paramedic_view,
        name="admin-add-paramedic",
    ),
    path(
        "admin-approve-paramedic",
        views.admin_approve_paramedic_view,
        name="admin-approve-paramedic",
    ),
    path(
        "approve-paramedic/<int:pk>",
        views.approve_paramedic_view,
        name="approve-paramedic",
    ),
    path(
        "reject-paramedic/<int:pk>",
        views.reject_paramedic_view,
        name="reject-paramedic",
    ),
    path("admin-patient", views.admin_patient_view, name="admin-patient"),
    path(
        "admin-view-patient", views.admin_view_patient_view, name="admin-view-patient"
    ),
    path(
        "delete-patient-from-hospital/<int:pk>",
        views.delete_patient_from_hospital_view,
        name="delete-patient-from-hospital",
    ),
    path("update-patient/<int:pk>", views.update_patient_view, name="update-patient"),
    path("admin-add-patient", views.admin_add_patient_view, name="admin-add-patient"),
    path(
        "admin-approve-patient",
        views.admin_approve_patient_view,
        name="admin-approve-patient",
    ),
    path(
        "approve-patient/<int:pk>", views.approve_patient_view, name="approve-patient"
    ),
    path("reject-patient/<int:pk>", views.reject_patient_view, name="reject-patient"),
    path(
        "admin-discharge-patient",
        views.admin_discharge_patient_view,
        name="admin-discharge-patient",
    ),
    path(
        "discharge-patient/<int:pk>",
        views.discharge_patient_view,
        name="discharge-patient",
    ),
    path("download-pdf/<int:pk>", views.download_pdf_view, name="download-pdf"),
    path("admin-appointment", views.admin_appointment_view, name="admin-appointment"),
    path(
        "admin-view-appointment",
        views.admin_view_appointment_view,
        name="admin-view-appointment",
    ),
    path(
        "admin-add-appointment",
        views.admin_add_appointment_view,
        name="admin-add-appointment",
    ),
    path(
        "admin-approve-appointment",
        views.admin_approve_appointment_view,
        name="admin-approve-appointment",
    ),
    path(
        "admin-approved-appointment/<int:pk>",
        views.admin_approved_appointment_view,
        name="admin-approved-appointment",
    ),
    path(
        "reject-appointment/<int:pk>",
        views.reject_appointment_view,
        name="reject-appointment",
    ),
    path("admin-facility", views.admin_facility_view, name="admin-facility"),
    path("admin-add-facility", views.admin_add_facility, name="admin-add-facility"),
    path(
        "admin-view-facility",
        views.admin_view_facility_view,
        name="admin-view-facility",
    ),
    path(
        "admin-delete-facility-from-hospital/<int:pk>",
        views.admin_delete_facility_from_hospital_view,
        name="admin-delete-facility-from-hospital",
    ),
]


# ---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path("doctor-dashboard", views.doctor_dashboard_view, name="doctor-dashboard"),
    path("doctor-patient", views.doctor_patient_view, name="doctor-patient"),
    path(
        "doctor-view-patient",
        views.doctor_view_patient_view,
        name="doctor-view-patient",
    ),
    path(
        "doctor-view-discharge-patient",
        views.doctor_view_discharge_patient_view,
        name="doctor-view-discharge-patient",
    ),
    path(
        "doctor-appointment", views.doctor_appointment_view, name="doctor-appointment"
    ),
    path(
        "doctor-view-appointment",
        views.doctor_view_appointment_view,
        name="doctor-view-appointment",
    ),
    path(
        "doctor-delete-appointment",
        views.doctor_delete_appointment_view,
        name="doctor-delete-appointment",
    ),
    path(
        "delete-appointment/<int:pk>",
        views.delete_appointment_view,
        name="delete-appointment",
    ),
    path(
        "doctor-approve-appointment",
        views.doctor_approve_appointment_view,
        name="doctor-approve-appointment",
    ),
    path(
        "doctor-approved-appointment/<int:pk>",
        views.doctor_approved_appointment_view,
        name="doctor-approved-appointment",
    ),
    path(
        "doctor-discharge-patient",
        views.doctor_discharge_patient_view,
        name="doctor-discharge-patient",
    ),
    path(
        "doc-discharge-patient/<int:pk>",
        views.doc_discharge_patient_view,
        name="doc-discharge-patient",
    ),
    path("download-pdf/<int:pk>", views.download_pdf_view, name="download-pdf"),
    path(
        "doctor-create-room",
        views.doctor_create_room_view,
        name="doctor_create_room_view",
    ),
    path(
        "doctor-add-review/<int:pk>",
        DoctorAddReview.as_view(),
        name="doctor-add-review",
    ),
    # path('video_call/<int:patient_id>/', views.video_call_view, name='video_call'),
    #     path('doctor-approve-appointment', views.doctor_approve_appointment_view,name='doctor-approve-appointment'),
    #     path('doctor-appointment/<int:pk>', views.doc_approve_appointment_view,name='doc-approve-appointment'),
]

# ---------FOR PARAMEDIC RELATED URLS-------------------------------------
urlpatterns += [
    path(
        "paramedic-dashboard",
        views.paramedic_dashboard_view,
        name="paramedic-dashboard",
    ),
    path("paramedic-patient", views.paramedic_patient_view, name="paramedic-patient"),
    path(
        "paramedic-view-patient",
        views.paramedic_view_patient_view,
        name="paramedic-view-patient",
    ),
    path(
        "para-delete-patient-from-hospital/<int:pk>",
        views.para_delete_patient_from_hospital_view,
        name="para-delete-patient-from-hospital",
    ),
    path(
        "para-update-patient/<int:pk>",
        views.para_update_patient_view,
        name="para-update-patient",
    ),
    path(
        "paramedic-add-patient",
        views.paramedic_add_patient_view,
        name="admin-add-patient",
    ),
    path(
        "paramedic-approve-patient",
        views.paramedic_approve_patient_view,
        name="paramedic-approve-patient",
    ),
    path(
        "para-approve-patient/<int:pk>",
        views.para_approve_patient_view,
        name="para-approve-patient",
    ),
    path(
        "para-reject-patient/<int:pk>",
        views.para_reject_patient_view,
        name="para-reject-patient",
    ),
    path(
        "paramedic-appointment",
        views.paramedic_appointment_view,
        name="paramedic-appointment",
    ),
    path(
        "paramedic-view-appointment",
        views.paramedic_view_appointment_view,
        name="paramedic-view-appointment",
    ),
    path(
        "paramedic-add-appointment",
        views.paramedic_add_appointment_view,
        name="paramedic-add-appointment",
    ),
    path(
        "paramedic-approve-appointment",
        views.paramedic_approve_appointment_view,
        name="paramedic-approve-appointment",
    ),
    path(
        "paramedic-approved-appointment/<int:pk>",
        views.paramedic_approved_appointment_view,
        name="paramedic-approved-appointment",
    ),
]


# ---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path("patient-dashboard", views.patient_dashboard_view, name="patient-dashboard"),
    path(
        "patient-appointment",
        views.patient_appointment_view,
        name="patient-appointment",
    ),
    path(
        "patient-book-appointment",
        views.patient_book_appointment_view,
        name="patient-book-appointment",
    ),
    path(
        "patient-view-appointment",
        views.patient_view_appointment_view,
        name="patient-view-appointment",
    ),
    path("patient-discharge", views.patient_discharge_view, name="patient-discharge"),
    # path('join',views.paitient_join_romm_view, name='join_room'),
    path("patient-view-review", views.patient_view_review, name="patient-view-review"),
    # views for video calling
    path("meeting/", views.videocall, name="meeting"),
    path("join/", views.join_room, name="join_room"),
]
