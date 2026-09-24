"""Small helper functions for checking and saving user avatars."""

from pathlib import Path


# Only normal image formats are allowed.
# Anything outside this list should not be saved as an avatar.
ALLOWED_AVATAR_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
}


# Get the avatar upload folder for this Flask app.
def get_avatar_folder(app):
    """Find the folder where uploaded avatars should be saved."""

    return (
        Path(app.root_path)
        / "static"
        / "uploads"
        / "avatars"
    )


# Get a normalised file extension from an avatar filename.
def get_avatar_extension(filename):
    """Get the lowercase extension from an avatar filename."""

    return (
        Path(filename)
        .suffix
        .lower()
        .lstrip(".")
    )


# Check the file extension before saving an avatar.
def allowed_avatar(filename):
    """Check if the uploaded avatar uses an allowed image format."""

    return (
        get_avatar_extension(
            filename
        )
        in ALLOWED_AVATAR_EXTENSIONS
    )
