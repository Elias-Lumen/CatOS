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
    ALLOWED_AVATAR_EXTENSIONS,
    allowed_avatar,
    get_avatar_folder,
)


def register_setting_routes(app):

    # Settings page.
    @app.route(
        "/setting",
        methods=["GET", "POST"]
    )
    @login_required
    def setting():

        user_id = session["user_id"]

        user = get_user_by_id(
            user_id
        )

        # User uploaded a new avatar.
        if request.method == "POST":

            avatar = request.files.get(
                "avatar"
            )

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

            if not allowed_avatar(
                avatar.filename
            ):

                flash(
                    "Unsupported avatar file type."
                )

                return redirect(
                    url_for("setting")
                )

            original_name = secure_filename(
                avatar.filename
            )

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

            avatar_folder = get_avatar_folder(
                app
            )

            avatar_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = (
                f"user_{user_id}_"
                f"{uuid4().hex}."
                f"{extension}"
            )

            file_path = (
                avatar_folder
                / filename
            )

            avatar.save(
                file_path
            )

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

                if old_file_path.exists():

                    old_file_path.unlink()

            flash(
                "Avatar updated."
            )

            return redirect(
                url_for("setting")
            )

        # Page opened normally.
        user = get_user_by_id(
            user_id
        )

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