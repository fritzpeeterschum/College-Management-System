from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from student.models import *
from payment.models import *

# Create your views here.
def managePayment(request):
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    current_month = datetime.now().month
    current_year = datetime.now().year
    if 1 <= current_month <= 4:
        current_semester = 'first'
    elif 5 <= current_month <= 8:
        current_semester = 'second'
    else:
        current_semester = 'third'

    data = {
        "current_semester":current_semester,
        "current_year":current_year,
        "student_instance":student_instance
    }
    return render(request, 'student/feesManagement.html', context=data)

def makePayment(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        payment_method = request.POST["payment_method"]
        current_month = datetime.now().month
        current_year = datetime.now().year

        student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
        if  student_instance:
            Payment_instance = Payment(student = student_instance, amount = amount, payment_method = payment_method, month = current_month, academic_year = current_year)
            Payment_instance.save()
            messages.success(request, "Payment successful.")
            return redirect('/manage-payment')
        else:
            messages.success(request, "Something went wrong.")
            return redirect('/manage-payment')
        
def paymentHistory(request):
    student_instance = Student.objects.get(user=User.objects.get(email=request.user.email))
    payment_instance = Payment.objects.filter(student = student_instance)

    data = {
       "payment_instance":payment_instance,
       "student_instance":student_instance
    }
    return render(request, 'student/payment_history.html', context=data)