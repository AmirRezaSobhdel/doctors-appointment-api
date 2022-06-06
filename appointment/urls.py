
from django.urls import path
import appointment.views as views

app_name = "appointment"
urlpatterns = [
    path("doctor/",views.DoctorListCreateView.as_view({"get": "list", "post": "create"})),
    path("doctor/<int:pk>/",views.DoctorDestroyView.as_view()),
    path("available/<date>/",views.AvailableAppointmentsListView.as_view()),
    path("patient/<phone_number>/",views.PatientAppointmentsListView.as_view()),
    path("patient/",views.PatientAppointmentCreateView.as_view()),
]
