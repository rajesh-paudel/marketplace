from django.contrib.auth.models import AbstractUser
from django.db import models

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