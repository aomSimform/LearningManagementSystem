import * as auth from "./auth/authCheck.js";

const user = await auth.default();

const access =
    localStorage.getItem(
        "access"
    );

const isInstructor =
    user &&
    user.role === "instructor";



const loginBtn =
    document.getElementById(
        "login-btn"
    );

const registerBtn =
    document.getElementById(
        "register-btn"
    );

const logoutBtn =
    document.getElementById(
        "logout-btn"
    );

const createCourseBtn =
    document.getElementById(
        "create-course-btn"
    );




loginBtn.addEventListener(
    "click",
    function() {
        window.location.href =
            "pages/login.html";
    }
);

registerBtn.addEventListener(
    "click",
    function() {
        window.location.href =
            "pages/register.html";
    }
);

createCourseBtn.addEventListener(
    "click",
    function() {
        window.location.href =
            "pages/create-course.html";
    }
);




/* show buttons */
if (!user) {

    const buttons =
        document.getElementsByClassName(
            "not-loggedin"
        );

    for (
        const item
        of buttons
    ) {
        item.style.display =
            "inline-block";
    }

} else {

    document.getElementById(
            "loggedin"
        ).style.display =
        "block";

    document.getElementById(
            "username"
        ).textContent +=
        user.profile.user.first_name +
        " " +
        user.profile.user.last_name;

    logoutBtn.style.display =
        "inline-block";


    if (isInstructor) {

        document.getElementById(
                "create-course-box"
            ).style.display =
            "block";

    }

}





/* logout */
logoutBtn.addEventListener(
    "click",
    async function() {

        const refresh =
            localStorage.getItem(
                "refresh"
            );

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/user/logout/", {
                        method: "POST",

                        headers: {
                            Authorization: `Bearer ${access}`,
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            refresh: refresh
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {
                throw data;
            }

            localStorage.removeItem(
                "access"
            );

            localStorage.removeItem(
                "refresh"
            );

            window.location.href =
                "pages/login.html";

        } catch (error) {

            alert(
                error.detail ||
                "Logout failed"
            );

        }

    }
);






async function openCourse(
    courseId
) {

    const errorBox =
        document.getElementById(
            "courseError"
        );

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/`, {
                    headers: {
                        Authorization: `Bearer ${access}`
                    }
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw data;
        }

        window.location.href =
            `pages/course.html?id=${courseId}`;

    } catch (error) {

        errorBox.textContent =
            error.detail ||
            "Could not open course";

        errorBox.classList.remove(
            "d-none"
        );

    }

}





async function enrollCourse(
    courseId,
    button
) {

    button.disabled = true;

    button.innerText =
        "Enrolling...";

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/enroll/`, {
                    method: "POST",

                    headers: {
                        Authorization: `Bearer ${access}`,
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({})
                }
            );

        const data =
            await response.json();

        if (!response.ok) {
            throw data;
        }

        window.location.reload();

    } catch (error) {

        alert(
            error.detail ||
            "Enrollment failed"
        );

        button.disabled = false;

        button.innerText =
            "Enroll";

    }

}







/* load courses */
try {

    if (!access) {
        throw new Error(
            "No access token"
        );
    }


    const response =
        await fetch(
            "http://127.0.0.1:8000/courses/", {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${access}`,
                    "Content-Type": "application/json"
                }
            }
        );


    if (!response.ok) {
        throw new Error(
            "Could not load courses"
        );
    }


    const courses =
        await response.json();

    console.log(
        courses
    );


    let list =
        `<div class="list-group">`;



    for (
        const course
        of courses
    ) {

        const enrolled =
            course.enroll === true;


        /*
        INSTRUCTOR:
        always open course

        STUDENT:
        open if enrolled
        otherwise enroll
        */

        let actionButton = "";


        if (isInstructor) {

            actionButton = `
<button
class="
btn btn-primary
open-course-btn
"
data-id="${course.id}"
>
Open Course
</button>
`;

        } else if (enrolled) {

            actionButton = `
<button
class="
btn btn-primary
open-course-btn
"
data-id="${course.id}"
>
Open Course
</button>
`;

        } else {

            actionButton = `
<button
class="
btn btn-success
enroll-btn
"
data-id="${course.id}"
>
Enroll
</button>
`;

        }



        list += `
<div class="
list-group-item
mb-3
">

<h5>
${course.title}
</h5>

<p class="mb-2">
${course.description}
</p>

<div class="
d-flex gap-2
">

${actionButton}

</div>

</div>
`;

    }


    list +=
        `</div>`;


    document.getElementById(
            "course-list"
        ).innerHTML =
        list;




    /* open course handlers */
    document
        .querySelectorAll(
            ".open-course-btn"
        )
        .forEach(
            function(button) {

                button.addEventListener(
                    "click",
                    function() {

                        openCourse(
                            this.dataset.id
                        );

                    }
                );

            }
        );




    /* enroll handlers */
    document
        .querySelectorAll(
            ".enroll-btn"
        )
        .forEach(
            function(button) {

                button.addEventListener(
                    "click",
                    function() {

                        enrollCourse(
                            this.dataset.id,
                            this
                        );

                    }
                );

            }
        );


} catch (error) {

    console.error(
        error
    );

    document.getElementById(
            "course-list"
        ).innerHTML =
        "Failed to load courses.";

}