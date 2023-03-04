from django import forms

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField

from .models import Post, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=128)
    category = forms.ChoiceField(label='Category', choices=Post.CATEGORIES)
    content = forms.CharField(label='Content', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
        ]


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = [
            'text',
        ]
