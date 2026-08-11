document.addEventListener("DOMContentLoaded", () => {

    // -----------------------------
    // Utility: format seconds -> HH:MM:SS
    // -----------------------------
    function formatTime(seconds) {
        const h = String(Math.floor(seconds / 3600)).padStart(2, "0");
        const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
        const s = String(seconds % 60).padStart(2, "0");
        return `${h}:${m}:${s}`;
    }

    // -----------------------------
    // Spawn a new empty case
    // -----------------------------
    let newCaseCounter = 1;

    function spawnEmptyCase() {
        const template = document.querySelector(".case-template");
        if (!template) return;

        const clone = template.cloneNode(true);

        // Assign unique ID
        const uniqueId = `new_${newCaseCounter++}`;
        clone.dataset.caseId = uniqueId;

        // Update field names
        clone.querySelector(".case-body").name = `case_body_${uniqueId}`;
        clone.querySelector(".case-hours").name = `case_hours_${uniqueId}`;

        // Reset fields
        clone.querySelector(".case-body").value = "";
        clone.querySelector(".case-hours").value = "";
        clone.querySelector('input[data-field="created"]').value = "";
        clone.querySelector('input[data-field="logged_by"]').value = "";
        clone.querySelector(".case-timer-display").textContent = "00:00:00";

        // Append to cases tab
        const container = document.querySelector("#cases");
        container.appendChild(clone);

        // Re-bind logic
        setupNewCase(clone);
        setupTimer(clone);
    }

    // -----------------------------
    // Auto-init NEW case + spawn next empty case
    // -----------------------------
    function setupNewCase(caseEl) {

        let initialized = false;

        const bodyField = caseEl.querySelector(".case-body");
        const hoursField = caseEl.querySelector(".case-hours");
        const createdField = caseEl.querySelector('input[data-field="created"]');
        const loggedByField = caseEl.querySelector('input[data-field="logged_by"]');

        function initNewCase() {
            if (initialized) return;
            initialized = true;

            // Fill created date
            const today = new Date().toISOString().split("T")[0];
            createdField.value = today;

            // Fill logged_by
            loggedByField.value = window.CURRENT_USERNAME;

            // Mark as pending
            caseEl.dataset.caseId = "pending";

            // Spawn next empty case
            spawnEmptyCase();
        }

        bodyField.addEventListener("input", initNewCase);
        hoursField.addEventListener("input", initNewCase);
    }

    // -----------------------------
    // Timer logic for each case
    // -----------------------------
    function setupTimer(caseEl) {
        const timerBtn = caseEl.querySelector(".case-timer-btn");
        const timerDisplay = caseEl.querySelector(".case-timer-display");
        const hoursField = caseEl.querySelector(".case-hours");

        if (!timerBtn || !timerDisplay) return;

        let timerRunning = false;
        let timerSeconds = 0;
        let timerInterval = null;

        timerBtn.addEventListener("click", () => {
            if (!timerRunning) {
                timerRunning = true;
                timerBtn.textContent = "⏱ Stop Timer";

                timerInterval = setInterval(() => {
                    timerSeconds++;
                    timerDisplay.textContent = formatTime(timerSeconds);
                }, 1000);

            } else {
                timerRunning = false;
                timerBtn.textContent = "⏱ Start Timer";

                clearInterval(timerInterval);

                const hours = timerSeconds / 3600;
                const rounded = Math.round(hours * 4) / 4;
                hoursField.value = rounded;
            }
        });
    }

    // -----------------------------
    // Initialize existing cases + first empty case
    // -----------------------------
    document.querySelectorAll(".case-item").forEach(caseEl => {
        setupTimer(caseEl);

        if (caseEl.dataset.caseId === "new") {
            setupNewCase(caseEl);
        }
    });

});
