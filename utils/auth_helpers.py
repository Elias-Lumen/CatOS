"""Small helper functions used to protect pages that need a logged in user."""

from functools import wraps

from flask import (
    redirect,
    session,
    url_for,
)


# Protect pages that should only be available
# after the user has logged in.
def login_required(view_function):
    """Make sure the user is logged in before opening a protected page."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        """Run the page normally if there is a logged in user."""

        # user_id only exists in session after a successful login.
        # If it is missing, send the user back to Login instead.
        if "user_id" not in session:

            return redirect(
                url_for("login")
            )

        # Login exists, so the original page can run normally.
        return view_function(
            *args,
            **kwargs
        )

    return wrapped_view
