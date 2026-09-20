from flask import Flask

from database import (
    create_tables,
    get_tags_by_user,
    get_cat_by_user,
)

from routes.auth_routes import register_auth_routes
from routes.task_routes import register_task_routes
from routes.label_routes import register_label_routes
from routes.page_routes import register_page_routes
from routes.setting_routes import register_setting_routes
from routes.cat_routes import register_cat_routes


app = Flask(__name__)


# Flask needs this for session and flash messages.
# This is only a development key for now.
app.config["SECRET_KEY"] = "CatOS-development-secret-key"


# Do not allow giant image uploads.
app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)


# Register CatOS routes.
register_auth_routes(app)
register_task_routes(app)
register_label_routes(app)
register_page_routes(app)
register_setting_routes(app)
register_cat_routes(app)


# Make saved labels available to the floating Add task modal.
# The modal lives in base.html and can open from any page.
@app.context_processor
def inject_global_task_modal_data():

    from flask import session

    if "user_id" not in session:

        return {
            "global_task_tags": [],
            "cat_name": "Cat"
        }

    user_id = session["user_id"]

    user_cat = get_cat_by_user(
        user_id
    )

    return {
        "global_task_tags": get_tags_by_user(
            user_id
        ),

        "cat_name": (
            user_cat["cat_name"]
            if user_cat
            else "Cat"
        )
    }


# Only start the Flask server if this file is run directly.
if __name__ == "__main__":

    # Make sure all the database tables exist before CatOS starts.
    create_tables()

    # debug=True is useful while developing.
    # Definitely not something I want forever.
    app.run(debug=True)