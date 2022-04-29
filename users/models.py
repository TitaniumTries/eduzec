from email.policy import default
from django.db import models
from django.contrib.auth.models import ( 
    AbstractBaseUser, BaseUserManager
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.utils import timezone

from imagekit.models import ProcessedImageField

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError("Users must have a username.")
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

from imagekit.processors import ResizeToFill, Thumbnail, ResizeToFit

class CustomUser(AbstractBaseUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 40 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=40, unique=True, validators=[UnicodeUsernameValidator, ], verbose_name='username')
    email = models.EmailField(max_length=254,help_text='Required. 254 characters or fewer.', validators=[validate_email] ,verbose_name='email address', unique=True)
    avatar = ProcessedImageField(null=True, blank=True, upload_to='avatars',
                                           processors=[ResizeToFit(50, 100)],
                                           format='JPEG',
                                           options={'quality': 60})
    first_name =  models.CharField(blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser =  models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='stuff status')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='date joined')
    groups = models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')
    hide_email = models.BooleanField(default=True, help_text='Make user email private.', verbose_name='hide email')
    email_verified = models.BooleanField(default=False) #to be implemented to allow only users with verified email addresses to sign in. See auth.py to add.

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_staff

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True