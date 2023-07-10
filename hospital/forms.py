from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']

class ParamedicUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class ParamedicForm(forms.ModelForm):
    facility = forms.ModelChoiceField(queryset=models.Facility.objects.all(), empty_label=None)
    class Meta:
        model=models.Paramedic
        fields=['address','mobile','status','profile_pic','facility']   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facility'].label = 'Facility'

        facilities = models.Facility.objects.all()
        facility_choices = [(facility.id, f"{facility.name} - {facility.city}") for facility in facilities]
        self.fields['facility'].choices = facility_choices



#for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']

class FacilityForm(forms.ModelForm):
    class Meta:
        model=models.Facility
        fields=['name','city','address','contact_number']
        



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    infected_pic = forms.ImageField()
    class Meta:
        model=models.Appointment
        fields=['description','status','infected_pic']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    infected_pic = forms.ImageField()
    class Meta:
        model=models.Appointment
        fields=['description','status','infected_pic']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AddReviewForm(forms.ModelForm):
    class Meta:
        model=models.Appointment
        fields=['sumptoms','disease','medicine']

        widgets = {
        'sumptoms': forms.Textarea(attrs={"placeholder": "Symptoms", "class": "form-control"}),
        'disease': forms.Textarea(attrs={"placeholder": "Disease Name", "class": "form-control"}),
        'medicine': forms.TextInput(attrs={"placeholder": "Medicine Name", "class": "form-control"}),
        }