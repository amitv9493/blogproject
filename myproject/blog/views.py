from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator
# Create your views here.

def post_list(request):

    # Pagination with 3 posts per page
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    posts = paginator.page(page_number)

    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts':posts})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
        status = Post.Status.PUBLISHED,
        slug=post,
        publish__year = year,
        publish__month= month,
        publish__day = day,
    )
    return render(request, 'blog/post/detail.html', {'post':post})

