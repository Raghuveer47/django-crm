from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm, UpdateForm, RecordForm  # Ensure you import RecordForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CashReceipt
from .forms import CashReceiptForm
from .forms import UploadCSVForm
from django.db.models import Q
import csv
from .models import Record

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

    myrecords = Record.objects.all()

    context = {'records': myrecords}

    return render(request, 'webapp/dashboard.html', context=context)


#crud

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    
    context = {"form": form}
    return render(request, 'webapp/create_record.html', context)

@login_required(login_url='login')
def update(request, pk):
    record = get_object_or_404(Record, id=pk)
    form = UpdateForm(instance=record)

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'webapp/update.html', context=context)



@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/viewrecord.html', context=context)



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


@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    

    return redirect("dashboard")

from django.shortcuts import render
from .models import Record

@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('query', '')
    if query:
        records = Record.objects.filter(Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query) | Q(city__icontains=query) | Q(college__icontains=query))
        receipts = CashReceipt.objects.filter(Q(receipt_number__icontains=query) | Q(description__icontains=query))
    else:
        records = Record.objects.all().order_by('id')
        receipts = CashReceipt.objects.all().order_by('id')
    return render(request, 'webapp/dashboard.html', {'records': records, 'receipts': receipts})

#reciept genrtion


@login_required(login_url='login')
def create_receipt(request):
    if request.method == 'POST':
        form = CashReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.save()
            send_receipt_email(receipt)
            return redirect('dashboard')
    else:
        form = CashReceiptForm()
    return render(request, 'webapp/create_receipt.html', {'form': form})

@login_required(login_url='login')
def view_receipt(request, pk):
    receipt = get_object_or_404(CashReceipt, pk=pk)
    return render(request, 'webapp/view_receipt.html', {'receipt': receipt})

def send_receipt_email(receipt):
    subject = f'Receipt {receipt.receipt_number} Generated'
    message = f'Hi {receipt.user.username},\n\nYour receipt has been generated.\n\nReceipt Details:\nReceipt Number: {receipt.receipt_number}\nDate: {receipt.date}\nAmount: {receipt.amount}\nGST Amount: {receipt.gst_amount}\nTotal Amount: {receipt.total_amount}\n\nDescription: {receipt.description}\n\nThank you!'
    from_email = 'your_email@example.com'
    recipient_list = [receipt.user.email]
    send_mail(subject, message, from_email, recipient_list)
