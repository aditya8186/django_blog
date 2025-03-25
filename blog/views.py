from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost, Blogger, Comment
from .forms import UserRegistrationForm, BlogPostForm, CommentForm
from django.db.models import Q

def index(request):
    """View function for home page of site."""
    num_posts = BlogPost.objects.all().count()
    num_bloggers = Blogger.objects.all().count()
    num_comments = Comment.objects.all().count()
    latest_posts = BlogPost.objects.all().order_by('-post_date')[:3]  # Get the 3 most recent posts
    
    context = {
        'num_posts': num_posts,
        'num_bloggers': num_bloggers,
        'num_comments': num_comments,
        'latest_posts': latest_posts,
    }
    return render(request, 'index.html', context=context)

class BlogPostListView(ListView):
    model = BlogPost
    paginate_by = 9
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogpost_list'

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class BloggerListView(ListView):
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'blogger_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(bio__icontains=search_query)
            )
        
        return queryset.order_by('user__username')

class BloggerDetailView(DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogger = self.get_object()
        context['blog_posts'] = BlogPost.objects.filter(author=blogger).order_by('-post_date')
        return context

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog_post = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-detail', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogpost'] = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        return context

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Blogger instance for the new user
            Blogger.objects.create(
                user=user,
                bio="Welcome to my blog! I'm excited to share my thoughts and experiences."
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_comment(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'blog_post': blog_post})

class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = Blogger.objects.get(user=self.request.user)
        return super().form_valid(form)
