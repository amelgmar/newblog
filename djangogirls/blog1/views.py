from crispy_forms.utils import render_crispy_form
from django.http import QueryDict, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from djangogirls.blog1 import forms
from .models import Post
from .forms import PostForm, MailForm

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render_to_response
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.context_processors import csrf
import json


class ListPost(generic.ListView):
    template_name = 'blog1/post_list.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class DetailPost(generic.DetailView):
    template_name = 'blog1/post_detail.html'
    model = Post


class NewPost(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog1/post_edit.html'

    def form_valid(self, form):
        form.instance.published_date = timezone.now()
        form.instance.author = self.request.user
        return super(NewPost, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog1:post_detail', kwargs={'pk': self.object.pk})


class EditPost(generic.UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'form_is_valid': True,
            'id': form.instance.id,
            'title': form.instance.title,
            'text': form.instance.text
        }

        return JsonResponse(data)

    def form_invalid(self, form):
        form_html = render_crispy_form(form, context=csrf(self.request))
        return JsonResponse({'html_form': form_html})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        ct = self.get_context_data()
        form_html = render_crispy_form(ct["form"], context=csrf(self.request))
        return JsonResponse({'html_form': form_html})


class deletepost(generic.DeleteView):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()

        data = {'delete': 'ok'}
        return JsonResponse(data)

    def get(self, request, *args, **kwargs):
        conte = {'post': self.get_object()}
        form_html = render_to_string('blog1/post_delete.html',
                                     conte,
                                     request=request, )

        return JsonResponse({'html_form': form_html})


class MailPost(generic.FormView):
    form_class = MailForm
    template_name = 'blog1/post_mail.html'
    success_url = reverse_lazy('blog1:post_list')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['feedback']
        destination = form.cleaned_data['destination']

        email = EmailMessage(subject, message, to=[destination])
        email.send()
        return super(MailPost, self).form_valid(form)
