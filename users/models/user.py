from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel

from utils.country import PHONE_CODE_CHOICES
from .user_manager import UserManager


class User(PolymorphicModel, AbstractUser):
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    country_code = models.CharField(max_length=4, choices=PHONE_CODE_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField('Email', unique=True, blank=False, )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __self__(self): return self.get_full_name

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self): return ('%s %s' % (self.first_name, self.last_name)).strip()

    @property
    def get_short_name(self): return self.first_name.strip()

    @property
    def name(self): return self.get_full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ProxyUser(User):
    pass

    class Meta:
        app_label = 'auth'
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Instructor(User):
    pass


class Student(User):
    pass
