from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post

# Defines count of posts on page
POSTS_ON_PAGE = 5


def post_list(request):
    """View for index page. Render html template."""
    return render(request, 'index.html')


def get_page(number: int):
    """Receive page with post from db and return it.

    number: number of page, that must be returned
    POST_ON_PAGE: number of posts, that can be shown on page
    """
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(queryset, POSTS_ON_PAGE)
    try:
        page = paginator.page(number)
    except PageNotAnInteger:
        # Deliver first page
        page = paginator.page(1)
    except EmptyPage:
        # If page number is out of range, deliver last page
        page = paginator.page(paginator.num_pages)
    return page


def get_page_number(request) -> int:
    """Process page_num parameter in GET request."""
    try:
        return int(request.GET.get('page'))
    except TypeError:
        print(
            'Error: failed to parse GET arguments. '
            'Cannot convert page_num parameter to int.'
        )
        # Return error code
        return -1


def empty_response():
    """Shortcut for empty HttpResponse.

    In accordance with DRY principles.
    """
    return HttpResponse("", content_type="text/html")


def page_out_of_bound(requested_page: int, current_page: int):
    """Check, that requested page is not out of bound.

    If page is out of bound, then there are no more pages available.
    """
    return requested_page > current_page


def render_blog_page(request):
    """Process GET request and put back next blog page.

    Blog page is sent in plain html format.

    There is only one parameter in GET request:
    page: number of the requested page
    """
    if request.method == 'GET':
        
        requested_page_num = get_page_number(request)
        if requested_page_num == -1:
            return empty_response()

        page = get_page(requested_page_num)

        if page_out_of_bound(requested_page_num, current_page=page.number):
            # If there are no more pages, return blank response
            return empty_response()
        return render(
            request, 'blog_page.html', {'post_list': page}
        )
    return empty_response()


class PostDetail(generic.DetailView):
    """Full post view."""

    model = Post
    template_name = 'post_detail.html'