from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, phone, password=None, **extra_fields):
        if not username:
            raise ValueError("The username is required")
        if not email:
            raise ValueError("The email is required")

        email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, first_name, last_name, phone, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class MemberDemand(models.Model):
    STATE_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='membership_requests',
        on_delete=models.CASCADE,
        help_text='User requesting to become a member'
    )

    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='validated_demands',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Responsable who accepted or refused'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.requester.username} → {self.status}"