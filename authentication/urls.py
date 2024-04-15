from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HelloAuthView.as_view(), name='hello_auth'),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('users/', views.UsersListView.as_view(), name='users'),
    path('user/@me/', views.UserDetailView.as_view(), name='user_detail'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', views.CustomTokenVerifyView.as_view(), name='verify_token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

