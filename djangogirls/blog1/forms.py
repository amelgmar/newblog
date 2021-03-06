from django import forms
from django.urls import reverse_lazy

from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        is_edit = True if self.instance and self.instance.id else False

        self.helper = FormHelper()
        
        if is_edit:
            self.helper.form_action = reverse_lazy('blog1:post_edit', kwargs={'pk': self.instance.pk})
            valuebutton = 'edit post'
            cancel_button = Button('cancel', 'Cancel', css_class="btn btn-default",
                                   data_dismiss="modal", )
        else:
            self.helper.form_action = reverse('blog1:post_new')
            valuation = 'add post'
            cancel_button = HTML("""<a href="{% url "blog1:post_list" %}" class="cancelbutton">Cancel</a>""")

        self.helper.layout = Layout(
            Field('title', max_length=30, ),
            Field('text', rows="3", ),
            Div(

                cancel_button,
                Submit('submit', valuation, css_class='btn btn-primary'),
                # style="background: FAFAFA; padding: 20px;"
                css_class='form-group buttons'
            ),
        )

        self.helper.form_class = "js-post-update-form"
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
