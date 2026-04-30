import * as auth from "../js/auth/authCheck.js";

const user = await auth.default();
const isInstructor = user && user.role === "instructor";

const params = new URLSearchParams(window.location.search);
const courseId = params.get("id");

const token = localStorage.getItem("access");

const errorBox = document.getElementById("errorBox");
const totalGradeBox = document.getElementById("total-grade-box");

if (!courseId) {
    errorBox.textContent = "Missing course id";
    errorBox.classList.remove("d-none");
    throw new Error("Missing course id");
}

if (isInstructor) {
    document.getElementById("create-subsection-box").style.display = "block";
}

/* ================= LOAD COURSE ================= */
async function loadCourse() {
    try {
        const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/`, {
            headers: { Authorization: token ? `Bearer ${token}` : "" }
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
        errorBox.textContent = err.detail || "Failed to load course";
        errorBox.classList.remove("d-none");
    }
}

/* ================= LOAD SUBSECTIONS ================= */
async function loadSubsections() {
    try {
        const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/subsections/`, {
            headers: { Authorization: token ? `Bearer ${token}` : "" }
        });

        const subsections = await res.json();
        if (!res.ok) throw subsections;

        subsections.sort((a, b) => a.order - b.order);

        let list = `<div class="list-group">`;
        let grandTotal = 0;

        for (const subsection of subsections) {

            /* ===== FETCH GRADES ===== */
            const gradeRes = await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsection.id}/grades/`,
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
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
                        <button class="btn btn-sm btn-warning"
                            onclick="window.location.href='add-assignment.html?courseid=${subsection.course}&subsectionid=${subsection.id}'">
                            Add Assignment
                        </button>
                    ` : ""}
                </div>

                <p class="mt-3">${subsection.description}</p>
            `;

            /* ===== ASSIGNMENTS ===== */
            if (subsection.assignments?.length) {

                for (const assignment of subsection.assignments) {

                    const gradeObj = grades.find(
                        g => g.assignment === assignment.id && g.user_details.id === user.id
                    );

                    const isGraded = gradeObj && gradeObj.grades !== null;
                    const gradeValue = isGraded ? gradeObj.grades : null;

                    if (isGraded) grandTotal += gradeValue;

                    list += `
                    <div class="card mt-2 p-3">
                        <h6>${assignment.title}</h6>

                        <div class="d-flex gap-2">

                            <a href="${assignment.assignment_url}" target="_blank"
                                class="btn btn-sm btn-outline-primary">
                                Open Assignment
                            </a>
                    `;

                    /* ===== STUDENT ===== */
                    if (!isInstructor) {
                        if (isGraded) {
                            list += `<span class="badge bg-success">Grade: ${gradeValue}</span>`;
                        } else {
                            list += `
                                <button class="btn btn-sm btn-success"
                                    onclick="window.location.href='submit-assignment.html?course_id=${subsection.course}&subsection_id=${subsection.id}&assignment_id=${assignment.id}'">
                                    Submit
                                </button>
                            `;
                        }
                    }

                    /* ===== INSTRUCTOR ===== */
                    if (isInstructor) {
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

        /* ===== TOTAL GRADE ===== */
        if (!isInstructor) {
            totalGradeBox.classList.remove("d-none");
            totalGradeBox.innerHTML = `<strong>Total Grade:</strong> ${grandTotal}`;
        }

    } catch (err) {
        console.error(err);
        document.getElementById("subsection-list").innerHTML = "Failed loading subsections";
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

        document.getElementById("subsectionForm").reset();
        await loadSubsections();

    } catch (err) {
        errorBox.textContent = err.detail || "Failed creating subsection";
        errorBox.classList.remove("d-none");
    } finally {
        btn.disabled = false;
        btn.innerText = "Create Subsection";
    }
});

/* ================= INIT ================= */
await loadCourse();
await loadSubsections();