from pathlib import Path


# Only normal image formats are allowed.
ALLOWED_AVATAR_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}


# Get the avatar upload folder for this Flask app.
def get_avatar_folder(app):

    return (
        Path(app.root_path)
        / "static"
        / "uploads"
        / "avatars"
    )


# Check the file extension before saving an avatar.
def allowed_avatar(filename):

    extension = (
        Path(filename)
        .suffix
        .lower()
        .lstrip(".")
    )

    return (
        bool(extension)
        and extension
        in ALLOWED_AVATAR_EXTENSIONS
    )