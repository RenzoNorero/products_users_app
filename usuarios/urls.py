from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name='signup'), # To sign up button
    path('signin', views.signin, name='signin'), # To sign in button
    path('signout', views.signout, name='signout'), # To logout button
    path('usuarios/', views.list_users, name='list_users'), # To access users list
    path('usuarios/modificar/<int:user_id>/', views.mod_user, name='mod_user'),
    path('usuarios/eliminar/<int:user_id>/', views.del_user, name='del_user'),
    path('usuarios/agregar/', views.create_users, name='create_users')

]

