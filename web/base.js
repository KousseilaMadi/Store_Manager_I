let state = {}

async function init_state(){
    if(!window.pywebview || !window.pywebview.api){
        setTimeout(init_state, 100)
        return
    }
    state = await pywebview.api.state.get_state()
    init_navbar()
}




document.addEventListener('DOMContentLoaded', function() {
    init_state()
})

function init_navbar(){
    const cashier_navbar = document.getElementById('user-navbar')
    const admin_navbar = document.getElementById('admin-navbar')
    if(state.current_user.role === 'ADMIN'){
        admin_navbar.style.display = 'flex'
        cashier_navbar.style.display = 'none'
    }else{
        admin_navbar.style.display = 'none'
        cashier_navbar.style.display = 'flex'
    }
}

async function closeApp() {
    await pywebview.api.debug("closing app...")
    await pywebview.api.close_app()
}
function toggleSection(sectionId, headerId) {
    const section = document.getElementById(sectionId);
    const arrow = section.previousElementSibling.querySelector('.dropdown-arrow');
    const header = document.getElementById(headerId)
    header.classList.toggle('collapsed')
    section.classList.toggle('collapsed');
    
    // Rotate arrow
    if (section.classList.contains('collapsed')) {
        arrow.style.transform = 'rotate(0deg)';
    } else {
        arrow.style.transform = 'rotate(180deg)';
    }
}

function toggleSubsection(subsectionId, subsectionHeaderId) {
    const subsection = document.getElementById(subsectionId);
    const arrow = subsection.previousElementSibling.querySelector('.dropdown-arrow');
    const header = document.getElementById(subsectionHeaderId)
    subsection.classList.toggle('collapsed');
    header.classList.toggle('collapsed')
    // Rotate arrow
    if (subsection.classList.contains('collapsed')) {
        arrow.style.transform = 'rotate(0deg)';
    } else {
        arrow.style.transform = 'rotate(180deg)';
    }
}

function openNotificationModal(title, message){
    document.getElementById('info-modal-title').textContent = title
    document.getElementById('info-modal-message').textContent = message
    document.getElementById('info-notification-modal').style.display = 'flex'
    document.getElementById('ok-btn').focus()
}
function closeNotificationModal(){
    document.getElementById('info-notification-modal').style.display = 'none'
}