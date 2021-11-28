from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Post
        fields = ['title', 'content', 'related_authority']
        # exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_authority'].queryset = self.fields['related_authority'].queryset.filter(is_authority=True)


class PostReplyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Post
        fields = ['reply_by_authority']
        # exclude = ('password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
