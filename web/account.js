document.addEventListener('DOMContentLoaded', function(){
    setTimeout(function() {
        init_account()
        if(state.current_user.role === 'ADMIN')
            fetch_users()
    }, 400)
})

function init_account(){
    const username = document.getElementById('current-username')
    const role = document.getElementById('current-role')
    username.textContent = state.current_user.username
    role.textContent = state.current_user.role

    const admin_section = document.getElementById('admin-section')
    if (state.current_user.role === 'ADMIN'){
        admin_section.style.display = 'block'
    }else{
        admin_section.style.display = 'none'
    }

}

function openConfirmPasswordModal(){
    document.getElementById('confirm-password-modal').style.display = 'flex';
}
function closeConfirmPasswordModal(){
    document.getElementById('confirm-password-modal').style.display = 'none';

}
async function performPasswordChange(){
    closeConfirmPasswordModal()
    const current_password = document.getElementById('current-password')
    const new_password = document.getElementById('new-password')
    const confirm_password = document.getElementById('confirm-password')
    if(new_password.value !== confirm_password.value){
        openNotificationModal('Error', 'new password and confirm password do not match')
        return
    }

    const result = await pywebview.api.auth.change_password(state.current_user.username, current_password.value, new_password.value)
    if(result.success){
        openNotificationModal('Success', result.message)
    }else{
        openNotificationModal('Error', result.message)
    }


}
function openLogoutConfirmModal(){
    document.getElementById('logout-confirm-modal').style.display = 'flex';
    document.getElementById('confirm-logout').focus();

}
function closeLogoutConfirmModal(){
    document.getElementById('logout-confirm-modal').style.display = 'none';
}
async function performLogout(){
    const result = await pywebview.api.auth.logout()
    if(result.success){
        state = {}
        await pywebview.api.state.set_state({})
        window.location.assign("login.html")
    }else{
        openNotificationModal('Something went wrong !', result.message)
    }
}
function openRoleChangeModal(username){
    document.getElementById('role-change-modal').style.display = 'flex';
    document.getElementById('role-select').focus();
    document.getElementById('role-change-modal').setAttribute('data-username', username)
    document.getElementById('user-to-role-change-name').textContent = username

}
function closeRoleChangeModal(){
    document.getElementById('role-change-modal').style.display = 'none';
}

async function applyRoleChange(){
    closeRoleChangeModal()
    const user_role = document.getElementById('role-select')
    const username = document.getElementById('role-change-modal').getAttribute('data-username')
    const result = await pywebview.api.auth.change_role(username, user_role.value)
    if(result.success){
        alert(result)
        openNotificationModal('Success', 'role changed !')
        fetch_users()
    }else{
        openNotificationModal('Error !', result.message)
    }

}

function openRemoveUserConfirmModal(username){
    document.getElementById('remove-user-confirm-modal').style.display = 'flex';
    document.getElementById('cancel-delete').focus()
    document.getElementById('remove-user-confirm-modal').setAttribute('data-username', username)
    document.getElementById('user-to-delete-name').textContent = username
}
function closeRemoveUserConfirmModal(){
    document.getElementById('remove-user-confirm-modal').style.display = 'none';
}

async function performUserDeletion(){
    closeAddUserConfirmModal()
    const username = document.getElementById('remove-user-confirm-modal').getAttribute('data-username')
    const result = await pywebview.api.auth.delete_user(username)
    if(result.success){
        openNotificationModal('Success', 'user deleted !')
        fetch_users()
    }else{
        openNotificationModal('Error', result.message)
    }
}

function openAddUserConfirmModal(){
    document.getElementById('add-user-confirm-modal').style.display = 'flex';
    document.getElementById('confirm-add').focus()
    const username = document.getElementById('new-username')
    const user_role = document.getElementById('new-user-role')
    const confirm_username = document.getElementById('confirm-new-username')
    const confirm_user_role = document.getElementById('confirm-new-role')
    confirm_username.textContent = username.value
    confirm_user_role.textContent = user_role.value

}
function closeAddUserConfirmModal(){
    document.getElementById('add-user-confirm-modal').style.display = 'none';
}

async function performAddUser(){
    closeAddUserConfirmModal()
    const username = document.getElementById('new-username')
    const password = document.getElementById('new-user-password')
    const confirm_password = document.getElementById('new-user-confirm-password')
    const user_role = document.getElementById('new-user-role')
    if(password.value !== confirm_password.value){
        openNotificationModal('Error !', 'passwords don\'t match')
        return
    }
    const result = await pywebview.api.auth.add_user(username.value, password.value, user_role.value)
    if(result.success){
        openNotificationModal('Success', username.value +' '+ result.message)
        fetch_users()
    }else{
        openNotificationModal('Error !', result.message)
    }

}

async function fetch_users(){
    const result = await pywebview.api.auth.list_users()
    if(result.success){
        const users_list_element = document.getElementById('users-list')
        const users = result.data.users
        var users_html = users.map(user => {
            return `
            <div class="user">
               <span>${user.username}</span>
               <span class="role">${user.role}</span>
               <div>
                   <button class="primary-btn" onclick="openRoleChangeModal('${user.username}')" style="font-size: 90%;">Change role</button>
                   <button class="danger-btn" onclick="openRemoveUserConfirmModal('${user.username}')" style="font-size: 90%;">Delete</button>
               </div>
            </div>
            `
        })
        users_list_element.innerHTML = users_html.join('')
    }else{
        openNotificationModal('Error !', result.message)
    }
}