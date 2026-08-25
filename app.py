from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename

from datetime import date

# bring the database functions over here
# otherwise app.py would have to do all the database work by itself
from database import (
    create_tables,
    create_task,
    create_tag,
    get_tasks_by_user,
    get_tags_by_user,
    get_tags_by_task,
    set_task_tags,
    toggle_task_completion,
    update_task,
    delete_task,
    create_subtask,
    get_subtasks_by_task,
    toggle_subtask_completion,
    update_subtask,
    delete_subtask,
    get_user_by_id,
    update_user_avatar,
)

# login and register logic is kept in auth.py
# so app.py does not become one giant file
from routes.auth import login_user, register_user


app = Flask(__name__)

# Flask needs this for session and flash messages
# this is only a development key for now
app.config["SECRET_KEY"] = "CatOS-development-secret-key"


# AVATAR SETTINGS

# Keep uploaded avatars in one folder inside static.
AVATAR_FOLDER = (
    Path(app.root_path)
    / "static"
    / "uploads"
    / "avatars"
)

# Only normal image formats are allowed.
ALLOWED_AVATAR_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}

# Do not allow giant image uploads.
app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)


# Check the file extension before saving an avatar.
def allowed_avatar(filename):

    extension = (
        Path(filename)
        .suffix
        .lower()
        .lstrip(".")
    )

    return (
        bool(extension)
        and extension
        in ALLOWED_AVATAR_EXTENSIONS
    )


# check that a date is a real date before saving it
def is_valid_date(date_value):
    # no date is allowed
    if date_value is None:
        return True

    try:
        date.fromisoformat(date_value)
        return True
    except (ValueError, TypeError):
        return False


# start date cannot be after the deadline
def are_task_dates_valid(start_date, due_date):
    if not is_valid_date(start_date):
        return False

    if not is_valid_date(due_date):
        return False

    if start_date and due_date:
        start = date.fromisoformat(start_date)
        due = date.fromisoformat(due_date)

        if start > due:
            return False

    return True


# turn comma-separated new tag names into tag ids
def get_new_tag_ids(user_id, new_tags_text):
    tag_ids = []

    if not new_tags_text:
        return tag_ids

    # allow users to type something like:
    # School, DTP, Important
    tag_names = new_tags_text.split(",")

    for tag_name in tag_names:
        tag_name = tag_name.strip()

        if tag_name:
            tag_id = create_tag(
                user_id=user_id,
                name=tag_name
            )

            tag_ids.append(tag_id)

    return tag_ids


# Attach labels to every task before sending them to the page.
# Otherwise the template knows the task, but not which labels belong to it.
def add_tags_to_tasks(tasks, user_id):

    tasks_with_tags = []

    for task in tasks:

        task_data = dict(task)

        task_data["tags"] = list(
            get_tags_by_task(
                task_id=task["id"],
                user_id=user_id
            )
        )

        tasks_with_tags.append(
            task_data
        )

    return tasks_with_tags


# Attach subtasks to every task before sending them to the page.
# Doing it here keeps the template nice and simple.
def add_subtasks_to_tasks(tasks, user_id):

    tasks_with_subtasks = []

    for task in tasks:

        task_data = dict(task)

        task_data["subtasks"] = list(
            get_subtasks_by_task(
                task_id=task["id"],
                user_id=user_id
            )
        )

        tasks_with_subtasks.append(
            task_data
        )

    return tasks_with_subtasks


# make saved labels available to the floating Add task modal
# because the modal lives in base.html and can open from any page
@app.context_processor
def inject_global_task_modal_data():
    if "user_id" not in session:
        return {
            "global_task_tags": []
        }

    return {
        "global_task_tags": get_tags_by_user(
            session["user_id"]
        )
    }


# home page and Today page are basically the same thing for now
@app.route("/", methods=["GET", "POST"])
def home():

    # no sneaking into the app without logging in first
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # if the user submits the task form, make a new task
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        # existing tags selected by the user
        selected_tag_ids = request.form.getlist("tag_ids")

        # new tags typed by the user
        new_tags_text = request.form.get(
            "new_tags",
            ""
        ).strip()

        # if the user does not choose one, just use normal
        priority = request.form.get(
            "priority",
            "normal"
        )

        # do not allow an invalid date to reach the database
        # blank dates are easier to deal with as None
        start_date = (
            request.form.get("start_date")
            or None
        )

        due_date = (
            request.form.get("due_date")
            or None
        )

        if not are_task_dates_valid(
            start_date,
            due_date
        ):
            flash(
                "Start date must be on or before the due date."
            )

            return redirect(
                url_for("home")
            )

        # a task without a title is not very useful
        if title:
            task_id = create_task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                start_date=start_date,
                due_date=due_date
            )

            # create any new tags that the user typed
            new_tag_ids = get_new_tag_ids(
                user_id=user_id,
                new_tags_text=new_tags_text
            )

            # combine selected existing tags and new tags
            all_tag_ids = (
                selected_tag_ids
                + new_tag_ids
            )

            # remove duplicates while keeping the values usable
            all_tag_ids = list(
                dict.fromkeys(all_tag_ids)
            )

            set_task_tags(
                task_id=task_id,
                user_id=user_id,
                tag_ids=all_tag_ids
            )

        # reload the page after adding the task
        # this also stops the form being submitted twice on refresh
        return redirect(
            url_for("home")
        )

    # only get tasks that belong to the current user
    tasks = get_tasks_by_user(user_id)

    # add the many-to-many tag information to each task
    tasks = add_tags_to_tasks(
        tasks,
        user_id
    )

    # Add each task's subtasks too.
    tasks = add_subtasks_to_tasks(
        tasks,
        user_id
    )

    # get all saved tags so users can reuse them
    tags = get_tags_by_user(user_id)

    today_date = date.today()

    overdue_tasks = []
    today_tasks = []

    # send the tasks to the Today page so Jinja can display them
    for task in tasks:

        start_date = (
            date.fromisoformat(
                task["start_date"]
            )
            if task["start_date"]
            else None
        )

        due_date = (
            date.fromisoformat(
                task["due_date"]
            )
            if task["due_date"]
            else None
        )

        # tasks that have not started yet belong in Upcoming
        if (
            start_date
            and start_date > today_date
        ):
            continue

        if (
            due_date
            and due_date < today_date
        ):
            overdue_tasks.append(task)

        else:
            today_tasks.append(task)

    return render_template(
        "today_task.html",
        tasks=tasks,
        tags=tags,
        overdue_tasks=overdue_tasks,
        today_tasks=today_tasks,
        today=today_date.isoformat()
    )


@app.route(
    "/task/<int:task_id>/toggle",
    methods=["POST"]
)
def toggle_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    toggle_task_completion(
        task_id=task_id,
        user_id=session["user_id"]
    )

    return redirect(
        url_for("home")
    )


@app.route(
    "/task/<int:task_id>/edit",
    methods=["POST"]
)
def edit_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    priority = request.form.get(
        "priority",
        "normal"
    )

    start_date = (
        request.form.get("start_date")
        or None
    )

    due_date = (
        request.form.get("due_date")
        or None
    )

    selected_tag_ids = (
        request.form.getlist("tag_ids")
    )

    new_tags_text = request.form.get(
        "new_tags",
        ""
    ).strip()

    if not are_task_dates_valid(
        start_date,
        due_date
    ):
        flash(
            "Start date must be on or before the due date."
        )

        return redirect(
            url_for("home")
        )

    if title:
        updated = update_task(
            task_id=task_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            start_date=start_date,
            due_date=due_date
        )

        if updated:
            new_tag_ids = get_new_tag_ids(
                user_id=user_id,
                new_tags_text=new_tags_text
            )

            all_tag_ids = (
                selected_tag_ids
                + new_tag_ids
            )

            all_tag_ids = list(
                dict.fromkeys(all_tag_ids)
            )

            set_task_tags(
                task_id=task_id,
                user_id=user_id,
                tag_ids=all_tag_ids
            )

    return redirect(
        url_for("home")
    )


@app.route(
    "/task/<int:task_id>/delete",
    methods=["POST"]
)
def remove_task(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    delete_task(
        task_id=task_id,
        user_id=session["user_id"]
    )

    return redirect(
        url_for("home")
    )


@app.route(
    "/task/<int:task_id>/subtask",
    methods=["POST"]
)
def add_subtask(task_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    if title:

        create_subtask(
            task_id=task_id,
            user_id=session["user_id"],
            title=title
        )

    return redirect(
        url_for("home")
    )


@app.route(
    "/subtask/<int:subtask_id>/toggle",
    methods=["POST"]
)
def toggle_subtask(subtask_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    toggle_subtask_completion(
        subtask_id=subtask_id,
        user_id=session["user_id"]
    )

    return redirect(
        url_for("home")
    )


# Edit one subtask.
@app.route(
    "/subtask/<int:subtask_id>/edit",
    methods=["POST"]
)
def edit_subtask(subtask_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    if title:

        update_subtask(
            subtask_id=subtask_id,
            user_id=session["user_id"],
            title=title
        )

    return redirect(
        url_for("home")
    )


# Delete one subtask.
@app.route(
    "/subtask/<int:subtask_id>/delete",
    methods=["POST"]
)
def remove_subtask(subtask_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    delete_subtask(
        subtask_id=subtask_id,
        user_id=session["user_id"]
    )

    return redirect(
        url_for("home")
    )


# register page
@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # POST means the user actually pressed the register button
    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            "",
        )

        # stop here if they somehow typed two different passwords
        if password != confirm_password:
            flash(
                "Passwords do not match."
            )

            return render_template(
                "register.html"
            )

        # auth.py does the actual account creation
        user = register_user(
            username,
            password
        )

        # None means something went wrong
        # usually duplicate username or missing information
        if user is None:
            flash(
                "Username already exists, or the form is incomplete."
            )

            return render_template(
                "register.html"
            )

        # registration worked
        # log the user in straight away because making them log in again is annoying
        session.clear()

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(
            url_for("home")
        )

    # if they only opened the page, just show the form
    return render_template(
        "register.html"
    )


# login page
@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # user pressed the login button
    if request.method == "POST":
        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        # ask auth.py if these login details are actually correct
        user = login_user(
            username,
            password
        )

        # wrong username or password
        if user is None:
            flash(
                "Invalid username or password."
            )

            return render_template(
                "login.html"
            )

        # remove anything left from an old login session
        session.clear()

        # remember who is logged in
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(
            url_for("home")
        )

    # they only opened /login, nothing exciting happened yet
    return render_template(
        "login.html"
    )


# log out button from Settings
@app.route("/logout")
def logout():

    # forget the current user completely
    session.clear()

    # send them back to login
    return redirect(
        url_for("login")
    )


# SETTINGS PAGE
# The avatar can be viewed and changed here.
@app.route(
    "/setting",
    methods=["GET", "POST"]
)
def setting():

    # Settings contains private user information.
    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    user = get_user_by_id(
        user_id
    )


    # USER UPLOADED A NEW AVATAR
    if request.method == "POST":

        avatar = request.files.get(
            "avatar"
        )


        # Nothing was selected.
        if (
            avatar is None
            or avatar.filename == ""
        ):

            flash(
                "Please choose an image."
            )

            return redirect(
                url_for("setting")
            )


        # Reject files that are not supported images.
        if not allowed_avatar(
            avatar.filename
        ):

            flash(
                "Unsupported avatar file type."
            )

            return redirect(
                url_for("setting")
            )


        # Clean the uploaded filename before using it.
        original_name = secure_filename(
            avatar.filename
        )

        # secure_filename can sometimes remove strange characters,
        # so check the cleaned name again before taking the extension.
        if (
            not original_name
            or "." not in original_name
        ):

            flash(
                "Unsupported avatar file type."
            )

            return redirect(
                url_for("setting")
            )


        extension = (
            Path(original_name)
            .suffix
            .lower()
            .lstrip(".")
        )


        if (
            not extension
            or extension
            not in ALLOWED_AVATAR_EXTENSIONS
        ):

            flash(
                "Unsupported avatar file type."
            )

            return redirect(
                url_for("setting")
            )


        # Make sure the upload folder exists.
        AVATAR_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )


        # A random filename avoids browser caching problems
        # when the user changes their avatar.
        filename = (
            f"user_{user_id}_"
            f"{uuid4().hex}."
            f"{extension}"
        )

        file_path = (
            AVATAR_FOLDER
            / filename
        )


        # Save the new image.
        avatar.save(
            file_path
        )


        # Save the new path in this user's database row.
        avatar_url = url_for(
            "static",
            filename=(
                "uploads/avatars/"
                + filename
            )
        )

        update_user_avatar(
            user_id=user_id,
            avatar_url=avatar_url
        )


        # Remove the user's old uploaded avatar.
        old_avatar_url = (
            user["avatar_url"]
            if user
            else None
        )

        if (
            old_avatar_url
            and old_avatar_url.startswith(
                "/static/uploads/avatars/"
            )
        ):

            old_filename = Path(
                old_avatar_url
            ).name

            old_file_path = (
                AVATAR_FOLDER
                / old_filename
            )

            if old_file_path.exists():

                old_file_path.unlink()


        flash(
            "Avatar updated."
        )

        return redirect(
            url_for("setting")
        )

        flash(
            "Avatar updated."
        )

        return redirect(
            url_for("setting")
        )


    # PAGE OPENED NORMALLY

    user = get_user_by_id(
        user_id
    )

    avatar_url = (
        user["avatar_url"]
        if user
        and user["avatar_url"]
        else url_for(
            "static",
            filename="icons/default_avatar.svg"
        )
    )

    return render_template(
        "setting.html",
        avatar_url=avatar_url
    )

# create a task from the floating Add task modal
@app.route(
    "/task",
    methods=["POST"]
)
def task():

    # user must be logged in before creating a task
    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    user_id = session["user_id"]

    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    priority = request.form.get(
        "priority",
        "normal"
    )

    start_date = (
        request.form.get("start_date")
        or None
    )

    due_date = (
        request.form.get("due_date")
        or None
    )

    # existing labels selected in the modal
    selected_tag_ids = (
        request.form.getlist("tag_ids")
    )

    # new labels typed by the user
    new_tags_text = request.form.get(
        "new_tags",
        ""
    ).strip()

    # remember which page opened the modal
    return_to = request.form.get(
        "return_to",
        ""
    ).strip()

    # only allow local paths as redirect destinations
    if (
        not return_to.startswith("/")
        or return_to.startswith("//")
    ):
        return_to = url_for("home")

    if not are_task_dates_valid(
        start_date,
        due_date
    ):
        flash(
            "Start date must be on or before the due date."
        )

        return redirect(
            return_to
        )

    if title:
        task_id = create_task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            start_date=start_date,
            due_date=due_date
        )

        # create any new labels typed into the modal
        new_tag_ids = get_new_tag_ids(
            user_id=user_id,
            new_tags_text=new_tags_text
        )

        # combine existing and newly-created labels
        all_tag_ids = (
            selected_tag_ids
            + new_tag_ids
        )

        # remove duplicates
        all_tag_ids = list(
            dict.fromkeys(all_tag_ids)
        )

        set_task_tags(
            task_id=task_id,
            user_id=user_id,
            tag_ids=all_tag_ids
        )

    # return to the page where Add task was opened
    return redirect(
        return_to
    )


# this page should eventually become the floating task editor
# currently still under construction
@app.route("/search")
def search():
    return render_template(
        "search.html"
    )


# filters and labels page
# need to be done
@app.route("/labels")
def labels():
    return render_template(
        "labels.html"
    )


# future tasks will go here
@app.route("/upcoming")
def upcoming():
    return render_template(
        "upcoming.html"
    )


# task data / progress page
@app.route("/data")
def data():
    return render_template(
        "data.html"
    )


# virtual cat page
@app.route("/cat")
def cat():
    return render_template(
        "cat.html"
    )


# later each user should probably have their own cat name
# maybe let them edit it in Settings too?


# help page
@app.route("/help")
def help():
    return render_template(
        "help.html"
    )


# only start the Flask server if this file is run directly
if __name__ == "__main__":

    # make sure all the database tables exist before CatOS starts
    create_tables()

    # debug=True is useful while developing
    # definitely not something I want forever
    app.run(debug=True)