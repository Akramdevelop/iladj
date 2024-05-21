import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from accounts import models, serializers

def is_admin(user):
    return user.is_superuser

def statistics(request):
    if is_admin(request.user):
        # get list of doctors: name + id
        doctors = models.DoctorProfile.objects.all()
        doctorSerializer = serializers.DoctorProfileSerializer(doctors, many=True)
        doctors_data = json.dumps(doctorSerializer.data)
        context = {
            'doctors': doctors_data,
        }
        return render(request, 'statistics/statistics.html', context)
    return redirect(reverse('admin:index'))
