from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify
class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER="customer","Customer"
        VENDOR ="vendor","Vendor"
        ADMIN="admin","Admin"
    email=models.EmailField(unique=True)    
    role=models.CharField(max_length=10,choices=Role.choices,default=Role.CUSTOMER)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]

    def __str__(self):
        return self.email


class Vendor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="vendor")    
    shop_name=models.CharField(max_length=120,unique=True)
    slug=models.SlugField(max_length=140,unique=True,blank=True)
    description=models.TextField(blank=True)
    commission_rate=models.DecimalField(max_digits=4,decimal_places=2,default=10)
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            base=slugify(self.shop_name)
            slug,n=base,1
            while Vendor.objects.filter(slug=slug).exists():
                n+=1
                slug=f"{base}-{n}"
            self.slug=slug
        super().save(*args,**kwargs)    

    def __str__(self):
        return self.shop_name
