from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def home(request):
    context = {}
    User = get_user_model()
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.is_staff:
                context['is_staff'] = True
                return render(request, "usuarios/index.html", context=context)
        except User.profile.RelatedObjectDoesNotExist:
            pass
    return render(request, "usuarios/index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        user_type = request.POST.get('user_type')
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)
                if user_type == 'admin':
                    user.is_staff = True
                    user.save()

                    # We add user to admins group
                    admin_group = Group.objects.get(name='administradores')
                    admin_group.user_set.add(user)

                messages.success(request, 'User registered successfully')
                return redirect('home')
        else:
            messages.error(request, 'Passwords dont match')
            return redirect('/signup')
    else:
        return render(request, 'usuarios/signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        # Autenticamos el usuario
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'usuarios/index.html', {'fname': fname})

        else:
            messages.error(request, 'Error. Check username or password')
            return redirect('home')

    return render(request, "usuarios/signin.html")

def signout(request):
    logout(request)
    messages.success(request, 'Log out successfully')
    return redirect('home')

# To show all users
@login_required
def list_users(request):
    users = User.objects.all()
    context = {'users': users, 'session_token': request.session.session_key}
    return render(request, 'usuarios/users_list.html', context)


# To edit users
@login_required
def mod_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        # This is to send email to admins
        enviar_correo_a_administradores(user)

        messages.success(request, 'User edited successfully')
        return redirect(reverse('list_users'))
    
    return render(request, 'usuarios/mod_users.html', {'user': user})

# To delete user
@login_required
def del_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()       
        messages.success(request, 'User deleted successfully')

        # This is to send email to admins
        # enviar_correo_a_administradores(user) 
        # The "#" must  be removed only after changing settings.py file on EMAIL_HOST_PASSWORD. Check README.

        return redirect(reverse('list_users'))
    except User.DoesNotExist:
        return HttpResponseNotFound('User not found')
    
# To create users
@login_required
def create_users(request):
    if request.method == 'POST':
        # We get data from form
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user_type = request.POST.get('user_type')
        
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('/usuarios/agregar')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('/usuarios/agregar')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    email=email,
                    first_name=fname,
                    last_name=lname)
                
                
                if user_type == 'admin': # If user was declared as admin, we set is_staff = True
                    user.is_staff = True
                    user.save()

                    # Then we add him to admins group
                    admin_group = Group.objects.get(name='administradores')
                    admin_group.user_set.add(user)

                messages.success(request, 'User created successfully')

                # This is to send email to admins
                # enviar_correo_a_administradores(user) 
                # The "#" must  be removed only after changing settings.py file on EMAIL_HOST_PASSWORD. Check README.
                
                return redirect('list_users')

    else:
        return render(request, 'usuarios/create_user.html')
    
def enviar_correo_a_administradores(user):
    asunto = 'Usuario modificado'
    mensaje = f"Se ha modificado al usuario {user.email}"
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    for email in admin_emails:
        try:
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        except Exception as e:
            print(f"No se pudo enviar correo a {email}. Error: {str(e)}")

