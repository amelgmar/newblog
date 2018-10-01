from django import forms

from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class PostForm(forms.ModelForm):
    helper = FormHelper()
    helper.layout = Layout(
        'title',
        'text',
        FormActions(
            Submit('add ', 'add post', css_class="btn-primary"),
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'text',)


class MailForm(forms.Form):
    subject = forms.CharField(max_length=30, required='False')
    feedback = forms.CharField(widget=forms.Textarea)
    destination = forms.EmailField()
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('subject', css_class='input-xlarge'),
        Field('feedback', rows="3", css_class='input-xlarge'),
        Field('destination', css_class='input-xlarge', placeholder="mail"),

        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
        )
    )

    def clean_destination(self):
        data = self.cleaned_data['destination']
        domain = data.split('@')[1]
        domain_list = 'softcatalyst.com'
        if domain == domain_list:
            raise forms.ValidationError("Please enter an Email Address with a valid domain")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
