from rest_framework import serializers
from appointment.models import Appointment, Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['name', 'phone_number']


class AppointmentSerializer(serializers.ModelSerializer):

    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = ["id", "starting_time", "patient"]
        read_only_fields = ["id"]


class TimeRangeSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def validate(self, data):
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("end time must occur after start time")
        return data


class SetAppointmentSerializer(serializers.Serializer):
    patient_name = serializers.CharField(max_length= 50)
    patient_phone_number = serializers.CharField(max_length=16)
    appointment_id = serializers.IntegerField()