from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostCreateForm, CommentCreateForm


class PostListView(ListView):
    """Список постов"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        # Показываем только одобренные посты
        return Post.objects.filter(moderation_status='approved').select_related('author')


class PostDetailView(DetailView):
    """Детальный просмотр поста"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(moderation_status='approved').select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем одобренные комментарии
        context['comments'] = self.object.comments.filter(
            moderation_status='approved'
        ).select_related('author').order_by('created_at')
        context['comment_form'] = CommentCreateForm()
        return context


class PostCreateView(CreateView):
    """Создание нового поста"""
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Пост успешно создан и отправлен на модерацию!')
        return super().form_valid(form)


@login_required
def add_comment(request, pk):
    """Добавление комментария к посту"""
    post = get_object_or_404(Post, pk=pk, moderation_status='approved')
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен и отправлен на модерацию!')
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = CommentCreateForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': form,
        'comments': post.comments.filter(moderation_status='approved')
    })

