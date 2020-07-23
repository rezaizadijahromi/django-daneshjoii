from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from django.shortcuts import get_object_or_404, redirect

from .serializers import (
    LessonNameSerializer, MasterNameSerialzier,
    QuestionSerializer, AnswerSerializer
)

from core_new_v.models import (
    Question, MasterName,
    LessonName,Answer,User,
    StudentProfile
)

from datetime import datetime, timezone


class QuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'


class AnswerView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        question = get_object_or_404(Question, slug=slug)
        left_time = (question.deadline - datetime.now(timezone.utc)).days
        user = self.request.user
        question_qs = Question.objects.filter(slug=slug)
        
        if left_time > 0:
            
            if self.request.user in question.user_answer.all():
                print("Bad")
                return Response(serializer.errors, status=400)
            else:
                description = serializer.validated_data.get('description')
                image_answer = serializer.validated_data.get('image_answer')
                answer = Answer(
                    username=self.request.user,
                    question=question,
                    description=description,
                    image_answer=image_answer
                )

                answer.save()
                #This is for display answers content
                question.answers.add(answer)
                #This is for knwo wuhich user is answer the question
                question.user_answer.add(self.request.user)
                question.save()
                serializer.save(username=user)
                return Response(status=status.HTTP_201_CREATED)
            
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)



class AnswerListAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

