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

from datetime import date, datetime, timedelta, timezone

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
    search_tasks,
    get_tasks_by_tag,
    update_tag,
    delete_tag,
    get_task_statistics,
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
# SEARCH PAGE
# Search task titles/descriptions and narrow the results with filters.
@app.route("/search")
def search():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    # GET values stay in the URL.
    # This makes search results easy to refresh and test.
    query = request.args.get(
        "q",
        ""
    ).strip()

    tag_id = request.args.get(
        "label",
        ""
    ).strip()

    priority = request.args.get(
        "priority",
        ""
    ).strip()

    state = request.args.get(
        "status",
        ""
    ).strip()


    # Only accept a number as a label id.
    if tag_id.isdigit():

        tag_id_value = int(
            tag_id
        )

    else:

        tag_id_value = None
        tag_id = ""


    # Ignore priority values that CatOS does not use.
    valid_priorities = {
        "normal",
        "low",
        "medium",
        "high",
    }

    if priority not in valid_priorities:
        priority = ""


    # Ignore status values that CatOS does not use.
    valid_states = {
        "not_started",
        "in_progress",
        "completed",
    }

    if state not in valid_states:
        state = ""


    # Only search once the user has entered something
    # or selected at least one filter.
    search_active = bool(
        query
        or tag_id_value
        or priority
        or state
    )


    if search_active:

        tasks = search_tasks(
            user_id=user_id,
            query=query,
            tag_id=tag_id_value,
            priority=priority or None,
            state=state or None
        )

        # Add each task's labels before sending results to the template.
        tasks = add_tags_to_tasks(
            tasks,
            user_id
        )

    else:

        tasks = []


    tags = get_tags_by_user(
        user_id
    )


    return render_template(
        "search.html",
        tasks=tasks,
        tags=tags,
        query=query,
        selected_label=tag_id,
        selected_priority=priority,
        selected_status=state,
        search_active=search_active
    )


# LABELS PAGE
# View all reusable labels and the tasks connected to them.
@app.route("/labels")
def labels():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    tags = get_tags_by_user(
        user_id
    )


    selected_tag_id = request.args.get(
        "label",
        ""
    )


    selected_tag = None
    tasks = []


    if selected_tag_id.isdigit():

        selected_tag_id = int(
            selected_tag_id
        )


        # Make sure the selected label belongs to this user.
        selected_tag = next(
            (
                tag
                for tag in tags
                if tag["id"]
                == selected_tag_id
            ),
            None
        )


        if selected_tag:

            tasks = get_tasks_by_tag(
                user_id=user_id,
                tag_id=selected_tag_id
            )

            tasks = add_tags_to_tasks(
                tasks,
                user_id
            )


    return render_template(
        "labels.html",
        tags=tags,
        selected_tag=selected_tag,
        tasks=tasks
    )


# RENAME LABEL
@app.route(
    "/label/<int:tag_id>/edit",
    methods=["POST"]
)
def edit_label(tag_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    name = request.form.get(
        "name",
        ""
    ).strip()


    if name:

        try:

            update_tag(
                tag_id=tag_id,
                user_id=session["user_id"],
                name=name
            )

        except Exception:

            flash(
                "That label name is already in use."
            )


    return redirect(
        url_for("labels")
    )


# DELETE LABEL
@app.route(
    "/label/<int:tag_id>/delete",
    methods=["POST"]
)
def remove_label(tag_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    delete_tag(
        tag_id=tag_id,
        user_id=session["user_id"]
    )


    return redirect(
        url_for("labels")
    )


# UPCOMING PAGE
# Show tasks that are scheduled to start after today.
@app.route("/upcoming")
def upcoming():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    today_date = date.today()


    # Start with all tasks belonging to this user.
    tasks = get_tasks_by_user(
        user_id
    )


    tasks = add_tags_to_tasks(
        tasks,
        user_id
    )


    tasks = add_subtasks_to_tasks(
        tasks,
        user_id
    )


    upcoming_tasks = []


    for task in tasks:

        # No start date means there is no future day
        # to put the task under.
        if not task["start_date"]:
            continue


        task_start_date = date.fromisoformat(
            task["start_date"]
        )


        if task_start_date > today_date:

            upcoming_tasks.append(
                task
            )


    # Sort by date first.
    # Inside the same date, unfinished tasks stay above completed ones.
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3,
        "normal": 4,
    }


    upcoming_tasks.sort(
        key=lambda task: (
            task["start_date"],

            1
            if task["state"] == "completed"
            else 0,

            priority_order.get(
                task["priority"],
                5
            ),

            -task["id"]
        )
    )


    # Group tasks under their start date.
    upcoming_groups = {}


    for task in upcoming_tasks:

        start_date = task[
            "start_date"
        ]

        if start_date not in upcoming_groups:

            upcoming_groups[
                start_date
            ] = []


        upcoming_groups[
            start_date
        ].append(
            task
        )


    return render_template(
        "upcoming.html",
        upcoming_groups=upcoming_groups,
        today=today_date.isoformat()
    )


# DATA PAGE
# Show task completion progress and simple daily / weekly statistics.
@app.route("/data")
def data():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    # Get the task information needed for the statistics.
    tasks = get_task_statistics(
        user_id
    )


    # SQLite CURRENT_TIMESTAMP is stored in UTC.
    # Convert it to the computer's current local time before comparing dates.
    def local_date_from_sqlite(timestamp):

        if not timestamp:
            return None

        utc_time = datetime.fromisoformat(
            str(timestamp)
        ).replace(
            tzinfo=timezone.utc
        )

        return utc_time.astimezone().date()


    # OVERALL PROGRESS

    total_tasks = len(
        tasks
    )


    completed_tasks = sum(
        1
        for task in tasks
        if task["state"] == "completed"
    )


    # No tasks means 0%.
    # This also stops us dividing by zero.
    if total_tasks == 0:

        completion_rate = 0

    else:

        completion_rate = round(
            (
                completed_tasks
                / total_tasks
            )
            * 100
        )


    # TODAY

    today_date = date.today()

    created_today = 0
    completed_today = 0


    for task in tasks:

        created_date = local_date_from_sqlite(
            task["created_at"]
        )

        completed_date = local_date_from_sqlite(
            task["completed_at"]
        )


        if created_date == today_date:

            created_today += 1


        if completed_date == today_date:

            completed_today += 1


    # THIS WEEK

    # Find Monday of the current week.
    week_start = (
        today_date
        - timedelta(
            days=today_date.weekday()
        )
    )


    week_days = []


    # Make one statistics entry for each day,
    # starting with Monday and ending with Sunday.
    for day_number in range(7):

        current_date = (
            week_start
            + timedelta(
                days=day_number
            )
        )


        completed_count = sum(
            1
            for task in tasks
            if local_date_from_sqlite(
                task["completed_at"]
            ) == current_date
        )


        week_days.append({
            "name": current_date.strftime(
                "%a"
            ),
            "date": current_date.isoformat(),
            "completed": completed_count
        })


    # Find the biggest daily value.
    # The HTML uses this to decide how tall each bar should be.
    max_weekly_completed = max(
        (
            day["completed"]
            for day in week_days
        ),
        default=0
    )


    # Work out each bar height here.
    # This keeps maths out of the HTML.
    for day in week_days:

        if max_weekly_completed == 0:

            day["height"] = 0

        else:

            day["height"] = round(
                (
                    day["completed"]
                    / max_weekly_completed
                )
                * 100
            )


    return render_template(
        "data.html",

        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_rate=completion_rate,

        created_today=created_today,
        completed_today=completed_today,

        week_days=week_days,
        max_weekly_completed=max_weekly_completed
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