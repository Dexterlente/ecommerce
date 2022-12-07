from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category_types = models.CharField(max_length=15)
    def __str__(self):
        return self.category_types

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    
class Listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_price")
    active_listing = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, null=True, related_name="list_watchlist")
    def __str__(self):
        return self.title

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    commented = models.CharField(max_length=300)
    def __str__(self):
        return f"{self.commenter} comment on {self.listing}"

