from django.shortcuts import render,redirect
from .models import Tourist,Contact,Destinations,Book_trip,Transaction
from django.core.mail import send_mail
import random
from django.conf import settings
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt


def initiate_payment(request):
    try:
    	print("1")
    	amount = int(request.POST['trip_fees'])
    	tourist = Tourist.objects.get(email=request.session['email'])
    	print("amount : ",amount)
    except:
    	print("2")
    	return render(request, 'trip_fees_payment.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=tourist, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return redirect('index')
    else:
    	return redirect('index')
    	    

def index(request):
	return render(request,'index.html')

def login(request):
	if request.method=="POST":
		try:
			tourist=Tourist.objects.get(
				email=request.POST['email'],
				password=request.POST['password'],
				)
			request.session['fname']=tourist.fname
			request.session['email']=tourist.email
			return render(request,'index.html')
		except:		
			msg="Email Or Password Is Inccorrect !"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')	

def singup(request):
	if request.method=="POST":
		try:
			tourist=Tourist.objects.get(email=request.POST['email'])
			if tourist:
				msg="Email is Already Registered !"
				return render(request,'signup.html',{'msg':msg})
		except:
			if not request.POST['password']==request.POST['cpassword']:
				msg="Password & Confirm Password is Does Not Matched !"
				return render(request,'signup.html',{'msg':msg})
			else:
				Tourist.objects.create(
						fname=request.POST['fname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						password=request.POST['password'],
						cpassword=request.POST['cpassword'],	
					)
				msg="Sign Up Successfully ! "
				return render(request,'login.html',{'msg':msg})
	else:	
		return render(request,'signup.html')

def about(request):
	destinations=Destinations.objects.all()
	return render(request,'about.html',{'destinations':destinations})		

def service(request):
	return render(request,'service.html')	

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks'],
			)
		contacts=Contact.objects.all().order_by('-id')
		msg="Contact Saved Successfully !"
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by('-id')
		return render(request,'contact.html',{'contacts':contacts})	

def agency(request):
	return render(request,'agency.html')	

def logout(request):
	try:
		del request.session['fname']
		del request.session['email']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=Tourist.objects.get(email=request.POST['email'])
			rec=[request.POST['email'],]
			subject="OTP For Forgot Password"
			otp=random.randint(1000,9999)
			massage="Your OTP For Forgot Password Is "+str(otp)+" don't share with anyone"
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,massage,email_from,rec)
			return render(request,'otp.html',{'otp':otp,'email':request.POST['email']})
		except:
			msg="Email Does Not Exists !"
			return render(request,'forgot_password.html',{'msg':msg})	
	else:	
		return render(request,'forgot_password.html')

def verify_otp(request):
	try:
		user=Tourist.objects.get(email=request.POST['email'])
		if request.POST['otp']==request.POST['uotp']:
			return render(request,'new_password.html',{'email':request.POST['email']})
		else:
			msg="OTP Is Inccorrect !"
			return render(request,'otp.html',{'msg':msg,'email':request.POST['email'],'otp':request.POST['otp']})
	except:
		msg="OTP Is Inccorrect !"
		return render(request,'otp.html',{'msg':msg,'email':request.POST['email'],'otp':request.POST['otp']})

def update_password(request):
	try:
		user=Tourist.objects.get(email=request.POST['email'])
		if request.POST['password']==request.POST['cpassword']:
			user.password=request.POST['password']
			user.cpassword=request.POST['cpassword']
			user.save()
			msg="Password Update Successfully !"
			return render(request,'login.html',{'msg':msg})
		else:
			msg="Password & Confirm Password Does Not Matched !"
			return render(request,'new_password.html',{'email':request.POST['email'],'msg':msg})
	except:
		msg="Password & Confirm Password Does Not Matched !"
		return render(request,'new_password.html',{'email':request.POST['email']})

def change_password(request):
	if request.method=="POST":
		user=Tourist.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.cpassword=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password & Confirm Password Does Not Matched !"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg="Old Password Is Inccorrect !"
			return render(request,'change_password.html',{'msg':msg})
	else:
		return render(request,'change_password.html')

def destinations_detail(request,pk):
	destinations=Destinations.objects.get(pk=pk)
	return render(request,'destinations_detail.html',{'destinations':destinations}) 

def book_destination(request,pk):
	tourist=Tourist.objects.get(email=request.session['email'])
	destinations=Destinations.objects.get(pk=pk)
	if request.method=="POST":
		book_trip=Book_trip.objects.create(
			destinations=destinations, 
			tourist=tourist,
			trip_date=request.POST['trip_date'],
			adult=request.POST['adult'],
			)
		print(book_trip)
		return render(request,'trip_fees_payment.html',{'book_trip':book_trip})
	else:
		return render(request,'book_destination.html',{'tourist':tourist,'destinations':destinations})	 


def mytrip_view(request):
	tourist=Tourist.objects.get(email=request.session['email'])
	book_trip=Book_trip.objects.filter(tourist=tourist)
	return render(request,'mytrip_view.html',{'book_trip':book_trip})


