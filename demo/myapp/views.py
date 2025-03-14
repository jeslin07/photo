from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import ContactForm
from .models import ContactMessage
from .forms import WeddingBookingForm
from myapp.models import SaveTheDate
from .models import Product
from django.views.decorators.http import require_POST
import razorpay
from django.conf import settings

# Create your views here.
def base(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            # Redirect to the profile page
            return redirect('profile')  # Ensure 'profile' is the name of the URL pattern for the profile page
        else:
            # Show an error message if authentication fails
            messages.error(request, 'Invalid username or password.')
    
    # Render the login page
    return render(request, 'login.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated
    return render(request, 'profile.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        
        # Create and authenticate user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Automatically log in the user after registration
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")  # Redirect to profile page after login

    return render(request, "register.html")  # Show the registration page



def logout_view(request):
    logout(request)
    return redirect("base")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('base')  # Redirect to the home page or a success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'base.html', {'form': form})


def save_the_date(request):
    if request.method == 'POST':
        form = WeddingBookingForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, "Your booking request has been submitted. We'll contact you soon!")
            return redirect('base')  # Redirect to the same page or a success page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WeddingBookingForm()
    
    return render(request, 'base.html', {'form': form})



def product_view(request):
    products = Product.objects.all()
    
    # Add a delay value to each product
    for index, product in enumerate(products):
        product.delay = (index + 1) * 200  # Delay in milliseconds
    
    return render(request, 'product.html', {'products': products})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from form

    # Add product to cart logic here (e.g., using sessions or a cart model)
    # Example:
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

    messages.success(request, f"Added {quantity} x {product.name} to your cart.")
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    
    # Fetch product details and calculate total price
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity,
        })
    
    context = {
        'products': products,
        'total_price': total_price,
    }
    
    return render(request, 'cart.html', context)

def payment(request):
    return render(request, 'payment.html')