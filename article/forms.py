from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from article.models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('topic', 'title', 'content', 'image', 'is_published')
        widgets = {
            'topic': forms.Select(),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            'is_published': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control bg-light'


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('topic', 'title', 'content', 'image', 'is_published')
        widgets = {
            'topic': forms.Select(),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            'is_published': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control bg-light'
