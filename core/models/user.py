from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password,**extra_fields):
        if not email:
            raise ValueError('user must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email,
                       full_name=full_name,
                       **extra_fields
                       )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,full_name,password):
        user = self.create_user(email,full_name,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name',)

    def __str__(self):
        return self.full_name