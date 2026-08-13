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