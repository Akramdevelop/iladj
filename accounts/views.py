from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from . import models
import re
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from datetime import datetime
import random
import string
from django.db.models import Q
from django.core.files.base import ContentFile

# akram errors
#####
# err1: Username Used
# err2: Password Less Than 8 Char
# err3: Invalid Phone Number
# err4: Few Information
# err5: username not found
# err6: Username and password not matching
# err7: Phone not match any user
# err8: more than one checkbox
# err9: Invalid date
# err10: marry and not


def signup(request):
    return render(request, 'accounts/signup.html', {})


def signuppost(request):
    username = None
    password = None
    email = None
    fname = None
    lname = None
    nickname = None
    address = None
    phoneNumber = None
    if request.method == 'POST' and 'btnsignup' in request.POST:
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        if 'address' in request.POST:
            address = request.POST['address']
        if 'phoneNumber' in request.POST:
            phoneNumber = request.POST['phoneNumber']
    if username and password and address and phoneNumber:
        if not User.objects.filter(username=username).exists():
            if not len(password) < 8:
                if re.match(r'^01[0125][0-9]{8}$', phoneNumber) or re.match(r'^\+201[0125][0-9]{8}$', phoneNumber):
                    user = User.objects.create_user(
                        username=username, email="user@iladj.com", password=password)
                    user.save()
                    patientprofile = models.PatientProfile(
                        user=user, address=address, phoneNumber=phoneNumber[-10:])
                    patientprofile.save()
                    return JsonResponse({'success': True})
                return JsonResponse({'err3': 'Invalid phone number'})
            return JsonResponse({'err2': 'Password less than 8 char'})
        return JsonResponse({'err1': 'Username used'})
    return JsonResponse({'error': 'Few information'})


def signin(request):
    return render(request, 'accounts/signin.html', {})


def signinpost(request):
    username = None
    password = None
    isDoctor = False
    isAssistant = False
    if request.method == 'POST' and 'btnsignin' in request.POST:
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
    if username and password:
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if models.DoctorProfile.objects.filter(user=user).exists():
                    isDoctor = True
                if models.AssistantProfile.objects.filter(user=user).exists():
                    isAssistant = True
                return JsonResponse({'success': True, 'isDoctor': isDoctor, 'isAssistant': isAssistant})
            return JsonResponse({'err6': 'Username and password not matching'})
        return JsonResponse({'err5': 'Username not found'})


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def changePassword(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        return render(request, 'accounts/changePass.html', {})
    redirect('index')


def changePasswordPost(request):
    password = None
    repassword = None
    if request.method == 'POST' and 'btnchange' in request.POST:
        if request.POST['btnchange'] == "1":
            if 'password' in request.POST:
                password = request.POST['password']
            if 'repassword' in request.POST:
                repassword = request.POST['repassword']
    if password and repassword:
        if password == repassword:
            if request.user.is_authenticated and not request.user.is_anonymous:
                user = request.user
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                return JsonResponse({'success': "تم تغيير كلمة السر بنجاح"})
            return JsonResponse({'error': "not logged in"})
        return JsonResponse({'error': "Password and repassword not match"})
    return JsonResponse({'error': "Few Informations"})


def addpatientcard(request):
    name = None
    age = None
    address = None
    phone = None
    prescriptionImg = None
    XRaysImg = None
    analysisImg = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST' and 'btnaddcard' in request.POST:
            if 'name' in request.POST:
                name = request.POST['name']
            if 'age' in request.POST:
                age = request.POST['age']
            if 'address' in request.POST:
                address = request.POST['address']
            if 'phone' in request.POST:
                phone = request.POST['phone']
            if 'prescriptionImg' in request.FILES:
                prescriptionImg = request.FILES['prescriptionImg']
            if 'XRaysImg' in request.FILES:
                XRaysImg = request.FILES['XRaysImg']
            if 'analysisImg' in request.FILES:
                analysisImg = request.FILES['analysisImg']
    if name and age and address and phone:
        isNewUser = False
        if not models.PatientProfile.objects.filter(phoneNumber=phone[-10:]).exists():
            # test if username is taken
            def generate_unique_username(base_username):
                # Try to use the base_username first
                new_username = base_username

                while User.objects.filter(username=new_username).exists():
                    # Generate a random two-digit number and append it to the base_username
                    random_number = random.randint(0, 99)
                    new_username = f"{base_username}{random_number:02}"

                return new_username
            username = generate_unique_username(name)

            # def generate_random_password(length=10):
            #     # Define the characters to use for the password
            #     # Uppercase letters + lowercase letters + digits
            #     characters = string.ascii_letters + string.digits

            #     # Generate a random password by sampling characters
            #     password = ''.join(random.choice(characters)
            #                        for _ in range(length))

            #     return password

            password = phone[-10:]
            user = User.objects.create_user(
                username=username, email="user@iladj.com", password=password)
            user.save()
            patientprofile = models.PatientProfile(
                user=user, address=address, phoneNumber=phone[-10:])
            patientprofile.save()
            isNewUser = True

        if models.PatientProfile.objects.filter(phoneNumber=phone[-10:]).exists():
            patient = models.PatientProfile.objects.get(
                phoneNumber=phone[-10:])
            if (models.AssistantProfile.objects.filter(user=request.user).exists()):
                assistant = models.AssistantProfile.objects.get(
                    user=request.user)
                patientcard = models.PatientCard(
                    patient=patient, assistant=assistant, name=name, age=int(age), address=address, phoneNumber=phone[-10:])
                patientcard.save()
                tempdoctorcard = models.TempDoctorCard(
                    patientCard=patientcard)
                if prescriptionImg is not None:
                    tempdoctorcard.prescription = prescriptionImg
                if XRaysImg is not None:
                    tempdoctorcard.xRays = XRaysImg
                if analysisImg is not None:
                    tempdoctorcard.analysis = analysisImg
                tempdoctorcard.save()
                if isNewUser:
                    return JsonResponse({'success': 'تم الإضافة بنجاح', 'isNewUser': isNewUser, 'datas': {'username': username, 'password': password}})
                else:
                    return JsonResponse({'success': 'تم الإضافة بنجاح', 'isNewUser': isNewUser})
            return JsonResponse({'error': "you are not assistant"})
        else:
            return JsonResponse({'err7': 'Phone not match any user'})
    return JsonResponse({'error': "something wrong"})


@api_view(['GET'])
def searchpatient(request):
    # search_query = request.GET.get('q', '')
    search_query = request.GET['q']
    mydate = request.GET['date']
    assistantId = request.GET['assistantId']
    isDoctor = None
    isAssistant = None
    try:
        # Attempt to parse the date string using the desired format
        parsed_date = datetime.strptime(mydate, '%Y-%m-%d')
        # If parsing succeeds, the date is in the correct format
        is_date_correct = True
    except ValueError:
        # If parsing fails, the date is not in the correct format
        is_date_correct = False

    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if models.DoctorProfile.objects.filter(user=user).exists():
            doctor = models.DoctorProfile.objects.get(user=user)
            if models.AssistantProfile.objects.filter(doctor=doctor).exists():
                isDoctor = True
        elif models.AssistantProfile.objects.filter(user=user).exists():
            isAssistant = True
        if isDoctor is not None or isAssistant is not None:
            assistant = models.AssistantProfile.objects.get(pk=assistantId)
            if is_date_correct:
                if search_query != "":
                    patientcards = models.PatientCard.objects.filter(
                        Q(assistant=assistant), Q(name__icontains=search_query) | Q(phoneNumber__icontains=search_query)).order_by('-pk')
                else:
                    patientcards = models.PatientCard.objects.filter(
                        Q(assistant=assistant), date=parsed_date, Finished=False).order_by('checked', 'pk')
                if patientcards.exists():
                    serializer = PatientCardSerializer(
                        patientcards, many=True)
                    return Response({'success': serializer.data})
                return JsonResponse({'success': "Void"})
            return JsonResponse({'err9': "invalid date"})
        return JsonResponse({'error': "user isn't doctor nor assistant or doctor has no assistants"})
    return JsonResponse({'error': "not logged in"})


@api_view(['GET'])
def getpatientdata(request):
    favoritemedicines = None
    patientCardPk = request.GET['pk']
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if models.DoctorProfile.objects.filter(user=user).exists():
            doctor = models.DoctorProfile.objects.get(user=user)
            if models.FavoriteMedicine.objects.filter(doctor=doctor).exists():
                favoritemedicines = models.FavoriteMedicine.objects.filter(
                    doctor=doctor)
                favoritemedicinesSerializer = FavoriteMedicineSerializer(
                    favoritemedicines, many=True)
            if models.AssistantProfile.objects.filter(doctor=doctor).exists():
                # assistant = models.AssistantProfile.objects.get(doctor=doctor)
                if (models.PatientCard.objects.filter(pk=patientCardPk).exists()):
                    patientcard = models.PatientCard.objects.get(
                        pk=patientCardPk)
                    if models.TempDoctorCard.objects.filter(patientCard=patientcard).exists():
                        tempdoctorcard = models.TempDoctorCard.objects.get(
                            patientCard=patientcard)
                        tempdoctorcardserialiser = TempDoctorCardSerializer(
                            tempdoctorcard)
                    else:
                        tempdoctorcardserialiser = None
                    patientprofile = models.PatientProfile.objects.get(
                        pk=patientcard.patient.pk)
                    patientcards = models.PatientCard.objects.filter(
                        patient=patientprofile)
                    patientserializer = PatientCardSerializer(
                        patientcard)
                    if favoritemedicines is not None and favoritemedicinesSerializer is not None:
                        if models.DoctorCard.objects.filter(Q(patientCard__in=patientcards)).exists():
                            doctorcards = models.DoctorCard.objects.filter(
                                Q(patientCard__in=patientcards)).order_by('-id')
                            doctorserializer = DoctorCardSerializer(
                                doctorcards, many=True)
                            updatabledoctorcards = models.DoctorCard.objects.filter(
                                patientCard=patientcard)
                            updatabledoctorcardsserializer = DoctorCardSerializer(
                                updatabledoctorcards, many=True)
                            if tempdoctorcardserialiser is not None:
                                return Response({'success': patientserializer.data, 'doctorcards': doctorserializer.data, 'updatabledoctorcards': updatabledoctorcardsserializer.data, 'tempdoctorcard': tempdoctorcardserialiser.data, 'favoritemedicines': favoritemedicinesSerializer.data})
                            return Response({'success': patientserializer.data, 'doctorcards': doctorserializer.data, 'updatabledoctorcards': updatabledoctorcardsserializer.data, 'favoritemedicines': favoritemedicinesSerializer.data})
                        else:
                            if tempdoctorcardserialiser is not None:
                                return Response({'success': patientserializer.data, 'tempdoctorcard': tempdoctorcardserialiser.data, 'favoritemedicines': favoritemedicinesSerializer.data})
                            return Response({'success': patientserializer.data, 'favoritemedicines': favoritemedicinesSerializer.data})
                    if models.DoctorCard.objects.filter(Q(patientCard__in=patientcards)).exists():
                        doctorcards = models.DoctorCard.objects.filter(
                            Q(patientCard__in=patientcards)).order_by('-id')
                        doctorserializer = DoctorCardSerializer(
                            doctorcards, many=True)
                        updatabledoctorcards = models.DoctorCard.objects.filter(
                            patientCard=patientcard)
                        updatabledoctorcardsserializer = DoctorCardSerializer(
                            updatabledoctorcards, many=True)
                        if tempdoctorcardserialiser is not None:
                            return Response({'success': patientserializer.data, 'doctorcards': doctorserializer.data, 'updatabledoctorcards': updatabledoctorcardsserializer.data, 'tempdoctorcard': tempdoctorcardserialiser.data})
                        return Response({'success': patientserializer.data, 'doctorcards': doctorserializer.data, 'updatabledoctorcards': updatabledoctorcardsserializer.data})
                    else:
                        if tempdoctorcardserialiser is not None:
                            return Response({'success': patientserializer.data, 'tempdoctorcard': tempdoctorcardserialiser.data})
                        return Response({'success': patientserializer.data})
                return JsonResponse({'error': "thers no patient with this primary key"})
            return JsonResponse({'error': "doctor has no assistant"})
        return JsonResponse({'error': "user isn't doctor"})
    return JsonResponse({'error': "not logged in"})


@api_view(['GET'])
def getpatientdataforassistant(request):
    patientCardPk = request.GET['pk']
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if models.AssistantProfile.objects.filter(user=user).exists():
            # assistant = models.AssistantProfile.objects.get(doctor=doctor)
            if (models.PatientCard.objects.filter(pk=patientCardPk).exists()):
                patientcard = models.PatientCard.objects.get(
                    pk=patientCardPk)
                patientserializer = PatientCardSerializer(
                    patientcard)
                if models.DoctorCard.objects.filter(patientCard=patientcard).exists():
                    lastdoctorcard = models.DoctorCard.objects.filter(
                        patientCard=patientcard).last()
                    lastdoctorcardSerializer = DoctorCardSerializer(
                        lastdoctorcard)
                    return Response({'success': patientserializer.data, 'docCard': lastdoctorcardSerializer.data})
                return Response({'success': patientserializer.data})
            return JsonResponse({'error': "thers no patient with this primary key"})
        return JsonResponse({'error': "user isn't assistant"})
    return JsonResponse({'error': "not logged in"})


@api_view(['POST'])
def setdoctordata(request):
    # set data values
    Ctype = None
    CMarry = None
    CMarry2 = None
    patientcardpk = None
    work = None
    iswork = None
    name = None
    age = None
    address = None
    smoke = None
    issmoke = None
    marry2 = None
    marry = None
    ismarry2 = None
    ismarry = None
    check = None
    ischeck = None
    again = None
    isagain = None
    operation = None
    isoperation = None
    info = None
    isinfo = None
    notes = None
    isnotes = None
    medicine = None
    ismedicine = None
    prescriptionImg = None
    XRaysImg = None
    analysisImg = None
    savecheckbtn = None
    addbtn = None
    updatablecardslength = None
    isNewDoc = None
    curr_date = datetime.now().strftime('%Y-%m-%d')
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'POST' and 'savecheckbtn' in request.POST and 'addbtn' in request.POST:
            savecheckbtn = request.POST['savecheckbtn']
            addbtn = request.POST['addbtn']
            if 'updatablecardslength' in request.POST:
                updatablecardslength = request.POST['updatablecardslength']
            if 'patientcardpk' in request.POST:
                patientcardpk = request.POST['patientcardpk']
            if 'work' in request.POST:
                iswork = True
                work = request.POST['work']
            if 'name' in request.POST:
                name = request.POST['name']
            if 'age' in request.POST:
                age = request.POST['age']
            if 'address' in request.POST:
                address = request.POST['address']
            if 'smoke' in request.POST:
                issmoke = True
                if request.POST['smoke'] == 'true':
                    smoke = True
                else:
                    smoke = False
            if 'marry2' in request.POST:
                ismarry2 = True
                CMarry2 = request.POST['marry2']
                if request.POST['marry2'] == 'true':
                    marry2 = True
                else:
                    marry2 = False
            if 'marry' in request.POST:
                ismarry = True
                CMarry = request.POST['marry']
                if request.POST['marry'] == 'true':
                    marry = True
                else:
                    marry = False
            if 'check' in request.POST:
                ischeck = True
                check = request.POST['check']
            if 'again' in request.POST:
                isagain = True
                again = request.POST['again']
            if 'operation' in request.POST:
                isoperation = True
                operation = request.POST['operation']
            if 'info' in request.POST:
                isinfo = True
                info = request.POST['info']
            if 'notes' in request.POST:
                isnotes = True
                notes = request.POST['notes']
            if 'medicine' in request.POST:
                ismedicine = True
                medicine = request.POST['medicine']
            if 'isnewdoc' in request.POST:
                isNewDoc = request.POST['isnewdoc']
            if (check == 'true') and (again == "false") and (operation == "false"):
                Ctype = 'check'
            if (check == 'false') and (again == 'true') and (operation == "false"):
                Ctype = 'recheck'
            if (check == 'false') and (again == "false") and (operation == 'true'):
                Ctype = 'operation'
            if models.PatientCard.objects.filter(pk=patientcardpk).exists():
                temppatientcard = models.PatientCard.objects.get(
                    pk=patientcardpk)
                if models.TempDoctorCard.objects.filter(
                    patientCard=temppatientcard).exists():
                    temp_image = models.TempDoctorCard.objects.filter(
                        patientCard=temppatientcard).last()
                    if 'prescriptionImg' in request.POST:
                        if request.POST['prescriptionImg'] == "sameAsTemp":
                            prescriptionImg = ContentFile(
                                temp_image.prescription.read(), name=temp_image.prescription.name)
                    else:
                        prescriptionImg = request.FILES['prescriptionImg']
                    if 'X-raysImg' in request.POST:
                        if request.POST['X-raysImg'] == "sameAsTemp":
                            XRaysImg = ContentFile(
                                temp_image.xRays.read(), name=temp_image.xRays.name)
                    else:
                        XRaysImg = request.FILES['X-raysImg']
                    if 'analysisImg' in request.POST:
                        if request.POST['analysisImg'] == "sameAsTemp":
                            analysisImg = ContentFile(
                                temp_image.analysis.read(), name=temp_image.analysis.name)
                    else:
                        analysisImg = request.FILES['analysisImg']
                    temp_image.delete()
        if ((CMarry == 'true') and (CMarry2 == 'false')) or ((CMarry == 'false') and (CMarry2 == 'true')):
            if ((check == 'true') and (again == "false") and (operation == "false")) or ((check == 'false') and (again == 'true') and (operation == "false")) or ((check == 'false') and (again == "false") and (operation == 'true')):
                if patientcardpk and iswork and age and issmoke and ismarry and ischeck and isagain and isoperation and isinfo and isnotes and ismedicine:
                    user = request.user
                    if models.DoctorProfile.objects.filter(user=user).exists():
                        if models.PatientCard.objects.filter(pk=patientcardpk).exists():
                            patientcard = models.PatientCard.objects.get(
                                pk=patientcardpk)
                            # devide code here
                            if savecheckbtn == "1":
                                # check if patient card has doctorcard ==> update + check if add enabled
                                if models.DoctorCard.objects.filter(patientCard=patientcard).exists():
                                    for i in range(int(updatablecardslength)):
                                        if models.DoctorCard.objects.filter(pk=int(request.POST[f'doctorcard{i}id']), date=curr_date).exists():
                                            doctorcardindex = models.DoctorCard.objects.get(
                                                pk=int(request.POST[f'doctorcard{i}id']))
                                            doctorcardindex.diagnosis = request.POST[f'info{i}']
                                            doctorcardindex.notes = request.POST[f'notes{i}']
                                            doctorcardindex.medicine = request.POST[f'medicine{i}']
                                            if f'prescriptionImg{i}' in request.FILES:
                                                doctorcardindex.prescription = request.FILES[
                                                    f'prescriptionImg{i}']
                                            if f'X-raysImg{i}' in request.FILES:
                                                doctorcardindex.xRays = request.FILES[f'X-raysImg{i}']
                                            if f'analysisImg{i}' in request.FILES:
                                                doctorcardindex.analysis = request.FILES[
                                                    f'analysisImg{i}']
                                            doctorcardindex.save()
                                    # if add enabled ==> new Doctor card
                                if isNewDoc is not None and isNewDoc == "1":
                                    doctorcard = models.DoctorCard(
                                        patientCard=patientcard,
                                        diagnosis=info,
                                        notes=notes,
                                        medicine=medicine
                                    )
                                    if prescriptionImg is not None:
                                        doctorcard.prescription = prescriptionImg
                                    if XRaysImg is not None:
                                        doctorcard.xRays = XRaysImg
                                    if analysisImg is not None:
                                        doctorcard.analysis = analysisImg
                                    doctorcard.save()
                                    patientcard.checked = True
                                patientcard.work = work
                                if name is not None:
                                    patientcard.name = name
                                if age is not None:
                                    if isinstance(int(age), int):
                                        patientcard.age = age
                                if address is not None:
                                    patientcard.address = address
                                patientcard.isSmoker = smoke
                                patientcard.isMaried = marry2
                                patientcard.type = Ctype
                                patientcard.save()
                                return JsonResponse({'success': "تم حفظ تشخيص الحالة بنجاح"})
                            else:
                                return JsonResponse({'error': "no add card no save"})
                        return JsonResponse({'err9': "no card for this primary key"})
                    return JsonResponse({'error': "user isn't doctor"})
                return JsonResponse({'error': 'Few information'})
            return JsonResponse({'err8': "error in check"})
        return JsonResponse({'err10': "error in marry"})


def update_is_finished(request, pk):
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if models.DoctorProfile.objects.filter(user=user).exists() or models.AssistantProfile.objects.filter(user=user).exists():
            try:
                patient_card = models.PatientCard.objects.get(id=pk)
                patient_card.Finished = True
                patient_card.save()
                return JsonResponse({'success': True})
            except models.PatientCard.DoesNotExist:
                return JsonResponse({'error': 'patient card doesn\'t exist'})
        return JsonResponse({'error': "user isn't doctor nor assistant"})
    return JsonResponse({'error': "you are not logged in"})


def getcalculation(request):
    dateStart = None
    dateEnd = None
    doctorid = None
    doctor = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'GET':
            if 'dateStart' in request.GET:
                dateStart = request.GET['dateStart']
            if 'dateEnd' in request.GET:
                dateEnd = request.GET['dateEnd']
            if 'doctorid' in request.GET:
                doctorid = request.GET['doctorid']
        if dateStart is not None and dateEnd is not None:
            try:
                start_date = datetime.strptime(dateStart, "%Y-%m-%d")
                end_date = datetime.strptime(dateEnd, "%Y-%m-%d")

                if start_date <= end_date:
                    if doctorid is not None:
                        if isinstance(int(doctorid), int):
                            if models.DoctorProfile.objects.filter(pk=int(doctorid)).exists():
                                doctor = models.DoctorProfile.objects.get(pk=int(doctorid))
                    elif models.DoctorProfile.objects.filter(user=user).exists():
                        doctor = models.DoctorProfile.objects.get(user=user)
                    if doctor is not None:
                        # get doctor assistants
                        if models.AssistantProfile.objects.filter(doctor=doctor).exists():
                            assistants = models.AssistantProfile.objects.filter(
                                doctor=doctor)
                            # get all patient cards of assistans with type check
                            if models.PatientCard.objects.filter(Q(assistant__in=assistants)).exists():
                                checkcards = models.PatientCard.objects.filter(
                                    Q(assistant__in=assistants), Q(type='check'), Q(date__range=(start_date, end_date)))
                                recheckcards = models.PatientCard.objects.filter(
                                    Q(assistant__in=assistants), Q(type='recheck'))
                                operationcards = models.PatientCard.objects.filter(
                                    Q(assistant__in=assistants), Q(type='operation'))
                                checkprice = doctor.checkprice
                                recheckprice = doctor.recheckprice
                                operationprice = doctor.operationprice
                                return JsonResponse({'success': {'checks': [str(checkcards.__len__()), checkprice], 'rechecks': [str(recheckcards.__len__()), recheckprice], 'operations': [str(operationcards.__len__()), operationprice]}})
                            return
                        return JsonResponse({'message': 'الطبيب لا يملك مساعدين'})
                    return JsonResponse({'message': 'المستخدم ليس طبيبا'})
                else:
                    return JsonResponse({'message': 'هناك خلل في التاريخ، تأكد أن تاريخ الإنتهاء موجود قبل تاريخ البدأ'})
            except ValueError:
                return JsonResponse({'message': 'الرجاء إدخال تاريخ صالح'})
        return JsonResponse({'error': 'Few information'})
    return JsonResponse({'error': "not logged in"})


def getnessadata(request):
    patientcardpk = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'GET':
            if 'pk' in request.GET:
                patientcardpk = request.GET['pk']
        if patientcardpk is not None:
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.PatientCard.objects.filter(pk=patientcardpk, assistant__doctor=doctor).exists():
                    patientcard = models.PatientCard.objects.get(
                        pk=patientcardpk, assistant__doctor=doctor)
                    if models.NessaCard.objects.filter(patientprofile=patientcard.patient, doctorprofile=doctor).exists():
                        nessacard = models.NessaCard.objects.get(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                        nessacardserializer = NessaCardSerializer(nessacard)
                        return JsonResponse({'success': nessacardserializer.data})
                    return JsonResponse({'success': 'no prev data'})
                return JsonResponse({'error': "patient card not avaible"})
            return JsonResponse({'error': "user isn't doctor"})
        return JsonResponse({'error': 'Few information'})
    return JsonResponse({'error': "not logged in"})


def setnessadata(request):
    # check if has already nessa card
    # if yes => update with new values
    # if no => create new one
    patientcardpk = None
    childrennumber = None
    childrensex = None
    mariagedate = None
    lastperiode = None
    datebirth = None
    lastbirth = None
    typeofbirth = None
    typesofbirth = ['normal', 'caesarean']
    childsex = None
    childsexs = ['male', 'female', 'twin']
    prevbirth = None
    prevoperations = None
    notes = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'POST':
            if 'pk' in request.POST:
                patientcardpk = request.POST['pk']
            if 'childrennumber' in request.POST:
                childrennumber = request.POST['childrennumber']
            if 'childrensex' in request.POST:
                childrensex = request.POST['childrensex']
            if 'mariagedate' in request.POST:
                mariagedate = request.POST['mariagedate']
            if 'lastperiode' in request.POST:
                lastperiode = request.POST['lastperiode']
            if 'datebirth' in request.POST:
                datebirth = request.POST['datebirth']
            if 'lastbirth' in request.POST:
                lastbirth = request.POST['lastbirth']
            if 'typeofbirth' in request.POST:
                typeofbirth = request.POST['typeofbirth']
            if 'childsex' in request.POST:
                childsex = request.POST['childsex']
            if 'prevbirth' in request.POST:
                prevbirth = request.POST['prevbirth']
            if 'prevoperations' in request.POST:
                prevoperations = request.POST['prevoperations']
            if 'notes' in request.POST:
                notes = request.POST['notes']
            try:
                datetime_obj = datetime.strptime(mariagedate, "%Y-%m-%d")
                mariagedate = datetime_obj.date()
            except ValueError:
                mariagedate = None
            try:
                datetime_obj = datetime.strptime(lastperiode, "%Y-%m-%d")
                lastperiode = datetime_obj.date()
            except ValueError:
                lastperiode = None
            try:
                datetime_obj = datetime.strptime(datebirth, "%Y-%m-%d")
                datebirth = datetime_obj.date()
            except ValueError:
                datebirth = None
            try:
                datetime_obj = datetime.strptime(lastbirth, "%Y-%m-%d")
                lastbirth = datetime_obj.date()
            except ValueError:
                lastbirth = None
        if patientcardpk is not None:
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.PatientCard.objects.filter(pk=patientcardpk, assistant__doctor=doctor).exists():
                    patientcard = models.PatientCard.objects.get(
                        pk=patientcardpk, assistant__doctor=doctor)
                    if models.NessaCard.objects.filter(patientprofile=patientcard.patient, doctorprofile=doctor).exists():
                        nessacard = models.NessaCard.objects.get(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                    else:
                        nessacard = models.NessaCard(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                    if childrennumber is not None:
                        if childrennumber is not "":
                            if isinstance(int(childrennumber), int):
                                nessacard.childrennumber = int(childrennumber)
                            else:
                                nessacard.childrennumber = 0
                        else:
                            nessacard.childrennumber = None
                    if childrensex is not None:
                        nessacard.childrensex = childrensex
                    nessacard.mariagedate = mariagedate
                    nessacard.lastperiode = lastperiode
                    nessacard.datebirth = datebirth
                    nessacard.lastbirth = lastbirth
                    if typeofbirth in typesofbirth:
                        nessacard.typeofbirth = typeofbirth
                    else:
                        nessacard.typeofbirth = None
                    if childsex in childsexs:
                        nessacard.childsex = childsex
                    else:
                        nessacard.childsex = None
                    if prevbirth in typesofbirth:
                        nessacard.prevbirth = prevbirth
                    else:
                        nessacard.prevbirth = None
                    if prevoperations is not None:
                        nessacard.prevoperations = prevoperations
                    if notes is not None:
                        nessacard.notes = notes
                    nessacard.save()
                    return JsonResponse({'success': "تم الإضافة بنجاح"})
                return JsonResponse({'error': "patient card not avaible"})
            return JsonResponse({'error': "user isn't doctor"})
        return JsonResponse({'error': 'Few information'})
    return JsonResponse({'error': "not logged in"})


def getMedicines(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        if request.method == 'GET':
            user = request.user
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.FavoriteMedicine.objects.filter(doctor=doctor).exists():
                    favmeds = models.FavoriteMedicine.objects.filter(
                        doctor=doctor)
                    favmedsSerializer = FavoriteMedicineSerializer(
                        favmeds, many=True)
                    return JsonResponse({'success': favmedsSerializer.data})
                return JsonResponse({'success': "Void"})
            return JsonResponse({'error': 'user is not doctor'})
        return JsonResponse({'error': 'something wrong'})
    return JsonResponse({'error': "not logged in"})


def addMedicine(request):
    medicinename = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'POST':
            if 'medicinename' in request.POST:
                if request.POST['medicinename'] != "":
                    medicinename = request.POST['medicinename']
        if medicinename is not None:
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if not models.FavoriteMedicine.objects.filter(name=medicinename, doctor=doctor).exists():
                    favoritemedicine = models.FavoriteMedicine(
                        name=medicinename, doctor=doctor)
                    favoritemedicine.save()
                    return JsonResponse({'success': "تم إضافة الدواء بنجاح"})
                return JsonResponse({'success': 'عذرا، هذا الدواء موجود بالفعل'})
            return JsonResponse({'error': 'user is not doctor'})
        return JsonResponse({'error': 'Few Informations'})
    return JsonResponse({'error': "not logged in"})


def deleteMedicine(request, pk):
    favoritemedicineid = pk
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'POST':
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.FavoriteMedicine.objects.filter(pk=favoritemedicineid, doctor=doctor).exists():
                    models.FavoriteMedicine.objects.get(
                        pk=favoritemedicineid, doctor=doctor).delete()
                    return JsonResponse({'success': "تم حذف الدواء بنجاح"})
                return JsonResponse({'success': 'عذرا، هذا الدواء غير موجود بالفعل'})
            return JsonResponse({'error': 'user is not doctor'})
        return JsonResponse({'error': 'Something wrong'})
    return JsonResponse({'error': "not logged in"})


def updatepics(request):
    patientcardid = None
    prescriptionImg = None
    XRaysImg = None
    analysisImg = None
    name = None
    age = None
    address = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if (models.AssistantProfile.objects.filter(user=request.user).exists()):
            assistant = models.AssistantProfile.objects.get(user=request.user)
            if request.method == 'POST':
                if 'patientcardid' in request.POST:
                    patientcardid = request.POST['patientcardid']
                if 'name' in request.POST:
                    name = request.POST['name']
                if 'age' in request.POST:
                    age = request.POST['age']
                if 'address' in request.POST:
                    address = request.POST['address']
                if 'prescriptionImg' in request.FILES:
                    prescriptionImg = request.FILES['prescriptionImg']
                if 'XRaysImg' in request.FILES:
                    XRaysImg = request.FILES['XRaysImg']
                if 'analysisImg' in request.FILES:
                    analysisImg = request.FILES['analysisImg']
                if patientcardid is not None:
                    if patientcardid != "undefined":
                        if models.PatientCard.objects.filter(pk=int(patientcardid), assistant=assistant.id).exists():
                            patientcard = models.PatientCard.objects.get(
                                pk=int(patientcardid), assistant=assistant.id)
                            if name is not None:
                                if name != "":
                                    patientcard.name = name
                            if age is not None:
                                if isinstance(int(age), int):
                                    patientcard.age = age
                            if address is not None:
                                if address != "":
                                    patientcard.address = address
                            if models.DoctorCard.objects.filter(patientCard=patientcard).exists():
                                doctorcard = models.DoctorCard.objects.filter(
                                    patientCard=patientcard).last()
                                if prescriptionImg is not None:
                                    doctorcard.prescription = prescriptionImg
                                if XRaysImg is not None:
                                    doctorcard.xRays = XRaysImg
                                if analysisImg is not None:
                                    doctorcard.analysis = analysisImg
                                doctorcard.save()
                                patientcard.save()
                                return JsonResponse({'success': 'تم حفظ التغييرات بنجاح'})
                            elif models.TempDoctorCard.objects.filter(patientCard=patientcard).exists():
                                doctorcard = models.TempDoctorCard.objects.filter(
                                    patientCard=patientcard).last()
                                if prescriptionImg is not None:
                                    doctorcard.prescription = prescriptionImg
                                if XRaysImg is not None:
                                    doctorcard.xRays = XRaysImg
                                if analysisImg is not None:
                                    doctorcard.analysis = analysisImg
                                doctorcard.save()
                                patientcard.save()
                                return JsonResponse({'success': 'تم حفظ التغييرات بنجاح'})
                            return JsonResponse({'message': 'يرجى عمل إضافة للعميل أولا'})
                        return JsonResponse({'error': 'patient card inavaible'})
                    return JsonResponse({'message': 'يرجى اختيار عميل أولا'})
                return JsonResponse({'error': 'Few Information'})
            return JsonResponse({'error': 'Something wrong'})
        return JsonResponse({'error': "user isn't assistant"})
    return JsonResponse({'error': "you are not logged in"})


def addnessapics(request):
    patientprofileid = None
    nessaImg = None
    if request.method == 'POST':
        if 'patientcardid' in request.POST:
            patientcardid = request.POST['patientcardid']
            if models.PatientCard.objects.filter(pk=patientcardid).exists():
                patientcard = models.PatientCard.objects.get(pk=patientcardid)
                patientprofileid = patientcard.patient.pk
        if 'nessaImg' in request.FILES:
            nessaImg = request.FILES['nessaImg']
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if nessaImg is not None:
            if patientprofileid is not None:
                if models.PatientProfile.objects.filter(pk=int(patientprofileid)).exists():
                    patientprofile = models.PatientProfile.objects.get(
                        pk=int(patientprofileid))
                    if models.DoctorProfile.objects.filter(user=user).exists():
                        doctor = models.DoctorProfile.objects.get(user=user)
                        nessacard, created = models.NessaCard.objects.get_or_create(
                            patientprofile=patientprofile,
                            doctorprofile=doctor
                        )
                        if created:
                            nessacard.save()
                        nessapicture = models.NessaPictures(
                            nessacard=nessacard, picture=nessaImg)
                        nessapicture.save()
                        return JsonResponse({'success': 'تم إضافة الصورة بنجاح'})
                    return JsonResponse({'error': 'user is not doctor'})
                return JsonResponse({'error': 'patient Profile doesn\'t exists'})
            return JsonResponse({'error': 'Few Informations'})
        return JsonResponse({'error': 'لا توجد أي صور لإضافتها'})
    return JsonResponse({'error': 'Your are not logged In'})


def getnessapics(request):
    patientprofileid = None
    if request.method == 'GET':
        if 'patientcardid' in request.GET:
            patientcardid = request.GET['patientcardid']
            if models.PatientCard.objects.filter(pk=patientcardid).exists():
                patientcard = models.PatientCard.objects.get(pk=patientcardid)
                patientprofileid = patientcard.patient.pk
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if patientprofileid is not None:
            if models.PatientProfile.objects.filter(pk=int(patientprofileid)).exists():
                patientprofile = models.PatientProfile.objects.get(
                    pk=int(patientprofileid))
                if models.DoctorProfile.objects.filter(user=user).exists():
                    doctor = models.DoctorProfile.objects.get(user=user)
                    nessacard, created = models.NessaCard.objects.get_or_create(
                        patientprofile=patientprofile,
                        doctorprofile=doctor
                    )
                    if created:
                        nessacard.save()
                    if models.NessaPictures.objects.filter(nessacard=nessacard).exists():
                        nessapictures = models.NessaPictures.objects.filter(
                            nessacard=nessacard)
                        nessapicturesSerializer = NessaPicturesSerializer(
                            nessapictures, many=True)
                        return JsonResponse({'success': nessapicturesSerializer.data})
                    return JsonResponse({})
                return JsonResponse({'error': 'user is not doctor'})
            return JsonResponse({'message': 'هناك خطب ما بشأن هذا المستخدم، الرجاء التواصل مع المساعد لإعادة تسجيله'})
        return JsonResponse({'error': 'Few Informations'})
    return JsonResponse({'error': 'Your are not logged In'})


def getvasculardata(request):
    patientcardpk = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'GET':
            if 'pk' in request.GET:
                patientcardpk = request.GET['pk']
        if patientcardpk is not None:
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.PatientCard.objects.filter(pk=patientcardpk, assistant__doctor=doctor).exists():
                    patientcard = models.PatientCard.objects.get(
                        pk=patientcardpk, assistant__doctor=doctor)
                    if models.VascularCard.objects.filter(patientprofile=patientcard.patient, doctorprofile=doctor).exists():
                        vascularcard = models.VascularCard.objects.get(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                        vascularcardserializer = VascularCardSerializer(
                            vascularcard)
                        return JsonResponse({'success': vascularcardserializer.data})
                    return JsonResponse({'success': 'no prev data'})
                return JsonResponse({'error': "patient card not avaible"})
            return JsonResponse({'error': "user isn't doctor"})
        return JsonResponse({'error': 'Few information'})
    return JsonResponse({'error': "not logged in"})


def setvasculardata(request):
    # check if has already nessa card
    # if yes => update with new values
    # if no => create new one
    patientcardpk = None
    data = {
        'HB': None,
        'PLT': None,
        'WBC': None,
        'RBC': None,
        'HTC': None,
        'Cholesterol': None,
        'TGC': None,
        'LDL': None,
        'HDL': None,
        'VLDL': None,
        'Urea': None,
        'CREATE': None,
        'SGOT': None,
        'SGPT': None,
        'PT': None,
        'INR': None,
        'HbA1c': None,
        'Ddimer': None,
        'FBS': None,
        'PPBS': None,
        'caTotal': None,
        'caIoized': None,
        'ESR': None,
        'CRP': None,
        'PTNC': None,
        'PTNS': None,
        'AntithrombinIII': None,
        'Anticarviolipin': None,
        'AntiLupus': None,
        'Anticoagulant': None,
        'ANA': None,
        'ANCA': None,
        'Factor': None
    }
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if request.method == 'POST':
            if 'pk' in request.POST:
                patientcardpk = request.POST['pk']
            for i in data:
                data[i] = request.POST[i]
        if patientcardpk is not None:
            if models.DoctorProfile.objects.filter(user=user).exists():
                doctor = models.DoctorProfile.objects.get(user=user)
                if models.PatientCard.objects.filter(pk=patientcardpk, assistant__doctor=doctor).exists():
                    patientcard = models.PatientCard.objects.get(
                        pk=patientcardpk, assistant__doctor=doctor)
                    if models.VascularCard.objects.filter(patientprofile=patientcard.patient, doctorprofile=doctor).exists():
                        vascularcard = models.VascularCard.objects.get(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                    else:
                        vascularcard = models.VascularCard(
                            patientprofile=patientcard.patient, doctorprofile=doctor)
                    for field in data:
                        if field is not None:
                            setattr(vascularcard, field, data[field])
                    vascularcard.save()
                    return JsonResponse({'success': "تم الإضافة بنجاح"})
                return JsonResponse({'error': "patient card not avaible"})
            return JsonResponse({'error': "user isn't doctor"})
        return JsonResponse({'error': 'Few information'})
    return JsonResponse({'error': "not logged in"})


def addvascularpics(request):
    patientprofileid = None
    vascularImg = None
    if request.method == 'POST':
        if 'patientcardid' in request.POST:
            patientcardid = request.POST['patientcardid']
            if models.PatientCard.objects.filter(pk=patientcardid).exists():
                patientcard = models.PatientCard.objects.get(pk=patientcardid)
                patientprofileid = patientcard.patient.pk
        if 'vascularImg' in request.FILES:
            vascularImg = request.FILES['vascularImg']
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if vascularImg is not None:
            if patientprofileid is not None:
                if models.PatientProfile.objects.filter(pk=int(patientprofileid)).exists():
                    patientprofile = models.PatientProfile.objects.get(
                        pk=int(patientprofileid))
                    if models.DoctorProfile.objects.filter(user=user).exists():
                        doctor = models.DoctorProfile.objects.get(user=user)
                        vascularcard, created = models.VascularCard.objects.get_or_create(
                            patientprofile=patientprofile,
                            doctorprofile=doctor
                        )
                        if created:
                            vascularcard.save()
                        vascularpicture = models.VascularPictures(
                            vascularcard=vascularcard, picture=vascularImg)
                        vascularpicture.save()
                        return JsonResponse({'success': 'تم إضافة الصورة بنجاح'})
                    return JsonResponse({'error': 'user is not doctor'})
                return JsonResponse({'error': 'patient Profile doesn\'t exists'})
            return JsonResponse({'error': 'Few Informations'})
        return JsonResponse({'error': 'لا توجد أي صور لإضافتها'})
    return JsonResponse({'error': 'Your are not logged In'})


def getvascularpics(request):
    patientprofileid = None
    if request.method == 'GET':
        if 'patientcardid' in request.GET:
            patientcardid = request.GET['patientcardid']
            if models.PatientCard.objects.filter(pk=patientcardid).exists():
                patientcard = models.PatientCard.objects.get(pk=patientcardid)
                patientprofileid = patientcard.patient.pk
    if request.user.is_authenticated and not request.user.is_anonymous:
        user = request.user
        if patientprofileid is not None:
            if models.PatientProfile.objects.filter(pk=int(patientprofileid)).exists():
                patientprofile = models.PatientProfile.objects.get(
                    pk=int(patientprofileid))
                if models.DoctorProfile.objects.filter(user=user).exists():
                    doctor = models.DoctorProfile.objects.get(user=user)
                    vascularcard, created = models.VascularCard.objects.get_or_create(
                        patientprofile=patientprofile,
                        doctorprofile=doctor
                    )
                    if created:
                        vascularcard.save()
                    if models.VascularPictures.objects.filter(vascularcard=vascularcard).exists():
                        vascularpictures = models.VascularPictures.objects.filter(
                            vascularcard=vascularcard)
                        vascularpicturesSerializer = VascularPicturesSerializer(
                            vascularpictures, many=True)
                        return JsonResponse({'success': vascularpicturesSerializer.data})
                    return JsonResponse({})
                return JsonResponse({'error': 'user is not doctor'})
            return JsonResponse({'message': 'هناك خطب ما بشأن هذا المستخدم، الرجاء التواصل مع المساعد لإعادة تسجيله'})
        return JsonResponse({'error': 'Few Informations'})
    return JsonResponse({'error': 'Your are not logged In'})
