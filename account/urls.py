from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
     path('create', views.CreateUser.as_view(), name='create_user'),
     path('<int:pk>', views.OneUser.as_view(), name='one_user'),
     path('auth', views.Auth.as_view(), name='auth'),
     path('refresh_token', TokenRefreshView.as_view(), name='refresh'),
     path('verify', views.VerifyUser.as_view(), name='verify'),
     path('reset-password', views.PasswordResetView.as_view(), name='reset_password'),
     path('forgot-password', views.ForgotPasswordView.as_view(), name='forgot_password'),
     path('change-email', views.ChangeEmailView.as_view(), name='reset-email'),
     path('create-transaction', views.CreateTransaction.as_view(), name='create_transactions'),
     path('view-transactions', views.ViewTransactions.as_view(), name='view_transaction'),
]
