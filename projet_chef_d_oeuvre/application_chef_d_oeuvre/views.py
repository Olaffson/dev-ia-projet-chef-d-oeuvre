from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from . import forms

# Create your views here.


# def index(request):
#     return render(request, 
#                   'application_chef_d_oeuvre/index.html',
#                   )
    
# def logout_user(request):
    
#     logout(request)
#     return redirect('login')



# def login_page(request):
#     form = forms.LoginForm()
#     message = ''
#     if request.method == 'POST':
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#         message = 'Identifiants invalides.'
#     return render(request, 'application_chef_d_oeuvre/login.html', context={'form': form, 'message': message})


# def signup_page(request):
#     form = forms.SignupForm()
#     if request.method == 'POST':
#         form = forms.SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # auto-login user
#             login(request, user)
#             return redirect(settings.LOGIN_REDIRECT_URL)
#     return render(request, 'application_chef_d_oeuvre/signup.html', context={'form': form})





def index(request):
    if request.user.is_authenticated:
        return render(request, 'application_chef_d_oeuvre/index.html', {'first_name': request.user.first_name})
    else:
        return redirect('login')

    
def logout_user(request):
    
    logout(request)
    return redirect('login')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')  # change 'home' to 'index'
        message = 'Identifiants invalides.'
    return render(request, 'application_chef_d_oeuvre/login.html', context={'form': form, 'message': message})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # change settings.LOGIN_REDIRECT_URL to 'index'
    return render(request, 'application_chef_d_oeuvre/signup.html', context={'form': form})