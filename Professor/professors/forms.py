from django import forms
from .models import Professor

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['profile_picture', 'name', 'university', 'research_interests', 
                 'email', 'h_index', 'famous_articles', 'google_scholar_url', 
                 'researchgate_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'research_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'h_index': forms.NumberInput(attrs={'class': 'form-control'}),
            'famous_articles': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'google_scholar_url': forms.URLInput(attrs={'class': 'form-control'}),
            'researchgate_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )
