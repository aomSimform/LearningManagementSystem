const PROFILE_API = "http://127.0.0.1:8000/user/me";

async function checkAuthentication() {
    try {
        console.log('hello my name is aom kapadia')
        const token = localStorage.getItem("access");
        if (!token) {
            return null;
        }

        const response = await fetch(PROFILE_API, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            return null;
        }
        const profile = await response.json();

        if (profile.interests !== undefined) {
            return {
                role: "student",
                profile: profile,
            };
        }
        if (profile.expertise !== undefined) {
            return {
                role: "instructor",
                profile: profile,
            };
        }
        return null;
    } catch (error) {
        console.error("Auth check failed", error);
        return null;
    }
}


export default checkAuthentication