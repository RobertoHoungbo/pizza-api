from django.urls import path
from . import views

urlpatterns = [
    # path('hello', views.HelloOrdersView.as_view(), name='hello_orders'),
    path('', views.OrderCreateListView.as_view(), name='orders'),
    path('<int:order_id>/', views.OrderCreateDetailView.as_view(), name='order_details'),
    path('update-status/<int:order_id>/', views.UpdateOrderStatus.as_view(), name='order_status_update'),
    path('users/@me/orders/', views.UserOrdersView.as_view(), name='user_orders'),
    path('users/@me/order/<int:order_id>/', views.UserOrderDetailView.as_view(), name='user_order_detail')
]
