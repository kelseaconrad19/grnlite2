from django import forms
from .models import Manuscript, FeedbackTopic, Keyword, FeedbackQuestion, User, Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ManuscriptSubmissionForm(forms.ModelForm):
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 5,
        }),
        required=False,
        label="Keywords",
        help_text="Select relevant keywords."
    )
    feedback_topics = forms.ModelMultipleChoiceField(
        queryset=FeedbackTopic.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 5,
        }),
        required=False,  # Optional if authors can choose not to specify topics
        label=_("Feedback Topics"),
        help_text=_("Select the areas where you'd like beta readers to focus their feedback.")
    )
    class Meta:
        model = Manuscript
        fields = ['title', 'file_path', 'keywords', 'budget', 'beta_readers_needed', 'cover_art', 'nda_required', 'nda_file', 'plot_summary', 'feedback_topics']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'id_title', 
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
            'file_path': forms.FileInput(attrs={
                'class': 'form-control-file', 
                'id': 'id_file_path', 
                'style': 'padding: 5px; background-color: #f9f9f9; border-radius: 5px; margin-bottom: 20px;'
            }),
            'keywords': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input keyword-checkbox', 
                'id': 'id_keywords', 
                'style': 'margin: 10px 0 20px 0;'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'id_budget', 
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
            'beta_readers_needed': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'id_beta_readers_needed', 
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
            'cover_art': forms.FileInput(attrs={
                'class': 'form-control-file', 
                'id': 'id_cover_art', 
                'style': 'padding: 5px; background-color: #f9f9f9; border-radius: 5px; margin-bottom: 20px;'
            }),
            'nda_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input', 
                'id': 'id_nda_required', 
                'style': 'margin: 10px 0 20px 0;'
            }),
            'nda_file': forms.FileInput(attrs={
                'class': 'form-control-file', 
                'id': 'id_nda_file', 
                'style': 'padding: 5px; background-color: #f9f9f9; border-radius: 5px; margin-bottom: 20px;'
            }),
            'plot_summary': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'id_plot_summary', 
                'style': 'width: 100%; min-height: 150px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 20px;'
            }),
        }
        labels = {
                "title": _("Title"),
                'file_path': _('Manuscript File'),
                "keywords": _("Genre & Keywords"),
                "budget": _("Budget Per Reader"),
                "beta_readers_needed": _("Number of Beta Readers"),
                "cover_art": _("Cover Art (Optional)"),
                "nda_required": _("Do you want to require an NDA?"),
                "nda_field": _("NDA File (Optional)"),
                "plot_summary": _("Manuscript Plot Summary"),
                "feedback_topics": _("Feedback Topics")
            }
        help_texts = {
            'keywords': None,
            'nda_required': None,
            'feedback_topics': _("Select areas where you'd like detailed feedback from readers.")
        }

class BetaReaderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        feedback_topics = kwargs.pop("feedback_topics", None)  # Get the selected feedback topics
        super().__init__(*args, **kwargs)

        if feedback_topics:
            # Get all questions for the selected topics
            questions = FeedbackQuestion.objects.filter(topic__in=feedback_topics)

            # Dynamically add fields for each question
            for question in questions:
                self.fields[f"question_{question.id}"] = forms.CharField(
                    label=question.question_text,
                    widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
                    required=False,
                )
                
class AuthorRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']  # Map 'name' to 'first_name'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, role='author')  # Create profile with 'author' role
        return user


class ReaderRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name']  # Map 'name' to 'first_name'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, role='reader')  # Create profile with 'reader' role
        return user