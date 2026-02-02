from .models import Artwork, ProgressPhoto, PrivateComment, Challenge, TechniqueChoices
from django import forms

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'final_image', 'technique', 'video_timelapse', 'start_date', 'end_date']
        
ProgressPhotoFormSet = forms.inlineformset_factory(
    Artwork,
    ProgressPhoto,
    fields=['image', 'order'],
    extra=3,
    can_delete=True
)

class PrivateCommentForm(forms.ModelForm):
    class Meta:
        model = PrivateComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Describe your challenge...'}),
        }
        
class ArtworkFilterForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by title...'}))
    technique = forms.ChoiceField(choices=[('', 'All techniques')] + TechniqueChoices.choices, required=False)
    start_month = forms.IntegerField(required=False, min_value=1, max_value=12, widget=forms.NumberInput(attrs={'placeholder': 'Month (1-12)'}))
    start_year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Year (example: 2024)'}))