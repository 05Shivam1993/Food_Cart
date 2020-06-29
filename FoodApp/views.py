from django.shortcuts import render,redirect
from FoodApp.models import Order,Foods,Offers
from django.http import HttpResponse,HttpResponseRedirect
from FoodApp.forms import OrderForm,SignUpForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.db.models import Q
import random
from django.core.mail import send_mail


# Create your views here.
def home(request):
    print(request.user)
    return render(request,'foodapp/home.html')

def vegItems(request):
    return render(request,'foodapp/veg_items.html')

def nonVegItems(request):
    return render(request,'foodapp/non_veg_items.html')

def orderItems(request):
    # del request.session['basket']
    item = request.GET.get('item')
    price = request.GET.get('price')
    if request.session.get('basket'):
        if request.session.get('count'):
            count = request.session['count']
            if request.session['basket'].get(item):
                    pass
            else:
                print("under if")
                count = count + 1
            item_dict = dict()
            item_dict['item'] = item
            item_dict['price'] = price
            request.session['basket'].update({item:item_dict})
            request.session['count'] = count
    else:
        request.session['count'] = 1
        request.session['basket'] = dict()
        item_dict = dict()
        item_dict['item'] = item
        item_dict['price'] = price
        request.session['basket'].update({item:item_dict})
    count = request.session.get('count',0)
    basket = request.session.get('basket')
    return HttpResponse(count)

def cartItems(request):
    total_cost = 0.0
    if request.method == 'POST':
        coupan = request.POST.get('coupan')
        print(coupan)
        if request.session.get('basket'):
            print(request.session['basket'])
            for key in request.session['basket'].keys():
                total_cost += float((request.session['basket'][key]['price'].split('.')[0]).split(' ')[1])
            obj = Offers.objects.get(coupons = coupan)
            discount_percent = 0
            if obj:
                discount_percent = float(obj.percentage)
                if total_cost >= 150:
                    total_cost = total_cost - float(total_cost)*float(discount_percent/100)
                    return render(request,'foodapp/cart.html',{'total_cost':total_cost})
                else:
                    return HttpResponse("<center><h1>Coupan is Applicable on total_cost 150 or above</h1><hr></center>")
    if request.session.get('basket'):
        for key in request.session['basket'].keys():
            total_cost += float((request.session['basket'][key]['price'].split('.')[0]).split(' ')[1])
    return render(request,'foodapp/cart.html',{'total_cost':total_cost})

def cancelOrder(request,id):
    if id:
        order_obj = Order.objects.get(id = id,user_id=request.user)
        item = order_obj.dish_name
        email = order_obj.email
        if order_obj:
            order_obj.delete()
        message = "Hello " + str(request.user) + ", your order of " + "\'"+ item +"\'" + " has been cancelled."
        subject = "Order Cancelled"
        send_mail(subject,message,'shivam.innotical@gmail.com', [email])
    return render(request,'foodapp/cancel_order.html')

def myOrder(request):
    order_list = []
    order_dict = dict()
    try:
        order_qs = Order.objects.filter(user_id = request.user,cancel_order = False,delievery_status=False)
        if order_qs and len(order_qs):
            for order in order_qs:
                order_dict['id'] = order.id
                order_dict['dish_name'] = order.dish_name
                order_dict['quantity'] = order.quantity
                order_dict['cost'] = order.cost
                order_list.append(order_dict)
                order_dict = dict()
        return render(request,'foodapp/my_order.html',{'order_list':order_list})
    except:
        return render(request,'foodapp/my_order.html',{'order_list':order_list})


def deleteItem(request):
    total_cost = 0.0
    item = request.GET.get('item')
    del request.session['basket'][item]
    if request.session.get('basket'):
        for key in request.session['basket'].keys():
            total_cost += float((request.session['basket'][key]['price'].split('.')[0]).split(' ')[1])
    request.session['count'] = request.session['count'] - 1
    return render(request,'foodapp/cart.html',{'total_cost':total_cost})

@login_required
def checkoutForm(request):
    if request.session.get('basket'):
        form = OrderForm()
        kwargs = dict()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                mobile = form.cleaned_data.get('mobile')
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                kwargs['user_id'] = request.user
                kwargs['name'] = name
                kwargs['mobile'] = mobile
                kwargs['email'] = email
                kwargs['address'] = address
                if request.session.get('basket'):
                    item = ''
                    for key,val in request.session['basket'].items():
                        category = 'Veg'
                        kwargs['category'] = 'Veg'
                        kwargs['cost'] = float((val['price']).split()[1])
                        kwargs['dish_name'] = val['item']
                        item += val['item'] + ','
                        today = date.today()
                        kwargs['date'] = today.strftime("%Y") + '-' + today.strftime("%m") + '-' + today.strftime("%d")
                        obj = Order(**kwargs)
                        obj.save()

                    message = "Hello " + str(request.user) + ", your order of " + "\'"+ item +"\'" + " has been received."
                    subject = "Order Received"
                    send_mail(subject,message,'shivam.innotical@gmail.com', [email])
                    del request.session['count']
                    del request.session['basket']
                    return render(request,'foodapp/home.html')
        return render(request,'foodapp/form.html',{'form':form})
    else:
        return render(request,'foodapp/cart.html')

def logout(request):
    return render(request,'registration/logout.html')

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        print(request.POST['username'])
        print(request.POST['email'])
        try:
            user_exist = User.objects.get(Q(username = request.POST['username']) | Q(email = request.POST['email']))
            if user_exist:
                return HttpResponse("<center><h1>Either Username or email already exist !</h1></center>")
        except:
            form = SignUpForm(request.POST)
            user = form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/accounts/login')
    return render(request,'registration/signup.html',{'form':form})

def otp_for_resetPassword(request):
    otp = request.POST.get('otp')
    if otp == request.session.get('otp'):
        return render(request,'foodapp/new_password.html')
    else:
        return HttpResponse("<center><h2>Sorry ! Otp didn't match, Request again and fill the correct one</h2></center>")
    return render(request,'foodapp/otp.html')

def newPassword(request):
    email = request.session.get('email')
    password = request.POST.get('pwd')
    if email:
        try:
            user_obj = User.objects.get(email = email)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('/accounts/login')
        except:
            return HttpResponse("<center><h2>Oop's ! There is some error.</h2></center>")
    else:
        return HttpResponse("<center><h2>Oop's ! There is some error.</h2></center>")

def resetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # password = request.POST.get('pwd')
        print('email',email)
        # print('password',password)
        try:
            user_obj = User.objects.get(email=email)
            print('user_obj',user_obj)
            otp = ''
            for i in range(4):
                otp += str(random.randint(0,9))
            request.session['otp'] = otp
            request.session['email'] = email
            try:
                message = "Hello " + user_obj.username + ", your otp for password reset is " + otp
                subject = "OTP for password reset"
                print(message)
                send_mail(subject,message,'shivam.innotical@gmail.com', [email])
                return render(request,'foodapp/otp.html')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse("Your password has been successfully updated")
        except:
            return HttpResponse(" Please provide the email registered with us !")
    return render(request,'foodapp/reset_password.html')


def contact_us(request):
    if request.method == 'POST':
        name = 'Hello, My name is ' + request.POST['name'] + '.'
        from_email = 'This is my email ' + request.POST['email']
        if request.POST['phone']:
            phone = ' and mobile number ' + request.POST['phone'] + '. '
        else:
            phone = '. '
        message = request.POST['message']
        subject = request.POST['name']
        message = name + from_email + phone + message
        receiver_message = 'Hey ' + request.POST['name'] + ',' + ' We get\'s your mail and will contact you as soon as possible. Enjoy ! '
        try:
            send_mail("From User "+subject, message,'shivam.innotical@gmail.com', ['shivam.hbti05@gmail.com'])
            send_mail('Thanks for contacting us', receiver_message,'shivam.innotical@gmail.com', [request.POST['email']])
            return render(request,'foodapp/thank_you.html')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    return render(request,'foodapp/contact_form.html')


def aboutUs(request):
    return render(request,'foodapp/about.html')


def Food(request):
    import re
    list_of_items = []
    display_list_of_items = []
    if request.method == "POST":
        veg = request.POST.get('veg')
        nonVeg = request.POST.get('nonVeg')
        sweets = request.POST.get('sweets')
        if veg != 'select':
            if veg == 'pulses':
                veg = 'Dal'
            else:
                pass
            list_of_items.append(veg)
        if nonVeg != 'select':
            list_of_items.append(nonVeg)
        if sweets != 'select':
            list_of_items.append(sweets)
        for item in list_of_items:
            print(item)
            qs = list(Foods.objects.filter(category__icontains = item).values('item','price','image'))
            if qs and len(qs):
                display_list_of_items.append(qs)
    return render(request,'foodapp/foods.html',{'item':display_list_of_items})

def offers(request):
    qs = Offers.objects.all()
    offers_list = []
    if qs and len(qs):
        for i in qs:
            offers_dict = dict()
            offers_dict['coupan'] = i.coupons
            offers_dict['applicable'] = i.cost_applicable
            offers_dict['discount'] = i.percentage
            offers_list.append(offers_dict)
    return render(request,'foodapp/offers.html',{'offers':offers_list})
