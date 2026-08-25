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


    // SUBTASKS
    // Keep them folded by default so one task cannot take over the whole page.

    document
        .querySelectorAll(
            ".subtask-toggle, .show-subtask-form"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                (event) => {

                    // Do not let the subtask button trigger other task click events.
                    event.stopPropagation();


                    const targetId =
                        button.dataset
                            .subtaskTarget;


                    const list =
                        document.getElementById(
                            targetId
                        );


                    if (!list) {
                        return;
                    }


                    list.classList.toggle(
                        "hidden"
                    );


                    // Only the real subtask toggle has an arrow.
                    const arrow =
                        button.querySelector(
                            ".subtask-arrow"
                        );


                    if (arrow) {

                        arrow.textContent =
                            list.classList.contains(
                                "hidden"
                            )
                                ? "▸"
                                : "▾";

                    }


                    // The + Add subtask button is only needed before the list opens.
                    if (
                        button.classList.contains(
                            "show-subtask-form"
                        )
                    ) {

                        button.classList.add(
                            "hidden"
                        );


                        const input =
                            list.querySelector(
                                ".subtask-add-input"
                            );


                        if (input) {
                            input.focus();
                        }

                    }

                }
            );

        });

    // EDIT SUBTASK
    document
        .querySelectorAll(
            ".subtask-edit-button"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                (event) => {

                    event.stopPropagation();

                    const subtaskId =
                        button.dataset.subtaskId;

                    const display =
                        document.getElementById(
                            `subtaskDisplay${subtaskId}`
                        );

                    const form =
                        document.getElementById(
                            `subtaskEdit${subtaskId}`
                        );

                    const actions =
                        document.getElementById(
                            `subtaskActions${subtaskId}`
                        );

                    if (
                        !display ||
                        !form ||
                        !actions
                    ) {
                        return;
                    }

                    display.classList.add(
                        "hidden"
                    );

                    actions.classList.add(
                        "hidden"
                    );

                    form.classList.remove(
                        "hidden"
                    );


                    const input =
                        form.querySelector(
                            ".subtask-edit-input"
                        );

                    if (input) {

                        input.focus();
                        input.select();

                    }

                }
            );

        });


    // CANCEL SUBTASK EDIT
    document
        .querySelectorAll(
            ".subtask-cancel-button"
        )
        .forEach((button) => {

            button.addEventListener(
                "click",
                (event) => {

                    event.stopPropagation();

                    const subtaskId =
                        button.dataset.subtaskId;

                    const display =
                        document.getElementById(
                            `subtaskDisplay${subtaskId}`
                        );

                    const form =
                        document.getElementById(
                            `subtaskEdit${subtaskId}`
                        );

                    const actions =
                        document.getElementById(
                            `subtaskActions${subtaskId}`
                        );

                    if (
                        !display ||
                        !form ||
                        !actions
                    ) {
                        return;
                    }

                    form.classList.add(
                        "hidden"
                    );

                    display.classList.remove(
                        "hidden"
                    );

                    actions.classList.remove(
                        "hidden"
                    );

                }
            );

        });


    // CONFIRM BEFORE DELETING A SUBTASK
    document
        .querySelectorAll(
            ".subtask-delete-form"
        )
        .forEach((form) => {

            form.addEventListener(
                "submit",
                (event) => {

                    const confirmed =
                        window.confirm(
                            "Delete this subtask?"
                        );

                    if (!confirmed) {

                        event.preventDefault();

                    }

                }
            );

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
// Labels are saved and reused.
// Search the old ones first, and only create a new one if it really does not exist.

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


// Update the Labels button so the user can see how many are selected.
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


// Clear the search and show all the saved labels again.
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


// Find a saved label with exactly the same name.
// Lowercase is used here so School and school count as the same label.
function findExactLabel(
    picker,
    labelName
) {

    const wantedName =
        labelName
            .trim()
            .toLowerCase();


    if (!wantedName) {
        return null;
    }


    return Array
        .from(
            picker.querySelectorAll(
                ".label-item:not(.pending-label-item)"
            )
        )
        .find((item) => {

            return (
                item.dataset.labelName ===
                wantedName
            );

        }) || null;

}


// Select an existing label instead of accidentally making another copy.
function selectExistingLabel(
    picker,
    item
) {

    if (!item) {
        return;
    }


    const checkbox =
        item.querySelector(
            ".label-checkbox"
        );


    if (!checkbox) {
        return;
    }


    checkbox.checked = true;

    updateLabelButton(picker);

    resetLabelSearch(picker);

}


// New labels only get here after we already checked the saved ones.
function addPendingLabel(
    picker,
    labelName
) {

    const cleanName =
        labelName.trim();

    if (!cleanName) {
        return;
    }


    // If this label already exists, just select it.
    const existingLabel =
        findExactLabel(
            picker,
            cleanName
        );


    if (existingLabel) {

        selectExistingLabel(
            picker,
            existingLabel
        );

        return;
    }

    let pendingLabels =
        getPendingLabels(picker);

    // Do not create the same new label twice before the task is saved.
    const alreadyPending =
        pendingLabels.some(
            (label) =>
                label.toLowerCase() ===
                cleanName.toLowerCase()
        );

    if (alreadyPending) {
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


        // New labels are made with JS, so the SVG has to be added here too.
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


        // Unticking a new label removes it because it has not been saved yet.
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


// Set up every label picker on the page.
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


        // Open this label menu and close any other one.
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


        // Clicking inside the menu should not close it.
        menu.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

            }
        );


        // Existing labels can be selected and reused as many times as needed.
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
                        search.value.trim();

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


                    // Only offer Create when there is no saved label
                    // with exactly the same name.
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


                    // Exact saved label found:
                    // Enter selects it instead of creating another one.
                    const existingLabel =
                        findExactLabel(
                            picker,
                            value
                        );


                    if (existingLabel) {

                        selectExistingLabel(
                            picker,
                            existingLabel
                        );

                        return;

                    }


                    // No exact saved label exists, so this really is a new one.
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


                    // Check one more time before creating.
                    // Better to be annoyingly safe than make duplicate labels.
                    const existingLabel =
                        findExactLabel(
                            picker,
                            value
                        );


                    if (existingLabel) {

                        selectExistingLabel(
                            picker,
                            existingLabel
                        );

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