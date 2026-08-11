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