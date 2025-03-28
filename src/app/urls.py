"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.http import HttpResponse

import core.views as core_views

# required to override django default 404
handler404 = lambda *args, **kwargs: HttpResponse(status=404)

# rest api paths
# 's/' prefix for endpoints requiring an authorization header
urlpatterns = [
    # public endpoints
    path('health', core_views.health),
    path('anon_ask', core_views.anon_ask),

    # jwt secure endpoints
    path('s/health', core_views.secure_health),
    path('s/permissions', core_views.permissions),
    path('s/history', core_views.get_search_history),
    path('s/ask', core_views.post_search),
    path('s/chat/<str:chat_id>', core_views.get_chat_log)
]
