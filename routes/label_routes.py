"""Routes used for viewing, renaming, and deleting labels in CatOS."""

import sqlite3

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
    """Register all label related routes into the main CatOS app."""

    # Labels page.
    @app.route("/labels")
    @login_required
    def labels():
        """Show the user's labels and tasks under the selected label."""

        user_id = session["user_id"]

        # Get all labels first so they can be shown in the sidebar.
        tags = get_tags_by_user(
            user_id
        )

        # The selected label comes from the URL.
        selected_tag_id = request.args.get(
            "label",
            ""
        )

        # Start empty because the user may not have selected anything yet.
        selected_tag = None
        tasks = []

        # Label ids should only contain numbers.
        if selected_tag_id.isdigit():

            selected_tag_id = int(
                selected_tag_id
            )

            # Find the selected label from this user's own labels.
            # If the id does not belong to them, nothing gets selected.
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

                # Only load tasks after confirming
                # that this label belongs to the current user.
                tasks = get_tasks_by_tag(
                    user_id=user_id,
                    tag_id=selected_tag_id
                )

                # Tasks need their labels before the template displays them.
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
        """Rename one of the current user's labels."""

        # Remove spaces around the new name before saving it.
        name = request.form.get(
            "name",
            ""
        ).strip()

        # Empty label names are not useful.
        if name:

            try:

                update_tag(
                    tag_id=tag_id,
                    user_id=session["user_id"],
                    name=name
                )

            # A duplicate label name breaks the UNIQUE rule in the database.
            # Catch that specific problem instead of hiding every possible error.
            except sqlite3.IntegrityError:

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
        """Delete one label belonging to the current user."""

        # This only deletes the label.
        # Tasks using it should still stay in CatOS.
        delete_tag(
            tag_id=tag_id,
            user_id=session["user_id"]
        )

        return redirect(
            url_for("labels")
        )
