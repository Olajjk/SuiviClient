from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password1  = request.POST.get('password1', '')
        password2  = request.POST.get('password2', '')

        if not all([first_name, last_name, email, password1, password2]):
            messages.error(request, 'Tous les champs sont obligatoires.')
        elif password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
        elif len(password1) < 8:
            messages.error(request, 'Le mot de passe doit faire au moins 8 caractères.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe déjà.')
        else:
            User.objects.create_user(
                email      = email,
                password   = password1,
                first_name = first_name,
                last_name  = last_name,
            )
            send_mail(
                subject='Bienvenue sur SuiviClient !',
                message=f'Bonjour {first_name},\n\nTon compte a bien été créé.\n\nÀ bientôt !',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'Compte créé ! Un email de confirmation a été envoyé.')
            return redirect('login')

    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email et mot de passe requis.')
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # change vers ta page d'accueil
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html', {'user': request.user})