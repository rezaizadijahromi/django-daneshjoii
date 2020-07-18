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
    template_name = 'home.html'


class AddQ(View):
    def get(self, *args, **kwargs):
        querion = Question.objects.all()
        form = AddQuetionForm()
        slug = self.kwargs.get('slug')

        context = {
            'quetion':querion,
            'form':form
        }

        return render(self.request,'add_question.html', context)

    def post(self, request, *args, **kwargs):
        question = Question()
        form = AddQuetionForm(
            request.POST, 
            request.FILES
        )


        if form.is_valid():
            form.save()
            slug = question.slug
            return redirect(
                'core-v2:quetion', 
                slug=slug
            )
        else:
            form = AddQuetionForm()
            print("Somthing goes wrong in Quetion Form")
        
def QuetionView(reqeust, slug):
    quetion = get_object_or_404(Question, slug=slug)
    answer = Answer.objects.filter(quetion=quetion)
    time_left = (quetion.deadline - datetime.now(timezone.utc)).days

    context = {
        'question':quetion,
        'answer':answer,
        'time_left':time_left
    }

    return render(reqeust, 'checkout.html', context)

def AddAnswerToQuestion(request, slug):
    question = get_object_or_404(Question, slug=slug)
    left_time = (question.deadline - datetime.now(timezone.utc)).days

    form = AddAnswerForm()
    if left_time > 0:
        if request.user.is_authenticated:
            if request.user not in question.user.all():
                if request.method == 'POST':
                    form = AddAnswerForm(request.POST, request.FILES)
                    if form.is_valid():
                        description = form.cleaned_data['description']
                        image_answer = form.cleaned_data['image_answer']
                        
                        answer = Answer(
                            username=request.user,
                            question=Question.objects.get(slug=slug),
                            description=description,
                            image_answer=image_answer
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
                else:
                    form = AddAnswerForm()
                    return redirect('core-v2:question', slug=slug)
            else:
                messages.info(request, "You already answer this question")
                return redirect('core-v2:question', slug=slug)
        else:
            messages.info(request, "You should Login for answering this question")
            return redirect('core-v2:question', slug=slug)
    else:
        messages.info(request, "Time for answering this question is over")
        return redirect('core-v2:question', slug=slug)



