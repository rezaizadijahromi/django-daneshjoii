from django.contrib import admin
from django.urls import path, include

from .views import (
    QuestionView, QuestionDetailView,
    AnswerView, AnswerListAPIView
)

app_name = 'core_new_v'


urlpatterns = [
    path('question/', QuestionView.as_view(), name='question'),
    path('question/<slug:slug>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question/<slug:slug>/answer/', AnswerView.as_view(), name='answer'),
    path('answers/', AnswerListAPIView.as_view(), name='answer_list'),
]