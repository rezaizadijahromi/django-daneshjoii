from rest_framework import serializers 

from core_new_v.models import (
    Question, LessonName,
    MasterName, User, 
    StudentProfile,Answer
)


class LessonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonName
        fields = (
            'name','image',
        )

class MasterNameSerialzier(serializers.ModelSerializer):
    class Meta:
        model = MasterName
        fields = (
            'name',
        )

class QuestionSerializer(serializers.ModelSerializer):
    lesson_name = LessonNameSerializer(many=False)
    master_name = MasterNameSerialzier(many=False)

    class Meta:
        model = Question
        fields = (
            'lesson_name', 'master_name',
            'slug','ref_code',
            'image','day',
            'date', 'deadline'
        )
