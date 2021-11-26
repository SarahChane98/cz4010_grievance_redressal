from django import forms
from .models import Post
from users.models import User


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'related_authority']
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_authority'].queryset = self.fields['related_authority'].queryset.filter(is_authority=True)

