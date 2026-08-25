/*
    CatOS - Task Detail Modal
    -------------------------
    Controls opening and closing the floating task detail window.

    The task modal is intentionally separate from today_task.js
    so the existing composer / edit / label code does not need
    to be changed.
*/

document.addEventListener(
    "DOMContentLoaded",
    () => {

        let activeModal = null;


        /*
            Open a task modal by task ID.
        */
        function openTaskModal(taskId) {

            const modal =
                document.getElementById(
                    `taskModal${taskId}`
                );

            if (!modal) {
                return;
            }


            /*
                Close another modal first if one is already open.
            */
            if (
                activeModal &&
                activeModal !== modal
            ) {

                closeTaskModal(
                    activeModal
                );

            }


            modal.classList.remove(
                "hidden"
            );

            modal.setAttribute(
                "aria-hidden",
                "false"
            );


            document.body.classList.add(
                "task-modal-open"
            );


            activeModal = modal;


            /*
                Move keyboard focus to the close button
                after opening the dialog.
            */
            const closeButton =
                modal.querySelector(
                    "[data-close-task-modal]"
                );

            if (closeButton) {
                closeButton.focus();
            }

        }


        /*
            Close a task modal.
        */
        function closeTaskModal(modal) {

            if (!modal) {
                return;
            }


            modal.classList.add(
                "hidden"
            );

            modal.setAttribute(
                "aria-hidden",
                "true"
            );


            document.body.classList.remove(
                "task-modal-open"
            );


            if (activeModal === modal) {
                activeModal = null;
            }

        }


        /*
            Open the modal when the normal task display
            is clicked.
        */
        document
            .querySelectorAll(
                ".task-open-area"
            )
            .forEach((taskArea) => {

                taskArea.addEventListener(
                    "click",
                    () => {

                        const taskId =
                            taskArea.dataset.taskId;

                        openTaskModal(
                            taskId
                        );

                    }
                );


                /*
                    Keyboard support:
                    Enter or Space opens the task.
                */
                taskArea.addEventListener(
                    "keydown",
                    (event) => {

                        if (
                            event.key !== "Enter" &&
                            event.key !== " "
                        ) {
                            return;
                        }


                        event.preventDefault();


                        const taskId =
                            taskArea.dataset.taskId;

                        openTaskModal(
                            taskId
                        );

                    }
                );

            });


        /*
            Close buttons inside the modal.
        */
        document
            .querySelectorAll(
                "[data-close-task-modal]"
            )
            .forEach((button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const modal =
                            button.closest(
                                ".task-modal-overlay"
                            );

                        closeTaskModal(
                            modal
                        );

                    }
                );

            });


        /*
            Clicking the dark background closes the modal.

            Clicking the white modal itself does not close it.
        */
        document
            .querySelectorAll(
                ".task-modal-overlay"
            )
            .forEach((overlay) => {

                overlay.addEventListener(
                    "click",
                    (event) => {

                        if (
                            event.target !== overlay
                        ) {
                            return;
                        }


                        closeTaskModal(
                            overlay
                        );

                    }
                );

            });


        /*
            Escape closes the currently open task modal.
        */
        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape" ||
                    !activeModal
                ) {
                    return;
                }


                const modalToClose =
                    activeModal;


                closeTaskModal(
                    modalToClose
                );


                /*
                    Return focus to the task row that
                    originally opened this modal.
                */
                const taskId =
                    modalToClose.dataset.taskModal;


                const taskArea =
                    document.querySelector(
                        `.task-open-area[data-task-id="${taskId}"]`
                    );


                if (taskArea) {
                    taskArea.focus();
                }

            }
        );


        /*
            EDIT FROM MODAL

            Instead of creating another editing system,
            this button closes the modal and clicks the
            existing inline edit button.

            This keeps only one source of edit logic.
        */
        document
            .querySelectorAll(
                "[data-modal-edit-task]"
            )
            .forEach((button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const taskId =
                            button.dataset
                                .modalEditTask;


                        const modal =
                            button.closest(
                                ".task-modal-overlay"
                            );


                        closeTaskModal(
                            modal
                        );


                        const existingEditButton =
                            document.querySelector(
                                `.task-edit-button[data-task-id="${taskId}"]`
                            );


                        if (
                            existingEditButton
                        ) {

                            existingEditButton.click();

                        }

                    }
                );

            });


        /*
            DELETE CONFIRMATION INSIDE MODAL

            The existing Today page already has delete
            confirmation behaviour. This duplicate form
            lives inside the modal, so it receives its own
            confirmation here.
        */
        document
            .querySelectorAll(
                ".task-modal-delete-form"
            )
            .forEach((form) => {

                form.addEventListener(
                    "submit",
                    (event) => {

                        const confirmed =
                            window.confirm(
                                "Delete this task?"
                            );


                        if (!confirmed) {

                            event.preventDefault();

                        }

                    }
                );

            });

    }
);