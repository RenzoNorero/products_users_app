from django.conf import settings
from django.http import HttpResponseNotFound
from .models import Producto
from django.shortcuts import redirect, render, get_object_or_404
from .models import Producto
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from usuarios.models import User

def tienda(request):
    q = request.GET.get('q', '')
    products = Producto.objects.all()
    context = {'products': products, 'q': q}
    return render(request, 'productos/tienda.html', context)

def detalle_producto(request, sku):
    producto = Producto.objects.get(sku=sku)
    
    # To update click count
    producto.click_count += 1
    producto.save()
    
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required
def list_products(request):
    products = Producto.objects.all()
    return render(request, 'productos/prod_list.html', {'products': products})

# To modify products
@login_required
def mod_products(request, prod_sku):
    product = get_object_or_404(Producto, sku=prod_sku)
    if request.method == 'POST':
        product.username = request.POST['name']
        product.brand = request.POST['brand']
        product.price = request.POST['price']
        product.save()
        messages.success(request, 'Product edited successfully.')

        # This is to send email to admins
        # enviar_correo_a_administradores(product) 
        # The "#" must  be removed only after changing settings.py file on EMAIL_HOST_PASSWORD. Check README.
        
        return redirect(reverse('list_products'))
    
    return render(request, 'productos/mod_products.html', {'producto': product})

# To delete products
@login_required
def del_products(request, prod_sku):
    try:
        product = Producto.objects.get(sku=prod_sku)
        product.delete()
        messages.success(request, 'Product deleted successfully')

        # This is to send email to admins
        # enviar_correo_a_administradores(product) 
        # The "#" must  be removed only after changing settings.py file on EMAIL_HOST_PASSWORD. Check README.

        return redirect(reverse('list_products'))
    except Producto.DoesNotExist:
        return HttpResponseNotFound('Product not found') # Si no encuentra el id, retorna ese mensaje
    
# To create products
@login_required
def create_products(request):
    if request.method == 'POST':
        # We get the data from the form
        name = request.POST['name']
        brand = request.POST['brand']
        price = request.POST['price']
        
        # We create a new object
        new_product = Producto.objects.create(
            name=name,
            brand=brand,
            price=price
        )

        new_product.save() # Saves at database
        messages.success(request, 'Product created successfully')

        # This is to send email to admins
        # enviar_correo_a_administradores(new_product) 
        # The "#" must  be removed only after changing settings.py file on EMAIL_HOST_PASSWORD. Check README.


        return redirect('list_products')
    
    else:
        return render(request, 'productos/create_products.html')

def error_handler(request, exception=None):
    message = "You must sign in"
    return render(request, 'error.html', {'message': message})

# To send emails for notifications to admins
def enviar_correo_a_administradores(product):
    asunto = 'Product modified'
    mensaje = f"Product {product.name} has been modified"
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    for email in admin_emails:
        try:
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        except Exception as e:
            print(f"Couldn't send email to {email}. Error: {str(e)}")
