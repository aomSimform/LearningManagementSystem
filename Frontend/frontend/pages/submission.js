import * as auth from "../js/auth/authCheck.js";

await auth.default();

const params = new URLSearchParams(window.location.search);
const courseId = params.get("courseid");
const subsectionId = params.get("subsectionid");

const token = localStorage.getItem("access");

async function loadSubmissions() {

    const res = await fetch(
        `http://127.0.0.1:8000/courses/${courseId}/subsection/${subsectionId}/submissions/`,
        {
            headers: { Authorization: `Bearer ${token}` }
        }
    );

    const data = await res.json();

    let html = "";

    data.forEach(sub => {
        html += `
        <div class="card mb-2 p-3">

            <h6>${sub.user.first_name} (${sub.user.email})</h6>

            <a href="${sub.file}" target="_blank"
               class="btn btn-sm btn-primary">
               Open Submission
            </a>

            <button class="btn btn-sm btn-warning mt-2"
                onclick="window.location.href='grade.html?courseid=${courseId}&subsectionid=${subsectionId}&assignmentid=${sub.assignment}&userid=${sub.user.id}'">
                Grade
            </button>

        </div>
        `;
    });

    document.getElementById("submission-list").innerHTML = html;
}

loadSubmissions();