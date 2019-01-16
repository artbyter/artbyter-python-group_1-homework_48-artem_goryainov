from django.urls import path
from webauth.views import DeliveryLoginView
from django.contrib.auth.views import LogoutView



app_name = 'webauth'

urlpatterns = [
    path('login/', DeliveryLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
