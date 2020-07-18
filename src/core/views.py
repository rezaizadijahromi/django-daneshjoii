from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.db.models import Count,Q
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from datetime import datetime, timezone


from .models import (Question, Lesson, MasterName, User, 
        OrderQuestionQuantity,QuestionQuantity, Answer, OrderAnswerSubmite,
        Like, Dislike
)
from .forms import AddQuestion, AddAnswerForm

import string
import random

def serach(request):
    queryset = Question.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.objects.filter(
            Q(lesson_name__icontains=query)|
            Q(master_name__icontains=query)|
            Q(ref_code__icontains=query)
        ).distinct()

    context = {
        'queryset':queryset
    }

    return render(request, '', context)


def create_ref_code():
    return ''.join(random.choices(string.digits, k=5))

class Home(ListView):
    model = Question
    template_name = 'home.html'

class AddQ(View):

    def get(self, *args, **kwargs):
        question = Question.objects.all()
        form = AddQuestion()

        context = {
            'question':question,
            'form':form
        }

        return render(self.request, 'add_question.html', context)

    def post(self, *args, **kwargs):

        question = Question()
        question.ref_code = create_ref_code()
        form = AddQuestion(self.request.POST, self.request.FILES, instance=question)

        if form.is_valid():
            form.save()
            q = question.ref_code

            return redirect('core-app:question', slug=q)


        else:
            form = AddQuestion()

# def is_time_left(request, slug):
#     question = get_object_or_404(Question, slug=slug)
#     time_left = (question.deadline - datetime.now(timezone.utc)).days
#     if time_left > 0:
#         return True
#     return False

from datetime import datetime, timezone
def questionView(request, slug):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.filter(question=question)
    time_left = (question.deadline - datetime.now(timezone.utc)).days
    context = {
        'question':question,
        'answer':answer,
        'time_left':time_left
    }

    return render(request, 'checkout.html', context)


def add_request_quantity(request, slug):
    item = get_object_or_404(Question, slug=slug)
    order_item, created = QuestionQuantity.objects.get_or_create(
        question=item,
        user=request.user,
    )
    order_qs = OrderQuestionQuantity.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.question_req.filter(question__slug=item.slug).exists():
            messages.info(request, "You already pick this question")
            return redirect("core-app:home")
        else:
            order.question_req.add(order_item)
            order_item.request_quantity += 1
            order_item.save()

            messages.info(request, "This item was added to your cart.")
            return redirect("core-app:home")
    else:
        order = OrderQuestionQuantity.objects.create(
            user=request.user)
        order.question_req.add(order_item)
        order_item.request_quantity += 1
        order_item.save()

        messages.info(request, "This item was added to your cart.")
        return redirect("core-app:question", slug=slug)


def AddAnswerToQuestion(request, slug):
    item = get_object_or_404(Question, slug=slug)
    left_time =  (item.deadline - datetime.now(timezone.utc)).days


    form = AddAnswerForm()
    order_item = Answer.objects.filter(
        username=request.user,
        question=item,
        answered=False
    )

    order_qs = OrderAnswerSubmite.objects.filter(
        user=request.user,
         ordered=False,
          question=item
    )

    if left_time > 0:
        if order_qs.exists():
            order = order_qs[0]
            if order.answer.filter(question__slug=item.slug).exists():
                messages.info(request, 'u already pick this asshole')
                return redirect('core-app:question', slug=slug)
            else:
                messages.info(request, 'Your answer must be deleted sorry you cant add answer to this question any more')
                return redirect('core-app:question', slug=slug)

        else:
            print(request)
            if request.method == 'POST':
                form = AddAnswerForm(request.POST, request.FILES)
                if form.is_valid():

                    description = form.cleaned_data['description']
                    image_answer = form.cleaned_data['image_answer']

                    answer = Answer(
                        username=request.user,
                        question=Question.objects.get(slug=slug),
                        description=description,
                        image_answer=image_answer,
                        answered=True
                    )
                    answer.save()

                    # order = OrderAnswerSubmite.objects.create(
                    #     user=request.user, ordered=False
                    # )
                    order = OrderAnswerSubmite.objects.create(
                        user=request.user,
                        question=item
                    )
                    order.answer.add(answer)

                    messages.info(request, 'Answer submited successfully')
                    return redirect('core-app:question', slug=slug)
    else:
        messages.info(request, 'Time for answering this question is over')
        return redirect('core-app:question', slug=slug)


    context = {
        'form':form
    }

    return render(request, 'add_answer.html', context)

def AnswerToQuestion(request, slug):
    item = get_object_or_404(Question, slug=slug)
    left_time = (item.deadline - datetime.now(timezone.utc)).days

    form = AddAnswerForm()
    order_item = Answer.objects.filter(
        username=request.user,
        question=item,
        answered=False
    )

    if left_time> 0:
        if item.answers.filter().exists():
            messages.info(request, 'u already pick this asshole')
            return redirect('core:question', slug=slug)

        else:
             if request.method == 'POST':
                form = AddAnswerForm(request.POST, request.FILES)
                if form.is_valid():

                    description = form.cleaned_data['description']
                    image_answer = form.cleaned_data['image_answer']

                    answer = Answer(
                        username=request.user,
                        question=Question.objects.get(slug=slug),
                        description=description,
                        image_answer=image_answer,
                        answered=True
                    )
                    answer.save()

                    q = Question.answers.add(answer)

                    messages.info(request, 'Answer submited successfully')
                    return redirect('core:question', slug=slug)
    else:
        messages.info(request, 'Time for answering this question is over')
        return redirect('core:question', slug=slug)

    context = {
        'form':form
    }

    return render(request, 'add_answer.html', context)

    

def LikeVote(request, id):
    
    answer = get_object_or_404(Answer, id=id)
    answer_like = Answer()

    like_answer = Like.objects.get_or_create(
        answer=answer
    )[0]

    answer.likes = like_answer
    answer.save()

    if request.user not in like_answer.user.all():
        like_answer.counte += 1
        like_answer.user.add(request.user)
        answer.likes = like_answer
        like_answer.save()
        messages.info(request, 'thanks')
        return redirect('core-app:home')

    else:
        messages.info(request, 'You vote this answer already')
        return redirect('core-app:home')

    context = {
        'like_answer':like_answer
    }
    return render(request, 'checkout.html', context)

def DislikeVote(request, id):
    answer = get_object_or_404(Answer, id=id)

    dislike_answer = Dislike.objects.get_or_create(
        answer=answer
    )[0]

    answer.dislikes = dislike_answer
    answer.save()

    total = answer.likes.counte + answer.dislikes.counte
    print(total)

    if total > 0:

        if request.user not in dislike_answer.user.all():
            dislike_answer.counte -= 1
            dislike_answer.user.add(request.user)
            dislike_answer.save()
            messages.info(request, 'You dislike this answer')
            return redirect('core-app:home')
        

        else:
            messages.info(request, 'You vote this answer already')
            return redirect('core-app:home')

    else:
        if request.user not in dislike_answer.user.all():
            # dislike_answer.counte -= 1
            # dislike_answer.user.add(request.user)
            # dislike_answer.save()
            dislike_answer.delete()
            messages.info(request, 'You dislike this answer')
            return redirect('core-app:home')
        

        else:
            messages.info(request, 'You vote this answer already')
            return redirect('core-app:home')

    context = {
        'dislike':dislike_answer,
        'total':total
    }
    return render(request, 'checkout.html', context)




def AnswerDetail(request, slug, id):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.get(
        question=question,
        id=id,
    )

    context = {
        'answer':answer
    }

    return render(request, 'answer.html', context)

