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
    const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();

    document.getElementById("course-details").innerHTML = `
        <div class="card-body">
            <h2>${data.title}</h2>
            <p class="text-muted">Instructor: ${data.instructor}</p>
            <p>${data.description}</p>
        </div>
    `;
}

/* ================= LOAD SUBSECTIONS ================= */
async function loadSubsections() {

    const res = await fetch(`http://127.0.0.1:8000/courses/${courseId}/subsections/`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const subsections = await res.json();

    let list = `<div class="list-group">`;
    let totalGrade = 0;

    for (const subsection of subsections) {

        /* ===== FETCH SUBMISSIONS (IMPORTANT) ===== */
        const subRes = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsection.id}/submissions/`,
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );

        const submissions = await subRes.json();

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

                /* ===== CHECK SUBMISSION ===== */
                const submission = submissions.find(
                    s => s.assignment === assignment.id &&
                         s.user.id === user.id
                );

                const isSubmitted = !!submission;

                /* ===== CHECK GRADE ===== */
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

                /* ================= STUDENT ================= */
                if (!isInstructor) {

                    if (!isSubmitted) {
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
                        list += `
                        <span class="badge bg-success">
                            Grade: ${gradeValue}
                        </span>
                        `;
                    }
                }

                /* ================= INSTRUCTOR ================= */
                if (isInstructor) {

                    if (isSubmitted) {
                        list += `
                        <a href="${submission.file}" target="_blank"
                           class="btn btn-sm btn-info">
                           View Submission
                        </a>
                        `;
                    }

                    if (isGraded) {
                        list += `
                        <span class="badge bg-primary">
                            Grade: ${gradeValue}
                        </span>
                        `;
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
        totalGradeBox.innerHTML = `<strong>Total Grade:</strong> ${totalGrade}`;
    }
}

/* ================= INIT ================= */
await loadCourse();
await loadSubsections();