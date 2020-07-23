from django.contrib import messages
from django.shortcuts import (
    render, redirect,
    get_object_or_404
)
from django.views.generic import (
    ListView, DetailView, View
)


from .models import (
    Answer, Question,
    User, StudentProfile,
    MasterName, LessonName
)

from .forms import (
    AddQuetionForm,
    AddAnswerForm
)

from datetime import datetime, timezone


class Home(ListView):
    queryset = Question.objects.all()
    template_name = 'homev2.html'


class AddQ(View):
    def get(self, *args, **kwargs):
        question = Question.objects.all()
        form = AddQuetionForm()
        slug = self.kwargs.get('slug')

        context = {
            'question':question,
            'form':form
        }

        return render(self.request,'add_questionv2.html', context)

    def post(self, request, *args, **kwargs):
        question = Question()
        form = AddQuetionForm(
            request.POST, 
            request.FILES,
            instance=question
        )


        if form.is_valid():
            form.save()
            slug = question.ref_code
            return redirect(
                'core-v2:question', 
                slug=slug
            )
        else:
            form = AddQuetionForm()
            print("Somthing goes wrong in Quetion Form")
        
def QuetionView(reqeust, slug):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.filter(question=question)
    time_left = (question.deadline - datetime.now(timezone.utc)).days
    request_quantity = question.number_of_request.all().count()
    if request_quantity > 0:
        context = {
            'question':question,
            'answer':answer,
            'time_left':time_left
        }

        return render(reqeust, 'checkoutv2.html', context)
    else:
        messages.info(reqeust, "This question yet not reached to 5 request ask your friend to request this question")
        return redirect('core-v2:home')
        

def AddRequestQuantity(reqeust, slug):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.filter(question=question)
    time_left = (question.deadline - datetime.now(timezone.utc)).days
    if reqeust.user.is_authenticated:
        if reqeust.user in question.number_of_request.all():
            messages.info(reqeust, "You already request this question")
            return redirect('core-v2:home')
        else:
            question.number_of_request.add(reqeust.user)
            question.save()
            messages.info(reqeust, "Your request submited wait until get to 10 requests")
            return redirect('core-v2:home')
    else:
        messages.info(reqeust, "You should authenticate first")
        return redirect('core-v2:home')


def AddAnswerToQuestion(request, slug):
    question = get_object_or_404(Question, slug=slug)
    left_time = (question.deadline - datetime.now(timezone.utc)).days


    answer = Answer.objects.filter(
        username=request.user,
        question=question
    )

    form = AddAnswerForm()
    if left_time > 0:
        if request.user.is_authenticated:
            if request.user in question.user_answer.all() or question.answers.all()  :
                messages.info(request, "You answer this question")
                return redirect('core-v2:question', slug=slug)
            else:
                if request.method == 'POST':
                    print("after post method")
                    form = AddAnswerForm(request.POST, request.FILES)
                    if form.is_valid():

                        description = form.cleaned_data['description']
                        image_answer = form.cleaned_data['image_answer']

                        answer = Answer(
                            username=request.user,
                            question=Question.objects.get(slug=slug),
                            description=description,
                            image_answer=image_answer,
                        )
                        answer.save()
                        question.answers.add(answer)
                        question.user_answer.add(request.user)
                        question.save()
                        messages.info(request, "Answer Submited")
                        return redirect('core-v2:question', slug=slug)
                    else:
                        messages.info(request, "Error")
                        return redirect('core-v2:question', slug=slug)
                # else:
                #     messages.info(request, "Reqeust failed")
                #     return redirect("core-v2:question", slug=slug)
        else:
            messages.info(request, "You should Login first")
            return redirect("core-v2:question", slug=slug)
    else:
        messages.info(request, "Time for answering this question is over")
        return redirect("core-v2:question", slug=slug)

    context = {
        'form':form
    }

    return render(request, 'add_answerv2.html', context)


def LikeView(request, id):
    answer = Answer.objects.filter(id=id)
    
    if request.user.is_authenticated:
        is_like = Answer.objects.toggle_like(request.user, answer.first())
        messages.info(request, "Thanks")
        return redirect('core-v2:home')
    else:
        messages.info(request, "You sould login first")
        return redirect("core-v2:home")

    # context = {
    #     'is_liked':is_like
    # }

    # return render(request, 'checkoutv2.html', context)


def AnswerDetail(request, slug, id):
    question = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.get(
        question=question,
        id=id,
    )

    context = {
        'answer':answer
    }

    return render(request, 'answerv2.html', context)



# Another way to handel this function 
#       
# def AddAnswerToQuestion(request, slug):
#     question = get_object_or_404(Question, slug=slug)
#     left_time = (question.deadline - datetime.now(timezone.utc)).days

#     form = AddAnswerForm()
#     if left_time > 0:
#         if request.user.is_authenticated:
#             if request.user not in question.user_answer.all():
#                 if request.method == 'POST':
#                     print("We are in post method")
#                     form = AddAnswerForm(request.POST, request.FILES)
#                     if form.is_valid():
#                         description = form.cleaned_data['description']
#                         image_answer = form.cleaned_data['image_answer']
                        
#                         answer = Answer(
#                             username=request.user,
#                             question=Question.objects.get(slug=slug),
#                             description=description,
#                             image_answer=image_answer
#                         )
#                         answer.save()
#                         question.answers.add(answer)
#                         question.user_answer.add(request.user)
#                         question.save()
#                         messages.info(request, "Answer Submited")
#                         return redirect('core-v2:question', slug=slug)
#                     else:
#                         messages.info(request, "Error")
#                         return redirect('core-v2:question', slug=slug)
#                 else:
#                     print("Error1")
#                     form = AddAnswerForm()
#                     messages.info(request, "Not valid")
#                     return redirect('core-v2:question', slug=slug)
#             else:
#                 print("Error2")

#                 messages.info(request, "You already answer this question")
#                 return redirect('core-v2:question', slug=slug)
#         else:
#             print("Error3")
#             messages.info(request, "You should Login for answering this question")
#             return redirect('core-v2:question', slug=slug)
#     else:
#         print("Error4")
#         messages.info(request, "Time for answering this question is over")
#         return redirect('core-v2:question', slug=slug)



