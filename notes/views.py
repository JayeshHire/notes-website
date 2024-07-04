from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.views import generic
from .models import Note, TodoList, Todo
from . import user_view
from django.contrib.auth.models import User


# Create your views here.


class NotesList(generic.ListView):
    model = Note
    context_object_name = "note_list"
    template_name = "notes/note_list.html"


class NoteDetail(generic.DetailView):
    model = Note
    context_object_name = "note"
    template_name = "notes/note_detail.html"


class TodoListView(generic.ListView):
    model = TodoList
    context_object_name = "todo_list"
    template_name = "notes/todo_list.html"


class TodoListDetailView(generic.DetailView):
    model = TodoList
    context_object_name = "todo"
    template_name = "notes/todo_detail.html"


# get note list for user
@user_view.authorized
def user_note_list(request):
    username = request.session["username"]
    user = User.objects.get(username=username)
    note_list = user.note_set.all()
    context = {
        "note_list": note_list
    }
    return render(request, "notes/note_list.html", context)


# get note detail for user
@user_view.authorized
def user_note_detail(request, note_id):
    if not User.objects.filter(note__id=note_id).exists() or \
            User.objects.filter(note__id=note_id)[0].username != request.session["username"]:
        return HttpResponseRedirect(reverse("notes:note-list"))
    note = Note.objects.get(pk=note_id)
    context = {
        "note": note
    }
    return render(request, "notes/note_detail.html", context)


# creating a new note
@user_view.authorized
def note_form(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        username = request.session['username']
        user = User.objects.get(username=username)
        user.note_set.create(title=title, content=content)
        return HttpResponseRedirect(reverse("notes:note-list"))
    return render(request, "notes/note_form.html")


# Deleting a note
@user_view.authorized
def delete_note(request, note_id):
    username = request.session['username']
    user = User.objects.get(username=username)
    try:
        note = user.note_set.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse("notes:note-list"))

    if request.method == 'POST':
        yes_or_no = request.POST['surety']
        if yes_or_no == 'YES':
            note.delete()
        return HttpResponseRedirect(reverse("notes:note-list"))

    context = {
        "note": note
    }
    return render(request, "notes/note_deletion.html", context)


# EDIT note title
@user_view.authorized
def edit_note_title(request, note_id):
    user = User.objects.get(username=request.session["username"])
    try:
        note = user.note_set.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse("notes:note-list"))

    if request.method == 'POST':
        new_title = request.POST['title']
        note.title = new_title
        note.save()
        return HttpResponseRedirect(reverse("notes:note-list"))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-title.html", context)


# edit note content
@user_view.authorized
def edit_note_content(request, note_id):
    user = User.objects.get(username=request.session["username"])
    try:
        note = user.note_set.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse("notes:note-list"))

    if request.method == 'POST':
        new_content = request.POST['content']
        note.content = new_content
        note.save()
        return HttpResponseRedirect(reverse("notes:note-list"))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-content.html", context)


# edit note options
@user_view.authorized
def edit_note(request, note_id):
    user = User.objects.get(username=request.session["username"])
    try:
        note = user.note_set.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('notes:note-list'))

    if request.method == 'POST':
        edit_option = request.POST['edit-opt']
        if edit_option == 'title':
            return HttpResponseRedirect(reverse('notes:edit-note-title', args=(note_id,)))
        elif edit_option == 'content':
            return HttpResponseRedirect(reverse('notes:edit-note-content', args=(note_id,)))
        else:
            return HttpResponseRedirect(reverse('notes:edit-note-both', args=(note_id,)))

    context = {
        "note": note
    }
    return render(request, 'notes/note-edit.html', context=context)


# edit note both
@user_view.authorized
def edit_note_both(request, note_id):
    user = User.objects.get(username=request.session["username"])
    try:
        note = user.note_set.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('notes:note-list'))

    if request.method == 'POST':
        new_title = request.POST['title']
        new_content = request.POST['content']
        note.title = new_title
        note.content = new_content
        note.save()
        return HttpResponseRedirect(reverse("notes:note-detail", args=(note_id,)))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-both.html", context)


# Creating a new todo list
@user_view.authorized
def create_todolist_form(request):
    user = User.objects.get(username=request.session['username'])
    if request.method == 'POST':
        title = request.POST['title']
        task = request.POST['task']
        todoList = user.todolist_set.create(title=title)
        todoList.save()
        todo = todoList.todo_set.create(task=task)
        todoList.save()
        return HttpResponseRedirect(reverse("notes:todo-list-index"))

    return render(request, "notes/todo_form.html")


# authorized todo list
@user_view.authorized
def get_todo_list(request):
    user = User.objects.get(username=request.session["username"])
    todoList = user.todolist_set.all()
    context = {
        "todo_list": todoList
    }
    return render(request, "notes/todo_list.html", context)


# get todo list in detail
@user_view.authorized
def get_todo_list_detail(request, todo_list_id):
    if not User.objects.filter(todolist__id=todo_list_id).exists() or \
            User.objects.filter(todolist__id=todo_list_id)[0].username != request.session["username"]:
        return HttpResponseRedirect(reverse("notes:todo-list-index"))
    todolist = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo": todolist
    }
    return render(request, "notes/todo_detail.html", context)

# adding new task to the todo list
@user_view.authorized
def add_task(request, todo_list_id):
    user = User.objects.get(username=request.session["username"])
    try:
        todolist = user.todolist_set.get(pk=todo_list_id)
    except TodoList.DoesNotExist:
        return HttpResponseRedirect(reverse("notes:todo-list-index"))
    if request.method == 'POST':
        task = request.POST['task']
        todo = todolist.todo_set.create(task=task)
        return HttpResponseRedirect(reverse("notes:user-todo-detail", args=(todo_list_id,)))
    context = {
        "todo_list_id": todo_list_id
    }
    return render(request, 'notes/task-form.html', context=context)


# Marking task as complete in a todo list
@user_view.authorized
def mark_task_as_completed(request, todo_list_id):
    # user = User.objects.get(username=request.session["username"])
    if not User.objects.filter(todolist__id=todo_list_id).exists() or \
            User.objects.filter(todolist__id=todo_list_id)[0].username != request.session["username"]:
        return HttpResponseRedirect(reverse("notes:todo-list-index"))
    if request.method == 'POST':
        task_ids = request.POST['task']
        # for id in task_ids:
        #     task = Todo.objects.get(pk=int(id))
        #     task.status = True
        #     task.save()
        task = Todo.objects.get(pk=task_ids)
        todoList = TodoList.objects.get(pk=todo_list_id)
        owner_username = todoList.owner.username
        if owner_username != request.session["username"]:
            return HttpResponseRedirect(reverse("notes:user-todo-detail", args=(todo_list_id,)))
        task.status = True
        task.save()
        return HttpResponseRedirect(reverse("notes:user-todo-detail", args=(todo_list_id,)))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/task_completion.html", context=context)


# Deleting a task from a task list
@user_view.authorized
def delete_task(request, todo_list_id):
    if not User.objects.filter(todolist__id=todo_list_id).exists() or \
            User.objects.filter(todolist__id=todo_list_id)[0].username != request.session["username"]:
        return HttpResponseRedirect(reverse("notes:todo-list-index"))

    if request.method == 'POST':
        task_ids = request.POST['task']
        # print(task_ids)
        # for id in task_ids:
        #     task = Todo.objects.get(pk=id)
        #     task.delete()
        task = Todo.objects.get(pk=task_ids)
        task.delete()
        return HttpResponseRedirect(reverse("notes:user-todo-detail", args=(todo_list_id,)))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/task_deletion.html", context=context)


# Delete Todo list
@user_view.authorized
def delete_todo_list(request, todo_list_id):
    if not User.objects.filter(todolist__id=todo_list_id).exists() or \
            User.objects.filter(todolist__id=todo_list_id)[0].username != request.session["username"]:
        return HttpResponseRedirect(reverse("notes:todo-list-index"))

    if request.method == 'POST':
        yes_or_no = request.POST['surety']
        if yes_or_no == 'YES':
            todo_list = TodoList.objects.get(pk=todo_list_id)
            todo_list.delete()
        return HttpResponseRedirect(reverse("notes:todo-list-index"))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/todo_list_deletion.html", context=context)
