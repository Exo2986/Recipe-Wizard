document.addEventListener("DOMContentLoaded", () => {
    const emailInput = document.querySelector("#email-input")
    const emailConfirmInput = document.querySelector("#email-confirm-input")
    const updateEmailForm = document.querySelector("#updateEmailForm")
    
    function emailValidation(event) {
        if (emailInput.value !== emailConfirmInput.value) {
            event.target.setCustomValidity("Email addresses must match.")
            event.target.reportValidity()
        } else {
            emailInput.setCustomValidity("")
            emailConfirmInput.setCustomValidity("")
        }
    }

    emailInput.addEventListener("input", emailValidation)
    emailConfirmInput.addEventListener("input", emailValidation)

    const passwordInput = document.querySelector("#password-input")
    const passwordConfirmInput = document.querySelector("#password-confirm-input")
    const updatePasswordForm = document.querySelector("#updatePasswordForm")
    
    function passwordValidation(event) {
        if (passwordInput.value !== passwordConfirmInput.value) {
            event.target.setCustomValidity("Passwords must match.")
            event.target.reportValidity()
        } else {
            passwordInput.setCustomValidity("")
            passwordConfirmInput.setCustomValidity("")
        }
    }

    passwordInput.addEventListener("input", passwordValidation)
    passwordConfirmInput.addEventListener("input", passwordValidation)
})