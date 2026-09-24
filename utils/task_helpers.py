"""Helper functions shared by the different task pages in CatOS."""

from datetime import date

from database import (
    create_task,
    create_tag,
    get_tasks_by_user,
    get_tags_by_task,
    get_subtasks_by_task,
    set_task_tags,
)


# Check that a date is a real date before saving it.
def is_valid_date(date_value):
    """Check if a date value is empty or contains a real date."""

    # No date is allowed.
    if date_value is None:
        return True

    try:
        # If Python can turn it into a date, the format is usable.
        date.fromisoformat(date_value)
        return True

    except (ValueError, TypeError):
        # Wrong format or wrong data type, so do not save it.
        return False


# Start date cannot be after the deadline.
def are_task_dates_valid(
    start_date,
    due_date
):
    """Check that both task dates are valid and in the right order."""

    if not is_valid_date(
        start_date
    ):
        return False

    if not is_valid_date(
        due_date
    ):
        return False

    # Only compare them when the user actually entered both dates.
    if start_date and due_date:

        start = date.fromisoformat(
            start_date
        )

        due = date.fromisoformat(
            due_date
        )

        # A task cannot somehow start after its own deadline.
        if start > due:
            return False

    return True


# Turn comma-separated new tag names into tag ids.
def get_new_tag_ids(
    user_id,
    new_tags_text
):
    """Create any new labels typed by the user and return their ids."""

    tag_ids = []

    # Nothing was entered, so there is nothing to create.
    if not new_tags_text:
        return tag_ids

    # Allow users to type something like:
    # School, DTP, Important
    tag_names = new_tags_text.split(
        ","
    )

    for tag_name in tag_names:

        # Remove accidental spaces around each label.
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
    """Collect all task information from a submitted form."""

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
    """Put selected and newly created label ids into one list."""

    new_tag_ids = get_new_tag_ids(
        user_id=user_id,
        new_tags_text=new_tags_text
    )

    all_tag_ids = (
        selected_tag_ids
        + new_tag_ids
    )

    # A label should only be attached once even if it appeared twice.
    return list(
        dict.fromkeys(
            all_tag_ids
        )
    )


# Create a task and connect its labels in one place.
def create_task_with_tags(
    user_id,
    task_data
):
    """Create a task first and then connect all of its labels."""

    task_id = create_task(
        user_id=user_id,
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data["priority"],
        start_date=task_data["start_date"],
        due_date=task_data["due_date"]
    )

    all_tag_ids = get_combined_tag_ids(
        user_id=user_id,
        selected_tag_ids=task_data[
            "selected_tag_ids"
        ],
        new_tags_text=task_data[
            "new_tags_text"
        ]
    )

    set_task_tags(
        task_id=task_id,
        user_id=user_id,
        tag_ids=all_tag_ids
    )

    return task_id


# Attach labels to every task before sending them to the page.
# Otherwise the template knows the task,
# but not which labels belong to it.
def add_tags_to_tasks(
    tasks,
    user_id
):
    """Add the correct labels to every task before displaying them."""

    tasks_with_tags = []

    for task in tasks:

        # SQLite rows are changed into dictionaries so I can add more data.
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
    """Add the correct subtasks to every task before displaying them."""

    tasks_with_subtasks = []

    for task in tasks:

        # Same idea as tags: make a dictionary first so extra data can be added.
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


# Load tasks together with the extra information
# needed by the task pages.
def get_tasks_with_details(user_id):
    """Get a user's tasks together with their labels and subtasks."""

    tasks = get_tasks_by_user(
        user_id
    )

    # Add the extra information one layer at a time.
    tasks = add_tags_to_tasks(
        tasks,
        user_id
    )

    tasks = add_subtasks_to_tasks(
        tasks,
        user_id
    )

    return tasks
