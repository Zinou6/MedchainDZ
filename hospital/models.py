from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
    
departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons'),
('Generalist','Generalist')
]

sexe= [('Man','Man'),
('Woman','Woman')
]

doctype= [('Prescription','Prescription'),
('Radiology','Radiology'),
('Analyse','Analyse'),
('Comment','Comment')
]

class Doctor(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    profile_pic     = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address         = models.CharField(max_length=40)
    mobile          = models.CharField(max_length=20,null=True)
    department      = models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status          = models.BooleanField(default=False)
    identity        = models.CharField(max_length=255,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Receptionist(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    profile_pic     = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    department      = models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status          = models.BooleanField(default=False)
    identity        = models.CharField(max_length=255,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Patient(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic     = models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    brth_day        = models.DateField(default=datetime.date.today,null=False)
    address         = models.CharField(max_length=40)
    mobile          = models.CharField(max_length=20,null=False)
    sexe            = models.CharField(max_length=20,choices=sexe,default='Man')
    age             = models.IntegerField(null=True)
    situation_F     = models.CharField(max_length=40)
    nom_jeune_fille = models.CharField(max_length=40)
    assignedDoctorId= models.PositiveIntegerField(null=True)
    admitDate       = models.DateField(auto_now=True)
    status          = models.BooleanField(default=False)
    identity        = models.CharField(max_length=255,null=False)
    symptoms        = models.TextField(max_length=500,default=None)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId       = models.PositiveIntegerField(null=True)
    doctorId        = models.PositiveIntegerField(null=True)
    patientName     = models.CharField(max_length=40,null=True)
    doctorName      = models.CharField(max_length=40,null=True)
    appointmentDate = models.DateField(auto_now=True)
    description     = models.TextField(max_length=500)
    status          = models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId           = models.PositiveIntegerField(null=True)
    patientName         = models.CharField(max_length=40)
    assignedDoctorName  = models.CharField(max_length=40)
    address             = models.CharField(max_length=40)
    mobile              = models.CharField(max_length=20,null=True)
    symptoms            = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge          = models.PositiveIntegerField(null=False)
    medicineCost        = models.PositiveIntegerField(null=False)
    doctorFee           = models.PositiveIntegerField(null=False)
    OtherCharge         = models.PositiveIntegerField(null=False)
    total               = models.PositiveIntegerField(null=False)


class Prescription(models.Model):
    patientId      = models.PositiveIntegerField(null=True)
    doctorId       = models.PositiveIntegerField(null=True)
    date           = models.DateField(default=datetime.date.today,null=False)
    medicament     = models.CharField(max_length=40,null=True,blank=True)
    traitement     = models.CharField(max_length=40,null=True,blank=True)
    boite          = models.PositiveIntegerField(null=True,blank=True)
    medicament2    = models.CharField(max_length=40,null=True,blank=True)
    traitement2    = models.CharField(max_length=40,null=True,blank=True)
    boite2         = models.PositiveIntegerField(null=True,blank=True)
    medicament3    = models.CharField(max_length=40,null=True,blank=True)
    traitement3    = models.CharField(max_length=40,null=True,blank=True)
    boite3         = models.PositiveIntegerField(null=True,blank=True)
    medicament4    = models.CharField(max_length=40,null=True,blank=True)
    traitement4    = models.CharField(max_length=40,null=True,blank=True)
    boite4         = models.PositiveIntegerField(null=True,blank=True)
    medicament5    = models.CharField(max_length=40,null=True,blank=True)
    traitement5    = models.CharField(max_length=40,null=True,blank=True)
    boite5         = models.PositiveIntegerField(null=True,blank=True)

class Radiology(models.Model):
    patientId      = models.PositiveIntegerField(null=True)
    doctorId       = models.PositiveIntegerField(null=True)
    date           = models.DateField(default=datetime.date.today,null=False)
    radio_img      = models.ImageField(upload_to='radio_img/RadiologyImage/',null=True)

class Analyse(models.Model):
    patientId           = models.PositiveIntegerField(null=True)
    doctorId            = models.PositiveIntegerField(null=True)
    date                = models.DateField(default=datetime.date.today,null=False)
    analyse_document    = models.FileField(upload_to='pdfs/', null=True)

class Comment(models.Model):
    patientId           = models.PositiveIntegerField(null=True)
    doctorId            = models.PositiveIntegerField(null=True)
    date                = models.DateField(default=datetime.date.today,null=False)
    comment_text        = models.TextField(max_length=500)