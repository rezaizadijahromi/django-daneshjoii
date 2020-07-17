from django.contrib import admin

from .models import (
    Question, LessonName,
    MasterName, User, 
    StudentProfile
)


admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(Question)
admin.site.register(LessonName)
admin.site.register(MasterName)