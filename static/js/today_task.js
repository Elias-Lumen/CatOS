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


    // Show add-task composer
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
                taskComposer.querySelector(
                    'input[name="title"]'
                );

            if (titleInput) {
                titleInput.focus();
            }

        });

    }


    // Hide composer when Cancel is clicked
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


    // Open task editor
    const editButtons =
        document.querySelectorAll(".task-edit-button");

    editButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const taskId = button.dataset.taskId;

            const taskDisplay =
                document.getElementById(
                    `taskDisplay${taskId}`
                );

            const taskEditForm =
                document.getElementById(
                    `taskEdit${taskId}`
                );

            if (!taskDisplay || !taskEditForm) {
                return;
            }

            taskDisplay.classList.add("hidden");

            taskEditForm.classList.remove("hidden");

            button.classList.add("hidden");


            const titleInput =
                taskEditForm.querySelector(".edit-title");

            if (titleInput) {
                titleInput.focus();
                titleInput.select();
            }

        });

    });


    // Close task editor
    const cancelEditButtons =
        document.querySelectorAll(".edit-cancel");

    cancelEditButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const taskId = button.dataset.taskId;

            const taskDisplay =
                document.getElementById(
                    `taskDisplay${taskId}`
                );

            const taskEditForm =
                document.getElementById(
                    `taskEdit${taskId}`
                );

            const editButton =
                document.querySelector(
                    `.task-edit-button[data-task-id="${taskId}"]`
                );

            if (
                !taskDisplay ||
                !taskEditForm ||
                !editButton
            ) {
                return;
            }

            taskEditForm.classList.add("hidden");

            taskDisplay.classList.remove("hidden");

            editButton.classList.remove("hidden");

        });

    });

});

const priorityButton = document.getElementById("priorityButton");
const priorityMenu = document.getElementById("priorityMenu");

const priorityValue = document.getElementById("priorityValue");
const priorityButtonText = document.getElementById("priorityButtonText");
const priorityButtonIcon = document.getElementById("priorityButtonIcon");

const priorityItems = document.querySelectorAll(".priority-item");


priorityButton.addEventListener("click", () => {
    priorityMenu.classList.toggle("hidden");
});


priorityItems.forEach((item) => {
    item.addEventListener("click", () => {

        const priority = item.dataset.priority;

        // Give the selected value to Flask
        priorityValue.value = priority;

        // Change button text
        priorityButtonText.textContent =
            priority.charAt(0).toUpperCase() + priority.slice(1);

        // Change button icon
        priorityButtonIcon.src =
            `/static/icons/priority-${priority}.svg`;

        // Update selected option
        priorityItems.forEach((option) => {
            option.classList.remove("selected");
        });

        item.classList.add("selected");

        // Close dropdown
        priorityMenu.classList.add("hidden");
    });
});