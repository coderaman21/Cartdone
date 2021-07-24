from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='shopHome'),
    path('about/',views.about, name='about us'),
    path('tracker/',views.tracker, name='tracker'),
    path('productview/<int:myid>/',views.productview, name='productview'),
    path('contact/',views.contact, name='contact us'),
    path('checkout/',views.checkout, name='checkout'),
    path('search/',views.search, name='search'),
    path('signin/',views.handlesignin, name='signin'),
    path('signup/',views.handlesignup, name='signup'),
    path('signout/',views.handlesignout, name='signout'),
    
]