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
    get_tasks_by_tag,
    update_tag,
    delete_tag,
)

from utils.auth_helpers import (
    login_required,
)

from utils.task_helpers import (
    add_tags_to_tasks,
)


def register_label_routes(app):

    # Labels page.
    @app.route("/labels")
    @login_required
    def labels():

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


    # Rename label.
    @app.route(
        "/label/<int:tag_id>/edit",
        methods=["POST"]
    )
    @login_required
    def edit_label(tag_id):

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


    # Delete label.
    @app.route(
        "/label/<int:tag_id>/delete",
        methods=["POST"]
    )
    @login_required
    def remove_label(tag_id):

        delete_tag(
            tag_id=tag_id,
            user_id=session["user_id"]
        )

        return redirect(
            url_for("labels")
        )