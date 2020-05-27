from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics, authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.shortcuts import render, redirect, get_object_or_404


from .serializers import (QuestionSerializer,
                    UserSerializer,AnswerSerializer,
                    AuthTokenSerializer,QuestionDetailSerializer,
                    QuestionQuantitySerializer,
                    AnswerQuantitySerializer
                        )




from core.models import *



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticate user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user



@api_view(['GET'])
def Question_api_view(request):

    if request.method == 'GET':
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def QuestionDetail_api_view(request, slug):

    try:
        question = Question.objects.get(slug=slug)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddQ(generics.ListCreateAPIView):

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    lookup_field = 'slug'
    serializer_class = QuestionDetailSerializer


class AnswerListAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AddAnswerToQuestion(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = 'core-api:question_detail'

    def get_queryset(self):
        question = Answer.objects.all()
        return question

    def perform_create(self, serializer, slug=None):
        # if serializer.is_valid():
        #     username = serializer.validated_data['username']

        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        
        answer = Answer(
            question=question,
            username=self.request.user,
            answered=False
        )

        order_qs = OrderAnswerSubmite.objects.filter(
            user=self.request.user,
            ordered=False,
            question=question
        )

        if order_qs.exists():
            order = order_qs[0]
            if order.answer.filter(question__slug=question.slug).exists():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                return Response(status=status.HTTP_226_IM_USED)
        
        else:
            description = serializer.validated_data.get('description')
            image_answer = serializer.validated_data.get('image_answer')
            answer = Answer(
                username=self.request.user,
                question=Question.objects.get(slug=self.kwargs['slug']),
                description=description,
                image_answer=image_answer,
                answered=True
            )

            answer.save()

            order = OrderAnswerSubmite.objects.create(
                user=self.request.user,
                question=question
            )

            order.answer.add(answer)

            return Response(status=status.HTTP_201_CREATED)

        
            serializer.save(username=self.request.user, question=question)

class AddRequestQuantity(generics.CreateAPIView):


    serializer_class = QuestionQuantitySerializer
    lookup_field = 'slug'
    def perform_create(self, serializer, slug=None):
        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        order_item, created = QuestionQuantity.objects.get_or_create(
            question=question,
            user=self.request.user
        )

        order_qs = OrderQuestionQuantity.objects.filter(
            user=self.request.user,
            ordered=False
        )

        if order_qs.exists():
            order = order_qs[0]

            if order.question_req.filter(question__slug=question.slug).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                order.question_req.add(order_item)
                order_item.request_quantity += 1
                order_item.save()
                return Response(status=status.HTTP_200_OK)
        else:
            order= OrderQuestionQuantity.objects.create(
                user=self.request.user
            )
            order_item.request_quantity += 1
            order_item.save()
            order.question_req.add(order_item)
            return Response(status=status.HTTP_201_CREATED)


class LikeVoteAPIView(generics.CreateAPIView):

    pass

class DislikeVote(generics.DestroyAPIView):

    pass


















# @api_view(['GET','POST'])
# def Answer_api_view(request):

#     if request.method == 'GET':
#         answer = Answer.objects.all()
#         serializer = AnswerSerializer(answer, many=True)
#         return Response(serializer.data)


# @api_view(['POST','GET'])
# def AddAnswerToQuestion_api_view(request, slug):

#     permission_classes = (permissions.AllowAny,)
#     serializer = AnswerSerializer(data=request.data)
#     question = get_object_or_404(Question, slug=slug)

#     answer_item = Answer.objects.filter(
#         username=request.user,
#         question=question,
#         answered=False
#     )

#     answer_qs = OrderAnswerSubmite.objects.filter(
#         user=request.user,
#         ordered=False
#     )

#     if answer_qs.exists():
#         answer = answer_qs[0]
#         if answer.answer.filter(question__slug=question.slug).exists():
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'GET':
#         # question = question = get_object_or_404(Question, slug=slug)
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = AddAnswerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)

#             description = serializer.validated_data['description']
#             image_answer = serializer.validated_data['image_answer']

#             answer = Answer(
#                 username=request.user,
#                 question=Question.objects.get(slug=slug),
#                 description=description,
#                 image_answer=image_answer,
#                 answered=True
#             )
#             answer.save()

#             order = OrderAnswerSubmite.objects.create(
#                 user=request.user,
#                 question=question
#             )

#             order.answer.add(answer)
#             return Response(status=status.HTTP_201_CREATED)
#     return Response(status=status.HTTP_404_NOT_FOUND)
