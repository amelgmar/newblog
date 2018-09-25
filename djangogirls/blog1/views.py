from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Post
from .forms import PostForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render_to_response
from django.views.generic.edit import CreateView, DeleteView, UpdateView


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
    form_class = PostForm
    template_name = 'blog1/post_edit.html'
    model = Post

    def form_valid(self, form):
        form.instance.published_date = timezone.now()
        return super(EditPost, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog1:post_detail', kwargs={'pk': self.object.pk})


class DeletePost(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog1:post_list')

