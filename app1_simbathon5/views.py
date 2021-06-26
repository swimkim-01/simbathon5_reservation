from django.db.models.query_utils import Q
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .models import FAQ, Post, Comment

# Create your views here.

def showmain(request):
    return render(request, 'app1_simbathon5/main.html')

def frequentlyaskedquestions(request):
    faqs = FAQ.objects.all()
    return render(request, 'app1_simbathon5/FAQ.html',{'faqs':faqs})

def book(request):
    return render(request, 'app1_simbathon5/book.html')
    
def main(request):
    return render(request, 'app1_simbathon5/main.html')

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'app1_simbathon5/detail.html', {'post' : post,'comments':all_comments})

def post(request):
    posts = Post.objects.all()
    return render(request, "app1_simbathon5/post.html", {'posts':posts})


def new(request):
    return render(request, 'app1_simbathon5/new.html')

def create(request):
    new_post = Post()
    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.pub_date = timezone.now()
    new_post.body = request.POST['body']
    new_post.image = request.FILES.get('image')
    new_post.save()
    return redirect('app1_simbathon5:detail',new_post.id)

def edit(request, id):
    edit_post = Post.objects.get(id =id)
    return render(request, 'app1_simbathon5/edit.html', {'post': edit_post})

def update(request, id):
    update_post = Post.objects.get(id=id)
    update_post.title=request.POST['title']
    update_post.writer=request.user
    update_post.pub_date=timezone.now()
    update_post.body = request.POST['body']
    if request.FILES.get('image'):
        update_post.image = request.FILES.get('image')
    update_post.save()
    return redirect('app1_simbathon5:detail', update_post.id)

def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('app1_simbathon5:post')

def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        current_user = request.user
        comment_content = request.POST.get('content')
        Comment.objects.create(content=comment_content, writer=current_user, post=post)
    return redirect('app1_simbathon5:detail', post_id)
