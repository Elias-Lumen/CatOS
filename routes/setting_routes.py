"""Routes used for the CatOS settings page and profile picture changes."""

from pathlib import Path
from uuid import uuid4

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.utils import (
    secure_filename,
)

from database import (
    get_user_by_id,
    update_user_avatar,
)

from utils.auth_helpers import (
    login_required,
)

from utils.avatar_helpers import (
    allowed_avatar,
    get_avatar_extension,
    get_avatar_folder,
)


def register_setting_routes(app):
    """Register the settings routes into the main CatOS app."""

    # Settings page.
    @app.route(
        "/setting",
        methods=["GET", "POST"]
    )
    @login_required
    def setting():
        """Show Settings and deal with a new avatar if one is uploaded."""

        user_id = session["user_id"]

        # Get the current user first.
        # The old avatar is also stored here and may need to be deleted later.
        user = get_user_by_id(
            user_id
        )

        # POST means the user is trying to upload a new avatar.
        if request.method == "POST":

            avatar = request.files.get(
                "avatar"
            )

            # Nothing was actually selected.
            # There is no point going through the rest of the upload code.
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

            # Check the extension before saving anything.
            if not allowed_avatar(
                avatar.filename
            ):

                flash(
                    "Unsupported avatar file type."
                )

                return redirect(
                    url_for("setting")
                )

            # Clean the original filename before using any part of it.
            original_name = secure_filename(
                avatar.filename
            )

            # secure_filename can theoretically leave something unusable.
            # Also make sure there is still an extension to work with.
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

            extension = get_avatar_extension(
                original_name
            )

            avatar_folder = get_avatar_folder(
                app
            )

            # The folder may not exist on a fresh copy of CatOS yet.
            avatar_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            # Give every upload a new random name.
            # This avoids different users or uploads overwriting each other.
            filename = (
                f"user_{user_id}_"
                f"{uuid4().hex}."
                f"{extension}"
            )

            file_path = (
                avatar_folder
                / filename
            )

            # Save the new image first.
            avatar.save(
                file_path
            )

            # The database needs the URL used by the webpage,
            # not the local file path used above.
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

            old_avatar_url = (
                user["avatar_url"]
                if user
                else None
            )

            # Delete the previous uploaded avatar so old images
            # do not slowly pile up in the folder forever.
            # Only delete files from CatOS's own avatar folder.
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
                    avatar_folder
                    / old_filename
                )

                # The database may point to a file that is already gone,
                # so check before trying to delete it.
                if old_file_path.exists():

                    old_file_path.unlink()

            flash(
                "Avatar updated."
            )

            return redirect(
                url_for("setting")
            )

        # Use the saved avatar when the user has one.
        # Otherwise CatOS falls back to the default cat avatar.
        avatar_url = (
            user["avatar_url"]

            if (
                user
                and user["avatar_url"]
            )

            else url_for(
                "static",
                filename=(
                    "icons/"
                    "default_avatar.svg"
                )
            )
        )

        return render_template(
            "setting.html",
            avatar_url=avatar_url
        )
