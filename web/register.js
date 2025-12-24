window.addEventListener('load', function() {
    setTimeout(function() {
        init_tabs()
        switchRegister(state.current_register)
    }, 350)
})

function init_tabs(){
    
     var i = 0
    const tabs_html = Object.values(state.registers).map(register =>{
        i++
        return `
        <div id="register-tab-${i}" class="register-tab active" onclick="switchRegister(${i})">
            <span class="tab-label">Register ${i}</span>
            <button class="close-tab-btn btn-active" onclick="closeRegister(event, ${i}); return false;">×</button>
        </div>
        `
    })
    document.getElementById('tabs').innerHTML = tabs_html.join('')


}

async function switchRegister(registerId) {
    
    state.current_register = registerId
    const scan_input = document.getElementById('scan-input')
    const items_list = document.getElementById('cart-items-body')
    scan_input.value = ''
    items_list.innerHTML = `
    <p style="color:#66666699; text-align:center; margin-top:40px;">
        Empty
    </p>
    `
   



    const all_tabs = document.querySelectorAll(`[id^="register-tab-"]`)
    // change the color of the previous tab
    all_tabs.forEach(tab => {
        tab.classList.remove('active')
        const btn = tab.querySelector('.close-tab-btn')
        if(btn){
            btn.classList.remove('btn-active')
        }
    })
    
    
    
    // change the color of the next tab
    const register_tab = document.getElementById('register-tab-' + registerId)
    register_tab.classList.add('active')
    const tab_close_btn = register_tab.querySelector('.close-tab-btn')
    if(tab_close_btn){
        tab_close_btn.classList.add('btn-active')
    }
    
    
    
    const items = state.registers['register-' + state.current_register]
    const cart_html = items.map(item => {

        
        return `
        <div data-item-id="${item.id}" class="cart-row">
            <div class="cart-table-cell row_1">${item.name}</div>
            <div class="cart-table-cell row_1">${item.price.toFixed(2)} DZD</div>
            <div class="cart-table-cell row_1">${item.qty}</div>
            <div class="cart-table-cell row_1">${item.subtotal.toFixed(2)} DZD</div>
            <div class="actions-cell row_1">
            ${item['product-id'] ? `
                <button onclick="openQuantityModal('${item.id}')" class="action-button"><img src="edit.svg" width="30" height="30"></button>
                `:''}
                <button onclick="removeItem('${item.id}')" class="action-button"><img src="delete.svg" width="30" height="30"></button>
                </div>
        </div>
        `
        })
        if(cart_html.length > 0)
            items_list.innerHTML = cart_html.join('')
    const total = calculate_total('register-' + state.current_register)
    document.getElementById('total-amount').textContent = total.toFixed(2)

    await pywebview.api.state.set_state(state)

}


function closeRegister(event, registerId) {
    event.stopPropagation()
    event.preventDefault()
    if(Object.keys(state.registers).length === 1){
        state.current_register = Object.keys(state.registers)[0].split('-')[1]
        return
    }
    delete state.registers['register-' + registerId]
    document.getElementById('register-tab-' + registerId).remove()
    if(state.current_register === registerId){
        state.current_register = Object.keys(state.registers)[0].split('-')[1]
        switchRegister(state.current_register)
    }

}


async function createNewRegister() {
    const result = await pywebview.api.register.new_register()
    if(result.success){
        
    }else{
        openNotificationModal('Error', result.message)

    }
    const tabs_container = document.getElementById('tabs')
    var register_number = state.max_register_number + 1
    state.max_register_number += 1
    tabs_container.innerHTML += `
    <div id="register-tab-${register_number}" class="register-tab" onclick="switchRegister(${register_number})">
        <span class="tab-label">Register ${register_number}</span>
        <button class="close-tab-btn" onclick="closeRegister(event, ${register_number}); return false;">×</button>
    </div>
    `
    state.registers["register-" + register_number] = []
    state.current_register = register_number
    switchRegister(register_number)

}   

async function scanProduct() {
    const scan_input = document.getElementById('scan-input')
    const item_id = Date.now().toString() + Math.random().toString(36).substring(2, 9)
    const result = await pywebview.api.register.add_item('register-' + state.current_register, item_id, scan_input.value)
    scan_input.value = ''
    const items_list = document.getElementById('cart-items-body')
    if (result.success){
        const items = state.registers['register-' + state.current_register]
        
        const existingIndex = items.findIndex(item => item["product-id"] === result.data.item['product-id'])
        
        if (existingIndex !== -1){
            items[existingIndex].qty++
            items[existingIndex].subtotal = items[existingIndex].price * items[existingIndex].qty
        }else{
            
            const item = {
                "id": item_id,
                "product-id": result.data.item["product-id"],
                "name": result.data.item.name,
                "price": result.data.item.price,
                "qty": 1,
                "subtotal": result.data.item.price
            }
            items.push(item)

        }
        switchRegister(state.current_register)

        items_list.innerHTML = list.join('')

    }else{
        openNotificationModal('Error', result.message)
    }
}

function openDiversModal() {
    document.getElementById('divers-modal').style.display = 'flex';
    document.getElementById('divers-name').focus();
    

}

function closeDiversModal() {
    document.getElementById('divers-modal').style.display = 'none';
    //clear inputs
    document.getElementById('divers-name').value = '';
    document.getElementById('divers-price').value = '';
    document.getElementById('divers-quantity').value = '';
}

function openSeachModal() {
    document.getElementById("search-modal").style.display = "flex"
    document.getElementById('search-name').focus();
    searchProducts()
}
async function select_product(event, product_id, name, barcode, qty){
    event.preventDefault()
    const items = state.registers['register-' + state.current_register]
    const existingIndex = items.findIndex(item => item["product-id"] === product_id)
    const item_id = Date.now().toString() + Math.random().toString(36).substring(2, 9)
    
    const result = await pywebview.api.register.add_item('register-' + state.current_register, item_id, barcode)
    if(result.success){
        if (existingIndex !== -1){
            items[existingIndex].qty++
            items[existingIndex].subtotal = items[existingIndex].price * items[existingIndex].qty
        }else{
            const item = {
                "id": item_id,
                "product-id": result.data.item['product-id'],
                "name": result.data.item.name,
                "price": result.data.item.price,
                "qty": 1,
                "subtotal": result.data.item.price
            }
            items.push(item)
            
        }
    }else{
        openNotificationModal('Error', result.message)
    }
    switchRegister(state.current_register)
    closeSearchModal()
}

async function searchProducts(){
    const name_filter = document.getElementById('search-name').value
    const result = await pywebview.api.stock.fetch_products(name_filter, null, null, null)
    if(result.success){
        const products = result.data.products
        const product_list = document.getElementById('search-results-body')
        const products_html = products.map(p => {
            return `
            <div class="search-result-row" onclick="select_product(event, ${p.id},'${p.name}', '${p.barcode}',${p.qty})">
                <div>${p.name}</div>
                <div>${p.price.toFixed(2)} DZD</div>
            </div>
            `
        })
        
        product_list.innerHTML = products_html.join('')
    }else{
        openNotificationModal('Error', '')
    }
}

function closeSearchModal() {
    document.getElementById("search-modal").style.display = "none"
    document.getElementById('search-name').value = '';

}
function openQuantityModal(itemId){
    document.getElementById("quantity-modal").style.display = "flex"
    document.getElementById("quantity-input").focus()
    document.getElementById("quantity-input").setAttribute('data-item-id', itemId)
    const items = state.registers['register-' + state.current_register]
    const item_index = items.findIndex(item => item.id === itemId)
    document.getElementById("quantity-input").value = items[item_index].qty
}

function closeQuantityModal(){
    document.getElementById("quantity-modal").style.display = "none"
    document.getElementById("quantity-input").value = ''
}
async function applyQuantity(event){
    event.preventDefault()
    const qty_input = document.getElementById('quantity-input')
    var item_id = qty_input.getAttribute('data-item-id')
    const items = state.registers['register-' + state.current_register]
    const item_index = items.findIndex(item => item.id === item_id)
    items[item_index].qty = parseInt(qty_input.value)
    items[item_index].subtotal = items[item_index].qty * items[item_index].price
    const result = await pywebview.api.register.apply_quantity('register-' + state.current_register, item_id, parseInt(qty_input.value))
    if(result.success){
    }else{
        openNotificationModal('Error', result.message)
    }
    closeQuantityModal()
    switchRegister(state.current_register)
}
async function removeItem(item_id){
    const items = state.registers['register-' + state.current_register]
    const item_index = items.findIndex(item => item.id === item_id)
    items.splice(item_index, 1)
    const result = await pywebview.api.register.remove_item('register-' + state.current_register, item_id)
    if(result.success){

    }else{
        openNotificationModal('Error', result.message)
    }
    switchRegister(state.current_register)
}

async function addDiversItem(event) {
    event.preventDefault()
    const name = document.getElementById('divers-name').value
    const price = parseFloat(document.getElementById('divers-price').value)
    const qty = parseInt(document.getElementById('divers-quantity').value)
    const items = state.registers['register-' + state.current_register]
    const item_id = Date.now().toString() + Math.random().toString(36).substring(2, 9)

    const item = {
            "id": item_id,
            "product-id": null,
            "name": name,
            "price": price,
            "qty": qty,
            "subtotal": qty * price
            }
    items.push(item)


    const result = await pywebview.api.register.add_divers('register-' + state.current_register, item_id, price, price * qty, qty)
    if(result.success){

    }else{
        openNotificationModal('Error', result.message)
    }
    closeDiversModal()
    switchRegister(state.current_register)
}

async function checkout() {
    const result = await pywebview.api.register.checkout('register-' + state.current_register)
    if(result.success){
        clearRegister()
        await pywebview.api.state.set_state(state)

    }else{
        openNotificationModal('Error', result.message)
    }
}

async function clearRegister() {
    await pywebview.api.register.clear_register('register-' + state.current_register)
    const scan_input = document.getElementById('scan-input')
    const items_list = document.getElementById('cart-items-body')
    scan_input.value = ''
    items_list.innerHTML = `
    <p style="color:#66666699; text-align:center; margin-top:40px;">
    Empty
    </p>
    `
    state.registers['register-' + state.current_register] = []
    switchRegister(state.current_register)
}

function calculate_total(registerId){
    const items = state.registers[registerId]
    return items.reduce((acc , item) => acc + item.price * item.qty, 0)
}
