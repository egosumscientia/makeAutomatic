from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm

def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def contact(request):
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                subject=f"Nuevo mensaje de {cd['nombre']}",
                message=cd['mensaje'],
                from_email=cd['email'],
                recipient_list=['tuempresa@makeautomatic.com'],
            )
            sent = True
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'sent': sent})
