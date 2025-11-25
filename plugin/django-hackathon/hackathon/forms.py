
from django import forms
from django.db.models import Q
from django.contrib.auth.models import User

from .models import (
    Hackathon,
    HackathonPrize,
    HackathonSponsor,
    get_organization_model,
    HAS_ORGANIZATION,
)

# Get Organization model if available
Organization = get_organization_model() if HAS_ORGANIZATION else None

# Try to get Repo model (might be in website app)
Repo = None
if HAS_ORGANIZATION:
    try:
        from django.apps import apps
        # Try common app names where Repo model might exist
        for app_name in ['website', 'blt', 'main', 'core']:
            try:
                Repo = apps.get_model(app_name, 'Repo')
                break
            except LookupError:
                continue
    except ImportError:
        pass



class HackathonForm(forms.ModelForm):
    new_repo_urls = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": (
                    "w-full rounded-lg border-gray-300 shadow-sm focus:border-[#e74c3c] "
                    "focus:ring focus:ring-[#e74c3c] focus:ring-opacity-50"
                ),
                "placeholder": "https://github.com/owner/repo1\nhttps://github.com/owner/repo2",
            }
        ),
        label="New Repository URLs",
        help_text="Enter GitHub repository URLs (one per line) to add new repositories to this hackathon",
    )

    class Meta:
        model = Hackathon
        # Build fields list conditionally based on available models
        base_fields = [
            "name",
            "description",
            "start_time",
            "end_time",
            "banner_image",
            "rules",
            "registration_open",
            "max_participants",
            "sponsor_note",
            "sponsor_link",
        ]
        # Add organization OR owner field based on availability
        if HAS_ORGANIZATION:
            fields = ["name", "description", "organization"] + base_fields[2:] + ["repositories"]
        else:
            fields = ["name", "description", "owner"] + base_fields[2:]
            
        base_input_class = (
            "w-full rounded-lg border-gray-300 shadow-sm focus:border-[#e74c3c] "
            "focus:ring focus:ring-[#e74c3c] focus:ring-opacity-50"
        )
        
        # Build widgets conditionally
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": base_input_class,
                    "placeholder": "Enter hackathon name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": base_input_class,
                    "placeholder": "Describe your hackathon...",
                }
            ),
            "rules": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": base_input_class,
                    "placeholder": "Enter hackathon rules...",
                }
            ),
            "sponsor_note": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": base_input_class,
                    "placeholder": ("Provide information about sponsorship opportunities " "for this hackathon"),
                }
            ),
            "sponsor_link": forms.URLInput(
                attrs={
                    "class": base_input_class,
                    "placeholder": "https://example.com/sponsor",
                }
            ),
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": base_input_class,
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": base_input_class,
                }
            ),
            "max_participants": forms.NumberInput(
                attrs={
                    "class": base_input_class,
                    "placeholder": "Enter maximum number of participants",
                }
            ),
            "registration_open": forms.CheckboxInput(
                attrs={
                    "class": ("h-5 w-5 text-[#e74c3c] focus:ring-[#e74c3c] " "border-gray-300 rounded"),
                }
            ),
        }
        
        # Add organization or owner widget based on availability
        if HAS_ORGANIZATION:
            widgets["organization"] = forms.Select(
                attrs={
                    "class": base_input_class,
                }
            )
            widgets["repositories"] = forms.SelectMultiple(
                attrs={
                    "class": base_input_class,
                    "size": "5",
                }
            )
        else:
            widgets["owner"] = forms.Select(
                attrs={
                    "class": base_input_class,
                }
            )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if HAS_ORGANIZATION and Organization and user:
            # Handle organization field
            if hasattr(Organization, 'admin') and hasattr(Organization, 'managers'):
                self.fields["organization"].queryset = Organization.objects.filter(
                    Q(admin=user) | Q(managers=user)
                ).distinct()
            elif hasattr(Organization, 'owner'):
                self.fields["organization"].queryset = Organization.objects.filter(owner=user)
            else:
                self.fields["organization"].queryset = Organization.objects.all()

            # Handle repositories field if available
            if Repo and "repositories" in self.fields:
                if self.instance.pk and hasattr(self.instance, 'organization') and self.instance.organization:
                    self.fields["repositories"].queryset = Repo.objects.filter(organization=self.instance.organization)
                else:
                    self.fields["repositories"].queryset = Repo.objects.none()
        
        elif not HAS_ORGANIZATION and user:
            # Handle owner field
            self.fields["owner"].initial = user
            if not user.is_superuser:
                # Non-superusers can only set themselves as owner
                self.fields["owner"].queryset = User.objects.filter(id=user.id)
            else:
                # Superusers can select any active user
                self.fields["owner"].queryset = User.objects.filter(is_active=True)

    def clean_new_repo_urls(self):
        """Validate and parse new repository URLs."""
        new_repo_urls = self.cleaned_data.get("new_repo_urls", "")
        if not new_repo_urls:
            return []

        # Only validate repo URLs if Repo model is available
        if not Repo:
            return []

        urls = [url.strip() for url in new_repo_urls.strip().split("\n") if url.strip()]
        validated_urls = []

        for url in urls:
            # Basic validation for GitHub URLs
            if not url.startswith("https://github.com/"):
                raise forms.ValidationError(f"Invalid GitHub URL: {url}. URLs must start with https://github.com/")

            # Check if URL has the correct format
            parts = url.replace("https://github.com/", "").split("/")
            if len(parts) < 2:
                raise forms.ValidationError(
                    f"Invalid GitHub URL format: {url}. Expected format: https://github.com/owner/repo"
                )

            validated_urls.append(url)

        return validated_urls

    def clean_repositories(self):
        repositories = self.cleaned_data.get("repositories")
        organization = self.cleaned_data.get("organization")

        # Only validate if both Repo model and organization are available
        if repositories and organization and Repo:
            # Ensure all repositories belong to the selected organization
            valid_repos = Repo.objects.filter(id__in=[r.id for r in repositories], organization=organization)
            return valid_repos
        return repositories

    def save(self, commit=True):
        """Save the hackathon and create new repositories if provided."""
        instance = super().save(commit=False)

        if commit:
            instance.save()
            # Save many-to-many relationships
            self.save_m2m()

            # Create and add new repositories only if Repo model is available
            new_repo_urls = self.cleaned_data.get("new_repo_urls", [])
            if new_repo_urls and Repo and hasattr(instance, 'organization') and instance.organization:
                organization = instance.organization
                for repo_url in new_repo_urls:
                    # Extract repo name from URL
                    repo_name = repo_url.rstrip("/").split("/")[-1]

                    # Check if repo already exists
                    existing_repo = Repo.objects.filter(repo_url=repo_url).first()
                    if existing_repo:
                        # Add existing repo to hackathon
                        instance.repositories.add(existing_repo)
                    else:
                        # Create new repo
                        new_repo = Repo.objects.create(
                            name=repo_name,
                            repo_url=repo_url,
                            organization=organization,
                        )
                        instance.repositories.add(new_repo)

        return instance


class HackathonSponsorForm(forms.ModelForm):
    class Meta:
        model = HackathonSponsor
        # Build fields list conditionally based on available models
        base_fields = ["sponsor_name", "sponsor_level", "logo", "website"]
        if HAS_ORGANIZATION:
            fields = ["organization"] + base_fields
        else:
            fields = base_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add organization field conditionally if Organization model exists
        if HAS_ORGANIZATION and Organization:
            if 'organization' not in self.fields:
                self.fields['organization'] = forms.ModelChoiceField(
                    queryset=Organization.objects.all(),
                    required=False,
                    empty_label="Select organization (optional)",
                    help_text="Link to organization if available"
                )


class HackathonPrizeForm(forms.ModelForm):
    class Meta:
        model = HackathonPrize
        fields = ["position", "title", "description", "value", "sponsor"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full rounded-md border-gray-300 shadow-sm focus:border-[#e74c3c] focus:ring focus:ring-[#e74c3c] focus:ring-opacity-50",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        hackathon = kwargs.pop("hackathon", None)
        super().__init__(*args, **kwargs)

        # Filter sponsors to only show those associated with this hackathon
        if hackathon:
            self.fields["sponsor"].queryset = HackathonSponsor.objects.filter(hackathon=hackathon)
        else:
            self.fields["sponsor"].queryset = HackathonSponsor.objects.none()
