from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .filters import CommentFilter
from .forms import PostForm, CommentForm
from .models import Post, Comment


class PostList(generic.ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-date_creation'
    paginate_by = 10


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = self.object.comment_set.order_by('-date_creation').all()
        context['form'] = CommentForm()
        return context

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        context['comments'] = self.object.comment_set.order_by('-date_creation').all()
        context['form'] = form

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()

            context['form'] = CommentForm()
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostUpdate(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class UserPostList(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'user_posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user).order_by('-date_creation').all()
        return queryset


class UserPostCommentList(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'user_posts_comments.html'
    context_object_name = 'user_posts_comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(post__user=self.request.user).order_by('-date_creation').all()
        self.filterset = CommentFilter(self.request.GET, queryset)
        self.filterset.form.fields['post'].queryset = Post.objects.filter(user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def accept_comment(request, **kwargs):
    comment = Comment.objects.get(pk=int(kwargs['pk']))
    comment.is_accept = True
    comment.save()
    return redirect(request.META.get('HTTP_REFERER'))


def delete_comment(request, **kwargs):
    comment = Comment.objects.get(pk=int(kwargs['pk']))
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))
