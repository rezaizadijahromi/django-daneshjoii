from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model, authenticate

from core.models import *

from django.shortcuts import render, redirect, get_object_or_404



class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id','username',
            'email','password'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user


    def update(self, instance, validated_data):
        """Update a user setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type':'password'
        },
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class MasterNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterName
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


import random
import string
def create_ref_code():
    return ''.join(random.choices(string.digits, k=5))

class QuestionSerializer(serializers.ModelSerializer):

    lesson_name = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Lesson.objects.all()
    )

    master_name = serializers.PrimaryKeyRelatedField(
            many=False,
            queryset=MasterName.objects.all()
        )

    class Meta:
        model = Question
        fields = (
            'lesson_name','master_name',
            'slug','ref_code',
            'image','day',
            'date','deadline',
        )

    def create(self, validated_data):
        def create_ref_code():
            return ''.join(random.choices(string.digits, k=5))

        question = Question(
            master_name=validated_data['master_name'],
            lesson_name=validated_data['lesson_name'],
            image=validated_data['image'],
            day=validated_data['day'],
        )

        question.ref_code = create_ref_code()
        question.save()
        return question


class QuestionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'lesson_name','master_name',
            'slug','ref_code',
            'image','day',
            'date','deadline',
        )

class AnswerSerializer(serializers.ModelSerializer):

    question = serializers.PrimaryKeyRelatedField(
            read_only=True,
            many=False
        )

    class Meta:
        model = Answer
        fields = (
            'username','description',
            'image_answer','question',
            'answered',
        )

        read_only_fields = ('username','question')

    


    # def create(self, validated_data):
    #     answer = Answer.objects.create(
    #         username=validated_data['username'],
    #         description=validated_data['description'],
    #         image_answer=validated_data['image_answer'],
    #     )

    #     return answer

    def get_question(self, obj):
        return obj.question

class AddQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
                'lessong_name','master_name',
                'image','day',
            )

    def create(self, validated_data):
        obj = Question(
            
        )


class QuestionQuantitySerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
            read_only=True,
            many=False
        )

    class Meta:
        model = QuestionQuantity
        fields = (
            'request_quantity','question'
            
        )

    def get_question(self, obj):
        return obj.question

class AnswerQuantitySerializer(serializers.ModelSerializer):


    answer = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=False
    )


    class Meta:
        model = AnswerQuantity
        fields = (
            'user',
            'request_quantity',
            'answer'
        )
        read_only_fields = ('user',)