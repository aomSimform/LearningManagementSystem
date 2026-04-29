import * as auth from "./js/auth/authCheck.js";

const user = await auth.default();

if (!user) {
    const buttons = document.getElementsByClassName("not-loggedin");
    for (const item of buttons) {
        item.style.display = "inline-block";
    }
}

if (user && user.profile && user.profile.user) {
    document.getElementById("username").textContent +=
        user.profile.user.first_name + " " + user.profile.user.last_name;

    document.getElementById("loggedin").style.display = "block";

    if (user.role === "instructor") {
        document.getElementById("create-course-box").style.display = "block";
    }
}

const access = localStorage.getItem("access");

window.openCourse = async function(courseId) {
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/courses/${courseId}/`, {
                headers: {
                    Authorization: access ? `Bearer ${access}` : ""
                }
            }
        );

        if (!response.ok) {
            throw new Error("Cannot open course");
        }

        window.location.href = `pages/course.html?id=${courseId}`;
    } catch (err) {
        alert(err.message);
    }
};

const response = await fetch("http://127.0.0.1:8000/courses/");
const courses = await response.json();

let list = `<div class="list-group">`;

for (const course of courses) {
    list += `
   <button
      class="list-group-item list-group-item-action mb-3"
      onclick="f(${course.id})"
   >
      <h5>${course.title}</h5>
      <p>${course.description}</p>
   </button>
   `;
}

list += `</div>`;

document.getElementById("course-list").innerHTML = list;

window.f = function(courseId) {
    if (user) {
        window.openCourse(courseId);
    } else {
        alert("You need to login first");
    }
}