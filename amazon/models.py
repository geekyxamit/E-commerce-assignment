from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"
    
    class Meta(AbstractUser.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"


class CreateModelMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="created_by")


class UpdateModelMixin:
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name="created_by")


class DeleteModelMixin:
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name="deleted_by")

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()


class Product(models.Model, CreateModelMixin, UpdateModelMixin, DeleteModelMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"


class ShoppingCart(models.Model,  CreateModelMixin, UpdateModelMixin):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="cart")

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        db_table = "shopping_carts"


class CartItems(models.Model, CreateModelMixin, UpdateModelMixin, DeleteModelMixin):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.RESTRICT, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name="cart_items")
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.cart.user.username} - {self.product.name}"

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        db_table = "cart_items"