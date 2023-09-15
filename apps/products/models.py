from django.db import models
from apps.users.models import Seller, Customer
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Rate(models.Model):
    rate = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return str(self.rate)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(null=False, default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def update_rating(self):
        avg_rating = self.comments.aggregate(Avg('comment_rate__rate'))['comment_rate__rate__avg']
        if avg_rating is not None:
            avg_rating = round(avg_rating, 2)
        else:
            avg_rating = 0.00

        self.rating = avg_rating
        self.save()

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment_content = models.TextField(null=True)
    comment_rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f"Comment by {self.comment_author} on {self.product}"


class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.customer.name} - Created at {self.created_at}'


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} {self.product.name}(s) in {self.basket}'
