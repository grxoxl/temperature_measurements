from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.http import JsonResponse

User = get_user_model()

from .forms import UserCreateForm, UserCreateForm, LoginForm

def register_user(request):

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email=form.cleaned_data.get('email')
            user_username=form.cleaned_data.get('username')
            user_password=form.cleaned_data.get('password1')

            #Create new user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )
            
            return redirect('basepage:home')
    else:
        form = UserCreateForm()
    return render(request, 'account/register.html', {'form': form}) 

def login_user(request):
    form = LoginForm()

    # Check if user is already authenticated
    if request.user.is_authenticated:
        if request.headers.get("X-Telegram-Bot"):  # For Telegram bot authentication
            return JsonResponse({"authenticated": True, "message": "Already logged in."})
        return redirect('basepage:home')

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.headers.get("X-Telegram-Bot"):  # For Telegram bot authentication
                return JsonResponse({"authenticated": True, "message": "Authentication successful."})
            return redirect('basepage:home')
        else:
            if request.headers.get("X-Telegram-Bot"):  # For Telegram bot authentication
                return JsonResponse({"authenticated": False, "message": "Invalid credentials."})
            messages.info(request, 'Username or Password is incorrect')
            return redirect('account:login')

    if request.headers.get("X-Telegram-Bot"):  # If bot requests GET (unauthenticated)
        return JsonResponse({"authenticated": False, "message": "Please log in via POST request."})

    context = {'form': form}
    return render(request, 'account/login.html', context)

# def login_user(request):

#     form = LoginForm()

#     if request.user.is_authenticated:
#         return redirect('basepage:home')

#     if request.method == 'POST':

#         form = LoginForm(request.POST, request.FILES)

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('basepage:home')
#         else:
#             messages.info(request, 'Username or Password is incorrect')
#             return redirect('account:login')
#     context = {
#         'form': form
#     }
#     return render(request, 'account/login.html', context)


def logout_user(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        if key == 'session_key':
            continue
        del request.session[key]
    logout(request)
    return redirect('account:login')