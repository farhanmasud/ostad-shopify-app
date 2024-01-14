import shopify
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, FormView
from pyactiveresource.connection import UnauthorizedAccess
from shopify_auth.session_tokens.views import get_scope_permission
from accounts.models import Account
from .forms import CollectionCreateForm, ProductCreateForm, LanguageChoiceForm
from .models import LanguageChoice
from .utils import show_error_message_and_redirect


class SplashPageView(View):
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


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

    def get(self, request):
        with request.user.session:
            try:
                shopify_shop = shopify.Shop.current()
                user_email = shopify_shop.email
            except UnauthorizedAccess as e:
                user_email = str(e)

            context = {
                "user_email": user_email,
                "menu_link": "home",
            }
        return self.render_to_response(context)


class ShopView(LoginRequiredMixin, TemplateView):
    template_name = "core/shop.html"

    def get(self, request):
        with request.user.session:
            try:
                shopify_shop = shopify.Shop.current()
            except UnauthorizedAccess as e:
                shopify_shop = str(e)

            context = {
                "shopify_shop": shopify_shop,
                "menu_link": "shop",
            }
#         return self.render_to_response(context)


# class CollectionsListView(LoginRequiredMixin, TemplateView):
#     template_name = "core/collections_list.html"

#     def get(self, request):
#         with request.user.session:
#             custom_collections = shopify.CustomCollection.find()
#             smart_collections = shopify.SmartCollection.find()

#         context = {
#             "custom_collections": custom_collections,
#             "smart_collections": smart_collections,
#             "menu_link": "collections",
#         }

#         return self.render_to_response(context)


# class CollectionProuctsListView(LoginRequiredMixin, TemplateView):
#     template_name = "core/collection_products_list.html"

#     def get(self, request, collection_type, collection_id):
#         with request.user.session:
#             if collection_type == "custom":
#                 collection = shopify.CustomCollection.find(collection_id)
#             elif collection_type == "smart":
#                 collection = shopify.SmartCollection.find(collection_id)
#             else:
#                 raise PermissionDenied("Forbidden")

#             products_list = collection.products()

#         context = {
#             "collection": collection,
#             "products_list": products_list,
#             "collection_type": collection_type,
#             "collection": collection,
#             "menu_link": "collections",
#         }

#         return self.render_to_response(context)


# class CollectionCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = "core/collection_create.html"
#     form_class = CollectionCreateForm
#     success_url = reverse_lazy("core:collections_list")
#     success_message = "Collection added successfully!"

#     def form_invalid(self, form):
#         messages.error(self.request, "Please correct the erros")
#         return self.render_to_response(self.get_context_data(form=form))

#     def post(self, request):
#         form = self.get_form()
#         if form.is_valid():
#             with request.user.session:
#                 try:
#                     shopify.CustomCollection.create(
#                         {
#                             "title": form.cleaned_data["title"],
#                             "body_html": form.cleaned_data["description"],
#                         }
#                     )
#                 except Exception as e:
#                     print(str(e))
#                     show_error_message_and_redirect(
#                         request,
#                         "Clouldn't connect to Shopify API",
#                         "core:collections_list",
#                     )
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


# class CollectionEditView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = "core/collection_edit.html"
#     form_class = CollectionCreateForm
#     success_url = reverse_lazy("core:collections_list")
#     success_message = "Collected edited successfully!"

#     def get(self, request, custom_collection_id):
#         context = self.get_context_data()

#         try:
#             with request.user.session:
#                 collection = shopify.CustomCollection.find(custom_collection_id)
#         except Exception as e:
#             print(str(e))
#             show_error_message_and_redirect(
#                 request,
#                 "Clouldn't connect to Shopify API",
#                 "core:collections_list",
#             )

#         form = self.get_form()
#         form.fields["title"].initial = collection.title
#         form.fields["description"].initial = collection.body_html

#         context["form"] = form

#         return self.render_to_response(context)

#     def post(self, request, custom_collection_id):
#         form = self.get_form()

#         if form.is_valid():
#             try:
#                 with request.user.session:
#                     collection = shopify.CustomCollection.find(custom_collection_id)
#                     collection.title = form.cleaned_data["title"]
#                     collection.body_html = form.cleaned_data["description"]
#                     collection.save()
#             except Exception as e:
#                 print(str(e))
#                 show_error_message_and_redirect(
#                     request,
#                     "Clouldn't connect to Shopify API",
#                     "core:collections_list",
#                 )
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


# class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = "core/product_create.html"
#     form_class = ProductCreateForm
#     success_message = "Product added successfully!"

#     def get_success_url(self):
#         self.success_url = reverse_lazy(
#             "core:collection_products_list",
#             kwargs={
#                 "collection_type": "custom",
#                 "collection_id": self.kwargs["collection_id"],
#             },
#         )
#         return str(self.success_url)

#     def form_invalid(self, form):
#         messages.error(self.request, "Please correct the erros")
#         return self.render_to_response(self.get_context_data(form=form))

#     def get(self, request, collection_id):
#         context = self.get_context_data()
#         context["back_url"] = self.get_success_url()
#         return self.render_to_response(context)

#     def post(self, request, collection_id):
#         form = self.get_form()
#         if form.is_valid():
#             with request.user.session:
#                 try:
#                     product = shopify.Product.create(
#                         {
#                             "title": form.cleaned_data["title"],
#                             "body_html": form.cleaned_data["description"],
#                         }
#                     )
#                     collection = shopify.CustomCollection.find(collection_id)
#                     collect = shopify.Collect(
#                         {"product_id": product.id, "collection_id": collection.id}
#                     )
#                     collect.save()
#                 except Exception as e:
#                     print(str(e))
#                     show_error_message_and_redirect(
#                         request,
#                         "Clouldn't connect to Shopify API",
#                         self.get_success_url(),
#                     )
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


# class ProductEditView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = "core/product_edit.html"
#     form_class = ProductCreateForm
#     success_message = "Collection added successfully!"

#     def get_success_url(self):
#         self.success_url = reverse_lazy(
#             "core:collection_products_list",
#             kwargs={
#                 "collection_type": "custom",
#                 "collection_id": self.kwargs["collection_id"],
#             },
#         )
#         return str(self.success_url)

#     def form_invalid(self, form):
#         messages.error(self.request, "Please correct the erros")
#         return self.render_to_response(self.get_context_data(form=form))

#     def get(self, request, collection_id, product_id):
#         context = self.get_context_data()
#         with request.user.session:
#             try:
#                 product = shopify.Product.find(product_id)
#                 form = self.get_form()
#                 form.fields["title"].initial = product.title
#                 form.fields["description"].initial = product.body_html

#                 context["form"] = form
#             except Exception as e:
#                 print(str(e))

#         context["back_url"] = self.get_success_url()
#         return self.render_to_response(context)

#     def post(self, request, collection_id, product_id):
#         form = self.get_form()
#         if form.is_valid():
#             with request.user.session:
#                 try:
#                     product = shopify.Product.find(product_id)
#                     product.title = form.cleaned_data["title"]
#                     product.body_html = form.cleaned_data["description"]
#                     product.save()
#                 except Exception as e:
#                     print(str(e))
#                     show_error_message_and_redirect(
#                         request,
#                         "Clouldn't connect to Shopify API",
#                         self.get_success_url(),
#                     )
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


# class LanguageChoiceUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
#     template_name = "core/language_settings.html"
#     form_class = LanguageChoiceForm
#     success_message = "Language options updated successfully!"

#     def get_success_url(self):
#         self.success_url = reverse_lazy(
#             "core:home",
#         )
#         return str(self.success_url)
    
#     def form_valid(self, form):
#         try:
#             prev_instance = LanguageChoice.objects.get(shop=self.request.user)
#         except LanguageChoice.DoesNotExist:
#             prev_instance = None

#         foo_form = self.form_class(form.cleaned_data, instance=prev_instance)
#         foo_form.save()
#         return self.render_to_response(self.get_context_data(form=form))

#     def form_invalid(self, form):
#         print("Form invalid")
#         print(self.get_form().errors)
#         messages.error(self.request, "Please correct the erros")
#         return self.render_to_response(self.get_context_data(form=form))

#     def get(self, request):
#         context = self.get_context_data()
#         with request.user.session:
#             try:
#                 try:
#                     instance = LanguageChoice.objects.get(shop=request.user)
#                 except LanguageChoice.DoesNotExist:
#                     instance = None
                
#                 if instance:
#                     form_class = self.get_form_class()
#                     form = form_class(instance=instance)
#                 else:
#                     form = self.get_form()
#                     form.fields["shop"].initial = request.user

#                 context["form"] = form
#             except Exception as e:
#                 print(str(e))

#         context["back_url"] = self.get_success_url()
#         return self.render_to_response(context)

#     def post(self, request):
        
#         form = self.get_form()
#         if form.is_valid():
            
#             instance = form.save()
#             with request.user.session:
#                 print(",".join(list(instance.translate_to.all().values_list("code", flat=True))))
#                 metafield_1 = shopify.Metafield.create(
#                     {
#                         'value_type': 'string',
#                         'namespace': 'translate-app',
#                         'value': ",".join(list(instance.translate_to.all().values_list("code", flat=True))),
#                         'key': 'language-choices',
#                     }
#                 )
#                 metafield_1.save()

#                 metafield_2 = shopify.Metafield.create(
#                     {
#                         'value_type': 'string',
#                         'namespace': 'translate-app',
#                         'value': instance.site_language.code,
#                         'key': 'site-language',
#                     }
#                 )
#                 metafield_2.save()

#             # with request.user.session:
#             #     try:
#             #         product = shopify.Product.find(product_id)
#             #         product.title = form.cleaned_data["title"]
#             #         product.body_html = form.cleaned_data["description"]
#             #         product.save()
#             #     except Exception as e:
#             #         print(str(e))
#             #         show_error_message_and_redirect(
#             #             request,
#             #             "Clouldn't connect to Shopify API",
#             #             self.get_success_url(),
#             #         )
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
