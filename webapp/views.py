from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm, UpdateForm, RecordForm, InvoiceForm, ItemDetailFormSet, UploadCSVForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Invoice, Record
from django.db.models import Q
import csv
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, FloatField

def home(request):
    return render(request, 'webapp/index.html')

def base(request):
    return render(request, 'webapp/base.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_welcome_email(user.email, user.username)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'webapp/register.html', {'form': form})

def send_welcome_email(email, username):
    subject = 'Welcome to Our Website'
    message = f'Hi {username},\n\nThank you for registering at our website. We are thrilled to have you on board!\n\nBest regards,\nThe Team'
    from_email = 'your_email@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'webapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('query', '')
    if query:
        records = Record.objects.filter(Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(city__icontains=query) | Q(college__icontains=query))
        invoices = Invoice.objects.filter(Q(invoice_no__icontains=query) | Q(description__icontains=query))
    else:
        records = Record.objects.all().order_by('id')
        invoices = Invoice.objects.all().order_by('id')
    return render(request, 'webapp/dashboard.html', {'records': records, 'invoices': invoices})

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    return render(request, 'webapp/create_record.html', {'form': form})

@login_required(login_url='login')
def update(request, pk):
    record = get_object_or_404(Record, id=pk)
    form = UpdateForm(instance=record)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'webapp/update.html', {'form': form})

@login_required(login_url='login')
def singular_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    return render(request, 'webapp/viewrecord.html', {'record': record})

@login_required(login_url='login')
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                Record.objects.create(
                    firstname=row['firstname'],
                    lastname=row['lastname'],
                    email=row['email'],
                    phone=row['phone'],
                    city=row['city'],
                    college=row['college']
                )
            return redirect('dashboard')
    else:
        form = UploadCSVForm()
    return render(request, 'webapp/upload_csv.html', {'form': form})

@login_required(login_url='login')
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    record.delete()
    return redirect("dashboard")

@login_required(login_url='login')
def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = ItemDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user  # assuming user is logged in
            invoice.save()
            item_details = formset.save(commit=False)
            for item in item_details:
                item.invoice = invoice
                item.save()
            # send_receipt_email(invoice)  # Uncomment if you have this function
            return redirect('view_invoice', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = ItemDetailFormSet()
    return render(request, 'webapp/create_invoice.html', {'form': form, 'formset': formset})

@login_required(login_url='login')
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    total_amount = invoice.item_details.annotate(
        item_total=ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField())
    ).aggregate(total=Sum('item_total'))['total'] or 0
    return render(request, 'webapp/view_invoice.html', {'invoice': invoice, 'total_amount': total_amount})

def send_receipt_email(invoice):
    subject = f'Invoice {invoice.invoice_no} Generated'
    message = f'Hi {invoice.user.username},\n\nYour invoice has been generated.\n\nInvoice Details:\nInvoice Number: {invoice.invoice_no}\nDate: {invoice.date}\nTotal Amount: {invoice.total_amount}\n\nDescription: {invoice.description}\n\nThank you!'
    from_email = 'your_email@example.com'
    recipient_list = [invoice.billed_to_email]
    send_mail(subject, message, from_email, recipient_list)
