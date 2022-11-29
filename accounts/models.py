from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name  = last_name,
        )
      

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, first_name, last_name, password=None ):
        """
        Creates and saves a superuser with the given email, username fisrt_name  ,lastname and password
        """
        user = self.create_user(
            email,
            password=password,
            first_name = first_name,
            last_name = last_name,
            username= username
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank = True, max_length=100)
    address_line_2 = models.CharField(blank = True, max_length=100)
    profile_picture = models.ImageField(blank = True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length= 20)
    state = models.CharField(blank=True, max_length= 20)
    country = models.CharField(blank=True, max_length= 20)
    phone_number = models.CharField(blank = True, max_length=20)
   


    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'


class Messages(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.TextField()
    
    def __str__(self):
        return self.name