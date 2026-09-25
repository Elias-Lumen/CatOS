"""Routes used for the Search, Data, and Help pages in CatOS."""

from datetime import (
    date,
    datetime,
    timedelta,
    timezone,
)

from flask import (
    render_template,
    request,
    session,
)

from database import (
    search_tasks,
    get_tags_by_user,
    get_task_statistics,
)

from utils import (
    login_required,
    add_tags_to_tasks,
)


def register_page_routes(app):
    """Register the general page routes into the main CatOS app."""

    # Search page.
    @app.route("/search")
    @login_required
    def search():
        """Search the current user's tasks using the selected filters."""

        user_id = session["user_id"]

        # Read all filters from the URL.
        # Missing filters just become empty strings.
        query = request.args.get(
            "q",
            ""
        ).strip()

        tag_id = request.args.get(
            "label",
            ""
        ).strip()

        priority = request.args.get(
            "priority",
            ""
        ).strip()

        state = request.args.get(
            "status",
            ""
        ).strip()

        # Label ids should be numbers.
        # Anything else is treated as no label filter.
        if tag_id.isdigit():

            tag_id_value = int(
                tag_id
            )

        else:

            tag_id_value = None
            tag_id = ""

        # Only allow priorities that actually exist in CatOS.
        valid_priorities = {
            "normal",
            "low",
            "medium",
            "high",
        }

        if priority not in valid_priorities:
            priority = ""

        # Same thing for task states.
        valid_states = {
            "not_started",
            "in_progress",
            "completed",
        }

        if state not in valid_states:
            state = ""

        # There is no reason to search the whole database
        # until the user actually enters at least one filter.
        search_active = bool(
            query
            or tag_id_value
            or priority
            or state
        )

        if search_active:

            tasks = search_tasks(
                user_id=user_id,
                query=query,
                tag_id=tag_id_value,
                priority=priority or None,
                state=state or None
            )

            # Search results also need their labels
            # before they can be displayed on the page.
            tasks = add_tags_to_tasks(
                tasks,
                user_id
            )

        else:

            tasks = []

        # All labels are needed for the search filter menu.
        tags = get_tags_by_user(
            user_id
        )

        return render_template(
            "search.html",
            tasks=tasks,
            tags=tags,
            query=query,
            selected_label=tag_id,
            selected_priority=priority,
            selected_status=state,
            search_active=search_active
        )


    # Data page.
    @app.route("/data")
    @login_required
    def data():
        """Calculate and show the user's task statistics."""

        user_id = session["user_id"]

        tasks = get_task_statistics(
            user_id
        )

        # SQLite CURRENT_TIMESTAMP is stored in UTC.
        # Convert it to local time before comparing dates.
        def local_date_from_sqlite(
            timestamp
        ):
            """Turn a SQLite UTC timestamp into a local date."""

            # Some tasks are not completed yet,
            # so completed_at can be empty.
            if not timestamp:
                return None

            utc_time = datetime.fromisoformat(
                str(timestamp)
            ).replace(
                tzinfo=timezone.utc
            )

            return (
                utc_time
                .astimezone()
                .date()
            )

        # Basic numbers for the top of the Data page.
        total_tasks = len(
            tasks
        )

        completed_tasks = sum(
            1
            for task in tasks
            if task["state"]
            == "completed"
        )

        # Avoid dividing by zero when the user has no tasks yet.
        if total_tasks == 0:

            completion_rate = 0

        else:

            completion_rate = round(
                (
                    completed_tasks
                    / total_tasks
                )
                * 100
            )

        today_date = date.today()

        created_today = 0
        completed_today = 0

        # Count tasks created and completed today separately.
        for task in tasks:

            created_date = local_date_from_sqlite(
                task["created_at"]
            )

            completed_date = local_date_from_sqlite(
                task["completed_at"]
            )

            if created_date == today_date:
                created_today += 1

            if completed_date == today_date:
                completed_today += 1

        # weekday() uses Monday as 0,
        # so this finds the Monday of the current week.
        week_start = (
            today_date
            - timedelta(
                days=today_date.weekday()
            )
        )

        week_days = []

        # Build one set of data for each day from Monday to Sunday.
        for day_number in range(7):

            current_date = (
                week_start
                + timedelta(
                    days=day_number
                )
            )

            # Count how many tasks were completed on this day.
            completed_count = sum(
                1
                for task in tasks
                if local_date_from_sqlite(
                    task["completed_at"]
                ) == current_date
            )

            week_days.append({
                "name": current_date.strftime(
                    "%a"
                ),
                "date": current_date.isoformat(),
                "completed": completed_count
            })

        # Find the busiest day so the chart bars
        # can be scaled relative to the largest value.
        max_weekly_completed = max(
            (
                day["completed"]
                for day in week_days
            ),
            default=0
        )

        for day in week_days:

            # If nothing was completed this week,
            # every bar should just have zero height.
            if max_weekly_completed == 0:

                day["height"] = 0

            else:

                # The busiest day becomes 100%.
                # Other bars are shown relative to that day.
                day["height"] = round(
                    (
                        day["completed"]
                        / max_weekly_completed
                    )
                    * 100
                )

        return render_template(
            "data.html",

            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_rate=completion_rate,

            created_today=created_today,
            completed_today=completed_today,

            week_days=week_days,
            max_weekly_completed=max_weekly_completed
        )


    # Help page.
    @app.route("/help")
    def help_page():
        """Show the CatOS Help page."""

        # Nothing complicated here for now.
        # It is just a normal static help page.
        return render_template(
            "help.html"
        )
