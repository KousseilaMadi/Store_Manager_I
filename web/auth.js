async function register(event){
    event.preventDefault()
    const username = document.getElementById('register-username').value
    const password = document.getElementById('register-password').value
    const confirm_password = document.getElementById('register-confirm-password').value
    if(password !== confirm_password){
        openNotificationModal("Password Issue !", "confirm password doesnt match the password.")
        return
    }

    const result = await pywebview.api.auth.add_user(username, password, 'CASHIER')
    if (result.success){
        openNotificationModal("User Added Successfully !", username + " was created.")
    }else{
        openNotificationModal("Something Went Wrong !", "error: " + result.message)
    }
}

async function login(event){
    event.preventDefault()
    const username = document.getElementById('login-username').value
    const password = document.getElementById('login-password').value
    const result = await pywebview.api.auth.login(username, password)
    if(result.success){
        state.current_user = result.data
        await pywebview.api.state.set_state(state)
        window.location.assign("register.html")
    }else{
        openNotificationModal("Something Went Wrong !", "error: " + result.message)
    }
}