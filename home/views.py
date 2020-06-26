from django.shortcuts import render,HttpResponse
from django.http import *
from . models import Contact
from blog.models import Post,PostView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Count

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
    # return render(request,'home/home.html')
    
 
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
    # messages.error(request,'error')
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
        allposts = allpoststitle.union(allpostscontent)

    context={
        'query':query,
        'allposts':allposts
    }

    if allposts.count()==0:
        messages.warning (request,'No Search Result Found. Please Refine Your Search Query')
    return render(request,'home/search.html',context)


def signupuser(request):
    if(request.method=="POST"):
        signupusername = request.POST['signupusername']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        signupemail = request.POST['signupemail']
        signuppassword = request.POST['signuppassword']
        signuppassword2 = request.POST['signuppassword2']

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

        user1 = User.objects.create_user(signupusername,signupemail,signuppassword)
        user1.first_name = firstname
        user1.last_name = lastname
        user1.save()
        messages.success(request,"Your CodeNista Account Has Been Successfully Created")

        return HttpResponseRedirect('/')

    else:
        return HttpResponse('error 404')

def loginuser(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request,username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"You Are Logged In Successfully")
            return HttpResponseRedirect("/")

        else:
            messages.error(request,"Invalid Username or Password")
            return HttpResponseRedirect("/")

    else:
        return HttpResponse('error')

def logoutuser(request):
    logout(request)
    messages.success(request,"You Are Logged Out")
    return HttpResponseRedirect("/")