from django.urls import path
from account import views
urlpatterns=[
path('register/',views.UserRegistrationView.as_view(),name='register'),
path('login/',views.UserLoginView.as_view(),name='login'),
path('profile/',views.UserProfileView.as_view(),name='login'),
path('changepass/',views.UserChangePassword.as_view(),name='changepass'),
path('reset/',views.SendPasswordResetEmail.as_view(),name='reset_link'),
path('resetpass/<uid>/<token>/',views.UserPasswordResetView.as_view(),name='reset_pass'),
]