from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path(route="chat/", view=include("chat.urls")),
    path(route="admin/", view=admin.site.urls),
]
