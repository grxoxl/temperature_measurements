from django.shortcuts import redirect, render
from django.http import HttpResponse

def home(request):
    
    if not request.user.is_authenticated:
        return redirect('account:login')
    return render(request, 'base.html')


