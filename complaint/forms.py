from django import forms

from complaint.models import Complaint


class ComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('text_moderator', 'status')
        # widgets = {
        #     'status': forms.Select(attrs={'summernote': {'width': '100%', 'height': '600px'}}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-light'
