from django.shortcuts import render, redirect
from .forms import CreateUserForm

# Create your views here.

def register(request):
    form = CreateUserForm()
    
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('store')
        
    context = {'form': form}
    
    return render(request, 'account/registration/register.html', context=context)


def email_verification(request):
    pass


def email_verification_success(request):
    pass


def email_verification_failed(request):
    pass


def email_verification_sent(request):
    pass