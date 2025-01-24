from django.contrib import admin
from allauth.socialaccount.models import SocialAccount
from .models import (
    Manuscript,
    Profile,
    Keyword,
    FeedbackQuestion,
    ManuscriptFeedbackPreference,
    FeedbackResponse,
    AuthorSettings,
    Resource,
    BetaReaderApplication,
    ResourceInteraction,
    MyModel,
    Notification,
    ReaderManuscript,
    FeedbackTopic, 
    BetaReader,
)


# admin.site.register(SocialAccount)


# admin.site.register(MyModel)
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ["field1"]


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status")
    list_filter = ("status",)
    search_fields = ("title", "author__username")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(FeedbackQuestion)
class FeedbackQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "is_active", "topic")
    list_filter = ("is_active", "topic")
    search_fields = ("question_text", "topic")

@admin.register(BetaReader)
class BetaReaderAdmin(admin.ModelAdmin):
    list_display = ('profile', 'experience', 'rating', 'total_reviews')
    search_fields = ('profile__user__username', 'experience')
    list_filter = ('keywords',)

@admin.register(FeedbackResponse)
class FeedbackResponseAdmin(admin.ModelAdmin):
    list_display = ("manuscript", "reader", "question", "review_date")
    list_filter = ("review_date",)
    search_fields = ("manuscript__title", "reader__username")


@admin.register(AuthorSettings)
class AuthorSettingsAdmin(admin.ModelAdmin):
    list_display = ("author", "profile_visibility", "auto_submit_feedback")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title",)


@admin.register(BetaReaderApplication)
class BetaReaderApplicationAdmin(admin.ModelAdmin):
    list_display = ("manuscript", "beta_reader", "status", "application_date")
    list_filter = ("status", "application_date")
    search_fields = ("manuscript__title", "beta_reader__username")
    
@admin.register(ReaderManuscript)
class ReaderManuscriptAdmin(admin.ModelAdmin):
    list_display = ('reader', 'manuscript', 'status', 'updated_at')
    list_filter = ('status',)
    search_fields = ('reader__username', 'manuscript__title')
    
@admin.register(FeedbackTopic)
class FeedbackTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)     