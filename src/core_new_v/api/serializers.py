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
    # lesson_name = serializers.SerializerMethodField()
    # master_name = MasterNameSerialzier(many=False)
    number_of_request = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'lesson_name', 'master_name',
            'slug','ref_code',
            'image','day',
            'date', 'deadline',
            'user_answer', 'number_of_request'
        )

    def get_number_of_request(self, obj):
        return obj.number_of_request.all().count()

    # def get_lesson_name(self, obj):
    #     return LessonNameSerializer(obj.lesson_name).data

class AnswerSerializer(serializers.ModelSerializer):
    # liked = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            'username','description',
            'image_answer','question',
            'liked'
        )
        read_only_fields = ('username','question')

    # def get_liked(self, obj):
    #     return obj.liked.all()

    