from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import OrderCreationSerializer, OrderStatusSerializer, OrderDetailSerializer
from .models import Order, User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from authentication.authentication import CustomJWTAuthentication

# Create your views here.


# class HelloOrdersView(generics.GenericAPIView):

#    def get(self, request):
#        return Response(data={"message": "Hello Orders !"}, status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = OrderCreationSerializer
    queryset = Order.objects.all()
    # permission_classes = [IsAuthenticated]

    """"@swagger_auto_schema(
        operation_summary="View all orders",
        operation_description="This allow you to view all orders of the database"
    )
    def get(self, request):
        orders = Order.objects.all()

        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)"""

    @swagger_auto_schema(
        operation_summary="Create a new order",
        operation_description="This allow you to create a new order.")
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateDetailView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View details of an order",
        operation_description="This allows you to view all details of a specific order")
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update an order",
        operation_description="This allows you to update a specific order")
    def put(self, request, order_id):
        data = request.data

        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete an order",
        operation_description="This allows you to delete a specific order")
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        order.delete()

        return Response({"message": "The order have been deleted !"}, status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatus(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = OrderStatusSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Update an order status",
        operation_description="This allow you to update an order status")
    def put(self, request, order_id):
        data = request.data

        order = get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = OrderCreationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View all orders made by a user",
        operation_description="This allow you to view all orders made by a specific user")
    def get(self, request):
        user = request.user

        orders = Order.objects.all().filter(customer=user)

        serializer = self.serializer_class(instance=orders, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserOrderDetailView(generics.GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View details of an order made by a user",
        operation_description="This allow you to view the details of an specific order made by a specific user.")
    def get(self, request, order_id):

        user = request.user

        order = Order.objects.all().filter(customer=user).get(pk=order_id)

        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

