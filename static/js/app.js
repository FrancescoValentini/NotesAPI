
const API_URL = "http://localhost:8000/api/v1";

let token = localStorage.getItem("access_token");
let username = localStorage.getItem("username");
let isRegister = false;

const authSection = document.getElementById("authSection");
const notesSection = document.getElementById("notesSection");
const notesContainer = document.getElementById("notesContainer");
const emptyState = document.getElementById("emptyState");

const noteModal = new bootstrap.Modal(
    document.getElementById("noteModal")
);

// API helper
async function apiRequest(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...options.headers
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (response.status === 401) {
        logout();
        throw new Error("Session expired. Please login again.");
    }

    if (!response.ok) {
        const message = data?.detail
            ? Array.isArray(data.detail)
                ? data.detail.map(e => e.msg).join(", ")
                : data.detail
            : data?.message || "Something went wrong";

        throw new Error(message);
    }

    if (data?.error) {
        throw new Error(data.message || "API request failed");
    }

    return data?.result;
}

// Alerts
function showAlert(message, type = "success") {
    const alertArea = document.getElementById("alertArea");

    alertArea.innerHTML = "";

    const alert = document.createElement("div");
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.setAttribute("role", "alert");

    const text = document.createElement("span");
    text.textContent = message;

    const close = document.createElement("button");
    close.type = "button";
    close.className = "btn-close";
    close.dataset.bsDismiss = "alert";

    alert.append(text, close);
    alertArea.appendChild(alert);
}

// Authentication UI
function showDashboard() {
    authSection.classList.add("d-none");
    notesSection.classList.remove("d-none");

    document.getElementById("userArea").classList.remove("d-none");
    document.getElementById("usernameDisplay").textContent =
        username || "User";

    loadNotes();
}

function showLogin() {
    authSection.classList.remove("d-none");
    notesSection.classList.add("d-none");
    document.getElementById("userArea").classList.add("d-none");
}

// Toggle login/register
document.getElementById("authToggle").addEventListener("click", e => {
    e.preventDefault();

    isRegister = !isRegister;

    document.getElementById("authTitle").textContent =
        isRegister ? "Register" : "Login";

    document.getElementById("authButton").textContent =
        isRegister ? "Create Account" : "Login";

    document.getElementById("authToggle").textContent =
        isRegister ? "Login" : "Register";

    document.getElementById("authToggleText").textContent =
        isRegister ? "Already have an account?" : "Don't have an account?";
});

// Login/Register
document.getElementById("authForm").addEventListener("submit", async e => {
    e.preventDefault();

    const user = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const button = document.getElementById("authButton");

    button.disabled = true;
    button.textContent = "Please wait...";

    try {
        if (isRegister) {
            await apiRequest("/auth/register", {
                method: "POST",
                body: JSON.stringify({
                    username: user,
                    password
                })
            });

            showAlert("Registration successful! Please login.");

            isRegister = false;
            document.getElementById("authToggle").click();

        } else {
            const result = await apiRequest("/auth/login", {
                method: "POST",
                body: JSON.stringify({
                    username: user,
                    password
                })
            });

            token = result.access_token;
            username = user;

            localStorage.setItem("access_token", token);
            localStorage.setItem("username", username);

            showDashboard();
            showAlert("Welcome back!");
        }

    } catch (error) {
        showAlert(error.message, "danger");
    } finally {
        button.disabled = false;
        button.textContent = isRegister ? "Create Account" : "Login";
    }
});

// Logout
function logout() {
    token = null;
    username = null;

    localStorage.removeItem("access_token");
    localStorage.removeItem("username");

    showLogin();
}

// Load notes
async function loadNotes() {
    notesContainer.innerHTML = `
        <div class="col-12 text-center py-4">
            <div class="spinner-border text-primary"></div>
        </div>
    `;

    try {
        const notes = await apiRequest("/notes/");

        renderNotes(notes || []);

    } catch (error) {
        notesContainer.innerHTML = "";
        showAlert(error.message, "danger");
    }
}

// Render notes safely
function renderNotes(notes) {
    notesContainer.innerHTML = "";

    emptyState.classList.toggle("d-none", notes.length !== 0);

    notes.forEach(note => {
        const col = document.createElement("div");
        col.className = "col-md-6 col-lg-4";

        const card = document.createElement("div");
        card.className = "card note-card shadow-sm";

        const body = document.createElement("div");
        body.className = "card-body d-flex flex-column";

        const title = document.createElement("h5");
        title.className = "card-title";
        title.textContent = note.title;

        const content = document.createElement("p");
        content.className = "note-content flex-grow-1";
        content.textContent = note.content || "No content";

        const actions = document.createElement("div");
        actions.className = "note-actions mt-3";

        const edit = document.createElement("button");
        edit.className = "btn btn-sm btn-outline-primary";
        edit.textContent = "Edit";
        edit.addEventListener("click", () => editNote(note));

        const view = document.createElement("button");
        view.className = "btn btn-sm btn-outline-secondary";
        view.textContent = "View";
        view.addEventListener("click", () => viewNote(note));

        const remove = document.createElement("button");
        remove.className = "btn btn-sm btn-outline-danger";
        remove.textContent = "Delete";
        remove.addEventListener("click", () => deleteNote(note.id));

        actions.append(edit, view, remove);
        body.append(title, content, actions);
        card.appendChild(body);
        col.appendChild(card);

        notesContainer.appendChild(col);
    });
}

// Open create modal
function openCreateModal() {
    document.getElementById("noteForm").reset();
    document.getElementById("noteId").value = "";

    document.getElementById("modalTitle").textContent = "Create Note";

    noteModal.show();
}

// Edit note
function editNote(note) {
    document.getElementById("noteId").value = note.id;
    document.getElementById("noteTitle").value = note.title;
    document.getElementById("noteContent").value = note.content;

    document.getElementById("modalTitle").textContent = "Edit Note";

    noteModal.show();
}

// View note
function viewNote(note) {
    document.getElementById("noteId").value = note.id;
    document.getElementById("noteTitle").value = note.title;
    document.getElementById("noteContent").value = note.content;

    document.getElementById("modalTitle").textContent = "View Note";

    document.getElementById("noteTitle").disabled = true;
    document.getElementById("noteContent").disabled = true;

    document.querySelector("#noteForm button[type=submit]").classList.add("d-none");

    noteModal.show();

    document.getElementById("noteModal").addEventListener(
        "hidden.bs.modal",
        resetModal,
        { once: true }
    );
}

function resetModal() {
    document.getElementById("noteTitle").disabled = false;
    document.getElementById("noteContent").disabled = false;

    document.querySelector("#noteForm button[type=submit]").classList.remove("d-none");
}

// Create or update note
document.getElementById("noteForm").addEventListener("submit", async e => {
    e.preventDefault();

    const id = document.getElementById("noteId").value;

    const title = document.getElementById("noteTitle").value.trim();
    const content = document.getElementById("noteContent").value;

    if (!title) {
        showAlert("Title is required.", "danger");
        return;
    }

    try {
        if (id) {
            await apiRequest(`/notes/${id}`, {
                method: "PUT",
                body: JSON.stringify({ title, content })
            });

            showAlert("Note updated successfully!");

        } else {
            await apiRequest("/notes/", {
                method: "POST",
                body: JSON.stringify({ title, content })
            });

            showAlert("Note created successfully!");
        }

        noteModal.hide();
        resetModal();
        loadNotes();

    } catch (error) {
        showAlert(error.message, "danger");
    }
});

// Delete note
async function deleteNote(id) {
    if (!confirm("Are you sure you want to delete this note?")) {
        return;
    }

    try {
        await apiRequest(`/notes/${id}`, {
            method: "DELETE"
        });

        showAlert("Note deleted successfully!");
        loadNotes();

    } catch (error) {
        showAlert(error.message, "danger");
    }
}

// Initial application state
if (token) {
    showDashboard();
} else {
    showLogin();
}
