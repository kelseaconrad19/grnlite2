from django.urls import path, include, re_path
from . import views
from .views import (
    GoogleLoginView,
    UserProfileView,
    BetaReaderListCreateView,
    find_beta_readers,
    beta_reader_list,
    active_titles_count
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from register import views as v

app_name = "my_app"

urlpatterns = [
    path("", views.home, name="home"),
    # User URLs
    path("signin/", views.user_signin, name="signin"),
    path("register/", v.register, name="register"),
    path("login/", v.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("users/", views.UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("social_django.urls", namespace="social")),
    # Google OAuth2 URLs
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    path("api/manuscripts/", views.manuscripts_api, name="manuscripts_api"),
    path("beta-readers/<int:pk>/", views.beta_reader_public_profile, name="beta_reader_public_profile"),
    path("api/feedback-count/", views.get_feedback_count, name="feedback-count"),
    # Profile URLs
    path(
        "profiles/", views.ProfileListCreateView.as_view(), name="profile-list-create"
    ),
    path(
        "profiles/<int:pk>/", views.ProfileDetailView.as_view(), name="profile-detail"
    ),
    # Manuscript URLs
    path(
        "manuscripts/",
        views.ManuscriptListCreateView.as_view(),
        name="manuscript-list-create",
    ),
    path(
        "manuscripts/<int:pk>/",
        views.ManuscriptDetailView.as_view(),
        name="manuscript-detail",
    ),
    path("active-titles/", active_titles_count, name="active-titles"),
    path("notifications/", views.get_notifications, name="notifications"),
    # Keyword URLs
    path("keywords/", views.KeywordListCreateView.as_view(), name="keyword-list"),
    path(
        "keywords/<int:pk>/", views.KeywordDetailView.as_view(), name="keyword-detail"
    ),
    # Feedback Question URLs
    path(
        "feedback-questions/",
        views.FeedbackQuestionListCreateView.as_view(),
        name="feedback-question-list",
    ),
    path(
        "feedback-questions/<int:pk>/",
        views.FeedbackQuestionDetailView.as_view(),
        name="feedback-question-detail",
    ),
    # Manuscript Feedback Preference URLs
    path(
        "manuscript-feedback-preferences/",
        views.ManuscriptFeedbackPreferenceListCreateView.as_view(),
        name="manuscript-feedback-preference-list",
    ),
    path(
        "manuscript-feedback-preferences/<int:pk>/",
        views.ManuscriptFeedbackPreferenceDetailView.as_view(),
        name="manuscript-feedback-preference-detail",
    ),
    # Feedback Response URLs
    path(
        "feedback-responses/",
        views.FeedbackResponseListCreateView.as_view(),
        name="feedback-response-list",
    ),
    path(
        "feedback-responses/<int:pk>/",
        views.FeedbackResponseDetailView.as_view(),
        name="feedback-response-detail",
    ),
    # Author Settings URLs
    path(
        "author-settings-view/",
        views.AuthorSettingsListCreateView.as_view(),
        name="author-settings-list",
    ),
    path(
        "author-settings/<int:pk>/",
        views.AuthorSettingsDetailView.as_view(),
        name="author-settings-detail",
    ),
    # Resource URLs
    path("resources/", views.ResourceListCreateView.as_view(), name="resource-list"),
    path(
        "resources/<int:pk>/",
        views.ResourceDetailView.as_view(),
        name="resource-detail",
    ),
    # Resource Interactions URLs
    path(
        "resource-interactions/",
        views.ResourceInteractionListCreateView.as_view(),
        name="resource-interaction-list",
    ),
    path(
        "resource-interactions/<int:pk>/",
        views.ResourceInteractionDetailView.as_view(),
        name="resource-interaction-detail",
    ),
    # Notification URLs
    path(
        "notifications/",
        views.NotificationListCreateView.as_view(),
        name="notification-list",
    ),
    path(
        "notifications/<int:pk>/",
        views.NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    # Beta Reader Application URLs
    path("beta_readers/", views.find_beta_readers, name="find-beta-readers-html"),
    # Optional: Different URL for the function-based beta_reader_list view
    path(
        "beta-reader-applications/<int:pk>/",
        views.BetaReaderApplicationDetailView.as_view(),
        name="beta-reader-application-detail",
    ),
    # Reader Dashboard URLs
    re_path(
        r"^reader-dashboard\.html$",
        views.reader_dashboard,
        name="reader-dashboard-html",
    ),
    path(
        "available-manuscripts/",
        views.available_manuscripts,
        name="available-manuscripts-html",
    ),
    path('book-details/<int:manuscript_id>/', views.view_project_as_reader, name='view-project'),
    path('choose-book/<int:manuscript_id>/', views.choose_book, name='choose-book'),
    path('beta-reader-books/', views.beta_reader_books, name='beta-reader-books'),
    path('feedback-form/<int:manuscript_id>/', views.feedback_form, name='feedback-form'),
    path("reader-feedback/", views.reader_feedback, name="reader-feedback-html"),
    path("reader-profile/", views.reader_profile, name="reader-profile-html"),
    path("reader-dashboard/", views.reader_dashboard, name="reader-dashboard-html"),
    path(
        "reader-resource-library/",
        views.reader_resource_library,
        name="reader-resource-library-html",
    ),
    path(
        "beta-reader-training/",
        views.beta_reader_training,
        name="beta-reader-training-html",
    ),
    path(
        "beta-reader-performance-metrics/",
        views.beta_reader_performance_metrics,
        name="beta-reader-performance-metrics-html",
    ),
    path(
        "reader-payment-page/",
        views.reader_payment_page,
        name="reader-payment-page-html",
    ),
    path("reader-settings/", views.reader_settings, name="reader-settings-html"),
    path("feedback/<int:manuscript_id>/", views.feedback_form, name="feedback_form"),
    
    path("feedback-success/", views.feedback_success, name="feedback-success"),
    path("api/manuscripts/", views.get_manuscripts, name="get_manuscripts"),
    path('api/reader-manuscripts/', views.get_reader_manuscripts, name='get_reader_manuscripts'),
    path('api/choose-manuscript/<int:manuscript_id>/', views.choose_manuscript, name='choose_manuscript'),
    path('author-feedback/', views.author_feedback, name='author-feedback'),
    path("api/feedback/", views.reader_feedback, name="reader_feedback"),
    path("api/manuscripts/", views.get_manuscripts, name="get_manuscripts"),
    # Author Dashboard URLs
    re_path(
        r"^author-dashboard\.html$",
        views.author_dashboard,
        name="author-dashboard-html",
    ),
    path('manuscripts/<int:manuscript_id>/view/', views.view_project, name='view-project'),
    path('manuscripts/<int:manuscript_id>/delete/', views.delete_manuscript, name='delete-manuscript'),
    path("my-manuscripts/", views.my_manuscripts, name="my-manuscripts-html"),
    path("my-books/", views.my_books, name="my-books-html"),
    path("author-profile/", views.author_profile, name="author-profile-html"),
    path("feedback-summary/", views.feedback_summary, name="feedback-summary-html"),
    path("manuscript-submission/", views.create_manuscript, name="manuscript-submission-html"),
    path("manuscript-success/", views.manuscript_success, name="manuscript-success"),
    path(
        "author-resource-library/",
        views.author_resource_library,
        name="author-resource-library-html",
    ),
    path(
        "author-community-groups/",
        views.author_community_groups,
        name="author-community-groups-html",
    ),
    path(
        "author-payment-page/",
        views.author_payment_page,
        name="author-payment-page-html",
    ),
    path("author-settings/", views.author_settings, name="author-settings-html"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
