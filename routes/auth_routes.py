from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from routes.auth import (
    login_user,
    register_user,
)


def register_auth_routes(app):

    # Register page.
    @app.route(
        "/register",
        methods=["GET", "POST"]
    )
    def register():

        # POST means the user actually pressed the register button.
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

            # Stop here if they somehow typed
            # two different passwords.
            if password != confirm_password:

                flash(
                    "Passwords do not match."
                )

                return render_template(
                    "register.html"
                )

            # auth.py does the actual account creation.
            user = register_user(
                username,
                password
            )

            # None means something went wrong.
            # Usually duplicate username
            # or missing information.
            if user is None:

                flash(
                    "Username already exists, "
                    "or the form is incomplete."
                )

                return render_template(
                    "register.html"
                )

            # Registration worked.
            # Log the user in straight away.
            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("home")
            )

        return render_template(
            "register.html"
        )


    # Login page.
    @app.route(
        "/login",
        methods=["GET", "POST"]
    )
    def login():

        if request.method == "POST":

            username = request.form.get(
                "username",
                ""
            )

            password = request.form.get(
                "password",
                ""
            )

            user = login_user(
                username,
                password
            )

            if user is None:

                flash(
                    "Invalid username or password."
                )

                return render_template(
                    "login.html"
                )

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html"
        )


    # Log out button from Settings.
    @app.route("/logout")
    def logout():

        session.clear()

        return redirect(
            url_for("login")
        )