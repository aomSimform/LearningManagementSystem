const PROFILE_API =
"http://127.0.0.1:8000/user/me/";

async function checkAuthentication(){

 try{

   const token =
   localStorage.getItem("access");

   if(!token){
      return null;
   }

   console.log(token);

   const response =
   await fetch(
      PROFILE_API,
      {
       method:"GET",

       headers:{
         Authorization:
         `Bearer ${token}`,

         "Content-Type":
         "application/json"
       }
      }
   );

   if(!response.ok){
      console.log(
       response.status
      );
      return null;
   }

   const profile =
   await response.json();

   console.log(profile);

   if(
     profile.interests
     !== undefined
   ){
      return {
        role:"student",
        profile:profile
      };
   }

   if(
     profile.expertise
     !== undefined
   ){
      return {
        role:"instructor",
        profile:profile
      };
   }

   return null;

 }catch(error){

   console.error(
    "Auth check failed",
    error
   );

   return null;
 }

}

export default
checkAuthentication;