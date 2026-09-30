"""Routes used for registering, logging in, and logging out of CatOS."""

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from services import (
    login_user,
    register_user,
)


def validate_password(password):
    """Check whether a password meets CatOS security requirements."""

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if len(password) > 64:
        return "Password must be no more than 64 characters long."

    if not any(
        character.isupper()
        for character in password
    ):
        return "Password must contain at least one uppercase letter."

    if not any(
        character.islower()
        for character in password
    ):
        return "Password must contain at least one lowercase letter."

    if not any(
        character.isdigit()
        for character in password
    ):
        return "Password must contain at least one number."

    return None


def register_auth_routes(app):
    """Register all account related routes into the main CatOS app."""

    # Register page.
    @app.route(
        "/register",
        methods=["GET", "POST"]
    )
    def register():
        """Show the register page and create a new account."""

        # POST means the user actually pressed the register button.
        if request.method == "POST":

            # Get whatever the user entered into the form.
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

            # Check the password before creating the account.
            password_error = validate_password(
                password
            )

            if password_error:

                flash(
                    password_error
                )

                return render_template(
                    "register.html"
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

            # The auth service does the actual account creation.
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
            # Clear anything old first and log the user in straight away.
            session.clear()

            # Keep the user information in session
            # so CatOS knows who is logged in on other pages.
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("home")
            )

        # GET just needs to show the empty register page.
        return render_template(
            "register.html"
        )


    # Login page.
    @app.route(
        "/login",
        methods=["GET", "POST"]
    )
    def login():
        """Show the login page and start a session for a valid user."""

        if request.method == "POST":

            # Read the login information from the form.
            username = request.form.get(
                "username",
                ""
            )

            password = request.form.get(
                "password",
                ""
            )

            # auth.py checks the username and password.
            user = login_user(
                username,
                password
            )

            # No matching user means the login information was wrong.
            if user is None:

                flash(
                    "Invalid username or password."
                )

                return render_template(
                    "login.html"
                )

            # Remove any old session before saving this login.
            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("home")
            )

        # Nothing submitted yet, just show the login page.
        return render_template(
            "login.html"
        )


    # Log out button from Settings.
    @app.route("/logout")
    def logout():
        """Log the current user out and send them back to Login."""

        # Removing the session means CatOS no longer
        # remembers this user as logged in.
        session.clear()

        return redirect(
            url_for("login")
        )
