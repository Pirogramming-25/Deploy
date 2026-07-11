from django.urls import path

from . import views

urlpatterns = [
    path("", views.idea_list, name="idea_list"),
    path("ideas/new/", views.idea_create, name="idea_create"),
    path("ideas/<int:pk>/", views.idea_detail, name="idea_detail"),
    path("ideas/<int:pk>/edit/", views.idea_update, name="idea_update"),
    path("ideas/<int:pk>/delete/", views.idea_delete, name="idea_delete"),
    path("ideas/<int:pk>/star/", views.toggle_star, name="toggle_star"),
    path("ideas/<int:pk>/interest/", views.change_interest, name="change_interest"),
    path("devtools/", views.devtool_list, name="devtool_list"),
    path("devtools/new/", views.devtool_create, name="devtool_create"),
    path("devtools/<int:pk>/", views.devtool_detail, name="devtool_detail"),
    path("devtools/<int:pk>/edit/", views.devtool_update, name="devtool_update"),
    path("devtools/<int:pk>/delete/", views.devtool_delete, name="devtool_delete"),
]