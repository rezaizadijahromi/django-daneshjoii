from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.text import slugify

from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # def __str__(self):
    #     return str(self.id)

    objects = UserManager()

    USERNAME_FIELD = 'email'

from datetime import datetime


class Daneshjoo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)

from datetime import datetime, timedelta
def get_deadline():
    return datetime.today() + timedelta(days=20)

class Question(models.Model):

    lesson_name = models.ForeignKey('Lesson',on_delete=models.CASCADE)
    master_name = models.ForeignKey('MasterName',on_delete=models.CASCADE)
    slug = models.SlugField()
    ref_code = models.CharField(max_length=5, blank=True, null=True)
    image = models.ImageField(upload_to='q_image/',null=True, blank=True)
    date_time = models.DateField(default=datetime.today)
    deadline = models.DateField(default=get_deadline)
    answers = models.ManyToManyField('Answer',related_name='answer')
    # zaman_tahvil = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if not self.slug and self.ref_code:
            self.slug = slugify(self.ref_code)
        super(Question,self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('core:question', kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add_request", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return 'The question was {} from {} master with ref_code {}'.format(self.lesson_name, self.master_name, self.ref_code)

# def answer_submit(sender, **kwargs):
#     if kwargs['instance'].answers.count() > 6:
#         raise ValidationError("You can't assign more than 5 answer")


# m2m_changed.connect(answer_submit, sender=Question.answers.through)



class Lesson(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to='lesson_image/')

    def __str__(self):
        return str(self.name)

class MasterName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Answer(models.Model):

    username = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True )
    description = models.TextField(null=True, blank=True)
    image_answer = models.ImageField(upload_to='answer/')
    question = models.ForeignKey('Question', on_delete=models.CASCADE,
                    blank=True, null=True, related_name='question')
    answered = models.BooleanField(default=False)

    def __str__(self):
        return '{} answer the question'.format(self.username)

    def get_absolute_url(self):
        return reverse('core:add_answer', kwargs={"slug": self.slug})

    def get_add_to_vote_url(self):
        return reverse("core:add_vote", kwargs={
            'id': self.id
        })

    def get_remove_to_vote_url(self):
        return reverse("core:remove_vote", kwargs={
            'id': self.id
        })

    def __str__(self):
        return str(self.question)

class OrderAnswerSubmite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ManyToManyField(Answer)
    ordered = models.BooleanField(default=False)



class QuestionQuantity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    request_quantity = models.PositiveIntegerField(default=0)
    question = models.ForeignKey('Question', models.CASCADE)

class OrderQuestionQuantity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True)
    question_req = models.ManyToManyField(QuestionQuantity)
    ordered = models.BooleanField(default=False)

class AnswerQuantity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True)
    request_quantity = models.IntegerField(default=0)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE,blank=True, null=True)

class VoteOrder(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vote_request = models.ManyToManyField('AnswerQuantity')
    ordered = models.BooleanField(default=False)