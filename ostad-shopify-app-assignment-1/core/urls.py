from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.SplashPageView.as_view(), name="splash"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductsView.as_view(), name="products"),
    path("collections/", views.CollectionsListView.as_view(), name="collections_list"),
]
