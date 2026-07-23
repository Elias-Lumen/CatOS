 const sidebar = document.getElementById("sidebar");
        const sidebarToggle = document.getElementById("sidebarToggle");
        const sidebarResizer = document.getElementById("sidebarResizer");

        const minimumWidth = 180;
        const maximumWidth = 420;
        const collapsedWidth = 64;

        const savedWidth = localStorage.getItem("sidebarWidth");
        const savedCollapsed = localStorage.getItem("sidebarCollapsed");

        if (savedWidth) {
            sidebar.style.width = `${savedWidth}px`;
        }

        if (savedCollapsed === "true") {
            sidebar.classList.add("collapsed");
            sidebarToggle.textContent = "›";
        }

        let isResizing = false;

        sidebarResizer.addEventListener("mousedown", () => {
            if (sidebar.classList.contains("collapsed")) {
                return;
            }

            isResizing = true;
            document.body.classList.add("resizing");
        });

        document.addEventListener("mousemove", (event) => {
            if (!isResizing) {
                return;
            }

            const newWidth = Math.min(
                maximumWidth,
                Math.max(minimumWidth, event.clientX)
            );

            sidebar.style.width = `${newWidth}px`;
        });

        document.addEventListener("mouseup", () => {
            if (!isResizing) {
                return;
            }

            isResizing = false;
            document.body.classList.remove("resizing");

            localStorage.setItem(
                "sidebarWidth",
                sidebar.getBoundingClientRect().width
            );
        });

        sidebarToggle.addEventListener("click", () => {
            const isCollapsed =
                sidebar.classList.toggle("collapsed");

            sidebarToggle.textContent = isCollapsed ? "›" : "‹";

            localStorage.setItem(
                "sidebarCollapsed",
                isCollapsed
            );
        });