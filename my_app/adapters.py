from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Add custom logic here, e.g., populate additional fields
        user.some_custom_field = "default_value"
        user.save()
        return user
