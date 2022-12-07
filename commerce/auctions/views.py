from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comment, Bid

def index(request):
    #Render Active Listings
    current_listings = Listing.objects.filter(active_listing=True)
    listed_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "list": current_listings,
        "categories": listed_categories
    })

def select_category(request):
    #Filtering categories
    if request.method == "POST":
        given_category = request.POST['category']
        category = Category.objects.get(category_types=given_category)
        current_listings = Listing.objects.filter(active_listing=True, category=category)
        listed_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "list": current_listings,
            "categories": listed_categories
        })

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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.POST['photo']
        category = request.POST['category']
        logged_user = request.user
        all_categories = Category.objects.get(category_types=category)
        bid = Bid(bid=int(price), user=logged_user)
        bid.save()
        created_listing = Listing(
            title=title,
            description=description,
            price = bid,
            image=image,
            seller=logged_user,
            category=all_categories           
        )
        created_listing.save()
        return HttpResponseRedirect(reverse(index))

    else:
        listed_categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": listed_categories
        })

def view_listing(request, id):
    listing_id = Listing.objects.get(pk=id)
    list_watchlist = request.user in listing_id.watchlist.all()
    all_comment = Comment.objects.filter(listing=listing_id)
    seller = request.user.username == listing_id.seller.username
    return render(request, "auctions/view_listing.html", {
        "listing": listing_id,
        "list_watchlist": list_watchlist,
        "all_comment": all_comment,
        "seller": seller
    })

def removelist_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    logged_user = request.user
    listing_data.watchlist.remove(logged_user)
    return HttpResponseRedirect(reverse("view_listing",args=(id, )))
    
def addlist_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    logged_user = request.user
    listing_data.watchlist.add(logged_user)
    return HttpResponseRedirect(reverse("view_listing",args=(id, )))

def display_watchlist(request):
    logged_user= request.user
    listings = logged_user.list_watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "list": listings
    }) 


def new_bid(request, id):
    bidding = request.POST['new_bid']
    listing_data = Listing.objects.get(pk=id)
    list_watchlist = request.user in listing_data.watchlist.all()
    seller = request.user.username == listing_data.seller.username
    all_comment = Comment.objects.filter(listing=listing_data)
    if int(bidding) > listing_data.price.bid:
        updated_bid = Bid(user=request.user, bid=int(bidding))
        updated_bid.save()
        listing_data.price = updated_bid
        listing_data.save()
        return render(request, "auctions/view_listing.html", {
            "listing": listing_data,
            "message": "Bidding Success",
            "update": True,
            "list_watchlist": list_watchlist,
            "all_comment": all_comment,
            "seller": seller
        })
    
    else:
        return render(request, "auctions/view_listing.html", {
            "listing": listing_data,
            "message": "Bidding Fail",
            "update": False,
            "listwatchlist": list_watchlist,
            "all_comment": all_comment,
            "seller": seller
        })

def auction_close(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.active_listing = False
    listing_data.save()
    seller = request.user.username == listing_data.seller.username
    all_comment = Comment.objects.filter(listing=listing_data)
    list_watchlist = request.user in listing_data.watchlist.all()
    return render(request, "auctions/view_listing.html", {
        "listing": listing_data,
        "message": "Your Auction Item Was Closed",
        "update": True,
        "list_watchlist": list_watchlist,
        "all_comment": all_comment,
        "seller": seller
        })

def comment_added(request, id):
    current_user = request.user
    listing = Listing.objects.get(pk=id)
    commented = request.POST['comment_added']

    final_comment = Comment(
        commenter=current_user,
        listing=listing,
        commented=commented
    )
    final_comment.save()
    return HttpResponseRedirect(reverse("view_listing",args=(id, )))
