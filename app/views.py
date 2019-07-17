from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DeleteView


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

# Create your views here.
from django.urls import reverse
from lxml.objectify import annotate
# from lxml.html._diffcommand import annotate
from app.forms import CommentForm, PostForm
from app.models import Post, Author, PostView
from marketing.models import Signup

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset
    }
    return render(request,'search_results.html',context)


def get_category_count():
        queryset = Post.objects.values('category__title').annotate(Count('category__title'))
        return queryset

def index(request):
        featured = Post.objects.filter(featured = True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        if request.method == 'POST':
            email = request.POST["email"]
            new_signup = Signup()
            new_signup.email = email
            new_signup.save()
        context = {
            'object_list' : featured,
            'latest' : latest
        }
        return render(request,'index.html',context)

def blog(request):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        post_list = Post.objects.all()
        paginator = Paginator(post_list,4)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)
        try:
            paginatod_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginatod_queryset = paginator.page(1)
        except EmptyPage:
            paginatod_queryset = paginator.page(paginator.num_pages)

        context = {
            'queryset':paginatod_queryset,
            'most_recent':most_recent,
            'page_request_var':page_request_var,
            'category_count':category_count
        }
        return render(request,'blog.html',context)

def post(request,pk):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        post = get_object_or_404(Post,pk=pk)
        if request.user.is_authenticated:
            PostView.objects.get_or_create(user=request.user,post=post)
        form = CommentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.instance.user = request.user
                form.instance.post = post
                form.save()
                return redirect(reverse('post-detail',kwargs={
                    'pk':post.pk
                }))
        context = {
            'form':form,
            'post':post,
            'most_recent': most_recent,
            'category_count': category_count
        }
        return render(request,'post.html',context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None ,request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk':form.instance.pk
            }))
    context = {
        'title':title,
        "form":form
    }
    return render(request,"post_create.html",context)

def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post,pk=pk)
    form = PostForm(request.POST or None ,request.FILES or None , instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk':form.instance.pk
            }))
    context = {
        'title':title,
        "form":form
    }
    return render(request,"post_create.html",context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'

def post_delete(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect(reverse("post-list"))
