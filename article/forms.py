from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from article.models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('topic', 'title', 'content', 'image', 'is_moderated')
        widgets = {
            'topic': forms.Select(),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            'is_moderated': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_moderated':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control bg-light'


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('moderate_comment', 'topic', 'title', 'content', 'image', 'is_moderated')
        widgets = {
            'topic': forms.Select(),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            'is_moderated': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_moderated':
                field.widget.attrs['class'] = 'form-check-input'
            elif name == 'moderate_comment':
                field.widget.attrs['readonly'] = True
                field.widget.attrs['class'] = 'form-control bg-light'
                field.widget.attrs['rows'] = 5
            else:
                field.widget.attrs['class'] = 'form-control bg-light'
