from django import forms

from .models import Music

class PostForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            "title",
            "tag_name",
            "audio_file_name",
             ]