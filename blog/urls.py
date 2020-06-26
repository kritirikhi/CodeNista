from django.urls import path,include 
from . import views

urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('postcomment',views.postcomment,name='postcomment'),
    path('myblogs',views.myblogs,name='myblogs'),
    path('bookmark',views.bookmark,name='bookmark'),
    path('mybookmarks',views.mybookmarks,name='mybookmarks'),
    path('deletebookmark',views.deletebookmark,name='deletebookmark'),
    path('createpost',views.createpost,name='createpost'),
    path('createpostaction',views.createpostaction,name='createpostaction'),
    path('postcommentNotuser',views.postcommentNotuser,name='postcommentNotuser'),
    path('updateaction',views.updateaction,name='updateaction'),
    path('deleteaction',views.deleteaction,name='deleteaction'),
    path('deletedone',views.deletedone,name='deletedone'),
    path('updatedone',views.updatedone,name='updatedone'),
    path('<str:slug>',views.blogpost,name='blogpost')
]
