from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
   path('singup/',views.singup,name='singup'),
   path('about/',views.about,name='about'),
   path('service/',views.service,name='service'),
   path('contact/',views.contact,name='contact'),
   path('agency/',views.agency,name='agency'),
   path('logout/',views.logout,name='logout'),
   path('forgot_password/',views.forgot_password,name='forgot_password'),
   path('verify_otp/',views.verify_otp,name='verify_otp'),
   path('update_password/',views.update_password,name='update_password'),
   path('change_password/',views.change_password,name='change_password'),
   path('destinations_detail/<int:pk>/',views.destinations_detail,name='destinations_detail'),
   path('book_destination/<int:pk>/',views.book_destination,name='book_destination'),
   path('pay/',views.initiate_payment, name='pay'),
   path('callback/',views.callback, name='callback'),
   path('mytrip_view/',views.mytrip_view,name='mytrip_view'),
]
