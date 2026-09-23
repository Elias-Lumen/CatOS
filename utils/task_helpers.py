from datetime import date

from database import (
    create_tag,
    get_tags_by_task,
    get_subtasks_by_task,
)


# Check that a date is a real date before saving it.
def is_valid_date(date_value):

    # No date is allowed.
    if date_value is None:
        return True

    try:
        date.fromisoformat(date_value)
        return True

    except (ValueError, TypeError):
        return False


# Start date cannot be after the deadline.
def are_task_dates_valid(
    start_date,
    due_date
):

    if not is_valid_date(
        start_date
    ):
        return False

    if not is_valid_date(
        due_date
    ):
        return False

    if start_date and due_date:

        start = date.fromisoformat(
            start_date
        )

        due = date.fromisoformat(
            due_date
        )

        if start > due:
            return False

    return True


# Turn comma-separated new tag names into tag ids.
def get_new_tag_ids(
    user_id,
    new_tags_text
):

    tag_ids = []

    if not new_tags_text:
        return tag_ids

    # Allow users to type something like:
    # School, DTP, Important
    tag_names = new_tags_text.split(
        ","
    )

    for tag_name in tag_names:

        tag_name = tag_name.strip()

        if tag_name:

            tag_id = create_tag(
                user_id=user_id,
                name=tag_name
            )

            tag_ids.append(
                tag_id
            )

    return tag_ids


# Read task form values in one place.
# Creating and editing tasks use the same fields.
def get_task_form_data(request):

    return {
        "title": request.form.get(
            "title",
            ""
        ).strip(),

        "description": request.form.get(
            "description",
            ""
        ).strip(),

        "priority": request.form.get(
            "priority",
            "normal"
        ),

        "start_date": (
            request.form.get(
                "start_date"
            )
            or None
        ),

        "due_date": (
            request.form.get(
                "due_date"
            )
            or None
        ),

        "selected_tag_ids": request.form.getlist(
            "tag_ids"
        ),

        "new_tags_text": request.form.get(
            "new_tags",
            ""
        ).strip(),
    }


# Combine selected labels with newly created labels.
# dict.fromkeys removes duplicates while keeping the original order.
def get_combined_tag_ids(
    user_id,
    selected_tag_ids,
    new_tags_text
):

    new_tag_ids = get_new_tag_ids(
        user_id=user_id,
        new_tags_text=new_tags_text
    )

    all_tag_ids = (
        selected_tag_ids
        + new_tag_ids
    )

    return list(
        dict.fromkeys(
            all_tag_ids
        )
    )


# Attach labels to every task before sending them to the page.
# Otherwise the template knows the task,
# but not which labels belong to it.
def add_tags_to_tasks(
    tasks,
    user_id
):

    tasks_with_tags = []

    for task in tasks:

        task_data = dict(
            task
        )

        task_data["tags"] = list(
            get_tags_by_task(
                task_id=task["id"],
                user_id=user_id
            )
        )

        tasks_with_tags.append(
            task_data
        )

    return tasks_with_tags


# Attach subtasks to every task before sending them to the page.
# Doing it here keeps the template nice and simple.
def add_subtasks_to_tasks(
    tasks,
    user_id
):

    tasks_with_subtasks = []

    for task in tasks:

        task_data = dict(
            task
        )

        task_data["subtasks"] = list(
            get_subtasks_by_task(
                task_id=task["id"],
                user_id=user_id
            )
        )

        tasks_with_subtasks.append(
            task_data
        )

    return tasks_with_subtasks