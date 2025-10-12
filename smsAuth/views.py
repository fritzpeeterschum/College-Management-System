from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from schoolManagement.models import *
from student.models import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def createManageAccount(request):
    return render(request, 'auth/createManagementAccount.html')

def createStudentAccount(request):
    department_instance = SchoolDepartment.objects.all()
    data = {
        "department_instance":department_instance
    }
    return render(request, 'auth/createStudentAccount.html', context=data)

    
@transaction.atomic
def createManagementAccountAuth(request):
    if request.method == "POST":
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        dob = request.POST['dob']
        marital_status = request.POST['marital_status']
        address = request.POST['address']
    
    if User.objects.filter(email = email, status = True).exists():
        messages.success(request, "User already exist.")
        return redirect('/create-management-account')
    
    if not User.objects.filter(email = email).exists():
        newUserInstance = User.objects.create_user(username = username, password = password, email = email, first_name = firstname, last_name = lastname)
        if newUserInstance:
            newUserInstance.save()
            newManagementInstance = Management(user = newUserInstance)
            newManagementInstance.DOB = dob
            newManagementInstance.employee_number = username
            newManagementInstance.marital_status = marital_status
            newManagementInstance.address = address
            newManagementInstance.save()
            messages.success(request, "Account created successfully")
            return redirect('/create-management-account')
        
        else:
            messages.success(request, "Something went wrong")
            return redirect('/create-management-account')
        
    else:
        messages.success(request, "Something went wrong")
        return redirect('/create-management-account')
    
@transaction.atomic
def createStudentAccountAuth(request):
    if request.method == "POST":
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        is_student = True
        dob = request.POST['dob']
        address = request.POST['address']
        department_id = request.POST['department']
    
    if User.objects.filter(email = email).exists():
        messages.success(request, "User already exist.")
        return redirect('/create-student-account')
    
    if not User.objects.filter(email = email).exists():
        newUserInstance = User.objects.create_user(username = username, password = password, email = email, first_name = firstname, last_name = lastname, is_student = is_student)
        department = SchoolDepartment.objects.get(id=department_id)
        if newUserInstance:
            newUserInstance.save()
            newStudentInstance = Student(user = newUserInstance)
            newStudentInstance.student_number = username
            newStudentInstance.DOB = dob
            newStudentInstance.address = address
            newStudentInstance.department = department
            newStudentInstance.save()
            messages.success(request, "Account created successfully")
            return redirect('/create-student-account')
        
        else:
            messages.success(request, "Something went wrong")
            return redirect('/create-student-account')
        
    else:
        messages.success(request, "Something went wrong")
        return redirect('/create-student-account')
        

def studentUserLogin(request):
    return render(request, 'auth/studentLogin.html')

def managementUserLogin(request):
    return render(request, 'auth/managementLogin.html')

@transaction.atomic
def schoolUserAuthentication(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
    if not User.objects.filter(username=username).exists():
        messages.success(request, "User does not exist.")
        return redirect('/')
    
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.is_student and user.status == "True":
                login(request, user)
                return redirect('/student-profile')
            if user.status == "suspend":
                messages.success(request, "Account Suspended.")
                return redirect('/')
            if user.status == "False":
                messages.success(request, "User not found.")
                return redirect('/')
            else:
                messages.success(request, "Incorrect username or password.")
            return redirect('/')
        else:
            messages.success(request, "Incorrect username or password.")
            return redirect('/')
        
def managementUserAuthentication(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
    
    if not User.objects.filter(username=username).exists():
        messages.success(request, "User does not exist.")
        return redirect('/')
    
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.is_teacher and user.status == "True":
                login(request, user)
                return redirect('/teacher-profile')
            if user.is_active and user.is_parent and user.status == "True":
                login(request, user)
                return redirect('/parent-profile')
            if user.is_active and user.is_admin and user.status == "True":
                login(request, user)
                return redirect('/admin-profile')
            if user.status == "suspend":
                messages.success(request, "Account Suspended.")
                return redirect('/')
            if user.status == "False":
                messages.success(request, "User not found.")
                return redirect('/')
            else:
                messages.success(request, "Incorrect username or password.")
            return redirect('/')
        else:
            messages.success(request, "Incorrect username or password.")
            return redirect('/')

def studentUserLogout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect('/')

def managementUserLogout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect('/management-login')

def resetPassword(request):
    return render(request, 'auth/resetPassword.html')

@transaction.atomic
def resetPasswordAuth(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user_instance = User.objects.get(email = email)

        if email == user_instance.email and password == user_instance.password:
            messages.success(request, "The password you entered is the old password")
            return redirect('/reset-password')
        elif email == user_instance.email and password != user_instance.password:
            user_instance.set_password(password)
            user_instance.save()
            messages.success(request, "Password reset successfully")
            return redirect('/reset-password')
        else: 
            messages.success(request, "Something went wrong")
            return redirect('/reset-password')