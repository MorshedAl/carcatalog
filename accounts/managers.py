
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,phone_number,password,**other_fields):
        if not email:
            raise ValueError("email may not be empty")
        
        if not phone_number:
            raise ValueError("phone may not be empty")
        
        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,phone_number,password,**other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if other_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        
        return self.create_user(email,phone_number,password,**other_fields)