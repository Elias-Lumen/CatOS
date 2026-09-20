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


def register_cat_routes(app):

    # Virtual cat page.
    @app.route(
        "/cat",
        methods=["GET", "POST"]
    )
    def cat():

        if "user_id" not in session:

            return redirect(
                url_for("login")
            )

        user_id = session["user_id"]

        # Every user gets their own cat.
        create_cat_for_user(
            user_id
        )

        # Rename the cat.
        if request.method == "POST":

            cat_name = request.form.get(
                "cat_name",
                ""
            ).strip()

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

            return redirect(
                url_for("cat")
            )

        user_cat = get_cat_by_user(
            user_id
        )

        return render_template(
            "cat.html",
            cat=user_cat
        )