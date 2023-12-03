from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.SplashPageView.as_view(), name="splash"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("collections/", views.CollectionsListView.as_view(), name="collections_list"),
    path(
        "collection/<str:collection_type>/<int:collection_id>/",
        views.CollectionProuctsListView.as_view(),
        name="collection_products_list",
    ),
    path(
        "collection/create/",
        views.CollectionCreateView.as_view(),
        name="collection_create",
    ),
    path(
        "collection/<int:custom_collection_id>/edit/",
        views.CollectionEditView.as_view(),
        name="collection_edit",
    ),
]
