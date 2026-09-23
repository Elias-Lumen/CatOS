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


# Get a normalised file extension from an avatar filename.
def get_avatar_extension(filename):

    return (
        Path(filename)
        .suffix
        .lower()
        .lstrip(".")
    )


# Check the file extension before saving an avatar.
def allowed_avatar(filename):

    return (
        get_avatar_extension(
            filename
        )
        in ALLOWED_AVATAR_EXTENSIONS
    )