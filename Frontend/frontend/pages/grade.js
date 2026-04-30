import * as auth from "../js/auth/authCheck.js";

/* ================= AUTH ================= */
const user = await auth.default();
if (!user || user.role !== "instructor") {
    alert("Access denied");
    window.location.href = "../index.html";
}

/* ================= PARAMS ================= */
const params = new URLSearchParams(window.location.search);

const courseId = params.get("courseid");
const subsectionId = params.get("subsectionid");

const token = localStorage.getItem("access");
const errorBox = document.getElementById("errorBox");

/* ================= VALIDATION ================= */
if (!courseId || !subsectionId) {
    errorBox.textContent = "Missing parameters";
    errorBox.classList.remove("d-none");
    throw new Error("Missing params");
}

/* ================= LOAD DATA ================= */
async function loadData() {

    try {

        /* ===== FETCH SUBMISSIONS ===== */
        const subRes = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsectionId}/submissions/`,
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );

        const submissions = await subRes.json();

        /* ===== FETCH GRADES ===== */
        const gradeRes = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsectionId}/grades/`,
            {
                headers: { Authorization: `Bearer ${token}` }
            }
        );

        const grades = await gradeRes.json();

        let html = "";

        submissions.forEach(sub => {

            const existingGrade = grades.find(
                g => g.assignment === sub.assignment &&
                     g.user_details.id === sub.user.id
            );

            const isGraded = existingGrade && existingGrade.grades !== null;

            html += `
            <div class="card mb-3 p-3">

                <h6>
                    ${sub.user.first_name} (${sub.user.email})
                </h6>

                <p>Assignment ID: ${sub.assignment}</p>

                <a href="${sub.file}" target="_blank"
                   class="btn btn-sm btn-primary mb-2">
                   Open Submission
                </a>

                ${
                    isGraded
                    ?
                    `<span class="badge bg-success">
                        Grade: ${existingGrade.grades}
                     </span>`
                    :
                    `
                    <div class="d-flex gap-2">

                        <input type="number"
                               min="0" max="100"
                               class="form-control"
                               id="grade-${sub.user.id}-${sub.assignment}"
                               placeholder="Enter marks">

                        <button class="btn btn-success"
                            onclick="submitGrade(${sub.user.id}, ${sub.assignment})">
                            Submit
                        </button>

                    </div>
                    `
                }

            </div>
            `;
        });

        document.getElementById("grade-list").innerHTML = html;

    } catch (err) {
        console.error(err);
        errorBox.textContent = "Failed to load data";
        errorBox.classList.remove("d-none");
    }
}

/* ================= SUBMIT GRADE ================= */
window.submitGrade = async function(userId, assignmentId) {

    const input = document.getElementById(`grade-${userId}-${assignmentId}`);
    const gradeValue = parseInt(input.value);

    if (isNaN(gradeValue) || gradeValue < 0 || gradeValue > 100) {
        alert("Enter valid marks (0-100)");
        return;
    }

    try {

        const res = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsectionId}/grades/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    user: userId,
                    assignment: assignmentId,
                    grades: gradeValue
                })
            }
        );

        const data = await res.json();

        if (!res.ok) throw data;

        alert("Grade submitted successfully");

        await loadData(); // refresh

    } catch (err) {
        console.error(err);
        errorBox.textContent = err.detail || "Failed to submit grade";
        errorBox.classList.remove("d-none");
    }
};

/* ================= INIT ================= */
loadData();