from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Patient, DatasetTable, Result

class PatientModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email    
    
    def save(self, commit=True):
        user = super(PatientModelForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # print(user.email)
        if commit:
            user.save()
        return user
    
    
class AdminModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email    
    
    def save(self, commit=True):
        user = super(AdminModelForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # print(user.email)
        user.is_staff = True
        if commit:
            user.save()
        return user
    
    
class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['admin',]
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        # fields = ['exclude']
        exclude = ['patient','managed_by']
        



# creating a form
class DatasetTableForm(forms.ModelForm):
    class Meta:
        model = DatasetTable
        exclude = ['datasetmodel']
		# specify fields to be used
		