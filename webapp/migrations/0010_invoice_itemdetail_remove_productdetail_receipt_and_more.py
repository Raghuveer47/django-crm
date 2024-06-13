# Generated by Django 4.2.7 on 2024-06-11 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_alter_cashreceipt_receipt_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=100, unique=True)),
                ('billed_to_name', models.CharField(max_length=100)),
                ('billed_to_email', models.EmailField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('order_no', models.CharField(max_length=100)),
                ('gst_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ItemDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_details', to='webapp.invoice')),
            ],
        ),
        migrations.RemoveField(
            model_name='productdetail',
            name='receipt',
        ),
        migrations.DeleteModel(
            name='CashReceipt',
        ),
        migrations.DeleteModel(
            name='ProductDetail',
        ),
    ]
