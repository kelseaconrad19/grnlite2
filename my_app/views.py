from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import AuthorRegistrationForm, ManuscriptSubmissionForm, ReaderRegistrationForm
from django.views.generic import ListView, CreateView
from django.http import JsonResponse, HttpResponse
from .models import Manuscript, Feedback
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

# from rest_framework.decorators import api_view, permission_classes
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


from .models import (
    Profile,
    Keyword,
    Manuscript,
    FeedbackQuestion,
    FeedbackResponse,
    ManuscriptFeedbackPreference,
    AuthorSettings,
    Resource,
    ResourceInteraction,
    Notification,
    BetaReaderApplication,
    BetaReader,
    ReaderManuscript,
)
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ManuscriptSerializer,
    KeywordSerializer,
    FeedbackQuestionSerializer,
    FeedbackResponseSerializer,
    AuthorSettingsSerializer,
    ResourceSerializer,
    ResourceInteractionSerializer,
    NotificationSerializer,
    BetaReaderApplicationSerializer,
    ManuscriptFeedbackPreferenceSerializer,
)


# Home View
def home(request):
    return render(request, "main.html")


def signup(request):
    return render(request, "signup.html")


def signin(request):
    return render(request, "signin.html")


def login(request):
    return render(request, "login.html")


def logout(request):
    return render(request, "logout.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_app:author_dashboard.html")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# Reader Dashboard Views
# def reader_dashboard(request):
#     return render(request, "reader-dashboard.html")

@login_required
@permission_required("my_app.can_view_reader_dashboard", raise_exception=True)
def reader_dashboard(request):
    return render(request, "reader-dashboard.html")


def available_manuscripts(request):
    return render(request, "Reader_Dashboard/available-manuscripts.html")


def reader_feedback(request):
    return render(request, "Reader_Dashboard/reader-feedback.html")


def reader_profile(request):
    return render(request, "Reader_Dashboard/reader-profile.html")


def reader_resource_library(request):
    return render(request, "Reader_Dashboard/reader-resource-library.html")


def beta_reader_training(request):
    return render(request, "Reader_Dashboard/beta-reader-training.html")


def beta_reader_performance_metrics(request):
    return render(request, "Reader_Dashboard/beta-reader-performance-metrics.html")


def reader_payment_page(request):
    return render(request, "Reader_Dashboard/reader-payment-page.html")


def reader_settings(request):
    return render(request, "Reader_Dashboard/reader-settings.html")


# Author Dashboard Views
@login_required
@permission_required("my_app.can_view_author_dashboard", raise_exception=True)
def author_dashboard(request):
    return render(request, "author-dashboard.html", {"user": request.user})

def user_signup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        print(f"Role received: {role}")  # Debugging role
        print(f"Form data: {request.POST}")  # Debug form data

        if role == "author":
            form = AuthorRegistrationForm(request.POST)
        elif role == "reader":
            form = ReaderRegistrationForm(request.POST)
        else:
            return render(request, "register.html", {"error": "Invalid role selected."})

        if form.is_valid():
            user = form.save()
            print(f"User created: {user.username}, Role: {role}")
            return redirect("my_app:signin")  # Redirect to the signin page
        else:
            print(f"Form data received: {request.POST}")
            print(f"Form errors: {form.errors}")  # Debug form errors
    else:
        form = AuthorRegistrationForm()  # Default form

    return render(request, "register.html", {"form": form})
def user_signup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        print(f"Role received: {role}")  # Debug role
        print(f"Form data: {request.POST}")  # Debug form data

        if not role:
            return render(request, "register.html", {"error": "Please select a role."})

        # Choose the appropriate form based on the role
        form = (
            AuthorRegistrationForm(request.POST)
            if role == "author"
            else ReaderRegistrationForm(request.POST)
        )

        if form.is_valid():
            user = form.save()
            print(f"User created: {user.username}, Role: {role}")
            return redirect("my_app:signin")  # Redirect to signin page
        else:
            print(f"Form errors: {form.errors}")  # Debug form errors

    else:
        form = AuthorRegistrationForm()  # Default form

    return render(request, "register.html", {"form": form})

@login_required
def user_signin(request):
    role = request.user.profile.role  # Assuming role is stored in Profile
    if role == "author":
        return redirect("my_app:author-dashboard-html")
    elif role == "reader":
        return redirect("my_app:reader-dashboard-html")
    return redirect("my_app:home")  # Default fallback

def author_signup(request):
    if request.method == "POST":
        form = AuthorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_app:author-dashboard-html")
    else:
        form = AuthorRegistrationForm()
    return render(request, "signup.html", {"form": form})
        
def reader_signup(request):
    if request.method == "POST":
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_app:reader-dashboard-html")
    else:
        form = ReaderRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def manuscripts_api(request):
    keywords = request.GET.get('keywords')
    author = request.GET.get('author')
    manuscripts = Manuscript.objects.all()
    
    if keywords:
        manuscripts = manuscripts.filter(keywords__name__icontains=keywords)
    if author:
        manuscripts = manuscripts.filter(author__username__icontains=author)

    data = {
        "manuscripts": [
            {
                "id": m.id,
                "title": m.title,
                "author": m.author.username if m.author else "Unknown",  # Serialize author as username
                "keywords": [kw.name for kw in m.keywords.all()],  # Serialize keywords as a list of names
                "cover_art": m.cover_art.url if m.cover_art else None
            }
            for m in manuscripts
        ]
    }
    return JsonResponse(data)

def beta_reader_list(request):
    query = request.GET.get("query", "")
    keyword = request.GET.get("keyword", "")

    beta_readers = BetaReader.objects.all()

    if query:
        beta_readers = beta_readers.filter(
            Q(profile__user__username__icontains=query) |
            Q(experience__icontains=query)
        )
    if keyword:
        beta_readers = beta_readers.filter(keywords__name__icontains=keyword)

    return render(request, "beta_readers/beta_reader_list.html", {"beta_readers": beta_readers})

@login_required
def my_books(request):
    manuscripts = Manuscript.objects.filter(author=request.user)
    return render(request, "Author_Dashboard/my-books.html", {'manuscripts':manuscripts})

@login_required
def view_project(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    return render(request, 'Author_Dashboard/view-project.html', {'manuscript': manuscript})

def view_project_as_reader(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)
    return render(request, 'Reader_Dashboard/book-details.html', {'manuscript': manuscript})

@login_required
def choose_book(request, manuscript_id):
    if request.method == 'POST':
        reader = request.user
        manuscript = get_object_or_404(Manuscript, id=manuscript_id)

        existing_entry = ReaderManuscript.objects.filter(reader=reader, manuscript=manuscript).first()
        if not existing_entry:
            ReaderManuscript.objects.create(reader=reader, manuscript=manuscript, status='in_progress')

        return redirect('my_app:reader-dashboard-html') 
    
@login_required
def beta_reader_books(request):
    reader_books = ReaderManuscript.objects.filter(reader=request.user)

    return render(request, 'Reader_Dashboard/beta-reader-books.html', {
        'reader_books': reader_books,
    })
    
@login_required
def feedback_form(request, manuscript_id):
    # Get the manuscript
    manuscript = get_object_or_404(Manuscript, id=manuscript_id)

    # Group questions by their topic
    feedback_topics = manuscript.feedback_topics.all()
    questions_by_topic = {
        topic: FeedbackQuestion.objects.filter(topic=topic, is_active=True)
        for topic in feedback_topics
    }

    if request.method == "POST":
        for topic, questions in questions_by_topic.items():
            for question in questions:
                response_text = request.POST.get(f"question_{question.id}")
                if response_text:
                    FeedbackResponse.objects.create(
                        manuscript=manuscript,
                        reader=request.user,
                        question=question,
                        answer_text=response_text)
            manuscript.status = "reviewed"
        return redirect("my_app:beta-reader-books")

    return render(
        request,
        "Reader_Dashboard/feedback-form.html",
        {"manuscript": manuscript, "questions_by_topic": questions_by_topic},
    )

@login_required
def author_feedback(request):
    # Fetch manuscripts authored by the logged-in user
    manuscripts = Manuscript.objects.filter(author=request.user)

    # Collect feedback responses for these manuscripts
    feedback = FeedbackResponse.objects.filter(
        manuscript__in=manuscripts
    ).select_related('manuscript', 'reader', 'question')

    # Group feedback by manuscript
    feedback_by_manuscript = {}
    for response in feedback:
        if response.manuscript not in feedback_by_manuscript:
            feedback_by_manuscript[response.manuscript] = []
        feedback_by_manuscript[response.manuscript].append(response)
    
    # Debug the structure
    for manuscript, feedbacks in feedback_by_manuscript.items():
        print(f"Manuscript: {manuscript.title}")
        for feedback in feedbacks:
            print(f"    Question: {feedback.question.question_text}, Answer: {feedback.answer_text}")

    return render(request, 'Author_Dashboard/feedback-overview.html', {
        'feedback_by_manuscript': feedback_by_manuscript,
    })

@login_required
def delete_manuscript(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    manuscript.delete()
    return redirect('my_app:my-books-html')

def my_manuscripts(request):
    return render(request, "Author_Dashboard/my-manuscripts.html")


def get_manuscripts(request):
    manuscripts = Manuscript.objects.all().values(
        "id", "title", "genre", "length", "chapters", "description", "cover"
    )
    return JsonResponse(list(manuscripts), safe=False)


def get_manuscripts(request):
    manuscripts = Manuscript.objects.all().values("id", "title", "description", "cover")
    return JsonResponse(list(manuscripts), safe=False)


def find_beta_readers(request):
    return render(request, "Author_Dashboard/beta-reader-list.html")


def beta_reader_list(request):
    # return HttpResponse("Debug: View is called")  # Temporary debug statement
    return render(request, "Author_Dashboard/beta-reader-list.html")


def manuscript_submission(request):
    return render(request, "Author_Dashboard/manuscript-submission.html")


def manuscript_success(request):
    return render(request, "Author_Dashboard/manuscript-success.html")


def my_books(request):
    return render(request, "Author_Dashboard/my-books.html")


@login_required
def create_manuscript(request):
    if request.method == "POST":
        form = ManuscriptSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            manuscript = form.save(commit=False)  # Prevent immediate database save
            manuscript.author = request.user  # Set the author to the logged-in user
            manuscript.save()  # Save to the database
            form.save_m2m()  # Save many-to-many relationships like keywords
            return redirect("my_app:author-dashboard-html")  # Redirect to the dashboard
    else:
        form = ManuscriptSubmissionForm()

    return render(
        request, "Author_Dashboard/manuscript-submission2.html", {"form": form}
    )


@login_required
def active_titles_count(request):
    """View to count active titles (draft manuscripts) for the logged-in user."""
    draft_count = Manuscript.objects.filter(author=request.user, status="draft").count()
    print(f"Draft Count: {draft_count}")
    return JsonResponse({"draft_count": draft_count})

@login_required
def get_feedback_count(request):
    if request.user.is_authenticated:
        feedback_count = FeedbackResponse.objects.filter(manuscript__author=request.user).count()
        return JsonResponse({"feedback_count": feedback_count}, status=200)
    return JsonResponse({"error": "Unauthorized"}, status=401)

@login_required
def get_notifications(request):
    """View to get notifications for the logged-in user."""
    notifications = Notification.objects.filter(user=request.user).values(
        "id", "message", "timestamp"
    )
    return JsonResponse(list(notifications), safe=False)


@csrf_exempt
@login_required
def submit_feedback(request):
    if request.method == "POST":
        manuscript_id = request.POST.get("manuscript")
        plot_feedback = request.POST.get("plot")
        characters_feedback = request.POST.get("characters")
        pacing_feedback = request.POST.get("pacing")
        worldbuilding_feedback = request.POST.get("worldbuilding")
        additional_comments = request.POST.get("comments")

        manuscript = Manuscript.objects.get(id=manuscript_id)
        feedback = Feedback.objects.create(
            manuscript=manuscript,
            reader=request.user,
            plot=plot_feedback,
            characters=characters_feedback,
            pacing=pacing_feedback,
            worldbuilding=worldbuilding_feedback,
            comments=additional_comments,
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def feedback_success(request):
    return render(request, "feedback_success.html")


def get_manuscripts(request):
    manuscripts = Manuscript.objects.all()
    manuscript_list = [
        {
            'id': manuscript.id,
            'title': manuscript.title,
            'author': manuscript.author.get_full_name() or manuscript.author.username,
            'keywords': [keyword.name for keyword in manuscript.keywords.all()],
            'plot_summary': manuscript.plot_summary,
            'cover_art': manuscript.cover_art.url if manuscript.cover_art else None,
            'file_path': manuscript.file_path.url if manuscript.file_path else None,
        }
        for manuscript in manuscripts
    ]
    return JsonResponse({'manuscripts': manuscript_list}, safe=False)

def get_reader_manuscripts(request):
    reader_manuscripts = ReaderManuscript.objects.filter(reader=request.user, status='in_progress')
    manuscripts_data = [
        {
            'id': rm.manuscript.id,
            'title': rm.manuscript.title,
            'author': rm.manuscript.author.get_full_name() or rm.manuscript.author.username,
            'plot_summary': rm.manuscript.plot_summary,
            'cover_art': rm.manuscript.cover_art.url if rm.manuscript.cover_art else None,
        }
        for rm in reader_manuscripts
    ]
    return JsonResponse({'manuscripts': manuscripts_data})

@csrf_exempt
def choose_manuscript(request, manuscript_id):
    if request.method == 'POST':
        reader = request.user
        manuscript = Manuscript.objects.get(id=manuscript_id)

        # Create a ReaderManuscript entry
        ReaderManuscript.objects.create(reader=reader, manuscript=manuscript, status='in_progress')

        return JsonResponse({'message': 'Manuscript added to your reading list.'})

@login_required
def my_books(request):
    manuscripts = Manuscript.objects.filter(author=request.user)
    return render(request, "Author_Dashboard/my-books.html", {'manuscripts':manuscripts})

@login_required
def view_project(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    return render(request, 'Author_Dashboard/view-project.html', {'manuscript': manuscript})

@login_required
def delete_manuscript(request, manuscript_id):
    manuscript = get_object_or_404(Manuscript, id=manuscript_id, author=request.user)
    manuscript.delete()
    return redirect('my_app:my-books-html')

def beta_reader_public_profile(request, pk):
    # Fetch the BetaReader instance by primary key (id)
    beta_reader = get_object_or_404(BetaReader, pk=pk)

    # Pass the BetaReader instance to the template
    return render(request, "beta_readers/beta_reader_profile.html", {"beta_reader": beta_reader})


def feedback_summary(request):
    return render(request, "Author_Dashboard/feedback-summary.html")


def author_resource_library(request):
    return render(request, "Author_Dashboard/author-resource-library.html")


def author_community_groups(request):
    return render(request, "Author_Dashboard/author-community-groups.html")


def author_profile(request):
    return render(request, "Author_Dashboard/author-profile.html")


def author_payment_page(request):
    return render(request, "Author_Dashboard/author-payment-page.html")


def author_settings(request):
    return render(request, "Author_Dashboard/author-settings.html")


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})


# Google Login View
class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token not provided"}, status=400)

        try:
            strategy = load_strategy(request)
            backend = GoogleOAuth2(strategy=strategy)
            user_data = backend.user_data(token)

            # Get or create the user
            user, created = User.objects.get_or_create(
                email=user_data["email"], defaults={"username": user_data["email"]}
            )

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response(
                {"access": str(refresh.access_token), "refresh": str(refresh)}
            )

        except Exception as e:
            return Response({"error": str(e)}, status=400)


# User Profile View
class MyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        )


# User Views
class UserListCreateView(generics.ListCreateAPIView):
    """
    GET: List all users.
    POST: Create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve user details.
    PUT/PATCH: Update user details.
    DELETE: Delete a user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Profile Views
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Manuscript Views
class ManuscriptListCreateView(generics.ListCreateAPIView):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer


class ManuscriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manuscript.objects.all()
    serializer_class = ManuscriptSerializer


# Keyword Views
class KeywordListCreateView(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class KeywordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


# Feedback Question Views
class FeedbackQuestionListCreateView(generics.ListCreateAPIView):
    queryset = FeedbackQuestion.objects.all()
    serializer_class = FeedbackQuestionSerializer


class FeedbackQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackQuestion.objects.all()
    serializer_class = FeedbackQuestionSerializer


# Manuscript Feedback Preference Views
class ManuscriptFeedbackPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = ManuscriptFeedbackPreference.objects.all()
    serializer_class = ManuscriptFeedbackPreferenceSerializer


class ManuscriptFeedbackPreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManuscriptFeedbackPreference.objects.all()
    serializer_class = ManuscriptFeedbackPreferenceSerializer


# Feedback Response Views
class FeedbackResponseListCreateView(generics.ListCreateAPIView):
    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer


class FeedbackResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackResponse.objects.all()
    serializer_class = FeedbackResponseSerializer


# Author Settings Views
class AuthorSettingsListCreateView(generics.ListCreateAPIView):
    queryset = AuthorSettings.objects.all()
    serializer_class = AuthorSettingsSerializer


class AuthorSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuthorSettings.objects.all()
    serializer_class = AuthorSettingsSerializer


# Resource Views
class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


# Resource Interaction Views
class ResourceInteractionListCreateView(generics.ListCreateAPIView):
    queryset = ResourceInteraction.objects.all()
    serializer_class = ResourceInteractionSerializer


class ResourceInteractionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceInteraction.objects.all()
    serializer_class = ResourceInteractionSerializer


# Notification Views
class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


# Beta Reader Application Views
class BetaReaderListCreateView(CreateView):
    template_name = "Author_Dashboard/beta-reader-list.html"
    model = BetaReader
    fields = "__all__"


class BetaReaderListCreateView(ListView):
    model = BetaReader
    template_name = "beta-reader-list.html"


class BetaReaderApplicationListCreateView(generics.ListCreateAPIView):
    queryset = BetaReaderApplication.objects.all()
    serializer_class = BetaReaderApplicationSerializer


class BetaReaderApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BetaReaderApplication.objects.all()
    serializer_class = BetaReaderApplicationSerializer


@receiver(post_save, sender=User)  # Or CustomUser if you're using it
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, profile_created = Profile.objects.get_or_create(user=instance)

        # Assign permissions based on role
        if profile.role == "author":
            assign_role_permissions(profile, "author")
        elif profile.role == "beta_reader":
            assign_role_permissions(profile, "beta_reader")

def assign_role_permissions(profile, role):
    content_type = ContentType.objects.get_for_model(Manuscript)
    if role == "author":
        permission = Permission.objects.get(
            codename="can_view_author_dashboard", content_type=content_type
        )
    elif role == "beta_reader":
        permission = Permission.objects.get(
            codename="can_view_reader_dashboard", content_type=content_type
        )

    profile.user.user_permissions.add(permission)
