"""Make the CatOS database functions available from one place."""

from .connection import get_connection

from .tables import create_tables

from .users import (
    get_user_by_id,
    update_user_avatar,
)

from .tasks import (
    create_task,
    get_tasks_by_user,
    toggle_task_completion,
    update_task,
    delete_task,
    search_tasks,
    get_task_statistics,
    get_task_state,
)

from .tags import (
    create_tag,
    get_tags_by_user,
    get_tasks_by_tag,
    update_tag,
    delete_tag,
    get_tags_by_task,
    set_task_tags,
)

from .subtasks import (
    create_subtask,
    get_subtasks_by_task,
    toggle_subtask_completion,
    update_subtask,
    delete_subtask,
)

from .cats import (
    get_cat_by_user,
    create_cat_for_user,
    rename_cat,
    reward_cat_for_task,
)
