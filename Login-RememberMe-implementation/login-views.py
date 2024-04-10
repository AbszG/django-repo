from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from django.conf import settings


#for Remember Me add the following line in settings.py
# SESSION_COOKIE_AGE = 604800  # 1 week 



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            if not remember_me:
                # If remember me checkbox is not checked, use the default session expiry
                request.session.set_expiry(0)  # Expiry set to 0 will use the default SESSION_COOKIE_AGE
            else:
                # If remember me checkbox is checked, use a longer session expiry
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return redirect('index') #redirects to Home page if login successful change if you want
        else:

            return render(request, 'tempdir/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'tempdir/login.html')