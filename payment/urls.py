
from django.urls import path, include # type: ignore
from payment import views


urlpatterns = [
    path('manage-payment', views.managePayment),
    path('make-payment', views.makePayment),
    path('payment-history', views.paymentHistory),
]