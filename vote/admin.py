from django.contrib import admin
from .models import VoteCast, Ministry, Question, QuestionChoice


admin.site.register(VoteCast)
admin.site.register(Ministry)
admin.site.register(Question)
admin.site.register(QuestionChoice)
