// 🔹 Get query params
const params = new URLSearchParams(window.location.search);

const courseId = params.get("courseid");
const subsectionId = params.get("subsectionid");

// 🔹 Token
const token = localStorage.getItem("access");

// 🔹 UI elements
const errorBox = document.getElementById("errorBox");
const successBox = document.getElementById("successBox");
const infoBox = document.getElementById("infoBox");

// 🔹 Validate params
if (!courseId || !subsectionId) {
    errorBox.textContent = "Missing query parameters";
    errorBox.classList.remove("d-none");
    throw new Error("Missing params");
}

// 🔹 Show info
infoBox.innerHTML = `
<strong>Course:</strong> ${courseId}<br>
<strong>Subsection:</strong> ${subsectionId}
`;

// 🔹 API URL
const assignmentUrl = `http://127.0.0.1:8000/courses/${courseId}/subsections/${subsectionId}/assignments/`;

// 🔹 Deadline setup
const deadlineInput = document.getElementById("deadline");

// prevent past dates
const now = new Date();
const formattedNow = now.toISOString().slice(0, 16);
deadlineInput.min = formattedNow;
deadlineInput.value = formattedNow;

// 🔹 Auto focus on deadline after file select
document.getElementById("assignmentFile").addEventListener("change", () => {
    deadlineInput.focus();
});

// 🔹 Form submit
document.getElementById("assignmentForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    errorBox.classList.add("d-none");
    successBox.classList.add("d-none");

    const btn = document.getElementById("createBtn");
    const fileInput = document.getElementById("assignmentFile");

    // 🔹 File validation
    if (!fileInput.files.length) {
        errorBox.textContent = "Select a file";
        errorBox.classList.remove("d-none");
        return;
    }

    const file = fileInput.files[0];

    const allowedTypes = [
        "application/pdf",
        "image/jpeg",
        "image/png"
    ];

    if (!allowedTypes.includes(file.type)) {
        errorBox.textContent = "Only PDF, JPG, PNG allowed";
        errorBox.classList.remove("d-none");
        return;
    }

    btn.disabled = true;
    btn.innerText = "Creating...";

    try {

        const formData = new FormData();

        formData.append("title", document.getElementById("title").value);
        formData.append("uploaded_file", file);

        // 🔥 IMPORTANT FIX (timezone safe)
        const localDate = document.getElementById("deadline").value;
        const isoDate = new Date(localDate).toISOString();

        formData.append("deadline", isoDate);

        const response = await fetch(assignmentUrl, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw data;
        }

        successBox.textContent = "Assignment created successfully";
        successBox.classList.remove("d-none");

        // redirect
        setTimeout(() => {
            window.location.href = `course.html?id=${courseId}`;
        }, 1500);

    } catch (error) {

        console.error(error);

        errorBox.textContent =
            error.detail ||
            JSON.stringify(error) ||
            "Assignment creation failed";

        errorBox.classList.remove("d-none");

    } finally {

        btn.disabled = false;
        btn.innerText = "Create Assignment";
    }

});