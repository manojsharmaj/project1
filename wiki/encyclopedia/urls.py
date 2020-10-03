from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new",views.new_entry,name="new"),
    path("edit/<str:name>",views.edit,name="edit"),
    path("rand",views.rand,name="random"),
    path("<str:title>",views.entry,name="title")
]
