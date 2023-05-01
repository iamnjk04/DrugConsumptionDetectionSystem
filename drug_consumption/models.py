from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
# Creating the model for the Patient
class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.admin.username}'
    
class Patient(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    gender_choices=[('M','Male'),('F','Female')]
    gender= models.CharField(max_length=7,choices=gender_choices)
    managed_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
# creating the model for the Dataset Table
    def __str__(self):
        return f'{self.patient.username}'

class DatasetTable(models.Model):
    datasetmodel=models.ForeignKey(Patient,on_delete=models.CASCADE)
    nscore = models.FloatField(
              validators=[
            MaxValueValidator(3.5),
            MinValueValidator(-4)
        ])
    escore = models.FloatField(
          validators=[
            MaxValueValidator(3.5),
            MinValueValidator(-3.5)
        ]
    )
    oscore = models.FloatField(
          validators=[
            MaxValueValidator(3.5),
            MinValueValidator(-3.5)
        ]
    )
    ascore = models.FloatField(
          validators=[
            MaxValueValidator(3.5),
            MinValueValidator(-3.5)
        ]
    )
    cscore = models.FloatField(
          validators=[
            MaxValueValidator(3.5),
            MinValueValidator(-3.5)
        ]
    )
    ethnicity_choices = [('White',"White"), 
                         ('Other','Other',),
                         ('Mixed-White/Black','Mixed-White/Black'),
                         ('Asian','Asian'),
                         ('Mixed-White/Asian','Mixed-White/Asian'),
                         ('Black','Black'),
                         ('Mixed-Black/Asian','Mixed-Black/Asian')
                         ]
    ethnicity = models.CharField(max_length=20, choices=ethnicity_choices)
    impulsive = models.FloatField(validators=[
            MaxValueValidator(3.0),
            MinValueValidator(-3.0)
        ]
    )
    drug_choices = [("coke","coke"),
                    ("heroin","heroin"),
                    ("mushroom","mushroom"),
                    ("lsd","lsd")]
    drug_type = models.CharField(max_length=20,choices=drug_choices)
    
# Creating the model for the Result 
class Result(models.Model):
    result = models.OneToOneField(DatasetTable,on_delete=models.CASCADE)
    classification_status = models.BooleanField(default=False)
    consumption_status = models.CharField(max_length=10,null=True,default=None)
    # consumption_status = models.BooleanField(null=True,default=None)