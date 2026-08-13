let currentConversation = null;
let lastMessageId = 0;

document.addEventListener("DOMContentLoaded", () => {

    // Click contact → load/create conversation
    document.querySelectorAll(".contact-item").forEach(item => {
        item.addEventListener("click", async () => {
            const userId = item.dataset.userId;

            // 🔹 Remove previous selection
            document.querySelectorAll(".contact-item").forEach(i =>
                i.classList.remove("contact-selected")
            );

            // 🔹 Highlight this contact
            item.classList.add("contact-selected");

            // Create or fetch conversation
            const response = await fetch(`/messenger/create_or_get/${userId}/`);
            const data = await response.json();

            currentConversation = data.conversation_id;

            loadMessages();
        });
    });



    // Send message
    document.getElementById("sendBtn").addEventListener("click", async () => {
        if (!currentConversation) return;

        const body = document.getElementById("chatInput").value.trim();
        if (!body) return;

        const formData = new FormData();
        formData.append("conversation_id", currentConversation);
        formData.append("body", body);

        await fetch("/messenger/send/", {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": getCSRFToken() }
        });

        document.getElementById("chatInput").value = "";
        loadMessages();
    });
    // Press Enter to send
    document.getElementById("chatInput").addEventListener("keydown", async (e) => {
        // Shift+Enter = new line
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // stop newline

            document.getElementById("sendBtn").click(); // reuse existing logic
        }
    });

});

// Load messages
async function loadMessages() {
    const chat = document.getElementById("chatWindow");
    const response = await fetch(`/messenger/conversation/${currentConversation}/messages/`);
    const data = await response.json();

    chat.innerHTML = "";

    data.messages.forEach(m => {
        lastMessageId = m.id;

        const bubble = document.createElement("div");
        bubble.className = m.sender === CURRENT_USERNAME ? "text-end mb-2" : "text-start mb-2";
        bubble.innerHTML = `
            <div class="p-2 rounded ${m.sender === CURRENT_USERNAME ? 'bg-primary text-white' : 'bg-white border'}">
                <strong>${m.sender}</strong><br>
                ${m.body}
            </div>
        `;
        chat.appendChild(bubble);
    });

    chat.scrollTop = chat.scrollHeight;
}

// CSRF helper
function getCSRFToken() {
    return document.getElementById("csrfToken").value;
}

// Polling helper
async function checkForNew(convId) {
    if (!convId) return;

    const response = await fetch(`/messenger/conversation/${convId}/check/?last_id=${lastMessageId}`);
    const data = await response.json();

    if (data.new) {
        loadMessages();
    }
}

// Refresh contact highlights
async function refreshContactHighlights(currentConv) {
    const response = await fetch("/messenger/unread_status/");
    const data = await response.json();

    const otherUserId = currentConv ? getOtherUserIdForConversation(currentConv, data) : null;

    document.querySelectorAll(".contact-item").forEach(item => {
        const uid = item.dataset.userId;

        // If this is the open conversation → never highlight yellow
        if (otherUserId && uid == otherUserId) {
            item.classList.remove("list-group-item-warning");
            return;
        }

        // If selected, do not touch its highlight
        if (item.classList.contains("contact-selected")) {
            return;
        }

        // Highlight only if unread is true
        if (data[uid] && data[uid].unread) {
            item.classList.add("list-group-item-warning");
        } else {
            item.classList.remove("list-group-item-warning");
        }
    });

}



function getOtherUserIdForConversation(convId, unreadData) {
    for (const uid in unreadData) {
        if (unreadData[uid].conversation_id == convId) {
            return unreadData[uid].other_user_id;
        }
    }
    return null;
}



setInterval(() => {
    checkForNew(currentConversation);
    refreshContactHighlights(currentConversation);
}, 2000);


