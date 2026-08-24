document.addEventListener("DOMContentLoaded", () => {

    // Collapse / expand task groups
    document.querySelectorAll(".group-header").forEach((header) => {

        header.addEventListener("click", () => {

            const targetId = header.dataset.target;
            const content = document.getElementById(targetId);

            if (!content) {
                return;
            }

            content.classList.toggle("collapsed");
            header.classList.toggle("collapsed");

        });

    });


    // Add task composer
    const showComposerButton =
        document.getElementById("showComposer");

    const taskComposer =
        document.getElementById("taskComposer");

    const cancelComposerButton =
        document.getElementById("cancelComposer");


    if (showComposerButton && taskComposer) {

        showComposerButton.addEventListener("click", () => {

            taskComposer.classList.remove("hidden");
            showComposerButton.style.display = "none";

            const titleInput =
                taskComposer.querySelector('input[name="title"]');

            if (titleInput) {
                titleInput.focus();
            }

        });

    }


    if (
        cancelComposerButton &&
        taskComposer &&
        showComposerButton
    ) {

        cancelComposerButton.addEventListener("click", () => {

            taskComposer.reset();
            taskComposer.classList.add("hidden");
            showComposerButton.style.display = "inline-block";

        });

    }


    // Close task editor
    function closeTaskEditor(taskId) {

        const display =
            document.getElementById(`taskDisplay${taskId}`);

        const form =
            document.getElementById(`taskEdit${taskId}`);

        const editButton =
            document.querySelector(
                `.task-edit-button[data-task-id="${taskId}"]`
            );

        if (!display || !form || !editButton) {
            return;
        }

        form.classList.add("hidden");
        display.classList.remove("hidden");
        editButton.classList.remove("hidden");

    }


    // Open task editor
    document
        .querySelectorAll(".task-edit-button")
        .forEach((button) => {

            button.addEventListener("click", () => {

                const taskId = button.dataset.taskId;

                const display =
                    document.getElementById(
                        `taskDisplay${taskId}`
                    );

                const form =
                    document.getElementById(
                        `taskEdit${taskId}`
                    );

                if (!display || !form) {
                    return;
                }

                display.classList.add("hidden");
                form.classList.remove("hidden");
                button.classList.add("hidden");


                // Remember what the form looked like
                // before the user changed anything
                form.dataset.original =
                    new URLSearchParams(
                        new FormData(form)
                    ).toString();


                const titleInput =
                    form.querySelector(".edit-title");

                if (titleInput) {
                    titleInput.focus();
                    titleInput.select();
                }

            });

        });


    // Cancel editing
    document
        .querySelectorAll(".edit-cancel")
        .forEach((button) => {

            button.addEventListener("click", () => {

                const taskId = button.dataset.taskId;

                closeTaskEditor(taskId);

            });

        });


    // Close editor automatically if nothing was changed
    document
        .querySelectorAll(".task-edit-form")
        .forEach((form) => {

            form.addEventListener("focusout", () => {

                setTimeout(() => {

                    // Still clicking inside the form
                    if (form.contains(document.activeElement)) {
                        return;
                    }

                    const current =
                        new URLSearchParams(
                            new FormData(form)
                        ).toString();

                    // Something changed, so keep it open
                    if (current !== form.dataset.original) {
                        return;
                    }

                    const taskId =
                        form.id.replace("taskEdit", "");

                    closeTaskEditor(taskId);

                }, 0);

            });

        });


    // Priority picker
    const priorityButton =
        document.getElementById("priorityButton");

    const priorityMenu =
        document.getElementById("priorityMenu");

    const priorityValue =
        document.getElementById("priorityValue");

    const priorityButtonText =
        document.getElementById("priorityButtonText");

    const priorityButtonIcon =
        document.getElementById("priorityButtonIcon");

    const priorityItems =
        document.querySelectorAll(".priority-item");


    if (
        priorityButton &&
        priorityMenu &&
        priorityValue &&
        priorityButtonText &&
        priorityButtonIcon
    ) {

        priorityButton.addEventListener("click", () => {

            priorityMenu.classList.toggle("hidden");

        });


        priorityItems.forEach((item) => {

            item.addEventListener("click", () => {

                const priority = item.dataset.priority;

                priorityValue.value = priority;

                priorityButtonText.textContent =
                    priority.charAt(0).toUpperCase()
                    + priority.slice(1);

                priorityButtonIcon.src =
                    `/static/icons/priority-${priority}.svg`;

                priorityItems.forEach((option) => {
                    option.classList.remove("selected");
                });

                item.classList.add("selected");

                priorityMenu.classList.add("hidden");

            });

        });

    }
    // Confirm task deletion
    document
        .querySelectorAll(".task-delete-form")
        .forEach((form) => {

            form.addEventListener("submit", (event) => {

                const confirmed =
                    window.confirm(
                        "Delete this task?"
                    );

                if (!confirmed) {
                    event.preventDefault();
                }

            });

        });
});
