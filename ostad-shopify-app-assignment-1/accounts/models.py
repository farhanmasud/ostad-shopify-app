import uuid
from django.db import models
from shopify_auth.models import AbstractShopUser


class Account(AbstractShopUser):
    """User model."""

    def __str__(self):
        return self.myshopify_domain
