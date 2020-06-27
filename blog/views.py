from django.shortcuts import HttpResponse,render
from django.http import *
from . models import Post,BlogComment,Bookmark
from django.contrib import messages
from blog.templatetags import extras

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

            context={
                'post':post,
                'title':posttitle,
                'pcomments': pcomments,
                'dReply' : dReply,
            }
            return render(request,'blog/mysingleblog.html',context)

    post = Post.objects.filter(slug=slug).first()

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

        if len(desc)==0 or len(posttitle)==0 or len(mytextarea)==0:
            messages.error(request,'All Fields Are Necessary To Be Filled')
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
        return HttpResponseRedirect('/blog/mybooksmarks')

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
        