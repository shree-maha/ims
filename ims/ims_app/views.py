from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Order, Customer


# Login View
def login_view(request):
    if request.method == "POST":
        user_id = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user is admin
        if user_id == 'admin@gmail.com' and password == 'admin@123':
            return redirect('admin_dashboard')  # Redirect to admin dashboard

        # Check if user is an existing customer
        try:
            customer = Customer.objects.get(username=user_id)
            if check_password(password, customer.password):  # Use hashed password check
                # Set session for the customer
                request.session['customer_id'] = customer.id
                request.session['username'] = customer.username
                return redirect('shopping_page')
            else:
                messages.error(request, "Invalid password for the existing customer.")
        except Customer.DoesNotExist:
            # Add new customer to the database with hashed password
            new_customer = Customer.objects.create(username=user_id, password=make_password(password))
            # Set session for the new customer
            request.session['customer_id'] = new_customer.id
            request.session['username'] = new_customer.username
            return redirect('shopping_page')

        messages.error(request, "Invalid username or password.")

    return render(request, 'index.html')


# Admin Dashboard View
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


# Shopping Page View (Display Products and Place Orders)
def shopping_page(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session.get('customer_id')
    username = request.session.get('username')

    # Get all products
    products = Product.objects.all()

    # Handle order placement
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        try:
            product = Product.objects.get(id=product_id)

            # Check if stock is available
            if product.stock_quantity >= quantity:
                # Create the order
                order = Order.objects.create(customer_id=customer_id, product=product, quantity=quantity)

                # Update the stock quantity
                product.stock_quantity -= quantity
                product.save()

                return redirect('order_page')
            else:
                messages.error(request, "Insufficient stock.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

    return render(request, 'shopping_page.html', {
        'username': username,
        'products': products,
    })


# Order Page View (Show Orders Placed by Customer)
def order_page(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session.get('customer_id')
    orders = Order.objects.filter(customer_id=customer_id)

    # Calculate grand total
    grand_total = sum(order.quantity * order.product.price for order in orders)

    return render(request, 'order_page.html', {
        'orders': orders,
        'grand_total': grand_total,
    })


# Customer Order Details View
def customer_order_details(request):
    orders = Order.objects.select_related('customer', 'product').all()

    return render(request, 'customer_order_details.html', {
        'orders': orders,
    })


# Product Tracking View
def ims_product_tracking(request):
    products = Product.objects.all()
    return render(request, 'ims_product_tracking.html', {'products': products})


# Add Product View
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        image = request.FILES.get('image')

        if not name or not description or not price or not stock_quantity:
            messages.error(request, "All fields are required!")
            return render(request, 'add_product.html')

        Product.objects.create(
            name=name,
            description=description,
            price=float(price),
            stock_quantity=int(stock_quantity),
            image=image
        )
        return redirect('ims_product_tracking')

    return render(request, 'add_product.html')


# Update Product View
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = float(request.POST.get('price', product.price))
        product.stock_quantity = int(request.POST.get('stock_quantity', product.stock_quantity))
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('ims_product_tracking')

    return render(request, 'update_product.html', {'product': product})


# Delete Product View
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('ims_product_tracking')
