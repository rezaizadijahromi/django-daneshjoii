from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from django.shortcuts import get_object_or_404

from .serializers import (
    LessonNameSerializer, MasterNameSerialzier,
    QuestionSerializer
)

from core_new_v.models import (
    Question, MasterName,
    LessonName,Answer,User,
    StudentProfile
)


class QuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


