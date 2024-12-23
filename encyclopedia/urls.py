from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>/', views.wiki_entry, name='wiki_page'),
    path('wiki/', views.querry_entry, name="querry"),
    path("newpage", views.new_page, name="newpage"),
    path("edit", views.edit_page, name="edit"),
    path("save", views.save, name="save"),
    path("random", views.randoom, name="random"),
]
