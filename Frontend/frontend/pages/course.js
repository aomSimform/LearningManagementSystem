import * as auth from "../js/auth/authCheck.js";

/* ================= SAFE COURSE ID ================= */
let courseId = new URLSearchParams(window.location.search).get("id");

if (!courseId) {
    courseId = localStorage.getItem("courseId");
}

if (courseId) {
    localStorage.setItem("courseId", courseId);
}

if (courseId && !window.location.search.includes("id=")) {
    window.history.replaceState({}, "", `${window.location.pathname}?id=${courseId}`);
}

/* ================= GLOBALS ================= */
const token = localStorage.getItem("access");
const errorBox = document.getElementById("errorBox");
const successBox = document.getElementById("successBox");
const totalGradeBox = document.getElementById("total-grade-box");

/* ================= ALERT HELPERS ================= */
function showSuccess(message) {
    successBox.textContent = message;
    successBox.classList.remove("d-none");

    errorBox.classList.add("d-none");

    setTimeout(() => {
        successBox.classList.add("d-none");
    }, 3000);
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("d-none");

    successBox.classList.add("d-none");

    setTimeout(() => {
        errorBox.classList.add("d-none");
    }, 4000);
}

/* ================= STOP IF NO ID ================= */
if (!courseId) {
    showError("Missing course id");
    throw new Error("Course ID missing");
}

/* ================= AUTH ================= */
const user = await auth.default();
const isInstructor = user && user.role === "instructor";

/* ================= SHOW INSTRUCTOR UI ================= */
if (isInstructor) {
    document.getElementById("create-subsection-box").style.display = "block";
}

/* ================= LOAD COURSE ================= */
async function loadCourse() {
    try {
        const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        const data = await res.json();
        if (!res.ok) throw data;

        document.getElementById("course-details").innerHTML = `
            <div class="card-body">
                <h2>${data.title}</h2>
                <p class="text-muted">Instructor: ${data.instructor}</p>
                <p>${data.description}</p>
            </div>
        `;
    } catch (err) {
        showError(err.detail || "Failed to load course");
    }
}

/* ================= LOAD SUBSECTIONS ================= */
async function loadSubsections() {
    try {
        const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/subsections/`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        const subsections = await res.json();
        if (!res.ok) throw subsections;

        let list = `<div class="list-group">`;
        let totalGrade = 0;

        for (const subsection of subsections) {

            const subRes = await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsection.id}/submissions/`,
                { headers: { Authorization: `Bearer ${token}` } }
            );

            const submissions = await subRes.json();

            const gradeRes = await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsection.id}/grades/`,
                { headers: { Authorization: `Bearer ${token}` } }
            );

            const grades = await gradeRes.json();

            list += `
            <div class="list-group-item mb-4">

                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h5>${subsection.topic}</h5>
                        <span class="badge bg-primary">Order: ${subsection.order}</span>
                    </div>

                    ${isInstructor ? `
                    <div class="d-flex gap-2">

                        <button class="btn btn-sm btn-warning"
                            onclick="window.location.href='add-assignment.html?courseid=${subsection.course}&subsectionid=${subsection.id}'">
                            Add Assignment
                        </button>

                        <button class="btn btn-sm btn-dark"
                            onclick="window.location.href='submissions.html?courseid=${subsection.course}&subsectionid=${subsection.id}'">
                            View Submissions
                        </button>

                    </div>
                    ` : ""}
                </div>

                <p class="mt-3">${subsection.description}</p>
            `;

            if (subsection.assignments?.length) {

                for (const assignment of subsection.assignments) {

                    const submission = submissions.find(
                        s => s.assignment === assignment.id &&
                             s.user.id === user.id
                    );

                    const gradeObj = grades.find(
                        g => g.assignment === assignment.id &&
                             g.user_details.id === user.id
                    );

                    const isGraded = gradeObj && gradeObj.grades !== null;
                    const gradeValue = isGraded ? gradeObj.grades : null;

                    if (isGraded) totalGrade += gradeValue;

                    list += `
                    <div class="card mt-2 p-3">
                        <h6>${assignment.title}</h6>

                        <div class="d-flex gap-2">

                            <a href="${assignment.assignment_url}" target="_blank"
                               class="btn btn-sm btn-outline-primary">
                               Open Assignment
                            </a>
                    `;

                    /* STUDENT */
                    if (!isInstructor) {

                        if (!submission) {
                            list += `
                            <button class="btn btn-sm btn-success"
                                onclick="window.location.href='submit-assignment.html?course_id=${subsection.course}&subsection_id=${subsection.id}&assignment_id=${assignment.id}'">
                                Submit
                            </button>
                            `;
                        } else {
                            list += `
                            <span class="badge bg-secondary">Already Submitted</span>

                            <a href="${submission.file}" target="_blank"
                               class="btn btn-sm btn-info">
                               Open Submission
                            </a>
                            `;
                        }

                        if (isGraded) {
                            list += `<span class="badge bg-success">Grade: ${gradeValue}</span>`;
                        }
                    }

                    /* INSTRUCTOR */
                    if (isInstructor) {

                        if (submission) {
                            list += `
                            <a href="${submission.file}" target="_blank"
                               class="btn btn-sm btn-info">
                               View Submission
                            </a>
                            `;
                        }

                        if (isGraded) {
                            list += `<span class="badge bg-primary">Grade: ${gradeValue}</span>`;
                        } else {
                            list += `
                            <button class="btn btn-sm btn-warning"
                                onclick="window.location.href='grade.html?courseid=${subsection.course}&subsectionid=${subsection.id}&assignmentid=${assignment.id}'">
                                Grade
                            </button>
                            `;
                        }
                    }

                    list += `</div></div>`;
                }

            } else {
                list += `<small>No assignments</small>`;
            }

            list += `</div>`;
        }

        list += `</div>`;

        document.getElementById("subsection-list").innerHTML = list;

        if (!isInstructor) {
            totalGradeBox.classList.remove("d-none");
            totalGradeBox.innerHTML = `<strong>Total Grade:</strong> ${totalGrade}`;
        }

    } catch (err) {
        console.error(err);
        showError("Failed loading subsections");
    }
}

/* ================= CREATE SUBSECTION ================= */
document.getElementById("subsectionForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const btn = document.getElementById("createSubBtn");
    btn.disabled = true;
    btn.innerText = "Creating...";

    try {
        const payload = {
            topic: document.getElementById("topic").value,
            description: document.getElementById("subsection_description").value,
            order: parseInt(document.getElementById("order").value)
        };

        const res = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/subsections/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await res.json();
        if (!res.ok) throw data;

        showSuccess("Subsection created successfully!");

        document.getElementById("subsectionForm").reset();

        await loadSubsections();

    } catch (err) {
        console.error(err);
        showError(err.detail || "Failed creating subsection");
    } finally {
        btn.disabled = false;
        btn.innerText = "Create Subsection";
    }
});

/* ================= INIT ================= */
await loadCourse();
await loadSubsections();