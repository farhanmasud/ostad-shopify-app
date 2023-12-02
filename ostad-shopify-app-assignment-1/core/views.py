import shopify
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect, render
from django.views import generic
from pyactiveresource.connection import UnauthorizedAccess
from shopify_auth.session_tokens.views import get_scope_permission
from accounts.models import Account


class SplashPageView(generic.View):
    template_name = "core/splash.html"

    def get(self, request):
        myshopify_domain = request.GET.get("shop")
        encoded_host = request.GET.get("host")

        if not myshopify_domain:
            return render(
                request,
                "shopify_auth/login.html",
                {},
            )
        try:
            shop = Account.objects.get(myshopify_domain=myshopify_domain)
        except Account.DoesNotExist:
            return get_scope_permission(request, myshopify_domain)

        with shop.session:
            try:
                shopify_shop = shopify.Shop.current()
                # Check for encoded_host because we're using it in next step
                if not encoded_host:
                    return redirect(
                        f"https://{myshopify_domain}/admin/apps/{settings.SHOPIFY_APP_API_KEY}"
                    )
            except UnauthorizedAccess:
                shop.uninstall()
                return get_scope_permission(request, myshopify_domain)

        user_logged_in.send(sender=shop.__class__, request=request, user=shop)

        return render(
            request,
            self.template_name,
            {
                "data": {
                    "shopOrigin": shop.myshopify_domain,
                    "apiKey": getattr(settings, "SHOPIFY_APP_API_KEY"),
                    "encodedHost": encoded_host,
                    "loadPath": request.GET.get(REDIRECT_FIELD_NAME) or "home/",
                }
            },
        )


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/index.html"

    def get(self, request):
        # print(request.user.session())

        with request.user.session:
            try:
                shopify_shop = shopify.Shop.current()
                message = f"Hi {shopify_shop.email}"
            except UnauthorizedAccess as e:
                message = str(e)
        return self.render_to_response({"title": message})


class ProductsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/products.html"

    def get(self, request):
        with request.user.session:
            products = shopify.Product.find(limit=10)
        return self.render_to_response({"products": products})


class CollectionsListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "core/collections_list.html"

    def get(self, request):
        with request.user.session:
            custom_collections = shopify.CustomCollection.find()
            smart_collections = shopify.SmartCollection.find()

        context = {
            "custom_collections": [collection.to_dict() for collection in custom_collections],
            "smart_collections": [collection.to_dict() for collection in smart_collections],
        }

        return self.render_to_response(context)
