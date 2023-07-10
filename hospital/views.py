from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from hospital.models import Patient
from django.core.cache import cache

from .imageblur import is_image_blurry, handle_uploaded_file


# Create your views here.
def home_view(request):
    # send_mail(
    #             'approval mail',
    #             'doctor is waiting for your approval ',
    #             'areezk17@gmail.com',
    #             ['areezaz999@gmail.com'],
    #             fail_silently=False,
    #             )
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/index.html")


# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/adminclick.html")


# for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/doctorclick.html")


def paramedicclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/paramedicclick.html")


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/patientclick.html")


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == "POST":
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name="ADMIN")
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect("adminlogin")
    return render(request, "hospital/adminsignup.html", {"form": form})


from django.core.mail import send_mail


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            # sender_email = user.email

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)

            success_message = "Registration successful! Please wait for approval."
            messages.success(request, success_message)

            send_mail(
                "approval mail",
                "doctor " + user.username + " is waiting for your approval ",
                "areezk17@gmail.com",  # sender's email address
                ["areezaz999@gmail.com"],  # receiver's email address
                fail_silently=False,
            )

        return redirect(reverse("doctorlogin") + "?success_message=" + success_message)
        # return HttpResponseRedirect('doctorlogin')
    return render(request, "hospital/doctorsignup.html", context=mydict)


def paramedic_signup_view(request):
    userForm = forms.ParamedicUserForm()
    paramedicForm = forms.ParamedicForm()
    mydict = {"userForm": userForm, "paramedicForm": paramedicForm}
    if request.method == "POST":
        userForm = forms.ParamedicUserForm(request.POST)
        paramedicForm = forms.ParamedicForm(request.POST, request.FILES)
        if userForm.is_valid() and paramedicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            paramedic = paramedicForm.save(commit=False)
            paramedic.user = user
            paramedic = paramedic.save()
            my_paramedic_group = Group.objects.get_or_create(name="PARAMEDIC")
            my_paramedic_group[0].user_set.add(user)
            success_message = "Registration successful! Please wait for approval."
            messages.success(request, success_message)

            send_mail(
                "approval mail",
                "paramedic " + user.username + " is waiting for your approval ",
                "areezk17@gmail.com",  # sender's email address
                ["areezaz999@gmail.com"],  # receiver's email address
                fail_silently=False,
            )

        return redirect(
            reverse("paramediclogin") + "?success_message=" + success_message
        )
        # return HttpResponseRedirect('paramediclogin')
    return render(request, "hospital/paramedicsignup.html", context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
            success_message = "Your Account has been Registered. Please login."
            messages.success(request, success_message)

        return redirect(reverse("patientlogin") + "?success_message=" + success_message)

    return render(request, "hospital/patientsignup.html", context=mydict)


class DoctorLoginView(LoginView):
    template_name = "hospital/doctorlogin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_message = self.request.GET.get("success_message")
        if success_message:
            context["success_message"] = success_message
        return context


class ParamedicLoginView(LoginView):
    template_name = "hospital/paramediclogin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_message = self.request.GET.get("success_message")
        if success_message:
            context["success_message"] = success_message
        return context


class PatientLoginView(LoginView):
    template_name = "hospital/patientlogin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success_message = self.request.GET.get("success_message")
        if success_message:
            context["success_message"] = success_message
        return context


# -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_paramedic(user):
    return user.groups.filter(name="PARAMEDIC").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")
    elif is_paramedic(request.user):
        accountapproval = models.Paramedic.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("paramedic-dashboard")
        else:
            return render(request, "hospital/paramedic_wait_for_approval.html")
    elif is_patient(request.user):
        return redirect("patient-dashboard")
        # accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        # if accountapproval:
        #     return redirect('patient-dashboard')
        # else:
        #     return render(request,'hospital/patient_wait_for_approval.html')


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by("-id")
    paramedics = models.Paramedic.objects.all().order_by("-id")
    patients = models.Patient.objects.all().order_by("-id")
    facility = models.Facility.objects.all().order_by("-id")
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    paramediccount = models.Paramedic.objects.all().filter(status=True).count()
    pendingparamediccount = models.Paramedic.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = (
        models.Appointment.objects.all().filter(status=False).count()
    )
    mydict = {
        "doctors": doctors,
        "patients": patients,
        "paramedics": paramedics,
        "facility": facility,
        "doctorcount": doctorcount,
        "pendingdoctorcount": pendingdoctorcount,
        "paramediccount": paramediccount,
        "pendingparamediccount": pendingparamediccount,
        "patientcount": patientcount,
        "pendingpatientcount": pendingpatientcount,
        "appointmentcount": appointmentcount,
        "pendingappointmentcount": pendingappointmentcount,
    }
    return render(request, "hospital/admin_dashboard.html", context=mydict)


# this view for sidebar click on admin page
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, "hospital/admin_doctor.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-view-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect("admin-view-doctor")
    return render(request, "hospital/admin_update_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-doctor")
    return render(request, "hospital/admin_add_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, "hospital/admin_approve_doctor.html", {"doctors": doctors})


from django.core.mail import send_mail


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()

    # Send email notification
    recipient_email = doctor.user.email
    subject = "Doctor Approval Status"
    message = "Dear Doctor, your approval status for the clinic is: Accepted."

    send_mail(subject, message, "areek.com", [recipient_email])

    return redirect(reverse("admin-approve-doctor"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-approve-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_doctor_specialisation.html", {"doctors": doctors}
    )


# paremdedic views
def admin_paramedic_view(request):
    return render(request, "hospital/admin_paramedic.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_paramedic_view(request):
    paramedic = models.Paramedic.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_paramedic.html", {"paramedic": paramedic}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_paramedic_view(request):
    # those whose approval are needed
    paramedic = models.Paramedic.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_paramedic.html", {"paramedic": paramedic}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_paramedic_view(request, pk):
    paramedic = models.Paramedic.objects.get(id=pk)
    paramedic.status = True
    paramedic.save()
    return redirect(reverse("admin-approve-paramedic"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_paramedic_view(request, pk):
    paramedic = models.Paramedic.objects.get(id=pk)
    user = models.User.objects.get(id=paramedic.user_id)
    user.delete()
    paramedic.delete()
    return redirect("admin-approve-paramedic")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_paramedic_from_hospital_view(request, pk):
    paramedic = models.Paramedic.objects.get(id=pk)
    user = models.User.objects.get(id=paramedic.user_id)
    user.delete()
    paramedic.delete()
    return redirect("admin-view-paramedic")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_paramedic_view(request, pk):
    paramedic = models.Paramedic.objects.get(id=pk)
    user = models.User.objects.get(id=paramedic.user_id)

    userForm = forms.ParamedicUserForm(instance=user)
    paramedicForm = forms.ParamedicForm(request.FILES, instance=paramedic)
    mydict = {"userForm": userForm, "paramedicForm": paramedicForm}
    if request.method == "POST":
        userForm = forms.ParamedicUserForm(request.POST, instance=user)
        paramedicForm = forms.ParamedicForm(
            request.POST, request.FILES, instance=paramedic
        )
        if userForm.is_valid() and paramedicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            paramedic = paramedicForm.save(commit=False)
            paramedic.status = True
            paramedic.save()
            return redirect("admin-view-paramedic")
    return render(request, "hospital/admin_update_paramedic.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_paramedic_view(request):
    userForm = forms.ParamedicUserForm()
    paramedicForm = forms.ParamedicForm()
    mydict = {"userForm": userForm, "paramedicForm": paramedicForm}
    if request.method == "POST":
        userForm = forms.ParamedicUserForm(request.POST)
        paramedicForm = forms.ParamedicForm(request.POST, request.FILES)
        if userForm.is_valid() and paramedicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            paramedic = paramedicForm.save(commit=False)
            paramedic.user = user
            paramedic.status = True
            paramedic.save()

            my_paramedic_group = Group.objects.get_or_create(name="PARAMEDIC")
            my_paramedic_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-paramedic")
    return render(request, "hospital/admin_add_paramedic.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, "hospital/admin_patient.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_patient.html", {"patients": patients})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            return redirect("admin-view-patient")
    return render(request, "hospital/admin_update_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()

            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-patient")
    return render(request, "hospital/admin_add_patient.html", context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse("admin-approve-patient"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-approve-patient")


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_discharge_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = date.today() - patient.admitDate  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        "patientId": pk,
        "name": patient.get_name,
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "admitDate": patient.admitDate,
        "todayDate": date.today(),
        "day": d,
        "assignedDoctorName": assignedDoctor[0].first_name,
    }
    if request.method == "POST":
        feeDict = {
            "roomCharge": int(request.POST["roomCharge"]) * int(d),
            "doctorFee": request.POST["doctorFee"],
            "medicineCost": request.POST["medicineCost"],
            "OtherCharge": request.POST["OtherCharge"],
            "total": (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"]),
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST["medicineCost"])
        pDD.roomCharge = int(request.POST["roomCharge"]) * int(d)
        pDD.doctorFee = int(request.POST["doctorFee"])
        pDD.OtherCharge = int(request.POST["OtherCharge"])
        pDD.total = (
            (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"])
        )
        pDD.save()
        return render(request, "hospital/patient_final_bill.html", context=patientDict)
    return render(request, "hospital/patient_generate_bill.html", context=patientDict)


# --------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return


def download_pdf_view(request, pk):
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=pk)
        .order_by("-id")[:1]
    )
    dict = {
        "patientName": dischargeDetails[0].patientName,
        "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
        "address": dischargeDetails[0].address,
        "mobile": dischargeDetails[0].mobile,
        "symptoms": dischargeDetails[0].symptoms,
        "admitDate": dischargeDetails[0].admitDate,
        "releaseDate": dischargeDetails[0].releaseDate,
        "daySpent": dischargeDetails[0].daySpent,
        "medicineCost": dischargeDetails[0].medicineCost,
        "roomCharge": dischargeDetails[0].roomCharge,
        "doctorFee": dischargeDetails[0].doctorFee,
        "OtherCharge": dischargeDetails[0].OtherCharge,
        "total": dischargeDetails[0].total,
    }
    return render_to_pdf("hospital/download_bill.html", dict)


# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, "hospital/admin_appointment.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(
        request, "hospital/admin_view_appointment.html", {"appointments": appointments}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {
        "appointmentForm": appointmentForm,
    }
    if request.method == "POST":
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.POST.get("patientId")
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get("patientId")
            ).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect("admin-view-appointment")
    return render(request, "hospital/admin_add_appointment.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(
        request,
        "hospital/admin_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approved_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse("admin-approve-appointment"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect("admin-approve-appointment")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_facility_view(request):
    return render(request, "hospital/admin_facility.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
# from django.shortcuts import render, redirect
# from . import forms


def admin_add_facility(request):
    form = forms.FacilityForm()

    if request.method == "POST":
        form = forms.FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin-dashboard")

    return render(request, "hospital/admin_add_facility.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_facility_view(request):
    facilities = models.Facility.objects.all().filter()
    return render(
        request, "hospital/admin_view_facility.html", {"facilities": facilities}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_delete_facility_from_hospital_view(request, pk):
    # paramedic=models.Paramedic.objects.get(id=pk)
    facility = models.Facility.objects.get(id=pk)
    # user=models.User.objects.get(id=paramedic.user_id)

    # facility=models.Facility.objects.get(id=pk)# Doctor
    # paramedic=models.Paramedic.objects.get(id=facility.facility_id) # User

    # doctor=models.Doctor.objects.get(id=pk)
    # user=models.User.objects.get(id=doctor.user_id)
    # user.delete()
    # paramedic.delete()
    facility.delete()

    return redirect("admin-view-facility")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect("admin-view-doctor")
    return render(request, "hospital/admin_update_doctor.html", context=mydict)


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .count()
    )
    appointmentcount = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .count()
    )
    patientdischarged = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
        .count()
    )

    # for  table in doctor dashboard
    appointments = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .order_by("-id")
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = (
        models.Patient.objects.all()
        .filter(status=True, user_id__in=patientid)
        .order_by("-id")
    )
    appointments = zip(appointments, patients)
    mydict = {
        "patientcount": patientcount,
        "appointmentcount": appointmentcount,
        "patientdischarged": patientdischarged,
        "appointments": appointments,
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_dashboard.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_patient.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(
        request,
        "hospital/doctor_view_discharge_patient.html",
        {"dischargedpatients": dischargedpatients, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(request, "hospital/doctor_appointment.html", {"doctor": doctor})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_view_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


# meeting generation
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
import random


def doctor_create_room_view(request):
    pk = request.GET.get("pk")
    appointment = models.Appointment.objects.get(id=pk)
    appointment.roomID = random.randint(1000, 9999)
    appointment.save()
    patienid = appointment.patientId
    patient = models.Patient.objects.get(user_id=patienid)
    print(appointment.roomID)
    print(patient)
    cache.set("roomID", appointment.roomID)
    # request.session['roomID'] = appointment.roomID
    return redirect("meeting")


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(
        status=True, doctorId=request.user.id
    )
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(
        request,
        "hospital/doctor_delete_appointment.html",
        {"appointments": appointments, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_approve_appointment_view(request):
    # Get the currently logged-in doctor
    doctor = request.user.doctor

    # Filter appointments where the associated doctor is the currently logged-in doctor
    appointments = models.Appointment.objects.filter(
        doctorId=doctor.get_id, status=False
    )
    return render(
        request,
        "hospital/doctor_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_approved_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse("doctor-approve-appointment"))


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_discharge_patient_view(request):
    # patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    # doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id
    )
    return render(
        request, "hospital/doctor_discharge_patient.html", {"patients": patients}
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doc_discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = date.today() - patient.admitDate  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        "patientId": pk,
        "name": patient.get_name,
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "admitDate": patient.admitDate,
        "todayDate": date.today(),
        "day": d,
        "assignedDoctorName": assignedDoctor[0].first_name,
    }
    if request.method == "POST":
        feeDict = {
            "roomCharge": int(request.POST["roomCharge"]) * int(d),
            "doctorFee": request.POST["doctorFee"],
            "medicineCost": request.POST["medicineCost"],
            "OtherCharge": request.POST["OtherCharge"],
            "total": (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"]),
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST["medicineCost"])
        pDD.roomCharge = int(request.POST["roomCharge"]) * int(d)
        pDD.doctorFee = int(request.POST["doctorFee"])
        pDD.OtherCharge = int(request.POST["OtherCharge"])
        pDD.total = (
            (int(request.POST["roomCharge"]) * int(d))
            + int(request.POST["doctorFee"])
            + int(request.POST["medicineCost"])
            + int(request.POST["OtherCharge"])
        )
        pDD.save()
        return render(
            request, "hospital/doctor_patient_final_bill.html", context=patientDict
        )
    return render(
        request, "hospital/doctor_patient_generate_bill.html", context=patientDict
    )


# import uuid
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
# def video_call_view(request, patient_id):
#     # Logic to initiate the video call
#     try:
#         # Retrieve patient details based on the patient_id
#         patient = Patient.objects.get(id=patient_id)

#         # Perform any necessary operations to initiate the call
#         # This can involve integrating with a WebRTC library or API

#         # Generate a unique call session ID or room name
#         call_session_id = str(uuid.uuid4())

#         # Save the call session ID in the session or database for later use
#         request.session['call_session_id'] = call_session_id

#         # Pass relevant data to the video_call.html template
#         context = {
#             'patient': patient,
#             'call_session_id': call_session_id,
#         }

#         return render(request, 'hospital/video_call.html', context)

#     except Patient.DoesNotExist:
#         return HttpResponse("Patient not found.")


from django.views.generic import UpdateView
from django.urls import reverse_lazy


class DoctorAddReview(UpdateView):
    template_name = "hospital/doctor_add_review.html"
    form_class = forms.AddReviewForm
    success_url = reverse_lazy("doctor-view-appointment")
    model = models.Appointment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        appointment = models.Appointment.objects.get(id=pk)

        patienid = appointment.patientId
        patient = models.Patient.objects.get(user_id=patienid)

        context["appointment"] = appointment

        return context

    def form_valid(self, form):
        form.save()
        return redirect("doctor-view-appointment")


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_dashboard_view(request):
    # for three cards
    # patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount = (
        models.Appointment.objects.all()
        .filter(status=True, doctorId=request.user.id)
        .count()
    )
    patientdischarged = (
        models.PatientDischargeDetails.objects.all()
        .distinct()
        .filter(assignedDoctorName=request.user.first_name)
        .count()
    )
    # below two lines taen from admin dashboard not from doctor to show total patients
    patients = models.Patient.objects.all().order_by("-id")
    patientcount = models.Patient.objects.all().filter(status=True).count()
    # for  table in para dashboard
    appointments = models.Appointment.objects.all().filter(status=True)
    # appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = (
        models.Patient.objects.all()
        .filter(status=True, user_id__in=patientid)
        .order_by("-id")
    )
    appointments = zip(appointments, patients)
    mydict = {
        "patientcount": patientcount,
        "appointmentcount": appointmentcount,
        "patientdischarged": patientdischarged,
        "appointments": appointments,
        "doctor": models.Paramedic.objects.get(
            user_id=request.user.id
        ),  # for profile picture of para in sidebar
    }
    mydict = {
        "patientcount": patientcount,  # this is also related with above teo lines copied from admin's dashboard
    }
    return render(request, "hospital/paramedic_dashboard.html", context=mydict)


def paramedic_patient_view(request):
    return render(request, "hospital/paramedic_patient.html")


# @login_required(login_url='paramediclogin')
# @user_passes_test(is_paramedic)
# def paramedic_view_patient_view(request):
#     patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
#     #doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#    #return render(request,'hospital/paramedic_view_patient.html',{'patients':patients,'doctor':doctor})
#     return render(request,'hospital/paramedic_view_patient.html',{'patients':patients})

# @login_required(login_url='paramediclogin')
# @user_passes_test(is_paramedic)
# def paramedic_view_patient_view(request):
#     patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     return render(request,'hospital/paramedic_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(
        request, "hospital/paramedic_view_patient.html", {"patients": patients}
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("paramedic-view-patient")


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            return redirect("paramedic-view-patient")
    return render(request, "hospital/paramedic_update_patient.html", context=mydict)


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()

            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect("paramedic-view-patient")
    return render(request, "hospital/paramedic_add_patient.html", context=mydict)


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(
        request, "hospital/paramedic_approve_patient.html", {"patients": patients}
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse("paramedic-approve-patient"))


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("paramedic-approve-patient")


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_appointment_view(request):
    return render(request, "hospital/paramedic_appointment.html")


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(
        request,
        "hospital/paramedic_view_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {
        "appointmentForm": appointmentForm,
    }
    if request.method == "POST":
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.POST.get("patientId")
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get("patientId")
            ).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect("paramedic-view-appointment")
    return render(request, "hospital/paramedic_add_appointment.html", context=mydict)


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(
        request,
        "hospital/paramedic_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_approved_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse("paramedic-approve-appointment"))


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect("paramedic-approve-appointment")


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_appointment_view(request):
    paramedic = models.Paramedic.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    # return render(request,'hospital/paramedic_appointment.html',{'paramedic':paramedic})
    return render(
        request, "hospital/paramedic_appointment.html", {"paramedic": paramedic}
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(
        request,
        "hospital/paramedic_view_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
# def paramedic_add_appointment_view(request):
#     appointmentForm = forms.AppointmentForm()
#     mydict = {
#         "appointmentForm": appointmentForm,
#     }
#     if request.method == "POST":
#         appointmentForm = forms.AppointmentForm(request.POST)
#         if appointmentForm.is_valid():
#             appointment = appointmentForm.save(commit=False)
#             appointment.doctorId = request.POST.get("doctorId")
#             appointment.patientId = request.POST.get("patientId")
#             appointment.doctorName = models.User.objects.get(
#                 id=request.POST.get("doctorId")
#             ).first_name
#             appointment.patientName = models.User.objects.get(
#                 id=request.POST.get("patientId")
#             ).first_name
#             appointment.status = True
#             appointment.save()
#         return HttpResponseRedirect("paramedic-view-appointment")
#     return render(request, "hospital/paramedic_add_appointment.html", context=mydict)


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_add_appointment_view(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {
        "appointmentForm": appointmentForm,
    }
    if request.method == "POST":
        appointmentForm = forms.AppointmentForm(request.POST, request.FILES)
        if appointmentForm.is_valid():
            # Check if the uploaded image is blurry
            image_file = request.FILES.get("infected_pic")
            if image_file:
                image_path = handle_uploaded_file(
                    image_file
                )  # Function to handle the uploaded image file
                blur_threshold = 100  # Adjust the threshold as per your requirement
                if is_image_blurry(image_path, blur_threshold):
                    message = (
                        "The uploaded image is blurry. Please upload a clear image."
                    )
                    return render(
                        request,
                        "hospital/paramedic_add_appointment.html",
                        {
                            "appointmentForm": appointmentForm,
                            "message": message,
                        },
                    )

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.POST.get("patientId")
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = models.User.objects.get(
                id=request.POST.get("patientId")
            ).first_name
            appointment.status = True
            appointment.save()
            return HttpResponseRedirect("paramedic-view-appointment")
    return render(request, "hospital/paramedic_add_appointment.html", context=mydict)


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def paramedic_approve_appointment_view(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(
        request,
        "hospital/paramedic_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="paramediclogin")
@user_passes_test(is_paramedic)
def para_approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse("paramedic-approve-appointment"))


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        "patient": patient,
        "doctorName": doctor.get_name,
        "doctorMobile": doctor.mobile,
        "doctorAddress": doctor.address,
        "symptoms": patient.symptoms,
        "doctorDepartment": doctor.department,
        "admitDate": patient.admitDate,
    }
    return render(request, "hospital/patient_dashboard.html", context=mydict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(request, "hospital/patient_appointment.html", {"patient": patient})


# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
# def patient_book_appointment_view(request):
#     appointmentForm=forms.PatientAppointmentForm()
#     patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     message=None
#     mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
#     if request.method=='POST':
#         appointmentForm=forms.PatientAppointmentForm(request.POST)
#         if appointmentForm.is_valid():
#             print(request.POST.get('doctorId'))
#             desc=request.POST.get('description')

#             doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))

#             if doctor.department == 'Cardiologist':
#                 if 'heart' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


#             if doctor.department == 'Dermatologists':
#                 if 'skin' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

#             if doctor.department == 'Emergency Medicine Specialists':
#                 if 'fever' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

#             if doctor.department == 'Allergists/Immunologists':
#                 if 'allergy' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

#             if doctor.department == 'Anesthesiologists':
#                 if 'surgery' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

#             if doctor.department == 'Colon and Rectal Surgeons':
#                 if 'cancer' in desc:
#                     pass
#                 else:
#                     print('else')
#                     message="Please Choose Doctor According To Disease"
#                     return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


#             appointment=appointmentForm.save(commit=False)
#             appointment.doctorId=request.POST.get('doctorId')
#             appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
#             appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
#             appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
#             appointment.status=False
#             appointment.save()
#         return HttpResponseRedirect('patient-view-appointment')
#     return render(request,'hospital/patient_book_appointment.html',context=mydict)
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    message = None
    mydict = {
        "appointmentForm": appointmentForm,
        "patient": patient,
        "message": message,
    }

    if request.method == "POST":
        appointmentForm = forms.PatientAppointmentForm(request.POST, request.FILES)
        if appointmentForm.is_valid():
            desc = request.POST.get("description")

            doctor = models.Doctor.objects.get(user_id=request.POST.get("doctorId"))

            # Check disease according to doctor's department
            if doctor.department == "Cardiologist" and "heart" not in desc:
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            if doctor.department == "Dermatologists" and "skin" not in desc:
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            if (
                doctor.department == "Emergency Medicine Specialists"
                and "fever" not in desc
            ):
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            if (
                doctor.department == "Allergists/Immunologists"
                and "allergy" not in desc
            ):
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            if doctor.department == "Anesthesiologists" and "surgery" not in desc:
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            if (
                doctor.department == "Colon and Rectal Surgeons"
                and "cancer" not in desc
            ):
                message = "Please Choose Doctor According To Disease"
                return render(
                    request,
                    "hospital/patient_book_appointment.html",
                    {
                        "appointmentForm": appointmentForm,
                        "patient": patient,
                        "message": message,
                    },
                )

            # Check if the uploaded image is blurry
            image_file = request.FILES.get("infected_pic")
            if image_file:
                image_path = handle_uploaded_file(
                    image_file
                )  # Function to handle the uploaded image file
                blur_threshold = 130  # Adjust the threshold as per your requirement
                if is_image_blurry(image_path, blur_threshold):
                    message = (
                        "The uploaded image is blurry. Please upload a clear image."
                    )
                    return render(
                        request,
                        "hospital/patient_book_appointment.html",
                        {
                            "appointmentForm": appointmentForm,
                            "patient": patient,
                            "message": message,
                        },
                    )

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get("doctorId")
            appointment.patientId = request.user.id
            appointment.doctorName = models.User.objects.get(
                id=request.POST.get("doctorId")
            ).first_name
            appointment.patientName = request.user.first_name
            appointment.status = False
            appointment.save()

            return HttpResponseRedirect("patient-view-appointment")

    return render(request, "hospital/patient_book_appointment.html", context=mydict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(
        request,
        "hospital/patient_view_appointment.html",
        {"appointments": appointments, "patient": patient},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def paitient_join_romm_view(request):
    if request.method == "POST":
        roomID = request.POST["roomID"]
        return redirect(f"/doctor-create-room?roomID={roomID}")

    return render(request, "hospital/patient_joinroom.html")


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    dischargeDetails = (
        models.PatientDischargeDetails.objects.all()
        .filter(patientId=patient.id)
        .order_by("-id")[:1]
    )
    patientDict = None
    if dischargeDetails:
        patientDict = {
            "is_discharged": True,
            "patient": patient,
            "patientId": patient.id,
            "patientName": patient.get_name,
            "assignedDoctorName": dischargeDetails[0].assignedDoctorName,
            "address": patient.address,
            "mobile": patient.mobile,
            "symptoms": patient.symptoms,
            "admitDate": patient.admitDate,
            "releaseDate": dischargeDetails[0].releaseDate,
            "daySpent": dischargeDetails[0].daySpent,
            "medicineCost": dischargeDetails[0].medicineCost,
            "roomCharge": dischargeDetails[0].roomCharge,
            "doctorFee": dischargeDetails[0].doctorFee,
            "OtherCharge": dischargeDetails[0].OtherCharge,
            "total": dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict = {
            "is_discharged": False,
            "patient": patient,
            "patientId": request.user.id,
        }
    return render(request, "hospital/patient_discharge.html", context=patientDict)


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_view_review(request):
    pk = request.GET.get("pk")
    appointment = models.Appointment.objects.get(id=pk)
    return render(
        request, "hospital/patient_view_review.html", {"appointment": appointment}
    )


# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, "hospital/aboutus.html")


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == "POST":
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data["Email"]
            name = sub.cleaned_data["Name"]
            message = sub.cleaned_data["Message"]
            send_mail(
                str(name) + " || " + str(email),
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False,
            )
            return render(request, "hospital/contactussuccess.html")
    return render(request, "hospital/contactus.html", {"form": sub})


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# Developed By : sumit kumar
# facebook : fb.com/sumit.luv
# Youtube :youtube.com/lazycoders


@login_required
def join_room(request):
    if request.method == "POST":
        roomID = request.POST["roomID"]
        return redirect("/meeting?roomID=" + roomID)
    return render(request, "hospital/joinroom.html")


@login_required
def videocall(request):
    # roomid = request.session['roomid']
    roomID = cache.get("roomID")
    return render(
        request,
        "hospital/videocall.html",
        {
            "name": request.user.first_name + " " + request.user.last_name,
            "roomID": roomID,
        },
    )
