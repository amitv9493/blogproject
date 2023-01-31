from django.views.generic import ListView
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Create your views here.


def post_list(request):
    post_list = Post.published.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:

        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # print(posts.object_list)
    # print(posts.paginator.num_pages)
    # posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments':comments, 'form':form})


# class based views


class PostListView(ListView):
    # model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommands you {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']} \'s comments:{cd['comments']}"

            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to'],], fail_silently=False)

            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    return render(request, 'blog/post/share.html',context=context)

@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status = Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        comment.save()
    context={
        'form': form,
        'post':post,
        'comment':comment,
    }
    return render(request, 'blog/post/comment.html',context=context)


# @require_POST
# def post_comment(request, pk):
#     post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
#     comment = None
#     # A comment was posted
#     form = CommentForm(data=request.POST)
#     if form.is_valid():
#         # Create a Comment object without saving it to the database
#         comment = form.save(commit=False)
#         # Assign the post to the comment
#         comment.post = post
#         # Save the comment to the database
#         comment.save()
#     return render(request, 'blog/post/comment.html',
#                            {'post': post,'form':form, 'comment':comment})