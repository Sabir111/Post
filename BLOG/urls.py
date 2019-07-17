"""BLOG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.views import index, blog, post, search, post_delete, post_update, post_create, PostDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('blog/',blog,name='post-list'),
    path('search/',search,name='search'),
    path('post/<pk>/',post,name='post-detail'),
    path('create/', post_create, name='post-create'),
    path('post/<pk>/update/', post_update, name='post-update'),
    #path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
