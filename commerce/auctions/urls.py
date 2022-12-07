from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("select_category", views.select_category, name="select_category"),
    path("listing/<int:id>", views.view_listing, name="view_listing"),
    path("removelist_watchlist/<int:id>", views.removelist_watchlist, name="removelist_watchlist"),
    path("addlist_watchlist/<int:id>", views.addlist_watchlist, name="addlist_watchlist"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("comment_added/<int:id>", views.comment_added, name="comment_added"),
    path("new_bid/<int:id>", views.new_bid, name="new_bid"),
    path("auction_close/<int:id>", views.auction_close, name="auction_close"),
]
