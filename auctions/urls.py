from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_view, name="create"),
    # path("bid/<int:listing_id>", views.new_bid, name="bid"),
    path("watch", views.watchlist_view, name="watch"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("categories", views.categories, name="categories"),
    path("category/<int:cat_id>", views.category, name="category"),
    path("watchlist/<int:listing_id>", views.watchlist_add, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("success", views.success, name = 'success'),
]