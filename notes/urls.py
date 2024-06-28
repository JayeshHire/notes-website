from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("note/", views.NotesList.as_view(), name="index"),
    path("note/<int:pk>/", views.NoteDetail.as_view(), name="detail"),
    path("note/operation/create", views.note_form, name="create-note"),
    path("note/operation/delete/<int:note_id>", views.delete_note, name="delete-note"),
    path("note/operation/edit/<int:note_id>", views.edit_note, name="edit-note"),
    path("note/operation/edit-title/<int:note_id>", views.edit_note_title, name="edit-note-title"),
    path("note/operation/edit-content/<int:note_id>", views.edit_note_content, name="edit-note-content"),
    path("note/operation/edit-both/<int:note_id>", views.edit_note_both, name="edit-note-both"),
    path("todo/", views.TodoListView.as_view(), name="todo-list"),
    path("todo/<int:pk>", views.TodoListDetailView.as_view(), name="todo-detail"),
    path("todo/create-todo", views.create_todolist_form, name="create-todo"),
    path("todo/<int:todo_list_id>/operation/add_task", views.add_task, name="add-task"),
    path("todo/<int:todo_list_id>/operation/mark_task_completed", views.mark_task_as_completed, name="mark-task-completed"),
    path("todo/<int:todo_list_id>/operation/task_deletion", views.delete_task, name="task_deletion"),
    path("todo/<int:todo_list_id>/operation/todo_list_deletion", views.delete_todo_list, name="todo_list_deletion"),
]
