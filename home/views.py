import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Product, Category, UserProfile, Cart, Wishlist, Booking

from django.shortcuts import render, get_object_or_404
from .models import Product  # Make sure to import any required models
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas  # Assuming you use reportlab for PDF generation

def pdf_report_create(request, pid):
    # Get the product using the provided 'pid'
    product = get_object_or_404(Product, id=pid)

    # Create a PDF response
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # You can customize the PDF content here
    p.drawString(100, 750, f"Product Name: {product.name}")
    p.drawString(100, 735, f"Product Price: {product.price}")
    # Add more product details as needed
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
# Create your views here.
def home(request):
    try:
        product = Product.objects.all()
        user = User.objects.get(id=request.user.id)
        data = UserProfile.objects.get(user=user)
    except:
        pass
    allcategory = Category.objects.all()
    return render(request, 'home.html', locals())

def user_product(request, pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, 'catogaryproduct.html', locals())

def logins(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('signup')
    return render(request, 'login.html', locals())

def about(request):
    return render(request, 'about.html', locals())

def signup(request):
    if request.method == "POST":
        try:
            usernames = request.POST["username"]
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            mobile = request.POST['mobilenumber']
            gender = request.POST['gender']
            user = User.objects.create_user(username=usernames, first_name=fname, last_name=lname, email=email, password=password)
            UserProfile.objects.create(user=user, mobile=mobile, gender=gender)
            messages.success(request, "Registration Successful")
            return redirect('home')
        except:
            messages.error(request, "Some error occurred")
            return redirect('signup')
    return render(request, 'signup.html', locals())

def addaddress(request):
    try:
        user = User.objects.get(id=request.user.id)
        data = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        data = None
    if request.method == "POST":
        fullname = request.POST["fullname"]
        mobile2 = request.POST["mobile2"]
        pincode = request.POST["pincode"]
        address = request.POST["address"]
        city = request.POST["city"]
        states = request.POST["state"]
        UserProfile.objects.filter(id=data.id).update(fullname=fullname, mobile2=mobile2, pincode=pincode, address=address, city=city, states=states)
        return redirect('addaddress')
    return render(request, 'addaddress.html', locals())

def personalinfo(request):
    try:
        user = User.objects.get(id=request.user.id)
        data = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        data = None
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobilenumber']
        User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile)
        messages.success(request, "Profile updated")
        return redirect('personalinfo')
    return render(request, 'createaccount.html', locals())

def emptycart(request):
    return render(request, 'emptycart.html')

def logouts(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:4]
    return render(request, "product_detail.html", locals())

def cart(request):
    try:
        user = User.objects.get(id=request.user.id)
        data = UserProfile.objects.get(user=user)
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        products = myli['objects'][0]
    except:
        products = []
        print("error")
    return render(request, 'cart.html', locals())

def wishlist(request):
    try:
        user = User.objects.get(id=request.user.id)
        data = UserProfile.objects.get(user=user)
        wish = Whishlist.objects.get(user=request.user)
        product = (wish.product).replace("'", '"')
        mylis = json.loads(str(product))
        product = mylis['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'whishlist.html', locals())

def addToCart(request, pid):
    myli = {"objects": []}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid): 1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('home')

def addwhishlist(request, pid):
    mylis = {"objects": []}
    try:
        wish = Whishlist.objects.get(user=request.user)
        mylis = json.loads((str(wish.product)).replace("'", '"'))
        try:
            mylis['objects'][0][str(pid)] = mylis['objects'][0].get(str(pid), 0) + 1
        except:
            mylis['objects'].append({str(pid): 1})
        wish.product = mylis
        wish.save()
    except:
        mylis['objects'].append({str(pid): 1})
        wish = Whishlist.objects.create(user=request.user, product=mylis)
    return redirect('home')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def deletecart(request, pid):
    cart = Whishlist.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Deleted Successfully")
    return redirect('wishlist')

def wishdeletecart(request, pid):
    wish = Whishlist.objects.get(user=request.user)
    product = (wish.product).replace("'", '"')
    mylis = json.loads(str(product))
    del mylis['objects'][0][str(pid)]
    wish.product = mylis
    wish.save()
    messages.success(request, "Deleted Successfully")
    return redirect('whishlist')

def booking(request):
    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    discounted = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product to cart.")
        return redirect('emptycart')
    for i, j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * float(product.price)
        price = float(product.price) * (100 - float(product.discount)) / 100
        discounted += int(j) * price
        deduction = total - discounted
    if request.method == "POST":
        return redirect('/payment/?total='+str(total)+'&discounted='+str(discounted)+'&deduction='+str(deduction))
    return render(request, "booking.html", locals())

def myorderlist(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, 'myorderlist.html', locals())

def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')

# home/views.py

from django.shortcuts import render
# Other imports...

def payment(request):
    # Your payment logic here
    return render(request, 'home/payment.html')  # Make sure to create this template

