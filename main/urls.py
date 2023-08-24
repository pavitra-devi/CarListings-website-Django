from django.urls import path
from . import views
urlpatterns=[
    path("",views.Landing_page,name="Landing_page"),
    path('home/',views.home,name='home_page'),
    path('list/',views.list_view,name='list'),
    path('listing/<str:id>/',views.listing_view,name='listing'),
    path('listing/<str:id>/edit/',views.edit_view,name='edit'),
    path('listing/<str:id>/like/',views.like_listing_view,name='like_listing'),
    path('listing/<str:id>/inquire/',views.inquire_listing_using_email,name='inquire_listing'),

]

