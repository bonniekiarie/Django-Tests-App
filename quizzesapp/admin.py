from django.contrib import admin
from quizzesapp.models import Test, Question, Choice

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    pass
class TestAdmin(admin.ModelAdmin):
    pass
class ChoiceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Choice, ChoiceAdmin)