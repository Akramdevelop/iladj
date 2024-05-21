from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    nickName = models.CharField(max_length=255, blank=True, null=True)
    phoneNumber = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    nickName = models.CharField(max_length=255, blank=True, null=True)
    speciality = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    checkprice = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    recheckprice = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)
    operationprice = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.user.username


class AssistantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    nickName = models.CharField(max_length=255, blank=True, null=True)
    clinicName = models.CharField(max_length=255, blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PatientCard(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    assistant = models.ForeignKey(
        AssistantProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)
    Finished = models.BooleanField(default=False)
    # new
    work = models.CharField(max_length=255, blank=True, null=True)
    isSmoker = models.BooleanField(default=False)
    isMaried = models.BooleanField(default=False)
    type = models.CharField(max_length=255, choices=(
        ('check', 'check'), ('recheck', 'recheck'), ('operation', 'operation')), default='check')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.assistant) + " / " + str(self.name)


def upload_to(instance, filename):
    today = datetime.today()
    year_month = today.strftime('%Y/%m')
    return f'doctor_images/{year_month}/{filename}'


def upload_to2(instance, filename):
    today = datetime.today()
    year = today.strftime('%Y')
    return f'assistant_images/{year}/{filename}'


def upload_to3(instance, filename):
    today = datetime.today()
    year_month = today.strftime('%Y/%m')
    return f'nessa_images/{year_month}/{filename}'


def upload_to4(instance, filename):
    today = datetime.today()
    year_month = today.strftime('%Y/%m')
    return f'vascular_images/{year_month}/{filename}'


class DoctorCard(models.Model):
    patientCard = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    medicine = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    analysis = models.ImageField(upload_to=upload_to, blank=True, null=True)
    xRays = models.ImageField(upload_to=upload_to, blank=True, null=True)
    prescription = models.ImageField(
        upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return str(self.patientCard) + " [" + str(self.pk) + "]"


class TempDoctorCard(models.Model):
    patientCard = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    analysis = models.ImageField(upload_to=upload_to2, blank=True, null=True)
    xRays = models.ImageField(upload_to=upload_to2, blank=True, null=True)
    prescription = models.ImageField(
        upload_to=upload_to2, blank=True, null=True)

    def __str__(self):
        return str(self.patientCard) + " [" + str(self.pk) + "]"


class FavoriteMedicine(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('doctor', 'name')


class NessaCard(models.Model):
    patientprofile = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE)
    doctorprofile = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE)
    childrennumber = models.IntegerField(blank=True, null=True)
    childrensex = models.CharField(max_length=255, blank=True, null=True)
    mariagedate = models.DateField(blank=True, null=True)
    lastperiode = models.DateField(blank=True, null=True)
    datebirth = models.DateField(blank=True, null=True)
    lastbirth = models.DateField(blank=True, null=True)
    typeofbirth = models.CharField(max_length=255, choices=(
        ('normal', 'normal'), ('caesarean', 'caesarean')), blank=True, null=True)
    childsex = models.CharField(max_length=255, choices=(
        ('male', 'male'), ('female', 'female'), ('twin', 'twin')), blank=True, null=True)
    prevbirth = models.CharField(max_length=255, choices=(
        ('normal', 'normal'), ('caesarean', 'caesarean')), blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    prevoperations = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('patientprofile', 'doctorprofile')


    def __str__(self):
        return str(self.patientprofile) + " [" + str(self.pk) + "]"


class NessaPictures(models.Model):
    nessacard = models.ForeignKey(NessaCard, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=upload_to3, blank=True, null=True)


class VascularCard(models.Model):
    patientprofile = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE)
    doctorprofile = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE)
    HB = models.CharField(max_length=255, blank=True, null=True)
    PLT = models.CharField(max_length=255, blank=True, null=True)
    WBC = models.CharField(max_length=255, blank=True, null=True)
    RBC = models.CharField(max_length=255, blank=True, null=True)
    HTC = models.CharField(max_length=255, blank=True, null=True)
    Cholesterol = models.CharField(max_length=255, blank=True, null=True)
    TGC = models.CharField(max_length=255, blank=True, null=True)
    LDL = models.CharField(max_length=255, blank=True, null=True)
    HDL = models.CharField(max_length=255, blank=True, null=True)
    VLDL = models.CharField(max_length=255, blank=True, null=True)
    Urea = models.CharField(max_length=255, blank=True, null=True)
    CREATE = models.CharField(max_length=255, blank=True, null=True)
    SGOT = models.CharField(max_length=255, blank=True, null=True)
    SGPT = models.CharField(max_length=255, blank=True, null=True)
    PT = models.CharField(max_length=255, blank=True, null=True)
    INR = models.CharField(max_length=255, blank=True, null=True)
    HbA1c = models.CharField(max_length=255, blank=True, null=True)
    Ddimer = models.CharField(max_length=255, blank=True, null=True)
    FBS = models.CharField(max_length=255, blank=True, null=True)
    PPBS = models.CharField(max_length=255, blank=True, null=True)
    caTotal = models.CharField(max_length=255, blank=True, null=True)
    caIoized = models.CharField(max_length=255, blank=True, null=True)
    ESR = models.CharField(max_length=255, blank=True, null=True)
    CRP = models.CharField(max_length=255, blank=True, null=True)
    PTNC = models.CharField(max_length=255, blank=True, null=True)
    PTNS = models.CharField(max_length=255, blank=True, null=True)
    AntithrombinIII = models.CharField(max_length=255, blank=True, null=True)
    Anticarviolipin = models.CharField(max_length=255, blank=True, null=True)
    AntiLupus = models.CharField(max_length=255, blank=True, null=True)
    Anticoagulant = models.CharField(max_length=255, blank=True, null=True)
    ANA = models.CharField(max_length=255, blank=True, null=True)
    ANCA = models.CharField(max_length=255, blank=True, null=True)
    Factor = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('patientprofile', 'doctorprofile')


class VascularPictures(models.Model):
    vascularcard = models.ForeignKey(VascularCard, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=upload_to4, blank=True, null=True)
