import base64

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad
from django.shortcuts import redirect

from Crypto.Hash import SHA256
from users.models import User
from .models import Post
from .forms import PostCreateForm, PostReplyForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-last_modified']


class UnreadPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/unread_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(related_authority=self.request.user, is_read=False).order_by('-last_modified')


class ResolvedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/resolved_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(related_authority=self.request.user, is_resolved=True).order_by('-last_modified')


class UnresolvedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/unresolved_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(related_authority=self.request.user, is_resolved=False).order_by('-last_modified')


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_read and request.user == self.object.related_authority:
            self.object.is_read = True
            self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PostCreateForm
    template_name = 'posts/post_form.html'
    redirect_field_name = 'posts-home'

    def get_from_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=self.request.user)
        if user.check_password(password):
            pri_key = user.pri_key
            # print(pri_key)
            post = form.save()
            h = SHA256.SHA256Hash(bytes(post.content,'utf-8'))
            padded_key = pad(bytes(form.cleaned_data.get('password'), 'utf-8'), 16)
            private_key = AES.new(padded_key, AES.MODE_EAX, b'0').decrypt(pri_key)
            # print(private_key)
            key = RSA.importKey(private_key)
            # print(key)
            post.reply_sig = pkcs1_15.new(key).sign(h)
            post.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Validation failed, re-enter password!')
            return redirect('post-create',)

    def test_func(self):
        if self.request.user.is_authority:
            return False
        return True

    def handle_no_permission(self):
        messages.error(self.request, f'Permission denied!')
        return redirect('posts-home')


class ReplyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostReplyForm
    template_name = 'posts/post_form.html'
    redirect_field_name = 'posts-home'
    # model = Post
    # fields = ['reply_by_authority']

    def get_queryset(self):
        return Post.objects.filter(id=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.is_resolved = True
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=self.request.user)
        if user.check_password(password):
            pri_key = user.pri_key
            # print(pri_key)
            post = form.save()
            h = SHA256.SHA256Hash(bytes(post.content, 'utf-8'))
            padded_key = pad(bytes(form.cleaned_data.get('password'), 'utf-8'), 16)
            private_key = AES.new(padded_key, AES.MODE_EAX, b'0').decrypt(pri_key)
            # print(private_key)
            key = RSA.importKey(private_key)
            # print(key)
            post.reply_sig = pkcs1_15.new(key).sign(h)
            post.save()
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Validation failed, re-enter password!')
            return redirect('reply-post', pk=self.kwargs.get('pk'))

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.related_authority:
            return True
        return False

    def handle_no_permission(self):
        messages.error(self.request, f'Permission denied!')
        return redirect('posts-home')
