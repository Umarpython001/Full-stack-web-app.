const sign_up_btn_submit = document.getElementById("sign_up_btn_submit")

const sign_up_form = document.getElementById("SignUpForm")

const sign_up_information = document.querySelectorAll(".form-control") // This gives ALL user information. This is a node list

const necessary_signup_information = Array.from(sign_up_information).slice(0, 5) //Here I get all necessary user information


let info_useful_object = {
                    first_name: "",
                    last_name:  "",
                    email_signup: "",
};

let info_as_strings;

const first_name_input = necessary_signup_information[0]
const last_name_input = necessary_signup_information[1]
const email_signup_input = necessary_signup_information[2]


function check_info(){

    const isFirstNameValid = first_name_input.value.trim().length >= 2;
    const isLastNameValid = last_name_input.value.trim().length >= 2;
    const isEmailValid = email_signup_input.value.includes(".") && email_signup_input.value.includes("@") && email_signup_input.value.length >= 5;


    let first_name = first_name_input.value
    let last_name = last_name_input.value
    let email_signup = email_signup_input.value
                
    info_useful_object.first_name = first_name
    info_useful_object.last_name = last_name
    info_useful_object.email_signup = email_signup
                  
    info_as_strings = JSON.stringify(info_useful_object)
    sessionStorage.setItem("user_information_key", info_as_strings)
        


    if(isFirstNameValid && isLastNameValid && isEmailValid){
        sign_up_btn_submit.disabled = false
    }
    else{
        sign_up_btn_submit.disabled = true
    }


}


function showInfo(){

    const invalidValues = new Set(["", " ", null, undefined]);

    const oldinfo = sessionStorage.getItem("user_information_key")

    if(!(invalidValues.has(oldinfo))){ //This checks to make sure that _oldinfo_ is valid. To make sure that it is 'defined'

        const oldinfo_object = JSON.parse(oldinfo)

        const oldinfo_array = Object.entries(oldinfo_object)
    
        for(let [key_object, value_object] of oldinfo_array){ //This goes through every key, value and checks them
            if(!(invalidValues.has(value_object.trim()))){ //This makes sure that the _value_ is a valid variable

                switch(true){
                    case key_object == "first_name":
                        first_name_input.value = value_object
                        break

                    case key_object == "last_name":
                        last_name_input.value = value_object
                        break

                    case key_object == "email_signup":
                        email_signup_input.value = value_object
                        break

                }
    
            }
        }

    }
    
}


document.addEventListener("DOMContentLoaded", (event) => {showInfo()})


sign_up_form.addEventListener("input", (event) => {check_info()}); // Triggers whenever a user types


sign_up_form.addEventListener("submit", (event) => {
    sessionStorage.removeItem("user_information_key");

    info_useful_object = { first_name: "", last_name: "", email_signup: "" };
});