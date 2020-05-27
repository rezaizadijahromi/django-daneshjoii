from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BAseUserAdmin

from .models import (User, Question, Lesson, MasterName,OrderAnswerSubmite, 
        OrderQuestionQuantity, Answer, QuestionQuantity,
        Like
)


class UserAdmin(BAseUserAdmin):

    ordering = ['-id']
    list_display = ['email', 'username']
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password'
            ),
        }),
        (('personal info'),{
            'fields': (
                'username',
            )
        }),
        (('Permissions'),{
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        (('Imported dates'),{
            'fields':(
                'last_login',
            )
        })
    )

    add_fieldsets = (
        (None, {
            'classes':(
                'wide',
            ),
            'fields': (
                'email', 'password1', 'password2'
            )

        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Lesson)
admin.site.register(MasterName)
admin.site.register(OrderQuestionQuantity)
admin.site.register(OrderAnswerSubmite)
admin.site.register(Answer)
admin.site.register(QuestionQuantity)
admin.site.register(Like)
# admin.site.register(LikeCounter)


