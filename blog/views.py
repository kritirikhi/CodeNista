from django.shortcuts import HttpResponse,render
from django.http import *
from . models import Post,BlogComment,Bookmark,PostView
from django.contrib import messages
from blog.templatetags import extras

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
def get_client_ip(request):
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def bloghome(request):
    allposts = Post.objects.all()
    context = {
        'allposts':allposts
    }
    return render(request,'blog/bloghome.html',context)

def blogpost(request,slug):
    if not request.user.is_anonymous:
        post = Post.objects.filter(slug=slug).first()
        if str(request.user)==str(post.author):
            posttitle = post.title 
            posttitle = posttitle.upper()
            pcomments = BlogComment.objects.filter(post=post,parent=None)

            replies = BlogComment.objects.filter(post=post).exclude(parent=None)

            dReply = {}
            for reply in replies:
                if reply.parent.sno not in dReply.keys():
                    dReply[reply.parent.sno] = [reply]
                else:
                    dReply[reply.parent.sno].append(reply)

            ipposts = PostView.objects.filter(post=post)
            context={
                'post':post,
                'title':posttitle,
                'pcomments': pcomments,
                'dReply' : dReply,
                'views' : len(ipposts)
            }
            return render(request,'blog/mysingleblog.html',context)

    
    # get ip address of the user
    ip = get_client_ip(request)
    post = Post.objects.filter(slug=slug).first()

    ipposts = PostView.objects.filter(post=post)

    # calc views on the post
    views=0
    for ippost in ipposts:
        views+=1

    # checking the false views
    ippresent = False
    for ippost in ipposts:
        if ippost.ipaddr==ip:
            ippresent=True 
            break

    if ippresent==False:
        views+=1
        postview = PostView(post=post,ipaddr=ip)
        postview.save()

    posttitle = post.title 
    posttitle = posttitle.upper()
    pcomments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    
    dReply = {}
    for reply in replies:
        if reply.parent.sno not in dReply.keys():
            dReply[reply.parent.sno] = [reply]
        else:
            dReply[reply.parent.sno].append(reply)

    context={
        'post':post,
        'title':posttitle,
        'pcomments': pcomments,
        'dReply' : dReply,
        'views' : views
    }

    return render(request,'blog/blogpost.html',context)

def postcomment(request):
    slug=''
    if request.method=='POST':
        comment = request.POST['comment']
        user = request.user
        postsno = request.POST['sno']
        post = Post.objects.get(sno=postsno)

        slug=post.slug
        parentsno= request.POST['csno']

        if len(comment)==0:
            messages.error(request,"Comment Can't Be Empty")
            return HttpResponseRedirect(f'/blog/{slug}')

        if parentsno=="":
            blogcomment = BlogComment(comment=comment,user=user,post=post)
            blogcomment.save()
            messages.success(request,'Your Comment Has Been Posted')
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            blogcomment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            blogcomment.save()
            messages.success(request,'Your Reply Has Been Posted')

    return HttpResponseRedirect(f'/blog/{slug}')


def postcommentNotuser(request):
    messages.error(request,"Please Login To Comment")
    return HttpResponseRedirect('/')

def createpost(request):
    if request.user.is_anonymous:
        messages.error(request,'Please Login To Create A Post')
        return HttpResponseRedirect('/')
    else:
        return render(request,'blog/createpost.html')

def createpostaction(request):
    if request.method=='POST':
        desc = request.POST['desc']
        posttitle = request.POST['posttitle']
        mytextarea = request.POST['mytextarea']
        if len(posttitle)==0 and len(mytextarea)==0:
            messages.error(request,'Title And Post Content Is Necessary')
            return HttpResponseRedirect('/blog/createpost')
        if len(posttitle)==0:
            messages.error(request,'Title Is Necessary')
            return HttpResponseRedirect('/blog/createpost')
        if len(mytextarea)==0:
            messages.error(request,'Post Content Is Necessary')
            return HttpResponseRedirect('/blog/createpost')
        if len(desc)>300:
            messages.error(request,'description should be brief')
            return HttpResponseRedirect('/blog/createpost')
        if len(posttitle)>255:
            messages.error(request,'Please shorten Your Title')
            return HttpResponseRedirect('/blog/createpost')
        
        t = ""
        for char in posttitle:
            if char != ' ':
                t=t+char
                
        slug = str(request.user) + t
        post = Post(title=posttitle,summary=desc,content=mytextarea,author=request.user,slug=slug)
        post.save()

        messages.success(request,'Your Post Has Been Created')
        return HttpResponseRedirect('/blog/myblogs')

    else:
        return HttpResponse('error')

def myblogs(request):
    if request.user.is_anonymous:
        messages.error(request,'Please Login To View Your Posts')
        return HttpResponseRedirect('/')
    
    else:
        posts = Post.objects.filter(author=request.user)

        context={
            'posts':posts,
        }
        return render(request,'blog/myblogs.html',context)

def updateaction(request):
    if request.method=='POST':
        psno = request.POST['psno']
        post = Post.objects.filter(sno=psno).first()

        context={
            'post':post
        }
        return render(request,'blog/updatepost.html',context)
    else:
        return HttpResponse('error')

def updatedone(request):
    if request.method=='POST':
        title=request.POST['posttitle']
        content=request.POST['mytextarea']
        summary=request.POST['desc']
        psno=request.POST['psno']

        post=Post.objects.get(sno=psno)
        post.title=title
        post.content=content
        post.summary = summary
        post.save()
        return HttpResponseRedirect("/blog/myblogs")
        
    
    else:
        return HttpResponse('error')

def deleteaction(request):
    if request.method=='POST':
        psno = request.POST['psno']
        post = Post.objects.filter(sno=psno).first()

        context={
            'post':post
        }
        return render(request,'blog/deletepost.html',context)
    else:
        return HttpResponse('error')

def deletedone(request):
    if request.method=='POST':
        psno=request.POST['psno']

        post=Post.objects.all().filter(sno=psno)
        post.delete()
        return HttpResponseRedirect("/blog/myblogs")

    else:
        return HttpResponse('error')

def bookmark(request):
    if request.user.is_authenticated:
        user = request.user
        postsno  = request.POST['postsno']

        post = Post.objects.filter(sno = postsno).first()
        bookmark  = Bookmark.objects.filter(post=post,user=request.user)
        print(bookmark)

        if len(bookmark)==0:
            bookmark = Bookmark(post=post,user=user)
            bookmark.save()
            messages.success(request,'bookmark created')
            return HttpResponseRedirect('/blog/mybookmarks')
        else:
            messages.warning(request,'bookmark already exists')
            return HttpResponseRedirect('/blog/mybookmarks')

    else:
        messages.error(request,'please login to bookmark the post')
        return HttpResponseRedirect('/blog/')

def mybookmarks(request):
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(user=request.user)
        context = {
            'bookmarks':bookmarks
        }
        return render(request,'blog/mybookmarks.html',context)


def deletebookmark(request):
    if request.user.is_authenticated:
        booksno = request.POST['booksno']
        
        bookmark=Bookmark.objects.all().filter(booksno = booksno)
        bookmark.delete()
        messages.success(request,'bookmark has been deleted')
        return HttpResponseRedirect("/blog/mybookmarks")
        