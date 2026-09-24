"""Make all CatOS route registration functions available from one place."""

from .auth_routes import register_auth_routes
from .task_routes import register_task_routes
from .label_routes import register_label_routes
from .page_routes import register_page_routes
from .setting_routes import register_setting_routes
from .cat_routes import register_cat_routes
