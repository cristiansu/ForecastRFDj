import profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return render(request, 'login.html')

def login_attemp(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password') 

        user_obj=User.objects.filter(username=username).first() 
        if user_obj is None:
            messages.success(request, 'Usuario no encontrado')
            #return redirect('/login') 
            return render(request, 'login.html')
        profile_obj=Profile.objects.filter(user=user_obj).first()  
        if not profile_obj.is_verified:
            messages.success(request, 'Usuario no verificado. Revisa tu mail')
            #return redirect('/login') 
            return render(request, 'login.html')
        user=authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Error Password')
            #return redirect('/login')
            return render(request, 'login.html')
        login(request, user)
        return redirect('/home')

    return render(request, 'login.html')

def register_attemp(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username ya existe')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request, 'email ya existe')
                return redirect('/register')
            
            user_obj=User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_after_registration(email, auth_token)
            return redirect('/token')
        
        except Exception as e:
            print(e)
                    
    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def verify(request, auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Tu cuenta est?? vigente')
                #return redirect('/login')
                return render(request, 'login.html')

            profile_obj.is_verified =True
            profile_obj.save()
            messages.success(request, 'Tu cuenta ha sido verificada correctamente')
            #return redirect('/login')
            return render(request, 'login.html')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'error.html')       

def send_mail_after_registration(email,token):
    subject='Tu cuenta necesita ser verificada'
    #message=f'Hola, haz click en el link para verificar tu cuenta: http://127.0.0.1:8000/verify/{token}'
    message=f'Hola, haz click en el link para verificar tu cuenta: https://forecast-app-rf.herokuapp.com/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email,]
    send_mail(subject, message, email_from, recipient_list)
