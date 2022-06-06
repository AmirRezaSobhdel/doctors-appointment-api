from django.test import TestCase, Client
import json


def bytearr_response_to_json_list(byte_arr):
    json_res = byte_arr.decode('utf8').replace("'", '"')
    json_arr_list = json.loads(json_res)
    return json_arr_list


def request_for_available_appointment_list_creation(client, start_time, end_time):
    response = client \
        .post('/appointment/doctor/', {'start_time': start_time, 'end_time': end_time})
    return response


def request_for_assigning_appointment(client, patient_name, patient_phone_number, appointment_id):
    return client.post('/appointment/patient/', {'patient_name': patient_name, 'patient_phone_number': patient_phone_number, 'appointment_id': appointment_id})


class AppoinmentSystemTestCase(TestCase):

    def setUp(self):
        pass

    def test_doctor_enters_an_end_date_that_is_sooner_than_start_date(self):

        response = request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:49:00')
        self.assertEqual(response.status_code, 200)

        response = request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T16:00:00')
        self.assertEqual(response.status_code, 400)

    def test_start_and_end_diff_less_than_30_mins_should_create_no_available_appointments(self):

        response = request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T17:40:00')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 0)

        response = request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 2)

    def test_if_there_is_no_appointment_set_empty_list_should_be_shown(self):

        response = self.client.get('/appointment/doctor/')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 0)

        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        response = self.client.get('/appointment/doctor/')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 2)

    def test_if_patients_info_is_shown_in_appointments_list_if_they_are_taken(self):
        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        request_for_assigning_appointment(self.client, 'Kevin', '123', 1)

        response = self.client.get('/appointment/doctor/')
        json_arr_list = bytearr_response_to_json_list(response.content)

        patient_existed = False
        for j in json_arr_list:
            if 'patient' in j and j['patient'] is not None:
                patient_existed = True

        self.assertEqual(True, patient_existed)

    def test_doctor_delete_available_appointments_if_doesnt_exist_404(self):
        response = self.client.delete('/appointment/doctor/898/')
        self.assertEqual(response.status_code, 404)

    def test_if_the_appointment_is_taken_by_a_patient_then_a_406_error_is_shown(self):
        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        request_for_assigning_appointment(self.client, 'Kevin', '123', 1)

        response = self.client.delete('/appointment/doctor/1/')
        self.assertEqual(response.status_code, 406)

    def test_if_no_available_appointment_that_day_then_an_empty_list_should_be_shown(self):

        response = self.client.get('/appointment/available/2022-5-10/')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 0)

    def test_if_either_phone_number_or_name_is_not_given_then_a_406_error_is_shown(self):
        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')

        response = self.client.post('/appointment/patient/',
                                    {'patient_phone_number': '266', 'appointment_id': 1})
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/appointment/patient/',
                                    {'patient_name': 'Alex', 'appointment_id': 1})
        self.assertEqual(response.status_code, 400)

    def test_if_the_appointment_is_already_taken_by_a_patient_then_a_409_error_is_shown(self):
        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        request_for_assigning_appointment(self.client, 'Kevin', '123', 1)

        response = request_for_assigning_appointment(self.client, 'Alex', '255', 1)
        self.assertEqual(response.status_code, 409)

    def test_if_the_appointment_is_deleted_then_a_404_error_is_shown(self):
        response = request_for_assigning_appointment(self.client, 'Kevin', '123', 1)
        self.assertEqual(response.status_code, 404)

    def test_if_no_appointment_for_phone_number_then_an_empty_list_should_be_shown(self):
        response = self.client.get('/appointment/patient/09365489687/')
        print(response.content)
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(len(json_arr_list), 0)

    def test_s(self):
        request_for_available_appointment_list_creation(self.client, '2022-06-05T17:30:00', '2022-06-05T18:40:00')
        request_for_assigning_appointment(self.client, 'Kevin', '123', 1)
        request_for_assigning_appointment(self.client, 'Kevin', '123', 2)

        response = self.client.get('/appointment/patient/123/')
        json_arr_list = bytearr_response_to_json_list(response.content)
        self.assertEqual(2, len(json_arr_list))