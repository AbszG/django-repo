from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') #redirect to homepage when valid, can render another page
    else:
        #add Handling and remove the line below if you don't want to, leave it as it is
        form = RegistrationForm()
    return render(request, 'tempdir/register.html', {'form': form}) 