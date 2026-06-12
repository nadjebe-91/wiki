from django.urls import path

from . import views
app_name ="wiki"
urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search/", views.search_entry, name="search_entry"),
    path("wiki/create/", views.create_page, name="create_page"),
    path("wiki/<str:title>/edit/", views.update_entry, name="update_entry"),
    path("wiki/random", views.random_entry, name="random_entry")
]
