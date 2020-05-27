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
# def get_deadline():
#     return datetime.today() + timedelta(days=20)
import random
import string
def create_ref_code():
    return ''.join(random.choices(string.digits, k=5))

class Question(models.Model):

    lesson_name = models.ForeignKey('Lesson',on_delete=models.CASCADE)
    master_name = models.ForeignKey('MasterName',on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    ref_code = models.CharField(max_length=5, blank=True, null=True)
    image = models.ImageField(upload_to='q_image/',null=True, blank=True)
    day = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.today)
    deadline = models.DateTimeField(default=datetime.today)
    answers = models.ManyToManyField('Answer',related_name='answer', blank=True)
    # zaman_tahvil = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if not self.slug and self.ref_code:
            self.slug = slugify(self.ref_code)
        self.ref_code = create_ref_code()
        self.slug = self.ref_code
        day = self.day
        time = timedelta(days=day)
        deadline = self.date + time
        self.deadline = deadline
        super(Question,self).save(*args, **kwargs)

    def get_time_left_for_answer(self):
        time = self.deadline - self.date
        return time.days


    def get_absolute_url(self):
        return reverse('core-app:question', kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core-app:add_request", kwargs={
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
    likes = models.ForeignKey(
            'Like',
            on_delete=models.CASCADE, 
            related_name='likes_answer',
        blank=True, null=True
        )
    dislikes = models.ForeignKey(
        'Dislike',
        on_delete=models.CASCADE,
        related_name='dislikes_answer',
        blank=True, null=True
     )

    def __str__(self):
        return '{} answer the question'.format(self.username)


    def get_final_vote(self):
        total = self.likes.counte + self.dislikes.counte
        return total

    def get_absolute_url(self):
        return reverse('core-app:add_answer', kwargs={"slug": self.slug})

    def get_add_to_vote_url(self):
        return reverse("core-app:add_vote", kwargs={
            'id': self.id
        })

    def get_remove_to_vote_url(self):
        return reverse("core-app:remove_vote", kwargs={
            'id': self.id
        })
    def get_answer_url(self):
        return reverse('core-app:answer_detail', kwargs={
            'slug': self.question.slug,
            'id': self.id
        })
    def __str__(self):
        return str(self.question)

class OrderAnswerSubmite(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ManyToManyField(Answer)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user)



class QuestionQuantity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    request_quantity = models.PositiveIntegerField(default=0)
    question = models.ForeignKey('Question', models.CASCADE)

class OrderQuestionQuantity(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True)
    question_req = models.ManyToManyField(QuestionQuantity)
    ordered = models.BooleanField(default=False)

class Like(models.Model):
    user = models.ManyToManyField('User')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    counte = models.IntegerField(default=0)

    def like_vote(self):
        return self.counte

class Dislike(models.Model):
    user = models.ManyToManyField('User')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    counte = models.IntegerField(default=0)

    def get_dislike_vote(self):
        return self.counte

