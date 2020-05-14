from django.urls import path, include

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_question/', views.AddQ.as_view(), name='add_question'),
    path('question/<slug:slug>/', views.questionView, name='question'),
    path('question_tedad/<slug:slug>/', views.add_request_quantity, name='add_request'),
    path('question/<slug:slug>/answer/', views.AddAnswerToQuestion, name='add_answer'),
    path('answer/<int:id>/', views.LikeVote, name='add_vote'),
    path('delete/<int:id>/', views.DislikeVote, name='remove_vote'),
    path('point/<int:user>/', views.point, name='point'),

]
