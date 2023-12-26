from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model in Django that extends the AbstractBaseUser and PermissionsMixin classes.
    
    Attributes:
        email (EmailField): The email address of the user (unique identifier).
        is_staff (BooleanField): Indicates whether the user is a staff member.
        is_active (BooleanField): Indicates whether the user is active.
        team (IntegerField): The team number of the user.
        date_joined (DateTimeField): The date and time the user joined.
        last_login (DateTimeField): The date and time of the user's last login.
        
    Methods:
        create_user(email, password=None, **extra_fields): Creates a new user with the given email and password.
        create_superuser(email, password=None, **extra_fields): Creates a new superuser with the given email and password.
    """
    
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    team = models.IntegerField(_('team number'), default=1)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email