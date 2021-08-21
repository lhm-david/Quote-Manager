from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('success',views.success),
    path('addquote', views.addquote),
    path('addlikes/<int:quote_id>',views.like),
    path('user/<int:user_id>',views.userprofile),
    path('delete/<int:quote_id>', views.delete),
    path('myaccount/<int:user_id>',views.editaccount),
    path('myaccount/<int:user_id>/update', views.updateuserprofile),
    path('logout',views.logout)
]
