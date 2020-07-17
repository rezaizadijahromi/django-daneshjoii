from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, 
    PermissionsMixin
)
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def creat_user(self, email, password=None, *args, **kwargs):
        if "gmail.com" not in email:
            raise ValidationError('gmail.com shold be in email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.creat_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.is_admin

    def __str__(self):
        return str(self.email)
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return  str(self.user)
    

def post_save_user_profile(sender, created, instance, *args, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

post_save.connect(post_save_user_profile, sender=User)
    

class MasterName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class LessonName(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        blank=True, null=True,
        upload_to='lesson_image/'
    )

    def __str__(self):
        return self.name

from datetime import datetime, timedelta
import random
import string

def create_ref_code():
    return ''.join(random.choices(string.digits, k=5))

class Question(models.Model):
    lesson_name = models.ForeignKey(LessonName, on_delete=models.CASCADE)
    master_name = models.ForeignKey(MasterName, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    ref_code = models.CharField(max_length=5, blank=True, null=True)
    image = models.ImageField(
        blank=True, null=True,
        upload_to='question/'
    )
    day = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.today)
    deadline = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return str(self.ref_code)
    
    # answers = models.ManyToManyField(Answer)

    
        
def pre_save_slug_ref_code(sender, instance, *args, **kwargs):
    print("here")
    # if not created:
    instance.ref_code = create_ref_code()
    instance.slug = instance.ref_code
    day = instance.day
    time = timedelta(days=day)
    deadline = instance.date + time
    instance.deadline = deadline
    
    print("running")

pre_save.connect(pre_save_slug_ref_code, sender=Question)