import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user,login_required

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm, TaskForm

from ..models import User, Task
from ..utils import current_time

tasks = Blueprint("tasks", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """

import requests

# ZenQuotes API endpoint
url = "https://zenquotes.io/api/random"
def quote():
    response = requests.get(url)
    if response.status_code == 200:
        quote_data = response.json()[0]
        quote = quote_data['q']
        author = quote_data['a']
        return f'"{quote}" - {author}'
    else:
        return "Failed to retrieve quote."


@tasks.route("/", methods=["GET", "POST"])
def index():     
    return render_template("index.html")#, quote=quote())


@tasks.route("/create-task", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
    #     task = StringField('Title', validators=[DataRequired()])
    # description = TextAreaField('Description', validators=[DataRequired()])
    # date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
        task = Task(
            user=current_user._get_current_object(),
            task=form.task.data,
            description=form.description.data,
            date=form.date.data,
            completed=False
        )
        task.save()
        #flash("Task created successfully", "success")
        return redirect(url_for("tasks.list_tasks"))
    

    return render_template("create_task.html", form=form)

@tasks.route("/tasks", methods=["GET"])
@login_required
def list_tasks():
    tasks = Task.objects(user=current_user._get_current_object())
    quote_text = quote()
    return render_template("view_tasks.html", tasks=tasks, quote=quote_text)


@tasks.route("/complete-task/<task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    task = Task.objects(id=task_id, user=current_user._get_current_object()).first()
    if task:
        task.completed = True
        task.save()
        #flash("Task marked as completed!", "success")
    return redirect(url_for("tasks.list_tasks"))

@tasks.route("/edit-task/<task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.objects(id=task_id, user=current_user._get_current_object()).first()

    if not task:
        #flash("Task not found or you do not have permission to edit it.", "danger")
        return redirect(url_for("tasks.list_tasks"))

    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.task = form.task.data
        task.description = form.description.data
        task.date = form.date.data
        task.save()

        #flash("Task updated successfully", "success")
        return redirect(url_for("tasks.list_tasks"))

    return render_template("edit_task.html", form=form, task=task)

@tasks.route("/delete-task/<task_id>", methods=["GET"])
@login_required
def delete_task(task_id):
    task = Task.objects(id=task_id, user=current_user._get_current_object()).first()

    if task:
        task.delete()
        #flash("Task deleted successfully", "success")
    
    return redirect(url_for("tasks.list_tasks"))
