from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect,render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from .forms import RegistrationForm,VendorForm

User =get_user_model()

def send_activation_email(request,user):
    context={
        "user":user,
        "domain":get_current_site(request).domain,
        "protocol":"https" if request.is_secure() else "http",
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "token":default_token_generator.make_token(user),
    }
    body=render_to_string("accounts/activation_email.txt",context)
    send_mail("Activate your Marketplace account",body,None,[user.email])

def register(request):
    if request.user.is_authenticated:
        return redirect("profile")    
    form=RegistrationForm(request.POST or None )
    if request.method=="POST" and form.is_valid():
        user=form.save(commit=False)
        user.is_Active=False
        user.save()
        send_activation_email(request,user)
        messages.success(request,"Account created. Check your email to activate it.")
        return redirect("login")
    return render(request,"accounts/register.html",{"form":form})    

def activate(request,uidb64,token):
    try:
        user=User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (User.DoesNotExist,ValueError,TypeError,OverflowError):
        user=None

    if user and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save(update_fields=["is_active"])        
        messages.success(request,"Email verified. YOu can log in now.")
        return redirect("login")
    return render(request,"accounts/activation_invalid.html")    

@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def become_vendor(request):
    if hasattr(request.user, "vendor"):
        return redirect("profile")
    form = VendorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        vendor = form.save(commit=False)
        vendor.user = request.user
        vendor.save()
        messages.success(request, "Shop submitted. An admin will approve it soon.")
        return redirect("profile")
    return render(request, "accounts/become_vendor.html", {"form": form})