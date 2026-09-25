"""Routes used for the virtual cat page in CatOS."""

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import (
    get_cat_by_user,
    create_cat_for_user,
    rename_cat,
)

from utils import login_required


def register_cat_routes(app):
    """Register the virtual cat routes into the main CatOS app."""

    # Virtual cat page.
    @app.route(
        "/cat",
        methods=["GET", "POST"]
    )
    @login_required
    def cat():
        """Show the user's virtual cat and handle cat name changes."""

        user_id = session["user_id"]

        # Every user should have their own cat.
        # This only creates one if the user somehow does not have one yet.
        create_cat_for_user(
            user_id
        )

        # POST means the user is trying to rename their cat.
        if request.method == "POST":

            cat_name = request.form.get(
                "cat_name",
                ""
            ).strip()

            # Do not let the cat end up with an empty name.
            if not cat_name:

                flash(
                    "Cat name cannot be empty."
                )

                return redirect(
                    url_for("cat")
                )

            rename_cat(
                user_id=user_id,
                cat_name=cat_name
            )

            # Reload the page after renaming
            # so the new name appears straight away.
            return redirect(
                url_for("cat")
            )

        # Get the cat again after making sure it exists.
        user_cat = get_cat_by_user(
            user_id
        )

        return render_template(
            "cat.html",
            cat=user_cat
        )
