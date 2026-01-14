from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    """Форма создания поста"""
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Добавьте подпись к фото...'
            }),
            'image': forms.FileInput(attrs={
                'accept': 'image/*'
            })
        }
        labels = {
            'image': 'Изображение',
            'caption': 'Подпись'
        }


class CommentCreateForm(forms.ModelForm):
    """Форма создания комментария"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите комментарий...'
            })
        }
        labels = {
            'text': 'Комментарий'
        }

