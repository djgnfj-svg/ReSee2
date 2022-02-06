from random import choice
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)

from reviewer.models import TimeStampedModel


# Create your models here.

class PayPlan(TimeStampedModel):
	class Memberships(models.IntegerChoices):
		FREE = 0
		PRIMIUM = 5000
		MAXIMUN = 19000

	name = models.CharField(max_length=20, default=Memberships.FREE.name, choices=Memberships.choices)
	price = models.IntegerField(default=Memberships.FREE, choices=Memberships.choices)
	print(Memberships.labels)

class Organization(TimeStampedModel):
	class Industries(models.TextChoices):
		PERSONAL = "personal"
		RETAIL = "retail"
		MANUFACTURING = "manufacturing"
		IT = "it"
		OTHERS = "others"
	name = models.CharField(max_length=50) # 회사이름
	industry = models.CharField(max_length=15, choices=Industries.choices,default=Industries.OTHERS)

class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        u = self.create_user(email=email,
                            nickname=nickname,
                            password=password,
                            )
        u.is_admin = True
        u.save(using=self._db)
        return u

class MyUser(AbstractBaseUser,  PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(
        u'닉네임',
        max_length=10,
        blank=False,
        unique=True,
        default='')

    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
