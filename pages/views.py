from django.http import JsonResponse
from django.shortcuts import redirect, render

from accounts.models import DoctorProfile, AssistantProfile, PatientCard


def index(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'pages/index.html', context)


def services(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'pages/service-index.html', context)


def doctors(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'pages/doctors-index.html', context)


def doctorDashboard(request):
    # Assuming you have a way to determine the currently logged-in doctor
    # For example, you might retrieve it based on the logged-in user's profile
    # Here, we assume you have a User object for the current user
    if request.user.is_authenticated and not request.user.is_anonymous and DoctorProfile.objects.filter(user=request.user).exists():
        try:
            doctor = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            doctor = None  # Handle the case where the user is not a doctor

        return render(request, 'pages/doctorDashboard.html', {'doctor': doctor})
    return redirect('signin')


def assistantIndex(request):
    if request.user.is_authenticated and not request.user.is_anonymous and AssistantProfile.objects.filter(user=request.user).exists():
        assistantId = AssistantProfile.objects.get(user=request.user).id
        context = {'assistant_id': assistantId}
        return render(request, 'pages/assistant-index.html', context)
    return redirect('signin')


def switchofdoctors(request):
    if request.user.is_authenticated and not request.user.is_anonymous and DoctorProfile.objects.filter(user=request.user).exists():
        username = request.user.username
        context = {'username': username}
        return render(request, 'pages/switchofdoctor.html', context)
    return redirect('signin')


def calculation(request):
    if request.user.is_authenticated and not request.user.is_anonymous and DoctorProfile.objects.filter(user=request.user).exists():
        username = request.user.username
        context = {'username': username}
        return render(request, 'pages/calculation.html', context)
    return redirect('signin')


def getnessa(request):
    pass


def sheet(request, patientcardpk):
    patientcard = None
    if request.user.is_authenticated and not request.user.is_anonymous and DoctorProfile.objects.filter(user=request.user).exists():
        user = request.user
        doctor = DoctorProfile.objects.get(user=request.user)
        if PatientCard.objects.filter(pk=patientcardpk).exists():
            patientcard = PatientCard.objects.get(pk=patientcardpk)
        if patientcard is not None:
            context = {'username': user,
                       'patientname': patientcard.name, 'primarykey': patientcardpk}
            if doctor.speciality == "nessa":
                return render(request, "pages/nessaDoctor.html", context)
            elif doctor.speciality == "vascular":
                return render(request, "pages/vascularDoctor.html", context)
            else:
                return redirect('doctorDashboard')
        return redirect('switchofdoctors')
    return redirect('signin')


def favoriteMedicine(request):
    if request.user.is_authenticated and not request.user.is_anonymous and DoctorProfile.objects.filter(user=request.user).exists():
        context = {}
        return render(request, 'pages/favoriteMedicines.html', context)
    return redirect('signin')
