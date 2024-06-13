from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)  # Changed to EmailField
    phone = models.CharField(max_length=13)  # Consider adding validators
    city = models.CharField(max_length=100)
    college = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True)
    billed_to_name = models.CharField(max_length=100)
    billed_to_email = models.EmailField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    order_no = models.CharField(max_length=100)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Invoice {self.invoice_no} - {self.billed_to_name}'

class ItemDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='item_details', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.name} - {self.invoice.invoice_no}'
