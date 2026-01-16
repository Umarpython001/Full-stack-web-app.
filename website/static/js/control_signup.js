

const sign_up_btn_submit = document.getElementById("sign_up_btn_submit")


const sign_up_form = document.getElementById("SignUpForm")

const sign_up_information = document.querySelectorAll(".form-control") // This gives ALL user information. This is a node list

const necessary_signup_information = Array.from(sign_up_information).slice(0, 5) //Here I get all necessary user information

const checkbox_confirm = document.getElementById("confirm_inputs")

let info_useful_object = {
                    first_name: "",
                    last_name:  "",
                    email_signup: "",
                    password1_signup: "",
                    password2_signup: "",
};

let info_as_strings;

const first_name_input = necessary_signup_information[0]
const last_name_input = necessary_signup_information[1]
const email_signup_input = necessary_signup_information[2]
const password1_signup_input = necessary_signup_information[3]
const password2_signup_input = necessary_signup_information[4]


document.addEventListener("DOMContentLoaded", showInfo)

function check_checkbox(){

    if(checkbox_confirm.checked){


        let first_name = first_name_input.value
        let last_name = last_name_input.value
        let email_signup = email_signup_input.value
        let password1_signup = password1_signup_input.value
        let password2_signup = password2_signup_input.value
    
        info_useful_object.first_name = first_name
        info_useful_object.last_name = last_name
        info_useful_object.email_signup = email_signup
        info_useful_object.password1_signup = password1_signup
        info_useful_object.password2_signup = password2_signup
    
    
        info_as_strings = JSON.stringify(info_useful_object)
        localStorage.setItem(storageKey, info_as_strings)
    
        sign_up_btn_submit.disabled = "false"
    
    }
    

}


function showInfo(){

    const oldinfo = localStorage.getItem(storageKey)

    let first_name = oldinfo.first_name
    let last_name = oldinfo.last_name
    let email_signup = oldinfo.email_signup
    let password1_signup = oldinfo.password1_signup
    let password2_signup = oldinfo.password2_signup

    first_name_input.value = first_name
    last_name_input.value = last_name
    email_signup_input.value = email_signup
    password1_signup_input.value = password1_signup
    password2_signup_input.value = password2_signup

}



