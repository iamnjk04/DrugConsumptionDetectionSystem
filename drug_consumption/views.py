from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .forms import AdminModelForm, AdminForm, PatientForm, PatientModelForm, DatasetTableForm
from .models import Admin, Patient, DatasetTable, Result
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .utils import Model

# Create your views here.

def admin_register(request): 
    if request.method == "POST":
        user_form = AdminModelForm(request.POST)
        if user_form.is_valid():
            admin_form = AdminForm(request.POST)
            if admin_form.is_valid():
                try:
                    admin_user = user_form.save()
                    phone = admin_form.cleaned_data['phone']
                    Admin.objects.create(admin = admin_user, phone=phone)
                    return redirect('drug_consumption:index')
                except Exception:
                    return redirect('drug_consumption:index')
                    # return redirect("drug_consumption:index")
    elif request.method =="GET":
        user_form = AdminModelForm()
        admin_form = AdminForm()
        context = {'userform':user_form, "adminform":admin_form}
        return render(request, 'drug_consumption/admin_registration.html',context)


@login_required
def patient_register(request): 
    if request.method == "POST":
        user_form = PatientModelForm(request.POST)
        patient_form = PatientForm(request.POST)
        # print(user_form)
        # print(admin_form)
        if user_form.is_valid():
            # print(user_form.cleaned_data)
            if patient_form.is_valid():
                patient_age = patient_form.cleaned_data['age']
                patient_gender = patient_form.cleaned_data['gender'] 
                # print(admin_phone)
                patient_user = user_form.save()
                # print(patient_user)
                admin = request.user.admin
                Patient.objects.create(patient = patient_user, age=patient_age, gender = patient_gender, managed_by=admin)
            print("Patient created sucessfully.")
            # return HttpResponse("Hello Patient created.")
            return redirect('drug_consumption:index')
    elif request.method =="GET":
        user_form = PatientModelForm()
        patient_form = PatientForm()
    context = {'userform':user_form, "adminform":patient_form}
    return render(request, 'drug_consumption/admin_registration.html',context)

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'drug_consumption/login.html'
    def get_success_url(self):
        return reverse_lazy('drug_consumption:index')
        # return HttpResponse("login") 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('drug_consumption:index')


def index(request):
    context = {}
    return render(request, 'drug_consumption/index.html',context)
 
class DatasetTableCreateView(CreateView):
 
    # specify the model for create view
    model = DatasetTable
 
    # specify the fields to be displayed
    success_url = reverse_lazy("drug_consumption:index")
    form_class = DatasetTableForm
    
    def form_valid(self, form):
        form.instance.datasetmodel = self.request.user.patient
        self.object = form.save()
        return super().form_valid(form)

class DatasetTableListView(ListView):
    model = DatasetTable
    
    def get_queryset(self):
        queryset = self.model._default_manager.all()
        print(self.request.user)
        if not self.request.user.is_staff:
            print(self.request.user.patient)
            patient = self.request.user.patient
            queryset = DatasetTable.objects.filter(datasetmodel = patient)
        else:
            # Admin user
            admin = self.request.user.admin
            print(admin)
            queryset = DatasetTable.objects.filter(datasetmodel__managed_by = admin)
        return queryset

        
class DatasetTableDetailView(DetailView):
    # specify the model to use
    model = DatasetTable
    
class DatasetTableUpdateView(UpdateView):
    # specify the model you want to use
    model = DatasetTable
    form_class = DatasetTableForm
    
    def get_success_url(self):
        return reverse_lazy('drug_consumption:drug_data_list')
    
def delete_view(request, pk):
    context ={}
    obj = get_object_or_404(DatasetTable, id = pk)
    obj.delete()
    return redirect("drug_consumption:drug_data_list")


def predict(request,pk):
    # Function used by machine learning.
    obj = get_object_or_404(DatasetTable, id = pk)
    classification_status = True
    consumption_status = "C1"
    try:
        r1 = Result.objects.create(result = obj, classification_status= classification_status, consumption_status=consumption_status)
        print("Object Created.")
    except:
        r1 = obj.result
    print(request.user.patient.age)
    model = Model("mushroom")
    model.set_values(obj.nscore,obj.escore,obj.oscore,obj.ascore,obj.cscore,obj.impulsive,request.user.patient.gender,request.user.patient.age,obj.ethnicity)
    prediction = model.predict_data()
    r1.consumption_status = str(prediction[0])
    context = {}
    context['prediction']  = r1.consumption_status
    print(context)
    return JsonResponse(context, status=200)

class ResultListView(ListView):
    model = Result
    
    def get_queryset(self):
        queryset = self.model._default_manager
        try:
            user = self.request.user.patient
        except:
            print("User is admin.")
        else:
            # loan = LoanDetails.objects.filter(loan_request__managed_by = employee)
            return queryset.filter(result__datasetmodel = user)
    
class ResultAllListView(ListView):
    model = Result
    template_name = "drug_consumption/result_all.html"
    
    def get_queryset(self):
        queryset = self.model._default_manager
        try:
            user = self.request.user.admin
        except:
            print("User is admin.")
        else:
            return queryset.filter(result__datasetmodel__managed_by = user)

def user_list(request):
    current_user = request.user.admin
    patients = Patient.objects.filter(managed_by = current_user)
    print(patients)
    context = {}
    context['patients'] = patients
    # for i in patients
    return render(request,'drug_consumption/patients_list.html', context)
    