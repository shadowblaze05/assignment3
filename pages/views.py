from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from pages.models import Announcement
from django.shortcuts import redirect


# Create your views here.
def home(request):
    ctx = {"title": "Home", "features": ["Django", "Templates", "Static files"]}
    return render(request, "home.html", ctx)

def about(request):
    return render(request, "about.html", {"title": "About"})

def hello(request, name):
    return render(request, "hello.html", {"name": name})

def gallery(request):
    # Assume images placed in pages/static/img/
    images = ["img1.jpg", "img2.jpg", "img3.jpg"]
    return render(request, "gallery.html", {"images": images})

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

def announcement_list(request):
    # Model.objects.all()
    posts = Announcement.objects.all().prefetch_related('comments') 
    context = {
        'posts': posts,
        'title': 'Posts',
    }
    return render(request, 'announcement_list.html', context)

def admin(request):
    return redirect('/admin/')

def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        if not title or not body:
            return HttpResponseBadRequest("Title and body are required.")
        Announcement.objects.create(title=title, body=body)
        return redirect('announcement_list')
    return render(request, 'post_form.html')

def post_detail(request, pk):
    post = Announcement.objects.get(pk=pk)
    comments = Announcement.objects.prefetch_related('comments')
    return render(request, 'post_detail.html', {'post': post})

def post_update(request, pk):
    post = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title') or post.title
        post.body = request.POST.get('body') or post.body
        post.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'post_form.html', {'post': post})
def post_delete(request, pk):
    post = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})