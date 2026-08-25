/*
    CatOS - Floating Add Task Modal
    --------------------------------
    Opens the Add Task window from the sidebar
    without leaving the current page.
*/

document.addEventListener(
    "DOMContentLoaded",
    () => {

        // Main modal controls
        const openButton =
            document.getElementById(
                "openTaskModal"
            );

        const overlay =
            document.getElementById(
                "addTaskOverlay"
            );

        const closeButton =
            document.getElementById(
                "closeTaskModal"
            );

        const cancelButton =
            document.getElementById(
                "cancelTaskModal"
            );

        const taskForm =
            overlay
                ? overlay.querySelector(
                    ".add-task-modal-form"
                )
                : null;


        // Stop here if this page does not contain the modal.
        if (
            !openButton ||
            !overlay
        ) {
            return;
        }


        /*
            Open modal.
        */
        function openTaskModal() {

            overlay.classList.remove(
                "hidden"
            );

            overlay.setAttribute(
                "aria-hidden",
                "false"
            );

            document.body.classList.add(
                "task-modal-open"
            );


            // Focus the task title automatically.
            const titleInput =
                overlay.querySelector(
                    'input[name="title"]'
                );

            if (titleInput) {
                titleInput.focus();
            }

        }


        /*
            Close modal.
        */
        function closeTaskModal() {

            overlay.classList.add(
                "hidden"
            );

            overlay.setAttribute(
                "aria-hidden",
                "true"
            );

            document.body.classList.remove(
                "task-modal-open"
            );


            // Return keyboard focus to Add task.
            openButton.focus();

        }


        /*
            Open from sidebar.
        */
        openButton.addEventListener(
            "click",
            () => {

                openTaskModal();

            }
        );


        /*
            Close using X button.
        */
        if (closeButton) {

            closeButton.addEventListener(
                "click",
                () => {

                    closeTaskModal();

                }
            );

        }


        /*
            Close using Cancel button.
        */
        if (cancelButton) {

            cancelButton.addEventListener(
                "click",
                () => {

                    closeTaskModal();

                }
            );

        }


        /*
            Click outside the white modal window
            to close it.
        */
        overlay.addEventListener(
            "click",
            (event) => {

                if (
                    event.target === overlay
                ) {

                    closeTaskModal();

                }

            }
        );


        /*
            Escape closes the modal.
        */
        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape"
                ) {
                    return;
                }


                if (
                    overlay.classList.contains(
                        "hidden"
                    )
                ) {
                    return;
                }


                closeTaskModal();

            }
        );


        /*
            Prevent clicks inside the modal itself
            from closing the window.
        */
        const modalWindow =
            overlay.querySelector(
                ".add-task-modal"
            );

        if (modalWindow) {

            modalWindow.addEventListener(
                "click",
                (event) => {

                    event.stopPropagation();

                }
            );

        }


        /*
            Reset the form when the user manually closes it.

            This keeps old title / description values from
            appearing the next time the modal is opened.
        */
        function resetTaskForm() {

            if (!taskForm) {
                return;
            }

            taskForm.reset();

        }


        /*
            Reset when Cancel is pressed.
        */
        if (cancelButton) {

            cancelButton.addEventListener(
                "click",
                () => {

                    resetTaskForm();

                }
            );

        }


        /*
            Reset when the X button is pressed.
        */
        if (closeButton) {

            closeButton.addEventListener(
                "click",
                () => {

                    resetTaskForm();

                }
            );

        }


        /*
            Reset when clicking the dark overlay.
        */
        overlay.addEventListener(
            "click",
            (event) => {

                if (
                    event.target !== overlay
                ) {
                    return;
                }

                resetTaskForm();

            }
        );


        /*
            Make sure the modal begins closed,
            even if another CSS rule accidentally
            interferes with the hidden class.
        */
        overlay.classList.add(
            "hidden"
        );

        overlay.setAttribute(
            "aria-hidden",
            "true"
        );

    }
);