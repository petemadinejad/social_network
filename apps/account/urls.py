from django.urls import path

from apps.account.views import SignUp, LogIn

urlpatterns = [

    path('login/', LogIn.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),

]
