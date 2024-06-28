from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Note, TodoList, Todo
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


# creating a new note

def note_form(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        note = Note(title=title, content=content)
        note.save()
        note_list = Note.objects.all()
        context = {
            "note_list" : note_list,
            "message" : "note is saved successfully"
        }
        return HttpResponseRedirect(reverse("notes:index" ))
    return render(request, "notes/note_form.html")


# Deleting a note
def delete_note(request, note_id):

    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist :
        return HttpResponseRedirect(reverse("notes:index"))

    if request.method == 'POST':
        yes_or_no = request.POST['surety']
        if yes_or_no == 'YES':
            note.delete()
        return HttpResponseRedirect(reverse("notes:index"))

    context = {
        "note": note
    }
    return render(request, "notes/note_deletion.html", context)


# EDIT note title
def edit_note_title(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist :
        return HttpResponseRedirect(reverse("notes:index"))

    if request.method == 'POST':
        new_title = request.POST['title']
        note.title = new_title
        note.save()
        return HttpResponseRedirect(reverse("notes:index"))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-title.html", context)


# edit note content
def edit_note_content(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse("notes:index"))

    if request.method == 'POST':
        new_content = request.POST['content']
        note.content = new_content
        note.save()
        return HttpResponseRedirect(reverse("notes:index"))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-content.html", context)


# edit note options
def edit_note(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('notes:index'))

    if request.method == 'POST':
        edit_option = request.POST['edit-opt']
        if edit_option == 'title':
            return HttpResponseRedirect(reverse('notes:edit-note-title', args=(note_id,)))
        elif edit_option == 'content':
            return HttpResponseRedirect(reverse('notes:edit-note-content',args=(note_id,)))
        else :
            return HttpResponseRedirect(reverse('notes:edit-note-both', args=(note_id,)))

    context = {
        "note": note
    }
    return render(request, 'notes/note-edit.html',context=context)


# edit note both
def edit_note_both(request, note_id):
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('notes:index'))

    if request.method == 'POST':
        new_title = request.POST['title']
        new_content = request.POST['content']
        note.title = new_title
        note.content = new_content
        note.save()
        return HttpResponseRedirect(reverse("notes:detail", args=(note_id,)))

    context = {
        "note": note
    }
    return render(request, "notes/note-edit-both.html", context)


# Creating a new todo list
def create_todolist_form(request):

    if request.method == 'POST':
        title = request.POST['title']
        task = request.POST['task']
        todoList = TodoList(title=title)
        todoList.save()
        todo = todoList.todo_set.create(task=task)
        todoList.save()
        return HttpResponseRedirect(reverse("notes:todo-list"))

    return render(request, "notes/todo_form.html")


# adding new task to the todo list
def add_task(request, todo_list_id):

    if request.method == 'POST':
        todolist = TodoList.objects.get(pk=todo_list_id)
        task = request.POST['task']
        todo = todolist.todo_set.create(task=task)
        return HttpResponseRedirect(reverse("notes:todo-detail", args=(todo_list_id,)))
    context = {
        "todo_list_id": todo_list_id
    }
    return render(request, 'notes/task-form.html', context=context)


# Marking task as complete in a todo list
def mark_task_as_completed(request, todo_list_id):

    if request.method == 'POST':
        task_ids = request.POST['task']
        for id in task_ids:
            task = Todo.objects.get(pk=int(id))
            task.status = True
            task.save()
        return HttpResponseRedirect(reverse("notes:todo-detail", args=(todo_list_id,)))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/task_completion.html", context=context)


# Deleting a task from a task list
def delete_task(request, todo_list_id):

    if request.method == 'POST':
        task_ids = request.POST['task']
        for id in task_ids:
            task = Todo.objects.get(pk=id)
            task.delete()
        return HttpResponseRedirect(reverse("notes:todo-detail", args=(todo_list_id,)))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/task_deletion.html", context=context)


# Delete Todo list
def delete_todo_list(request, todo_list_id):

    if request.method == 'POST':
        yes_or_no = request.POST['surety']
        if yes_or_no == 'YES' :
            todo_list = TodoList.objects.get(pk=todo_list_id)
            todo_list.delete()
        return HttpResponseRedirect(reverse("notes:todo-list"))

    todo_list = TodoList.objects.get(pk=todo_list_id)
    context = {
        "todo_list": todo_list
    }
    return render(request, "notes/todo_list_deletion.html", context=context)