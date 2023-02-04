from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing,name="landing"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    # path('Home/', views.PostList.as_view(), name="Home"),
    path('Home/', views.PostList, name="Home"),
    # path('blog/<slug:slug>/<int:pk>', views.PostDetail.as_view(), name="blog_detail"),
    path('blog/<slug:post>', views.PostDetail, name="blog_detail"),
    path('Profile/', views.Profile_user, name="Profile"),
    path('Bookmarks_add/<int:pid>', views.Bookmarks_add, name="Bookmarks_add"),
    path('Bookmarks/', views.Bookmarks_list, name="Bookmarks"),
    path('Delete_blog/<int:pid>', views.delete_post, name='Delete_blog'),
    path('Edit_blog/<slug:post_id>', views.UpdatePost, name='Edit_blog'),
    path('MyExperiences/', views.PostListFiltered.as_view(), name="MyExperiences"),
    path('logout/', views.logout_user, name="logout"),
    path('password_reset/', views.password_reset, name="password_reset"),
    # for forgot password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="MainApp/password_reset2.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="MainApp/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="MainApp/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="MainApp/password_reset_done.html"), name="password_reset_complete"),
    #
    path('create_blog/',views.create_blog, name="create_blog"),
    path('search/', views.search_func, name="search"),
    path('postComment',views.postComment,name="postComment"),
]