from datetime import date

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import (
    get_tags_by_user,
    set_task_tags,
    toggle_task_completion,
    update_task,
    delete_task,
    create_subtask,
    toggle_subtask_completion,
    update_subtask,
    delete_subtask,
    create_cat_for_user,
    reward_cat_for_task,
    get_task_state,
)

from utils.auth_helpers import (
    login_required,
)

from utils.task_helpers import (
    are_task_dates_valid,
    get_task_form_data,
    get_combined_tag_ids,
    create_task_with_tags,
    get_tasks_with_details,
)


def register_task_routes(app):

    # Home page and Today page are basically
    # the same thing for now.
    @app.route(
        "/",
        methods=["GET", "POST"]
    )
    @login_required
    def home():

        user_id = session["user_id"]

        if request.method == "POST":

            task_data = get_task_form_data(
                request
            )

            if not are_task_dates_valid(
                task_data["start_date"],
                task_data["due_date"]
            ):

                flash(
                    "Start date must be on or before the due date."
                )

                return redirect(
                    url_for("home")
                )

            if task_data["title"]:

                create_task_with_tags(
                    user_id=user_id,
                    task_data=task_data
                )

            return redirect(
                url_for("home")
            )

        tasks = get_tasks_with_details(
            user_id
        )

        tags = get_tags_by_user(
            user_id
        )

        today_date = date.today()

        overdue_tasks = []
        today_tasks = []

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

            if (
                start_date
                and start_date > today_date
            ):
                continue

            if (
                due_date
                and due_date < today_date
            ):

                overdue_tasks.append(
                    task
                )

            else:

                today_tasks.append(
                    task
                )

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
    @login_required
    def toggle_task(task_id):

        user_id = session["user_id"]

        old_state = get_task_state(
            task_id=task_id,
            user_id=user_id
        )

        changed = toggle_task_completion(
            task_id=task_id,
            user_id=user_id
        )

        if (
            changed
            and old_state
            and old_state != "completed"
        ):

            create_cat_for_user(
                user_id
            )

            reward_cat_for_task(
                user_id
            )

        return redirect(
            url_for("home")
        )


    @app.route(
        "/task/<int:task_id>/edit",
        methods=["POST"]
    )
    @login_required
    def edit_task(task_id):

        user_id = session["user_id"]

        task_data = get_task_form_data(
            request
        )

        if not are_task_dates_valid(
            task_data["start_date"],
            task_data["due_date"]
        ):

            flash(
                "Start date must be on or before the due date."
            )

            return redirect(
                url_for("home")
            )

        if task_data["title"]:

            updated = update_task(
                task_id=task_id,
                user_id=user_id,
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"],
                start_date=task_data["start_date"],
                due_date=task_data["due_date"]
            )

            if updated:

                all_tag_ids = get_combined_tag_ids(
                    user_id=user_id,
                    selected_tag_ids=task_data[
                        "selected_tag_ids"
                    ],
                    new_tags_text=task_data[
                        "new_tags_text"
                    ]
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
    @login_required
    def remove_task(task_id):

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
    @login_required
    def add_subtask(task_id):

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
    @login_required
    def toggle_subtask(subtask_id):

        toggle_subtask_completion(
            subtask_id=subtask_id,
            user_id=session["user_id"]
        )

        return redirect(
            url_for("home")
        )


    @app.route(
        "/subtask/<int:subtask_id>/edit",
        methods=["POST"]
    )
    @login_required
    def edit_subtask(subtask_id):

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


    @app.route(
        "/subtask/<int:subtask_id>/delete",
        methods=["POST"]
    )
    @login_required
    def remove_subtask(subtask_id):

        delete_subtask(
            subtask_id=subtask_id,
            user_id=session["user_id"]
        )

        return redirect(
            url_for("home")
        )


    # Create a task from the floating Add task modal.
    @app.route(
        "/task",
        methods=["POST"]
    )
    @login_required
    def task():

        user_id = session["user_id"]

        task_data = get_task_form_data(
            request
        )

        return_to = request.form.get(
            "return_to",
            ""
        ).strip()

        if (
            not return_to.startswith("/")
            or return_to.startswith("//")
        ):

            return_to = url_for(
                "home"
            )

        if not are_task_dates_valid(
            task_data["start_date"],
            task_data["due_date"]
        ):

            flash(
                "Start date must be on or before the due date."
            )

            return redirect(
                return_to
            )

        if task_data["title"]:

            create_task_with_tags(
                user_id=user_id,
                task_data=task_data
            )

        return redirect(
            return_to
        )


    # Upcoming page.
    @app.route("/upcoming")
    @login_required
    def upcoming():

        user_id = session["user_id"]

        today_date = date.today()

        tasks = get_tasks_with_details(
            user_id
        )

        upcoming_tasks = []

        for task in tasks:

            if not task["start_date"]:
                continue

            task_start_date = date.fromisoformat(
                task["start_date"]
            )

            if task_start_date > today_date:

                upcoming_tasks.append(
                    task
                )

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