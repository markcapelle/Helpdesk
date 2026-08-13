document.addEventListener("DOMContentLoaded", () => {

    let autosaveTimer = null;
    const AUTOSAVE_DELAY = 5000; // 5 seconds
    const form = document.querySelector("form");
    const indicator = document.getElementById("autosaveIndicator");

    if (!form) return;

    // -----------------------------
    // Show "Saved" popup
    // -----------------------------
    function showSavedIndicator() {
        indicator.style.display = "block";
        setTimeout(() => {
            indicator.style.display = "none";
        }, 1500);
    }

    // -----------------------------
    // Perform autosave
    // -----------------------------
    async function autosave() {
        const formData = new FormData(form);

        // Mark as autosave
        formData.append("autosave", "1");

        try {
            const response = await fetch(window.location.href, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();
            if (data.saved) {
                showSavedIndicator();
            }
        } catch (err) {
            console.error("Autosave failed:", err);
        }
    }

    // -----------------------------
    // Reset timer on any change
    // -----------------------------
    function scheduleAutosave() {
        clearTimeout(autosaveTimer);
        autosaveTimer = setTimeout(autosave, AUTOSAVE_DELAY);
    }

    // Watch ALL inputs, textareas, selects
    form.querySelectorAll("input, textarea, select").forEach(el => {
        el.addEventListener("input", scheduleAutosave);
        el.addEventListener("change", scheduleAutosave);
    });

});
