from django.urls import path

from blog import views


urlpatterns = [
    path('', views.post_list, name='home'),
    path('get_page/', views.render_blog_page, name='get_page'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
