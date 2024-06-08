from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    city = models.CharField(max_length=100)
    college = models.CharField(max_length=200)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

class CashReceipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100, default='hi')
    recipient_email = models.EmailField(default='h')
    receipt_number = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Receipt {self.receipt_number} - {self.user.username}'

class ProductDetail(models.Model):
    receipt = models.ForeignKey(CashReceipt, related_name='product_details', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.name} - {self.receipt.receipt_number}'
