# Doctor's appointment management system

Stack: Django, Sqlite

### models

#### Patient
this model represents a patient which can have multiple appointments

#### Appointment
this model represents a 30 minutes time slot added by the doctor for the patients to be able to take appointments.
if the **patient** relationship is null, then this time slot is open and available.
otherwise, its taken by a patient.