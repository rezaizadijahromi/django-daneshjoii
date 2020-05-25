from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (Question_api_view,QuestionDetail_api_view,
                    CreateUserView,CreateTokenView,ManageUserView,
                    AddQ,AddAnswerToQuestion,PostDetailAPIView,AddQ,
                    AnswerListAPIView,AddRequestQuantity
                    )

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('add-user', UserViewSets, basename='user')

app_name = 'core'

urlpatterns = [
    path('create/',CreateUserView.as_view(), name='create'),
    path('token/',CreateTokenView.as_view(), name='token'),
    path('me/',ManageUserView.as_view(), name='me'),
    # path('',include(router.urls)),
    path('question_list/',Question_api_view, name='question_list'),
    path('answer_list/',AnswerListAPIView.as_view(), name='answer_list'),
    path('add-question/',AddQ.as_view(), name='add_q'),
    path('add-request/<slug:slug>/',AddRequestQuantity.as_view(), name='request'),
    # path('add-question/',AddQuestion.as_view(), name='add_q'),
    path('question/<slug:slug>/',PostDetailAPIView.as_view(), name='question_detail'),
    path('question/<slug:slug>/answer/',AddAnswerToQuestion.as_view(), name='add_a'),
    # path('add_answer/',AddAnswerToQuestionAPIView.as_view(), name='answer'),
    # path('question/<slug:slug>/answer/',AddAnswerToQuestion_api_view, name='add_answer'),
    path('question_list/<slug:slug>/',QuestionDetail_api_view, name='question_detail'),

]
