from django.shortcuts import render
import pandas as pd
from rest_framework import viewsets, mixins, status
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from datetime import datetime
from appointment.models import Appointment, Patient
from appointment.serializers import AppointmentSerializer, SetAppointmentSerializer, TimeRangeSerializer


class DoctorListCreateView(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 viewsets.GenericViewSet):

    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return TimeRangeSerializer
        else:
            return AppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        instance_serializer = AppointmentSerializer(create_available_appointments(start_time, end_time), many=True)
        return Response(instance_serializer.data)


class DoctorDestroyView(DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer = AppointmentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.patient is not None:
            return Response({"error": "this time slot is taken by a patient"}, 406)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailableAppointmentsListView(ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        queryset = Appointment.objects.filter(patient__isnull=True, starting_time__contains= date)
        return queryset


class PatientAppointmentsListView(ListAPIView):

    def get_queryset(self):
        return Appointment.objects\
            .filter(patient__phone_number=self.kwargs['phone_number']).all()

    serializer_class = AppointmentSerializer


class PatientAppointmentCreateView(CreateAPIView):

    serializer_class = SetAppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient_name = serializer.validated_data['patient_name']
        patient_phone_number = serializer.validated_data['patient_phone_number']
        appointment_id = serializer.validated_data['appointment_id']

        appointment = get_or_none(Appointment, id=appointment_id)
        if appointment is None:
            return Response({"error": "appointment doesn't exist"}, 404)
        elif appointment.patient is not None:
            return Response({"error": "this time slot is already taken by a patient"}, 409)

        patient = Patient.objects.filter(phone_number=patient_phone_number).first()
        if patient is None:
            patient = Patient()
            patient.name = patient_name
            patient.phone_number = patient_phone_number
            patient.save()

        appointment.patient = patient
        appointment.save()

        return Response(AppointmentSerializer(appointment).data)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def create_available_appointments(start_time, end_time):

    time_slots = (pd.DataFrame(columns=['NULL'],
                               index=pd.date_range(start_time, end_time,
                                                   freq='30T'))
                  .index.strftime('%Y-%m-%dT%H:%M:%S')
                  .tolist()
                  )

    available_appointments = []

    for t in time_slots[0:-1]:
        available_appointment = Appointment()
        available_appointment.starting_time = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
        available_appointments.append(available_appointment)

    Appointment.objects.bulk_create(available_appointments)

    return available_appointments