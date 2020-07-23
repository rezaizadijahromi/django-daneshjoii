from django.contrib import admin
from django.urls import path, include

from .views import (
    QuestionView
)

app_name = 'core_new_v'


urlpatterns = [
    path('question/', QuestionView.as_view(), name='question')
]
