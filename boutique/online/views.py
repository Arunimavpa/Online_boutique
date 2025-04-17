from datetime import timedelta,date
from django.conf import settings
import razorpay
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot import get_answer
import re

razorpay_client = razorpay.Client(auth=('rzp_test_9zruMnoLDlsCLG','oXUZ9Mf5zhjoZsTFLc7RpABO'))

def home(request):
    pdt=tbl_Product.objects.all().order_by("-id")
    pdt1 = tbl_Product.objects.all()
    return render(request,'home.html',{"pdt":pdt,"pdt1":pdt1})
def Login(request):
    return render(request,'Login.html')
def check_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/dashboard/")
        elif tbl_Register.objects.filter(email=username,password=password).exists():
            g=tbl_Register.objects.get(email=username,password=password)
            request.session['userid']=g.id
            v=tbl_Cart.objects.filter(session_key=request.session.session_key)
            for i in v:
                i.user_id=g.id
                i.session_key=""
                i.save()
            return redirect("/cart/view/")
        else:
            return redirect("/Login")
def dashboard(request):
    return render(request,"dashboard.html")

def category_add(request):
    return render(request,"category_add.html")

def save_category(request):
    if request.method == "POST":
        obj = tbl_category_add()
        print(request.FILES.get("image"),"jj")
        obj.name=request.POST.get("name")
        obj.status=request.POST.get("status")
        obj.image=request.FILES.get("image")
        obj.save()
        return redirect("/category_add/")
def category_list(request):
    data = tbl_category_add.objects.all()
    return render(request,"category_list.html", {"data": data})

def edit_category(request,id):
    data=tbl_category_add.objects.get(id=id)
    return render(request,"edit_category.html",{"data":data})

def update_category(request,id):
    data=tbl_category_add.objects.get(id=id)
    data.name=request.POST.get("name")
    data.status=request.POST.get("status")
    image=request.FILES.get("image")
    if image:
        data.image=image
    data.save()
    return redirect("/category_list/")

def delete_category(request,id):
    data=tbl_category_add.objects.get(id=id)
    data.delete()
    return redirect("/category_list/")

def filter_active(request):
    data=tbl_category_add.objects.filter(status="Active")
    return render(request,"category_list.html",{"data":data})

def filter_inactive(request):
    data=tbl_category_add.objects.filter(status="Inactive")
    return render(request,"category_list.html",{"data":data})

def product_add(request):
    category=tbl_category_add.objects.all()
    return render(request,"product_add.html",{"category":category})


def save_product(request):
    if request.method=="POST":
        obj=tbl_Product()
        obj.name=request.POST.get("name")
        obj.image=request.FILES.get("image")
        obj.product_id=request.POST.get("product_id")
        obj.stock=request.POST.get("stock")
        obj.color=request.POST.get("color")
        obj.category_id=request.POST.get("category")
        obj.offer_price=request.POST.get("offer_price")
        obj.original_price=request.POST.get("original_price")
        obj.description=request.POST.get("description")
        obj.fabric = request.POST.get("fabric")
        obj.Pattern = request.POST.get("pattern")
        obj.WashCare = request.POST.get("WashCare")
        sizes = request.POST.getlist("size[]")
        size_str = ", ".join(sizes) if sizes else None
        obj.size = size_str
        obj.save()
        return redirect("/product_add/")

def product_list(request):
    data=tbl_Product.objects.all()
    return render(request,"product_list.html",{"data":data})

def edit_product(request,id):
    data=tbl_Product.objects.get(id=id)
    sizes = ["Free Size", "xxl", "xl", "l", "m", "s", "xs"]
    selected_sizes = data.size
    return render(request,"edit_product.html",{"data":data,"sizes":sizes,"selected_sizes":selected_sizes})

def update_product(request,id):
    obj=tbl_Product.objects.get(id=id)
    obj.name = request.POST.get("name")
    obj.product_id = request.POST.get("product_id")
    obj.vendor = request.POST.get("vendor")
    obj.stock = request.POST.get("stock")
    obj.category_id = request.POST.get("category")
    obj.offer_price = request.POST.get("offer_price")
    obj.original_price = request.POST.get("original_price")
    obj.description = request.POST.get("description")
    obj.fabric = request.POST.get("fabric")
    obj.Pattern = request.POST.get("pattern")
    obj.WashCare = request.POST.get("WashCare")
    sizes = request.POST.getlist("size[]")
    size_str = ", ".join(sizes) if sizes else None
    obj.size = size_str
    image = request.FILES.get("image")
    if image:
        obj.image = request.FILES.get("image")
    obj.save()
    return redirect("/product_list/")


def delete_product(request,id):
    obj=tbl_Product.objects.get(id=id)
    obj.delete()
    return redirect("/product_list/")


def add_product_variant(request,id):
    data=tbl_Product.objects.get(id=id)
    return render(request,"add_product_variant.html",{"data":data})


def save_product_variant(request,id):
    if request.method=="POST":
        obj=tbl_ProductVariant()
        obj.product_id = id
        obj.image=request.FILES.get("image")
        obj.color=request.POST.get("color")
        obj.save()
        return redirect("view_product_variant",id=id)
def view_product_variant(request,id):
    data1=tbl_Product.objects.get(id=id)
    data=tbl_ProductVariant.objects.filter(product=id)
    return render(request,"view_product_variant.html",{"data":data,"data1":data1})

def edit_product_variant(request,id):
    data=tbl_ProductVariant.objects.get(id=id)
    return render(request,"edit_product_variant.html",{"data":data})


def update_product_variant(request,id):
    obj = tbl_ProductVariant.objects.get(id=id)
    obj.product_id = obj.product.id
    obj.color = request.POST.get("color")
    image = request.FILES.get("image")
    if image:
        obj.image = request.FILES.get("image")
    obj.save()
    return redirect("view_product_variant",id=obj.product.id)

def product(request):
    data=tbl_Product.objects.all()
    return render(request,"product.html",{"data":data})

def cart_add(request, id):
    data = tbl_Product.objects.get(id=id)
    size_selected = request.POST.get("size")
    color_selected = request.POST.get("color")
    id1 = request.POST.get("image")
    print(color_selected,id1)

    if id1:
        table_id=tbl_ProductVariant.objects.get(id=id1)

    if request.POST.get("default_color"):
        table_id=data
        color_selected=data.color

    try:
        user = request.session['userid']
        cart, created = tbl_Cart.objects.get_or_create(
            product_id=id, user_id=user, size=size_selected, color=color_selected  # ✅ Save color
        )
        if not created:
            cart.quantity += 1
            cart.save()
        else:
            cart.quantity = 1
            if id1:
                cart.image=table_id.image.url
            cart.save()
        return redirect("/cart/view/")

    except:
        session_key = request.session.session_key
        if not session_key:
            session_key = request.session.create()
        cart, created = tbl_Cart.objects.get_or_create(
            product_id=id, session_key=session_key, size=size_selected, color=color_selected  # ✅ Save color
        )
        if not created:
            cart.quantity += 1
            cart.save()
        else:
            cart.quantity = 1
            if id1:
                cart.image = table_id.image.url
            cart.save()
        return redirect("/cart/view/")


def cart_view(request):
    try:

        user = request.session.get('userid')
        cart_items = tbl_Cart.objects.filter(user=user)
    except:

        session_key = request.session.session_key
        cart_items = tbl_Cart.objects.filter(session_key=session_key)

    cart_total = sum(item.total_price() for item in cart_items)

    return render(request, "cart_view.html", {"cart_items": cart_items, "cart_total": cart_total})




def update_cart(request):
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        quantity = int(request.POST.get("quantity"))

        cart_item = tbl_Cart.objects.get(id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()

        # Recalculate cart total
        cart_items = tbl_Cart.objects.filter(session_key=request.session.session_key)
        if not cart_items:
            cart_items = tbl_Cart.objects.filter(user=request.session['userid'])
        cart_total = sum(i.total_price() for i in cart_items)
        return JsonResponse({"cart_total": cart_total})

def checkout(request):
    try:
        cart_items = tbl_Cart.objects.filter(user=request.session['userid'])
        cart_total = sum(i.total_price() for i in cart_items)

        currency = 'INR'
        amount = int(cart_total) * 100
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'save_checkout'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = 'rzp_test_9zruMnoLDlsCLG'
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['cart_total']=cart_total
        context['cart_items']=cart_items
        return render(request,"checkout.html",context)
    except:
        return redirect("/Login/")
def save_contact(request):
    data=tbl_contact()
    data.Name = request.POST.get('name')
    data.phone_no = request.POST.get('phoneno')
    data.email = request.POST.get('email')
    data.message = request.POST.get('message')
    data.save()
    return redirect('/')

def save_checkout(request):
    cart_items = tbl_Cart.objects.filter(user=request.session['userid'])
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        phone = request.POST.get("phone")


        if not cart_items.exists():
            return redirect("/cart/view/")  # Redirect if cart is empty

        # Create Order
        order = Order.objects.create(
            user_id=request.session['userid'],
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total_price=sum(item.product.offer_price * item.quantity for item in cart_items),
            status="Ordered"
        )

        # Create Order Items and clear the cart
        for item in cart_items:

            c=OrderItem()
            c.order=order
            c.product=item.product
            c.quantity=item.quantity
            c.price=item.product.offer_price * item.quantity
            if item.color:
                c.color=item.color
            if item.size:
                c.size=item.size
            if item.image:
                c.image=item.image
            c.save()

            stock_udt=tbl_Product.objects.get(id=item.product.id)
            stock_udt.stock-=int(item.quantity)
            stock_udt.save()
            item.delete()
        razorpay_order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        # verify the payment signature.
        cart_total=sum(i.total_price() for i in cart_items)
        amount = int(cart_total) *100  # Rs. 200
        razorpay_client.payment.capture(payment_id, amount)


    return redirect("/")


def register(request):
    return render(request,"register.html")


def save_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate required fields
        if not full_name or not email or not phone_no or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('/register/')

        # Validate email format using regex
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            messages.error(request, "Invalid email address format.")
            return redirect('/register/')

        # Validate phone number (must be digits and 10 or more characters)
        if not phone_no.isdigit() or len(phone_no) < 10:
            messages.error(request, "Phone number must be at least 10 digits long.")
            return redirect('/register/')

        # Validate password (must be at least 6 characters)
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('/register/')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register/')

        # Check if email is already registered
        if tbl_Register.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('/register/')

        # Save the new registration to the database
        data = tbl_Register()
        data.name = full_name
        data.email = email
        data.mobile = phone_no
        data.password = password  # Make sure to hash the password before storing it!
        data.save()

        # Redirect to login page after successful registration
        messages.success(request, "Registration successful! Please log in.")
        return redirect('/Login/')

    return render(request, 'register.html')  # If the request method is not POST, show the form




def remove_from_cart(request,id):
    data=tbl_Cart.objects.get(id=id)
    data.delete()
    return redirect("/cart/view/")


def my_orders(request):
    data=Order.objects.filter(user=request.session['userid'])
    return render(request,"my_orders.html",{"data":data})


def my_profile(request):
    data=tbl_Register.objects.get(id=request.session['userid'])
    return render(request,"my_profile.html",{"data":data})

def Logout(request):
    del request.session['userid']
    return redirect("/")


def buy(request, id):
    d = tbl_Product.objects.get(id=id)
    sizes = d.size.split(", ") if d.size else []  # Ensure it's a list
    colors = tbl_ProductVariant.objects.filter(product=id)
    return render(request, "buy.html", {"d": d, "size": sizes, "colors": colors})

def forgot_password(request):
    return render(request,"forgot_password.html")

def check_password(request):
    email=request.POST.get("email")
    if tbl_Register.objects.filter(email=email).exists():
        data=tbl_Register.objects.get(email=email)
        subject = "Password Reset Link"
        reset_link = f"http://127.0.0.1:8000/reset_password/{data.id}"
        message = f"""
            <h1>Password Reset</h1>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}">{reset_link}</a>
        """
        send_mail(
            subject,
            "Click the link to reset your password",  # Plain text version (fallback)
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=message,  # HTML email content
        )

        messages.success(request, "Check your registered email for the reset link.")
        return redirect("/forgot_password/")
    else:
        messages.error(request, "Please Enter Registered Email-Id")
        return redirect("/forgot_password/")

def view_items(request,id):
    data=OrderItem.objects.filter(order=id)
    data1=Order.objects.get(id=id)
    order_date=data1.created_at
    expected_date=order_date + timedelta(days=7)
    return  render(request,"view_items.html",{"data":data,"data1":data1,"expected_date":expected_date})


def track_order(request,id):
    data=Order.objects.get(id=id)

    return render(request,"track_order.html",{"data":data})

def Logout_admin(request):
    return redirect("/")

def order_list(request):
    data=Order.objects.all()
    return render(request,"order_list.html",{"data":data})

def view_orders(request,id):
    data1=Order.objects.get(id=id)
    data= OrderItem.objects.filter(order=id)
    order_date = data1.created_at
    expected_date = order_date + timedelta(days=7)
    return render(request,"view_orders.html",{"data1":data1,"data":data,"expected_date":expected_date})

def view_cust_order(request,id):
    data1=Order.objects.get(id=id)
    data= OrderItem.objects.filter(order=id)
    order_date = data1.created_at
    expected_date = order_date + timedelta(days=7)
    return render(request,"view_cust_order.html",{"data1":data1,"data":data,"expected_date":expected_date})

def cust_invoice(request,id):
    data=CustomDressOrder.objects.filter(order=id)
    data1=CustomDressOrder.objects.get(id=id)
    return render(request,"cust_invoice.html",{"data":data,"data1":data1})

def invoice(request,id):
    data=OrderItem.objects.filter(order=id)
    data1=Order.objects.get(id=id)
    return render(request,"invoice.html",{"data":data,"data1":data1})

def user_list(request):
    data=tbl_Register.objects.all()
    return render(request,"user_list.html",{"data":data})

def customization(request):
    return render(request, "customization.html")

def save_custom(request):
    if request.method == 'POST':
        dress_name = request.POST.get('dressModel')
        fabric = request.POST.get('fabric')
        color = request.POST.get('color-text')
        size = request.POST.get('size')
        neck_design = request.POST.get('neck')
        custom_neck_design = request.POST.get('custom-neck', '')  # Default empty
        bust = request.POST.get('bust')
        waist = request.POST.get('waist')
        hips = request.POST.get('hips')
        length = request.POST.get('length')
        delivery_date = request.POST.get('delivery-date')
        reference_image = request.FILES.get('reference')
        additional_details = request.POST.get('details', '')

        # Save data to the model
        CustomDressOrder.objects.create(
            user_id=request.session['userid'],
            dress_name=dress_name,
            fabric=fabric,
            color=color,
            size=size,
            neck_design=neck_design,
            custom_neck_design=custom_neck_design,
            bust=bust,
            waist=waist,
            hips=hips,
            length=length,
            delivery_date=delivery_date,
            reference_image=reference_image,
            additional_details=additional_details,
            status="Pending",
            work_status="Pending"
        )

        return redirect('/')  # Redirect after successful submission
def cust_products(request):
    data=CustomDressOrder.objects.filter(user=request.session['userid'])
    return render(request,"cust_products.html",{"data":data})


def customized_orders(request):
    data=CustomDressOrder.objects.all()
    return render(request,"customized_orders.html",{"data":data})


def approve_custom_order(request,id):
    data=CustomDressOrder.objects.get(id=id)

    return render(request,"approve_custom_order.html",{"data":data})


def reject_custom_order(request,id):
    data=CustomDressOrder.objects.get(id=id)
    data.status="Reject"
    data.save()
    return redirect("/customized_orders/")


def completed_list(request):
    data=Order.objects.filter(status="Ordered")
    return render(request,"completed_list.html",{"data":data})



def update_cart_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        action = request.POST.get("action")

        cart_item = get_object_or_404(tbl_Cart, id=item_id)

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

        try:
            cart_total = sum(item.quantity * item.product.offer_price for item in tbl_Cart.objects.filter(user=request.session['userid']))
            item_total_price = cart_item.quantity * cart_item.product.offer_price
        except:
            cart_total = sum(item.quantity * item.product.offer_price for item in tbl_Cart.objects.filter(session_key=request.session.session_key))
            item_total_price = cart_item.quantity * cart_item.product.offer_price

        return JsonResponse({
            "status": "success",
            "new_quantity": cart_item.quantity,
            "cart_total": cart_total,
            "item_total_price": item_total_price,
        })

    return JsonResponse({"status": "error"}, status=400)

def reset_password(request,id):
    data=tbl_Register.objects.get(id=id)
    return render(request,"reset_password.html",{"data":data})


def update_password(request,id):
    if request.method=="POST":
        new_password=request.POST.get("password")
        data=tbl_Register.objects.get(id=id)
        data.password=new_password
        data.save()
        return redirect("/Login/")
    else:
        return redirect("reset_password",id=id)


def enquiries(request):
    data=tbl_contact.objects.all()
    return render(request,"enquiries.html",{"data":data})


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get("query", "")
            response = get_answer(user_query)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Send a POST request with 'query' parameter."})


@csrf_exempt
def update_order_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("status")
            if new_status == "Delivered":
                order = Order.objects.get(id=order_id)
                order.status = new_status
                order.d_date=date.today()
                order.save()
            elif new_status == "Processing":
                order = Order.objects.get(id=order_id)
                order.status = new_status
                order.p_date=date.today()
                order.save()

            return JsonResponse({"success": True, "message": "Order status updated."})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def about(request):
    return render(request,"about.html")



def view_custom_order(request, id):
    try:
        # Fetch the order using the provided id
        data1 = CustomDressOrder.objects.get(id=id)
        currency = 'INR'
        amount = int(data1.advance) * 100
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'save_advance'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = 'rzp_test_9zruMnoLDlsCLG'
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['data1'] = data1
        return render(request, "view_custom_order.html", context)
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        data1 = None
        return render(request, 'view_custom_order.html', {'data1': data1})

def save_approved_cost(request,id):
    data=CustomDressOrder.objects.get(id=id)
    data.status="Approved"
    data.total_cost=request.POST.get("total_cost")
    data.advance=request.POST.get("advance")
    data.payment_status="Pending"
    data.save()
    return redirect("/customized_orders/")


def save_advance(request,id):
    data=CustomDressOrder.objects.get(id=id)
    data.payment_status="Completed"
    data.save()
    razorpay_order_id = request.POST.get('order_id')
    payment_id = request.POST.get('payment_id', '')
    print(payment_id,"payment_id")
    signature = request.POST.get('razorpay_signature', '')
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    # verify the payment signature.
    amount = int(data.advance) * 100  # Rs. 200
    razorpay_client.payment.capture(payment_id, amount)
    return redirect("/cust_products/")


def update_work_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("status")
            if new_status == "Delivered":
                order = CustomDressOrder.objects.get(id=order_id)
                order.work_status = new_status
                order.save()
            elif new_status == "Processing":
                order = CustomDressOrder.objects.get(id=order_id)
                order.work_status = new_status
                order.save()

            return JsonResponse({"success": True, "message": "Order status updated."})
        except CustomDressOrder.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def view_remain_order(request,id):
    try:
        # Fetch the order using the provided id
        data1 = CustomDressOrder.objects.get(id=id)
        balance=data1.total_cost-data1.advance
        currency = 'INR'
        amount = int(balance) * 100
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'save_full_payment'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = 'rzp_test_9zruMnoLDlsCLG'
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['data1'] = data1
        context['balance']=balance
        return render(request, "view_remain_order.html", context)
    except Order.DoesNotExist:
        # Handle the case where the order does not exist
        data1 = None
        return render(request, 'view_remain_order.html', {'data1': data1})

def save_full_payment(request,id):
    data=CustomDressOrder.objects.get(id=id)
    data.payment_status="Full Payment Completed"
    data.save()
    balance=data.total_cost-data.advance
    razorpay_order_id = request.POST.get('order_id')
    payment_id = request.POST.get('payment_id', '')
    print(payment_id,"payment_id")
    signature = request.POST.get('razorpay_signature', '')
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    # verify the payment signature.
    amount = int(balance) * 100  # Rs. 200
    razorpay_client.payment.capture(payment_id, amount)
    return redirect("/cust_products/")
