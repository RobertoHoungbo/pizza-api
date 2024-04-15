from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from .views import OrderCreateListView, OrderCreateDetailView
from django.urls import reverse
from rest_framework import status
from .models import Order, User
# Create your tests here.


class PostOrderCreateTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = OrderCreateListView.as_view()
        self.url = "orders"

    def authenticate(self):
        self.client.post(reverse("signup"), {
            "username": "Bambi", "email": "bambi@app.com", "phone_number": "+22997989996", "password": "pa55w0rD"
        })

        response = self.client.post(reverse('token_obtain_pair'), {
            "email": "bambi@app.com",
            "password": "pa55w0rD"
        })

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_orders(self):
        self.authenticate()

        response = self.client.get(reverse(self.url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):

        self.authenticate()

        order = {"size": "SMALL", "quantity": 3}

        response = self.client.post(reverse(self.url), order)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderDeleteTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="Bambi",
            email="bambi@app.com",
            phone_number="+22997989996",
            password="pa55w0rD"
        )
        self.order = Order.objects.create(size="LARGE", quantity=4, customer=self.user)
        self.url = reverse("order_details", args=[self.order.id])
        self.view = OrderCreateDetailView.as_view()

    def authenticate(self):

        response = self.client.post(reverse('token_obtain_pair'), {
            "email": "bambi@app.com",
            "password": "pa55w0rD"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_delete_order(self):
        self.authenticate()

        response = self.client.delete(self.url)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
