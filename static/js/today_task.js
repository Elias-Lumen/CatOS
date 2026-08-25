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
                taskComposer.querySelector(
                    'input[name="title"]'
                );

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

            taskComposer
                .querySelectorAll(".new-tags-value")
                .forEach((input) => {
                    input.value = "";
                });

            taskComposer
                .querySelectorAll(".pending-label-item")
                .forEach((item) => {
                    item.remove();
                });

            taskComposer
                .querySelectorAll(".label-button-text")
                .forEach((text) => {
                    text.textContent = "Labels";
                });

            taskComposer
                .querySelectorAll(".label-menu")
                .forEach((menu) => {
                    menu.classList.add("hidden");
                });

            taskComposer.classList.add("hidden");

            showComposerButton.style.display =
                "inline-block";

        });

    }


    // Close task editor
    function closeTaskEditor(taskId) {

        const display =
            document.getElementById(
                `taskDisplay${taskId}`
            );

        const form =
            document.getElementById(
                `taskEdit${taskId}`
            );

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

                const taskId =
                    button.dataset.taskId;

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


                updateAllLabelButtons(form);


                const titleInput =
                    form.querySelector(
                        ".edit-title"
                    );

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

                const taskId =
                    button.dataset.taskId;

                closeTaskEditor(taskId);

            });

        });


    // Close editor automatically if nothing was changed
    document
        .querySelectorAll(".task-edit-form")
        .forEach((form) => {

            form.addEventListener("focusout", () => {

                setTimeout(() => {

                    if (
                        form.contains(
                            document.activeElement
                        )
                    ) {
                        return;
                    }

                    const current =
                        new URLSearchParams(
                            new FormData(form)
                        ).toString();

                    if (
                        current !==
                        form.dataset.original
                    ) {
                        return;
                    }

                    const taskId =
                        form.id.replace(
                            "taskEdit",
                            ""
                        );

                    closeTaskEditor(taskId);

                }, 0);

            });

        });


    // LABEL PICKERS

    function getPendingLabels(picker) {

        const hiddenInput =
            picker.querySelector(
                ".new-tags-value"
            );

        if (
            !hiddenInput ||
            !hiddenInput.value
        ) {
            return [];
        }

        return hiddenInput.value
            .split(",")
            .map((label) => label.trim())
            .filter(Boolean);

    }


    function savePendingLabels(
        picker,
        labels
    ) {

        const hiddenInput =
            picker.querySelector(
                ".new-tags-value"
            );

        if (!hiddenInput) {
            return;
        }

        hiddenInput.value =
            labels.join(",");

    }


    function updateLabelButton(picker) {

        const buttonText =
            picker.querySelector(
                ".label-button-text"
            );

        if (!buttonText) {
            return;
        }

        const selectedExisting =
            picker.querySelectorAll(
                ".label-checkbox:checked"
            ).length;

        const pendingLabels =
            getPendingLabels(picker);

        const count =
            selectedExisting +
            pendingLabels.length;

        if (count === 0) {

            buttonText.textContent =
                "Labels";

        } else if (count === 1) {

            buttonText.textContent =
                "1 Label";

        } else {

            buttonText.textContent =
                `${count} Labels`;

        }

    }


    function updateAllLabelButtons(
        container = document
    ) {

        container
            .querySelectorAll(
                ".label-picker"
            )
            .forEach((picker) => {

                updateLabelButton(picker);

            });

    }


    function resetLabelSearch(picker) {

        const search =
            picker.querySelector(
                ".label-search"
            );

        const createButton =
            picker.querySelector(
                ".create-label-button"
            );

        picker
            .querySelectorAll(
                ".label-item"
            )
            .forEach((item) => {

                item.classList.remove(
                    "hidden"
                );

            });

        if (search) {
            search.value = "";
        }

        if (createButton) {
            createButton.classList.add(
                "hidden"
            );
        }

    }


    function addPendingLabel(
        picker,
        labelName
    ) {

        const cleanName =
            labelName.trim();

        if (!cleanName) {
            return;
        }

        let pendingLabels =
            getPendingLabels(picker);

        const alreadyPending =
            pendingLabels.some(
                (label) =>
                    label.toLowerCase() ===
                    cleanName.toLowerCase()
            );

        if (alreadyPending) {
            return;
        }


        const existingNames =
            Array.from(
                picker.querySelectorAll(
                    ".label-item:not(.pending-label-item)"
                )
            ).map((item) =>
                item.dataset.labelName
            );


        if (
            existingNames.includes(
                cleanName.toLowerCase()
            )
        ) {
            return;
        }


        pendingLabels.push(cleanName);

        savePendingLabels(
            picker,
            pendingLabels
        );


        const labelList =
            picker.querySelector(
                ".label-list"
            );

        if (labelList) {

            const item =
                document.createElement(
                    "label"
                );

            item.className =
                "label-item pending-label-item";

            item.dataset.labelName =
                cleanName.toLowerCase();


            const left =
                document.createElement(
                    "span"
                );

            left.className =
                "label-item-left";


            const icon =
                document.createElement(
                    "img"
                );

            icon.className =
                "label-tag-icon";

            icon.src =
                "/static/icons/label.svg";

            icon.alt = "";


            const name =
                document.createElement(
                    "span"
                );

            name.className =
                "label-name";

            name.textContent =
                cleanName;


            const checkbox =
                document.createElement(
                    "input"
                );

            checkbox.type =
                "checkbox";

            checkbox.checked =
                true;

            checkbox.className =
                "pending-label-checkbox";


            checkbox.addEventListener(
                "change",
                () => {

                    if (
                        !checkbox.checked
                    ) {

                        pendingLabels =
                            getPendingLabels(
                                picker
                            ).filter(
                                (label) =>
                                    label
                                        .toLowerCase() !==
                                    cleanName
                                        .toLowerCase()
                            );

                        savePendingLabels(
                            picker,
                            pendingLabels
                        );

                        item.remove();

                        updateLabelButton(
                            picker
                        );

                    }

                }
            );


            left.appendChild(icon);
            left.appendChild(name);

            item.appendChild(left);
            item.appendChild(checkbox);

            labelList.appendChild(item);

        }


        updateLabelButton(picker);

    }


    document
        .querySelectorAll(
            ".label-picker"
        )
        .forEach((picker) => {

            const button =
                picker.querySelector(
                    ".label-button"
                );

            const menu =
                picker.querySelector(
                    ".label-menu"
                );

            const search =
                picker.querySelector(
                    ".label-search"
                );

            const createButton =
                picker.querySelector(
                    ".create-label-button"
                );

            const preview =
                picker.querySelector(
                    ".new-label-preview"
                );


            if (!button || !menu) {
                return;
            }


            button.addEventListener(
                "click",
                (event) => {

                    event.stopPropagation();


                    document
                        .querySelectorAll(
                            ".label-menu"
                        )
                        .forEach(
                            (otherMenu) => {

                                if (
                                    otherMenu !==
                                    menu
                                ) {

                                    otherMenu
                                        .classList
                                        .add(
                                            "hidden"
                                        );

                                }

                            }
                        );


                    menu.classList.toggle(
                        "hidden"
                    );


                    if (
                        !menu.classList.contains(
                            "hidden"
                        )
                    ) {

                        updateLabelButton(
                            picker
                        );

                        if (search) {
                            search.focus();
                        }

                    }

                }
            );


            menu.addEventListener(
                "click",
                (event) => {

                    event.stopPropagation();

                }
            );


            picker
                .querySelectorAll(
                    ".label-checkbox"
                )
                .forEach(
                    (checkbox) => {

                        checkbox.addEventListener(
                            "change",
                            () => {

                                updateLabelButton(
                                    picker
                                );

                            }
                        );

                    }
                );


            if (search) {

                search.addEventListener(
                    "input",
                    () => {

                        const searchText =
                            search.value
                                .trim();

                        const searchValue =
                            searchText
                                .toLowerCase();

                        let exactMatch =
                            false;


                        picker
                            .querySelectorAll(
                                ".label-item"
                            )
                            .forEach(
                                (item) => {

                                    const name =
                                        item.dataset
                                            .labelName;

                                    const matches =
                                        name.includes(
                                            searchValue
                                        );

                                    item.classList.toggle(
                                        "hidden",
                                        !matches
                                    );


                                    if (
                                        name ===
                                        searchValue
                                    ) {

                                        exactMatch =
                                            true;

                                    }

                                }
                            );


                        if (
                            createButton &&
                            preview
                        ) {

                            if (
                                searchValue &&
                                !exactMatch
                            ) {

                                preview.textContent =
                                    `"${searchText}"`;

                                createButton
                                    .classList
                                    .remove(
                                        "hidden"
                                    );

                            } else {

                                createButton
                                    .classList
                                    .add(
                                        "hidden"
                                    );

                            }

                        }

                    }
                );


                search.addEventListener(
                    "keydown",
                    (event) => {

                        if (
                            event.key !==
                            "Enter"
                        ) {
                            return;
                        }

                        const value =
                            search.value.trim();

                        if (!value) {
                            return;
                        }

                        event.preventDefault();

                        addPendingLabel(
                            picker,
                            value
                        );

                        resetLabelSearch(
                            picker
                        );

                    }
                );

            }


            if (
                createButton &&
                search
            ) {

                createButton.addEventListener(
                    "click",
                    () => {

                        const value =
                            search.value.trim();

                        if (!value) {
                            return;
                        }

                        addPendingLabel(
                            picker,
                            value
                        );

                        resetLabelSearch(
                            picker
                        );

                    }
                );

            }


            updateLabelButton(
                picker
            );

        });


    // Click outside closes label menus
    document.addEventListener(
        "click",
        () => {

            document
                .querySelectorAll(
                    ".label-menu"
                )
                .forEach((menu) => {

                    menu.classList.add(
                        "hidden"
                    );

                });

        }
    );


    // Priority picker
    const priorityButton =
        document.getElementById(
            "priorityButton"
        );

    const priorityMenu =
        document.getElementById(
            "priorityMenu"
        );

    const priorityValue =
        document.getElementById(
            "priorityValue"
        );

    const priorityButtonText =
        document.getElementById(
            "priorityButtonText"
        );

    const priorityButtonIcon =
        document.getElementById(
            "priorityButtonIcon"
        );

    const priorityItems =
        document.querySelectorAll(
            ".priority-item"
        );


    if (
        priorityButton &&
        priorityMenu &&
        priorityValue &&
        priorityButtonText &&
        priorityButtonIcon
    ) {

        priorityButton.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

                priorityMenu.classList.toggle(
                    "hidden"
                );

            }
        );


        priorityMenu.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

            }
        );


        priorityItems.forEach((item) => {

            item.addEventListener(
                "click",
                () => {

                    const priority =
                        item.dataset.priority;

                    priorityValue.value =
                        priority;

                    priorityButtonText.textContent =
                        priority
                            .charAt(0)
                            .toUpperCase()
                        + priority.slice(1);

                    priorityButtonIcon.src =
                        `/static/icons/priority-${priority}.svg`;

                    priorityItems.forEach(
                        (option) => {

                            option.classList.remove(
                                "selected"
                            );

                        }
                    );

                    item.classList.add(
                        "selected"
                    );

                    priorityMenu.classList.add(
                        "hidden"
                    );

                }
            );

        });

    }


    // Confirm task deletion
    document
        .querySelectorAll(
            ".task-delete-form"
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

});