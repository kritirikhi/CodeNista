from django.shortcuts import render,HttpResponse
from django.http import *
from . models import Contact
from blog.models import Post,PostView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile
from .tokens import account_activation_token,account_reset_token
import urllib
import re
import json

def home(request):
    topposts = PostView.objects.values('post').annotate(dcount=Count('post'))[0:4]
    list=[]
    for x in topposts:
        post = Post.objects.filter(sno=x['post']).first()
        list.append(post)

    context = {
        'topposts':list
    }

    return render(request,'home/home.html',context)
 
def about(request):
    posts = Post.objects.all()
    nposts = len(posts)

    nviews = PostView.objects.all().count()
    users = User.objects.all().count()

    context={
        'posts':nposts,
        'views':nviews,
        'users':users
    }
    return render(request,'home/about.html',context)

def contact(request):
    if(request.method=='POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)==0:
            messages.error(request,"Name Is A Required Field")
        
        if len(email)==0:
            messages.error(request,"Email Is A Necessary Field")

        if len(content)<=4:
            messages.error(request,"Add A Valid Issue")

        if len(phone)<10:
            messages.error(request,"Mobile Number Must Be Of 10 Digits")
        
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Message Sent Successfully")
 
    return render(request,'home/contact.html')

def search(request):
    query = request.GET['search']
    if len(query)==0:
        return HttpResponseRedirect('/')

    if len(query)>70:
        allposts=Post.objects.none()
    else:
        allpoststitle = Post.objects.filter(title__icontains=query)
        allpostscontent = Post.objects.filter(content__icontains=query)
        allpostsuser = Post.objects.filter(author__icontains=query)
        allposts = allpoststitle.union(allpostscontent)
        allposts = allposts.union(allpostsuser)

    context={
        'query':query,
        'allposts':allposts
    }

    if allposts.count()==0:
        messages.warning (request,'No Search Result Found. Please Refine Your Search Query')
    return render(request,'home/search.html',context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user1 = Profile.objects.filter(user=user).first()
        user1.verify = True
        user1.save()
        messages.success(request,'Your Account Is Verified Successfully')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')

def signupuser(request):
    if(request.method=="POST"):
        signupusername = request.POST['signupusername']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        signupemail = request.POST['signupemail']
        signuppassword = request.POST['signuppassword']
        signuppassword2 = request.POST['signuppassword2']

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex,signupemail)):  
            messages.error(request,"Please Enter a Valid Email Id")
            return HttpResponseRedirect('/') 

        if User.objects.filter(username=signupusername).exists():
            messages.error(request,"Username Already Taken")
            return HttpResponseRedirect('/')

        if User.objects.filter(email=signupemail).exists():
            messages.error(request,"Email Already Exists")
            return HttpResponseRedirect('/')

        if len(signupusername) > 10:
            messages.error(request,"Username Can't Exceed 10 Characters")
            return HttpResponseRedirect('/')
        
        if not signupusername.isalnum():
            messages.error(request,"Username Must Contain Alphabets And Numbers Only")
            return HttpResponseRedirect('/')

        if signuppassword != signuppassword2:
            messages.error(request,"Passwords Don't Match")
            return HttpResponseRedirect('/')
        
        if len(signuppassword)<8:
            messages.error(request,"Password must have atleast 8 characters")
            return HttpResponseRedirect('/')

        user1 = User.objects.create_user(signupusername,signupemail,signuppassword)
        user1.first_name = firstname
        user1.last_name = lastname
        user1.save()

        profile = Profile(user=user1)
        profile.save()

        user = User.objects.filter(email=signupemail).first()
        current_site = get_current_site(request)
        subject = 'CodeNista Registration Is Confirmed'
        message = render_to_string('home/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [signupemail,]
        send_mail( subject, message, email_from, recipient_list )

        messages.success(request,"Account is created successfully. Kindly verify your account by clicking the link sent to your mail and then login")
        return HttpResponseRedirect('/')

    else:
        return HttpResponse('error 404')

def loginuser(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request,username=loginusername, password=loginpassword)

        if user is not None:
            verifieduser = Profile.objects.filter(user=user).first()
            if(verifieduser.verify==False):
                messages.error(request,"Your Account Is Not Verified")
                return HttpResponseRedirect("/")
            else:
                login(request,user)
                messages.success(request,"You Are Logged In Successfully")
                return HttpResponseRedirect("/")
        else:
            messages.error(request,"Invalid Username or Password")
            return HttpResponseRedirect("/")
    else:
        return HttpResponse('404 error')

def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"You Are Logged Out")
        return HttpResponseRedirect("/")
    else:
        messages.error(request,"Anonymous User")
        return HttpResponseRedirect("/")

def resetpassword(request):
    return render(request,'home/resetpassword.html')

def resetpwdaction(request):
    if(request.method=='POST'):
        email = request.POST['email']

        if len(email)==0:
            messages.error(request,'Type the email in the box')
            return HttpResponseRedirect('/resetpassword')

        user = User.objects.filter(email=email).first()

        if user is not None:        
            current_site = get_current_site(request)
            subject = 'CodeNista Password Reset'
            message = render_to_string('home/acc_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_reset_token.make_token(user),
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail( subject, message, email_from, recipient_list )

            messages.success(request,'mail has been sent to the registered email. Use the link to reset your password')
            return HttpResponseRedirect('/resetpassword')
        else:
            messages.error(request,'Email is not registered')
            return HttpResponseRedirect('/resetpassword')

    else:
        return HttpResonse('404 error')

def resetdone(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_reset_token.check_token(user, token):
        context = {
            'email':user.email
        }
        return render(request,'home/resetpassworddone.html',context)
        
    else:
        return HttpResponse('This link is invalid!')

def resetpwddoneaction(request):
    if request.method=='POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        context = {
            'email':email
        }
        if(str(password) != str(password2)):
            messages.error(request,'Passwords Do Not Match')
            return render(request,'home/resetpassworddone.html',context)
        
        if len(password)==0 or len(password2)==0:
            messages.error(request,'both the fields are necessary to be filled')
            return render(request,'home/resetpassworddone.html',context)
        
        if len(password)<8:
            messages.error(request,'password must have atleast 8 characters')
            return render(request,'home/resetpassworddone.html',context)
 
        else:
            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            messages.success(request,'Your Password Is Reset')
            return HttpResponseRedirect('/')
    
    else:
        return HttpResponse('error')
    

def profilepage(request):
    username=request.GET['username']
    user = User.objects.filter(username=username).first()
    if user is None:
        return HttpResponse("404 Error")
        
    posts = Post.objects.filter(author=username)

    context={
        'posts':posts
    }
    return render(request,'home/profilepage.html',context)