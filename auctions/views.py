from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum

from . models import User, Category, Listing, Watchlist, Bid
from . forms import ListingForm, BidForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
       'listings' : listings 
    })

@login_required
def create_view(request):
    if request.method == 'POST': 
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            listing_id = form 
        form = (Bid, BidForm(request.POST), request.FILES)
        if form.is_valid(): 
            b = form
            b.listing_id = Listing.objects.get(pk=listing_id)
            b.user=request.user
            b.save()      
            return redirect('index') 
    else: 
        form = ListingForm() 
        return render(request, 'auctions/createform.html', {'form' : form}) 


@login_required
def watchlist_view(request):
    listings = Listing.objects.all().filter(watchlist__username=request.user, watchlist__in_watchlist=True)
    return render(request, "auctions/index.html", {
        'listings' : listings
        })


@login_required
def categories(request):    
    categories = Category.objects.all()
    print(categories)
    return render(request, "auctions/categories.html", {
        'categories' : categories
        })


@login_required
def category(request, cat_id):  
    listings = Listing.objects.all().filter(cat_id=cat_id)
    return render(request, "auctions/index.html", {
        'listings' : listings
        })


@login_required
def watchlist_add(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    wl, created = Watchlist.objects.get_or_create(
        username=request.user,
        listing_id = listing,
        defaults={'in_watchlist': True},
    )

    if created:
        print("The record didn't exist")
    else:
        if wl.in_watchlist == False:
            wl.in_watchlist = True
        else:
            wl.in_watchlist = False
    wl.save()

    return redirect('listing', listing_id=listing_id)


@login_required
def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.listing_owner == request.user and listing.listing_open == True:
        listing.listing_open =False
        listing.save()

    return redirect('listing', listing_id=listing_id)
 

def listing_view(request, listing_id):
    in_wl = False
    owner = False
    can_close = False
    try:
        listing = Listing.objects.get(pk=listing_id)
           
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    
    try:
        watchlist = Watchlist.objects.get(username=request.user, listing_id=listing_id)
        in_wl = watchlist.in_watchlist

    except Watchlist.DoesNotExist:
        in_wl = False

    listing=Listing.objects.get(pk=listing_id)
    print('listing: ',listing)
    print('listing.listing_owner: ', listing.listing_owner)
    
    category = Category.objects.get(cat_name=listing.cat_id)
    print('category: ', category.cat_name)
    
    print('request.user: ', request.user)
    print('listing.listing_open: ', listing.listing_open)
    if listing.listing_owner == request.user and listing.listing_open == True:
        owner = True
        can_close = True
    
    print('owner: ', owner)
    print('can_close: ', can_close)

    bid_max = Bid.objects.all().filter(listing_id=listing_id).aggregate(Max('user_bid'))
    print('bid_max: ', bid_max)

    highest_bid = bid_max['user_bid__max']
    if highest_bid == None:
        highest_bid = 0
    print('highest bid: ', highest_bid)
    
    your_actual_max = Bid.objects.all().filter(listing_id=listing_id, user=request.user).aggregate(Max('user_bid'))
    print('your_actual_max: ', your_actual_max)
    
    your_bid = your_actual_max['user_bid__max']
    if your_bid == None:
        your_bid = 0
    print('your bid:', your_bid)

    bid_count = Bid.objects.all().filter(listing_id=listing_id).count()
    print('bid count: ', bid_count)

    message =''

    if request.method == 'POST': 
            form = BidForm(request.POST, request.FILES)

            if form.is_valid(): 
                b = form.save(commit=False)
                b.bid_at = datetime.now()
                b.listing_id = Listing.objects.get(pk=listing_id)
                b.user=request.user
                b.bid_status =True
                if highest_bid < b.user_bid:
                    b.save()
                    highest_bid = b.user_bid
                    return render(request,'auctions/listing.html', {
                        "listing": listing,
                        "bid_count": bid_count,
                        "your_bid": your_bid,
                        "in_wl" : in_wl,
                        "form" : form,
                        "message" : message,
                        "owner": owner,
                        "can_close" : can_close,
                        "category" : category.cat_name,
                        }) 
                else:
                    message = 'Bid is lower than actual bid'
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "bid_count": bid_count,
                        "your_bid": your_bid,
                        "in_wl" : in_wl,
                        "form" : form,
                        "message" : message,
                        "owner": owner,
                        "can_close" : can_close,
                        "category" : category.cat_name,
                    })
    else:    
        form = BidForm()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_count": bid_count,
            "your_bid": your_bid,
            "in_wl" : in_wl,
            "form" : form,
            "message" : message,
            "owner": owner,
            "can_close" : can_close,
            "category" : category.cat_name,
            })


def success(request): 
    return HttpResponse('successfully uploaded') 


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")