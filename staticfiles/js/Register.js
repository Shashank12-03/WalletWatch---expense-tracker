const usernameField=document.querySelector("#usernameField");
const feedBackArea=document.querySelector(".invalid_feedback");
const emailField=document.querySelector("#emailField")
const emailFeedBackArea=document.querySelector(".emailFeedBackArea")
const usernameSuccessOutput=document.querySelector(".usernameSuccessOutput")
const showPasswordToggle=document.querySelector(".showPasswordToggle");
const passwordField=document.querySelector("#passwordField");
const submit=document.querySelector(".submit-btn")

usernameField.addEventListener("keyup",(e)=>{
    const usernameVal=e.target.value;
    usernameSuccessOutput.style.display="block";
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`;
    usernameField.classList.remove('is-valid');
    feedBackArea.style.display="none";
    
    if(usernameVal.length>0){
        fetch("/Authentication/validate_username",{ 
            body:JSON.stringify({username:usernameVal}),
            method:"POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                usernameField.classList.add('is-valid');
                feedBackArea.style.display="block";
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
                submit.setAttribute=true;
            }
            else{
                submit.removeAttribute("disabled");
            }
        });
    }
}); 


emailField.addEventListener("keyup",(e)=>{
    const emailVal=e.target.value;
    emailField.classList.remove('is-valid');
    emailFeedBackArea.style.display="none";
    
    if(emailField.length>0){
        fetch("/Authentication/validate_email",{ 
            body:JSON.stringify({email:emailVal}),
            method:"POST",
        })
        .then((res)=>res.json)
        .then((data)=>{
            console.log("data",data);
            if(data.username_error){
                emailField.classList.add('is-valid');
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML=`<p>${data.username_error}</p>`
                submit.setAttribute=true;
            }else{
                submit.removeAttribute("disabled");
            }
        });
    }
}); 


const handleToggle=(e)=>{
    if(showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute("type","text");
    }
    else{
        showPasswordToggle.textContent="SHOW";
        passwordField.setAttribute("type","password");
    }
};
showPasswordToggle.addEventListener('click',handleToggle);