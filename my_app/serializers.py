from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile,
    Manuscript,
    Keyword,
    FeedbackQuestion,
    FeedbackResponse,
    AuthorSettings,
    Resource,
    ResourceInteraction,
    Notification,
    BetaReaderApplication,
    ManuscriptFeedbackPreference,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},  # Password should not be readable
        }

    def create(self, validated_data):
        # Create a new user with hashed password
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "profile_img", "bio", "created_at", "updated_at"]


class ManuscriptSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    keywords = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manuscript
        fields = ["id", "title", "author", "file_path", "status", "keywords"]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name", "category"]


class FeedbackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackQuestion
        fields = ["id", "category", "question_text", "is_active"]


class FeedbackResponseSerializer(serializers.ModelSerializer):
    question = FeedbackQuestionSerializer()
    reader = UserSerializer()

    class Meta:
        model = FeedbackResponse
        fields = "__all__"


class ManuscriptFeedbackPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptFeedbackPreference
        fields = "__all__"


class AuthorSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSettings
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class ResourceInteractionSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer()
    user = UserSerializer()

    class Meta:
        model = ResourceInteraction
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class BetaReaderApplicationSerializer(serializers.ModelSerializer):
    manuscript = ManuscriptSerializer()
    beta_reader = UserSerializer()

    class Meta:
        model = BetaReaderApplication
        fields = "__all__"
