from django.urls import path
from . import views
urlpatterns=[
    path('',views.blog_page,name="blogname"),
    path('generate_blog/',views.generate_blog,name="generateblog")
]