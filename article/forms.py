from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from article.models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('topic', 'title', 'content', 'image')
        # fields = '__all__'
        widgets = {
            'topic': forms.Select(),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            # 'content': SummernoteTextField(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
            # 'user': forms.HiddenInput(request.user.id)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control bg-light'
            # if field.label == 'Статья':
            #     self.fields[key] = SummernoteTextField(SummernoteWidget(attrs={'summernote': {'width': '100%',
            #                                                                                    'height': '600px'}}))

