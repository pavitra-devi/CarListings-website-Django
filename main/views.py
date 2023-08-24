from imp import reload
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from . models import Listing,LikedListing
from . forms import ListingForm
from users.forms import LocationForm
from .filters import ListingFilter   
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.

def Landing_page(request):
    return render(request,'main/home.html',{'name':'pavi'})


@login_required
def home(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET,queryset=listings)
    context ={'listing_filter':listing_filter}
    return render(request,'main/home2.html',context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST,request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid and location_form.is_valid():
                listing = listing_form.save(commit= False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(request,f"{listing.model} Listing posted Successfully")
                return redirect('home_page')
            else:
                raise Exception()

        except Exception as e:
            print(e)
            messages.error(request,'An error occured while posting Listing')


    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request,'main/list.html',{'listing_form':listing_form,'location_form':location_form})


@login_required
def listing_view(request,id):
    try:
        listing = Listing.objects.get(id =id)
        if listing is None:
            raise Exception
        return render(request,'main/listing.html',{'listing':listing})
    except Exception as e:
        messages.error(request,f'Invalid Uid {id} was provided for the listing')
        return redirect('home_page')


@login_required
def edit_view(request,id):
    try:

        listing = Listing.objects.get(id =id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST,request.FILES,instance=listing)
            location_form = LocationForm(request.POST,instance=listing.location)
            if listing_form.is_valid and location_form.is_valid:
                listing_form.save()
                location_form.save()
                messages.info(request,f"Listing {id} updated successfully")
                return redirect('home_page')
            else:
                messages.error(request,f'An error occurred while editing  the listing')
                return reload()
            
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            context={
                'listing_form':listing_form,
                "location_form":location_form
                }
             
        return render(request,'main/edit.html',context)
    except Exception as e:
        messages.error(request,f'An error occurred while editing  the listing')
        return redirect('home_page')


@login_required
def like_listing_view(request,id):
    listing = get_object_or_404(Listing,id=id)
    liked_listing,created = LikedListing.objects.get_or_create(
        profile=request.user.profile,listing=listing)
    
    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()
    return JsonResponse({'is liked by user ':created })



@login_required
def inquire_listing_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.username} is interested in {listing.model}'
        emailMessage = f'Hi {listing.seller.user.username}, {request.user.username} is interested in your {listing.model} listing on AutoMax'
        send_mail(emailSubject, emailMessage, 'noreply@automax.com',
                  [listing.seller.user.email, ], fail_silently=True)
        messages.info(request,'Mail sent sucessfully')
        return redirect('home_page')
    
    except Exception as e:
        print(e)
        messages.error(request,"unable to send mail try again later")
        return redirect('home_page')

        