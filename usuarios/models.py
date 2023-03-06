from django.db import models
from django.contrib.auth.models import User, Group, Permission
from productos.models import Producto
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Producto)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=50)

# We create an admins group
admin_group, created = Group.objects.get_or_create(name='administradores')

# CWe create a signal to evaluate a user at creation. If is_staff = True, then add the user to admins group
@receiver(post_save, sender=User)
def add_user_to_admin_group(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        admin_group.user_set.add(instance)
