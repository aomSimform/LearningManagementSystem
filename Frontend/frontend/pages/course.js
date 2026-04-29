import * as auth from "../js/auth/authCheck.js";


const user =
    await auth.default();


const isInstructor =
    user &&
    user.role === "instructor";


const params =
    new URLSearchParams(
        window.location.search
    );


const courseId =
    params.get("id");


const token =
    localStorage.getItem(
        "access"
    );


const errorBox =
    document.getElementById(
        "errorBox"
    );



if (!courseId) {

    errorBox.textContent =
        "Missing course id";

    errorBox.classList.remove(
        "d-none"
    );

    throw new Error(
        "Missing course id"
    );

}



/* show create subsection form */
if (isInstructor) {

    document.getElementById(
            "create-subsection-box"
        ).style.display =
        "block";

}




async function loadCourse() {

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/`, {
                    headers: {
                        Authorization: token ?
                            `Bearer ${token}` : ""
                    }
                }
            );


        const courseData =
            await response.json();


        if (!response.ok) {
            throw courseData;
        }


        document.getElementById(
            "course-details"
        ).innerHTML = `
<div class="card-body">

<h2>
${courseData.title}
</h2>

<p class="text-muted">
Instructor:
${courseData.instructor}
</p>

<p>
${courseData.description}
</p>

</div>
`;

    } catch (error) {

        errorBox.textContent =
            error.detail ||
            "Could not load course";

        errorBox.classList.remove(
            "d-none"
        );

    }

}





async function loadSubsections() {

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/courses/${courseId}/subsections/`, {
                    headers: {
                        Authorization: token ?
                            `Bearer ${token}` : ""
                    }
                }
            );


        const subsections =
            await response.json();


        if (!response.ok) {
            throw subsections;
        }


        subsections.sort(
            (a, b) =>
            a.order - b.order
        );


        let list =
            `<div class="list-group">`;


        for (
            const subsection
            of subsections
        ) {

            list += `
<div class="
list-group-item
mb-4
">

<div class="
d-flex
justify-content-between
align-items-center
">

<div>

<h5>
${subsection.topic}
</h5>

<span class="
badge bg-primary
">
Order:
${subsection.order}
</span>

</div>


${
isInstructor
?
`
<button
class="
btn btn-sm
btn-warning
"
onclick="window.location.href='add-assignment.html?courseid=${subsection.course}&subsectionid=${subsection.id}'"
>
Add Assignment
</button>
`
:
""
}

</div>


<p class="mt-3">
${subsection.description}
</p>
`;



if(
subsection.assignments &&
subsection.assignments.length
){

for(
const assignment
of subsection.assignments
){

const submitUrl =
`submit-assignment.html?course_id=${subsection.course}&subsection_id=${subsection.id}&assignment_id=${assignment.id}`;


list += `
<div class="
card mt-2 p-3
">

<h6>
${assignment.title}
</h6>

<p>
${assignment.file_name}
</p>


<div class="
d-flex gap-2
">

<a
href="${assignment.assignment_url}"
target="_blank"
class="
btn btn-sm
btn-outline-primary
"
>
Open Assignment
</a>


<button
class="
btn btn-sm
btn-success
"
onclick="window.location.href='${submitUrl}'"
>
Submit Assignment
</button>

</div>

</div>
`;

}

}
else{

list += `
<small>
No assignments
</small>
`;

}


list += `
</div>
`;

}


list += `</div>`;


document.getElementById(
"subsection-list"
).innerHTML =
list;

}
catch(error){

console.error(
error
);

document.getElementById(
"subsection-list"
).innerHTML =
"Failed loading subsections";

}

}




await loadCourse();

await loadSubsections();





/* Create subsection */
document
.getElementById(
"subsectionForm"
)
?.addEventListener(
"submit",
async function(e){

e.preventDefault();

const btn =
document.getElementById(
"createSubBtn"
);

btn.disabled = true;

btn.innerText =
"Creating...";


try{

const payload = {

topic:
document.getElementById(
"topic"
).value,

description:
document.getElementById(
"subsection_description"
).value,

order:
parseInt(
document.getElementById(
"order"
).value
)

};


const response =
await fetch(
`http://127.0.0.1:8000/courses/${courseId}/subsections/`,
{
method:"POST",

headers:{
"Content-Type":
"application/json",

Authorization:
`Bearer ${token}`
},

body:
JSON.stringify(
payload
)

}
);


const data =
await response.json();


if(!response.ok){
throw data;
}


document.getElementById(
"subsectionForm"
).reset();


await loadSubsections();


}
catch(error){

errorBox.textContent =
error.detail ||
JSON.stringify(error) ||
"Could not create subsection";

errorBox.classList.remove(
"d-none"
);

}
finally{

btn.disabled = false;

btn.innerText =
"Create Subsection";

}

}
);