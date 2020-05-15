from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.db.models import Count,Q
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from .models import (Question, Lesson, MasterName, User, 
        OrderQuestionQuantity,QuestionQuantity, Answer, OrderAnswerSubmite,
        AnswerQuantity, VoteOrder
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

            return redirect('core:question', slug=q)


        else:
            form = AddQuestion()


def questionView(request, slug):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.filter(question=question)
    context = {
        'question':question,
        'answer':answer
    }

    return render(request, 'question.html', context)


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
            return redirect("core:home")
        else:
            order.question_req.add(order_item)
            order_item.request_quantity += 1
            messages.info(request, "This item was added to your cart.")
            return redirect("core:home")
    else:
        order = OrderQuestionQuantity.objects.create(
            user=request.user)
        order.question_req.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:question", slug=slug)


def AddAnswerToQuestion(request, slug):
    item = get_object_or_404(Question, slug=slug)

    form = AddAnswerForm()
    order_item = Answer.objects.filter(
        username=request.user,
        question=item,
        answered=False
    )

    order_qs = OrderAnswerSubmite.objects.filter(user=request.user, ordered=False, question=item)

    if order_qs.exists():
        order = order_qs[0]
        if order.answer.filter(question__slug=item.slug).exists():
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

                # order = OrderAnswerSubmite.objects.create(
                #     user=request.user, ordered=False
                # )
                order = OrderAnswerSubmite.objects.create(
                    user=request.user,
                    question=item
                )
                order.answer.add(answer)

                messages.info(request, 'Answer submited successfully')
                return redirect('core:question', slug=slug)


    context = {
        'form':form
    }

    return render(request, 'add_answer.html', context)                
    
    # else:

    #     if request.method == 'POST':
    #         form = AddAnswerForm(request.POST, request.FILES)
    #         if form.is_valid():

    #             description = form.cleaned_data['description']
    #             image_answer = form.cleaned_data['image_answer']

    #             answer = Answer(
    #                 user=request.user,
    #                 question=Question.objects.get(slug=slug),
    #                 description=description,
    #                 image_answer=image_answer,
    #                 answered=True
    #             )
    #             answer.save()

    #             order = OrderAnswerSubmite.objects.create(
    #                 user=request.user
    #             )
    #             order.question.add(answer)

    #             messages.info(request, 'Answer submited successfully')
    #             return redirect('core:question', slug=slug)
    #         else:
    #             messages.info(request, 'form is not valid')
    #             return redirect('core:question', slug=slug)
    #     else:
    #         messages.info(request, 'nothing posted')
    #         return redirect('core:question', slug=slug)
    # else:
    #     if request.method == 'POST':
    #         form = AddAnswerForm(request.POST, request.FILES)
    #         if form.is_valid():

    #             description = form.cleaned_data['description']
    #             image_answer = form.cleaned_data['image_answer']

    #             answer = Answer(
    #                 username=request.user,
    #                 question=Question.objects.get(slug=slug),
    #                 description=description,
    #                 image_answer=image_answer,
    #                 answered=True
    #             )
    #             answer.save()
    #             order = OrderAnswerSubmite.objects.create(
    #                 user=request.user
    #             )
    #             order.answer.add(answer)
    #             messages.info(request, 'Answer submited successfully')
    #             return redirect('core:question', slug=slug)






def LikeVote(request, id):
    # user_point = User.objects.filter(user=request.user)
    item = get_object_or_404(Answer, id=id)
    order_item, created = AnswerQuantity.objects.get_or_create(
        user=request.user,
        answer=item
    )
    order_qs = VoteOrder.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.vote_request.filter(answer__id=item.id).exists():
            messages.info(request, 'You vote this answer already')
            return redirect('core:home')
        else:
            order.vote_request.add(order_item)
            order_item.request_quantity += 1
            order_item.save()
            messages.info(request, 'Your vote submitet successfully')
            return redirect('core:home')
    else:
        order = VoteOrder.objects.create(
            user=request.user
        )
        order.vote_request.add(order_item)
        order_item.request_quantity += 1
        order_item.save()
        messages.info(request, 'Your vote submitet successfully')
        return redirect('core:home')


def DislikeVote(request, id):
    item = get_object_or_404(Answer, id=id)
    
    order_qs = VoteOrder.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.vote_request.filter(answer__id=item.id).exists():
            order_item = AnswerQuantity.objects.filter(
                user=request.user,
                answer=item,
            )[0]
            if order_item.request_quantity >= 1:
                order_item.request_quantity -= 1
                order_item.save()
                messages.info(request, 'You dislike this item')
                return redirect('core:home')

            elif order_item.request_quantity <= 0:
                order_item.delete()
                order.vote_request.remove(order_item)
                item.delete()
                messages.info(request, 'You dislike this item and the item deleted because of quantity is under 0')
                return redirect('core:home')
        else:
            messages.info(request, 'You should first add vote then dislike it')
            return redirect('core:home')

    else:
        messages.info(request, 'The item does not exists')
        return redirect('core:home')


# def AddAnswerToQuestion(request, slug):
#     question = get_object_or_404(Question, slug=slug)
#     q = question
#     # limit = Question.objects.filter(slug__in=slug).values('question__answer').annotate(Count('question__answer'))
#     # print(limit)
#     form = AddAnswerForm()
#     answer = Answer.objects.filter(
#         question=q,
#         username=request.user,
#     )
#     order_qs = OrderAnswerSubmite.objects.filter(user=request.user, ordered=False)

#     if Answer.objects.filter(username=request.user, answered=True):
#         messages.info(request, 'You are aleready answer this question')
#         return redirect('core:question', slug=slug)
#     else:
#         order = OrderAnswerSubmite.objects.get(
#                     user=request.user
#                 )
#         if request.method == 'POST':
#             form = AddAnswerForm(request.POST, request.FILES)
#             if form.is_valid():
#                 # if Answer.objects.filter(username=request.user, answered=False):

#                 description = form.cleaned_data['description']
#                 image_answer = form.cleaned_data['image_answer']

#                 answer = Answer(
#                     username=request.user,
#                     question=Question.objects.get(slug=slug),
#                     description=description,
#                     image_answer=image_answer,
#                     answered=True
#                 )
#                 answer.save()

#                 # question = Question.objects.filter(slug__in=slug)
#                 # order = OrderAnswerSubmite.objects.create(
#                 #     user=request.user
#                 # )
#                 order.answer.add(answer)

#                 messages.info(request, 'Answer submited successfully')
#                 return redirect('core:question', slug=slug)
#                 # elif Answer.objects.filter(username=request.user, answered=True):
#                 #     messages.info(request, 'you already answer this question')
#                 #     return redirect('core:home')

#         # else:
#         #     messages.info(request, 'Error')
#         #     form = AddAnswerForm()

#     context = {
#         'form':form
#     }

#     return render(request, 'add_answer.html', context)






# class AddQuestioAnswer(View):

#     def get(self, *args, **kwargs):
#         form = AddAnswerForm()
#         context = {
#             'form':form
#         }

#         return render(self.request, 'add_answer.html', context)
#     def post(self, *args, **kwargs):

#         form = AddAnswerForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             # username = form.cleaned_data['username']
#             description = form.cleaned_data['description']
#             image_answer = form.cleaned_data['image_answer']

#             answer = Answer(
#                 # username=username,
#                 description=description,
#                 image_answer=image_answer
#             )

#             return redirect('core:home')

#             answer.save()
#         else:
#             form = AddAnswerForm()

