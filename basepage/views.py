from django.shortcuts import redirect, render

def home(request):
    
    if not request.user.is_authenticated:
        return redirect('account:login')
    context = {
        'show_devices_header': True,
        'show_second_device_button': True,
        'show_first_device_button': True,
    }
    return render(request, 'base.html', context)


