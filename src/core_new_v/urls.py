from django.urls import path, include

from . import views

app_name = 'core_new_v'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_question/', views.AddQ.as_view(), name='add_question'),
    path('question/<slug:slug>/', views.QuetionView, name='question'),
    path('question/<slug:slug>/answer/', views.AddAnswerToQuestion, name='add_answer'),
    path('question/<slug:slug>/answer/<int:id>/', views.AnswerDetail, name='answer_detail'),
    # path('answer/<int:id>/', views.LikeVote, name='add_vote'),
    # path('delete/<int:id>/', views.DislikeVote, name='remove_vote'),

]
