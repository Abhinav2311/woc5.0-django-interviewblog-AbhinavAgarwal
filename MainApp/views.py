from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import check_password
from .forms import BlogCreateForm, ProfileForm
from .models import Post, Profile, BlogComment
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def landing(request):
    return render(request, 'MainApp/landing.html')


# @login_required(login_url='login')
# def Home(request):
#     return render(request, 'MainApp/Home.html')

#Creating home using class based view
# class PostList(LoginRequiredMixin, ListView):
#     login_url = 'login'
#     model = Post
#     queryset = Post.objects.order_by('-updated_at')
#     template_name = 'MainApp/Home.html'

@login_required(login_url='login')
def PostList(request):
    blogs = Post.objects.all().order_by('-updated_at')
    paginator = Paginator(blogs, 4)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = {'blogs':blogs,'page': page, 'post_list': post_list}
    return render(request,'MainApp/Home.html',context)


@login_required(login_url='login')
def PostDetail(request,post):
    post = get_object_or_404(Post, slug=post)
    books = bool
    if post.bookmarks.filter(id=request.user.id).exists():
        books = True
    comments = BlogComment.objects.filter(post=post).order_by('-timeStamp')

    context = {'post':post, 'books':books, 'comments':comments}
    return render(request,'MainApp/Blog_detail.html', context)
    
# class PostDetail(LoginRequiredMixin, DetailView):
#     login_url = 'login'
#     model = Post
#     template_name = 'MainApp/Blog_detail.html'
 

class PostListFiltered(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Post
    queryset = Post.objects.order_by('-updated_at')
    template_name = 'MainApp/MyExperiences.html'


@login_required(login_url='login')
def Profile_user(request):
    current = request.user
    try:
        profile = request.user.profile
    except:
        profile = Profile.objects.create(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES ,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, ('Your profile has been successfully updated! '))
    context = {'form':form}
    return render(request, 'MainApp/Profile.html', context)


@login_required(login_url='login')
def Bookmarks_add(request,pid):
    post = Post.objects.get(sno=pid)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
        messages.success(request, ('Blog successfully removed from bookmarks!'))
    else:
        post.bookmarks.add(request.user)
        messages.success(request, ('Blog successfully added to bookmarks!'))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # return render(request, 'MainApp/Bookmarks.html')

@login_required(login_url='login')
def Bookmarks_list(request):
    new = Post.objects.all().filter(bookmarks=request.user).order_by('-updated_at')
    return render(request,'MainApp/Bookmarks.html',{'new':new})

# @login_required(login_url='login')
# def MyExperiences(request):
#     return render(request, 'MainApp/MyExperiences.html')

def register_user(request):
    if request.method == 'POST':
        # Get Post Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        # Checking if username already exists
        userex = User.objects.filter(username=username)
        if userex.exists():
            messages.error(request,'Username already exists!! Enter a unique username.')
            return redirect('register')

        emailex = User.objects.filter(email=email)
        if emailex.exists():
            messages.error(request,'This email address is already registered!! Please Login.')
            return redirect('login')

        # Checks
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters !!")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must only contain letters and numbers !!")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Confirm password do not match with password !!")
            return redirect('register')

        
        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        user = authenticate(username=username, password=pass1)
        login(request,user)
        messages.success(request,'Your account has been successfully created !!')
        return redirect('Home')

    else:
        return render(request, 'MainApp/register.html')


def login_user(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfully logged in !!")
            return redirect('Home')
        else:
            messages.error(request,("Invalid Credentials!! Please try again or register."))
            return redirect('login')
    else:
        return render(request, 'MainApp/login.html')

def logout_user(request):
    logout(request)
    return redirect('landing')

###
@login_required(login_url='login')
def password_reset(request):
    if request.method == 'POST':
        pass3 = request.POST['pass3']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        userpassword = request.user.password
        current_user = request.user.id
        userobj = User.objects.get(id=current_user)
        matchcheck = check_password(pass3,userpassword)

        # Checks
        if matchcheck:
            if pass1 != pass2:
                messages.error(request, "Confirm new password do not match with new password !!")
                return redirect('password_reset')
            else:
                userobj.set_password(pass1)
                userobj.save()
                messages.success(request, "Password changed successfully !!")
                user = authenticate(username=userobj.username, password=pass1)
                login(request,user)
                return redirect('Home')
        else:
            messages.error(request, "Existing current password do not match with entered current password !!")
            return redirect('password_reset')


    else:
        return render(request, 'MainApp/Password_reset.html')

    
@login_required(login_url='login')
def create_blog(request):
    form = BlogCreateForm()
    if request.method == 'POST':
        form = BlogCreateForm(request.POST)
        #
        form.instance.author = request.user
        #
        if form.is_valid():
            form.save()
            form = BlogCreateForm()
            messages.success(request, "Your Interview Blog has been successfully posted !!")
            return redirect('Home')
    context = {'form':form}
    return render(request, 'MainApp/Blog_create.html',context)

#Delete Post
@login_required(login_url='login')
def delete_post(request, pid):
    post = get_object_or_404(Post, sno=pid)
    # context = {'post': post}  
    # if request.method == 'GET':
    #     return render(request, 'blog/post_confirm_delete.html',context)
    # elif request.method == 'POST':
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Your Blog has been successfully deleted!')
    else:
        messages.error(request, 'Only Blog owners can delete their blog!')
    return redirect('Home')

#Edit Post
@login_required(login_url='login')
def UpdatePost(request,post_id):
    post = Post.objects.get(slug=post_id)
    if post.author == request.user:
        if request.method != 'POST':
            form = BlogCreateForm(instance=post)

        else:
            form = BlogCreateForm(instance=post, data=request.POST) 
            if form.is_valid():
                form.save()
                messages.success(request, "Your Blog updated successfully!")
                return redirect('Home')

        context = {'post': post,'form': form}
        return render(request, 'MainApp/Blog_update.html', context)
    else:
        messages.error(request, 'Only Blog owners can edit their blog!')
        return redirect('Home')

@login_required(login_url='login')
def search_func(request):
    search = request.GET['search']
    resultTitle = Post.objects.filter(title__icontains=search)
    resultCompany = Post.objects.filter(company__icontains=search)
    resultOffer = Post.objects.filter(offer_type__icontains=search)
    resultProfile = Post.objects.filter(job_profile__icontains=search)
    resultContent = Post.objects.filter(content__icontains=search)
    results = resultTitle.union(resultCompany).union(resultOffer).union(resultProfile).union(resultContent).order_by('-updated_at')
    context = {'results':results}
    if results.count() == 0:
        messages.success(request, "No search results found for " + search + "! Try different keyword")
    else:
        messages.success(request, "Search results for " + search + " :-")
    return render(request,'MainApp/search.html', context)

@login_required(login_url='login')
def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)

        comment = BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully!")
    
    return redirect(f"/blog/{post.slug}")
    
