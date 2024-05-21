from rest_framework import serializers
from .models import DoctorProfile, PatientCard, DoctorCard, TempDoctorCard, NessaCard, FavoriteMedicine, NessaPictures, VascularCard, VascularPictures


class DoctorProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ['id', 'username']

    def get_username(self, obj):
        return obj.user.username


class PatientCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCard
        fields = '__all__'


class DoctorCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCard
        fields = '__all__'


class TempDoctorCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempDoctorCard
        fields = '__all__'


class NessaCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NessaCard
        fields = '__all__'


class FavoriteMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMedicine
        fields = '__all__'


class NessaPicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NessaPictures
        fields = '__all__'


class VascularCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VascularCard
        fields = '__all__'


class VascularPicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VascularPictures
        fields = '__all__'
