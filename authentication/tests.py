from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from .views import UserCreateView
from django.urls import reverse
from rest_framework import status
# Create your tests here.


User = get_user_model()


class CreateUserTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("signup")
        self.factory = APIRequestFactory()
        self.view = UserCreateView.as_view()

    def test_user_creation(self):
        user = {"username": "Bambi", "email": "bambi@app.com", "phone_number": "+22997989996", "password": "pa55w0rD"}

        request = self.factory.post(self.url, user)

        response = self.view(request)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


