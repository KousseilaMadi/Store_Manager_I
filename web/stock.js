window.addEventListener('load' ,function() {
    setTimeout(view_products, 350)
})

async function addProduct(event){
    event.preventDefault()
    const barcode_input = document.getElementById('product-barcode')
    const name_input = document.getElementById('product-name')
    const price_input = document.getElementById('product-price')
    const qty_input = document.getElementById('product-stock')
    const cost_price_input = document.getElementById('product-cost')

    const result = await pywebview.api.stock.add_product(
        barcode_input.value,
        name_input.value,
        price_input.value,
        qty_input.value,
        cost_price_input.value
    )
    if(result.success){
        openAddProductSuccessModal(event,
            barcode_input.value,
            name_input.value,
            price_input.value,
            qty_input.value,
            cost_price_input.value)
            view_products()
    }else{
        if(result.error_type === 'database'){
            openNotificationModal('Error', 'Barcode already exists !')
        }else{
            openNotificationModal('Error !', result.message)
        }
    }

}

function openAddProductSuccessModal(event,
            barcode,
            name,
            price,
            qty,
            cost_price){
    event.stopPropagation()
    document.getElementById('add-product-success-modal').style.display = 'flex'
    document.getElementById('success-name').textContent = name
    document.getElementById('success-barcode').textContent = barcode
    document.getElementById('success-price').textContent = price
    document.getElementById('success-quantity').textContent = qty
    document.getElementById('success-cost').textContent = cost_price
    document.getElementById('success-ok-btn').focus()
}
function closeAddProductSuccessModal(){
    document.getElementById('add-product-success-modal').style.display = 'none'
}

function openDeleteProductConfirmModal(productId){
    const modal = document.getElementById('delete-product-confirm-modal')
    modal.style.display = 'flex'
    modal.setAttribute('data-product-id', productId)
    document.getElementById('delete-btn').focus()
}
function closeDeleteProductConfirmModal(){
    document.getElementById('delete-product-confirm-modal').style.display = 'none'
    view_products()
}
async function performProductDeletion(){
    const product_id = document.getElementById('delete-product-confirm-modal').getAttribute('data-product-id')
    const result = await pywebview.api.stock.delete_product(product_id)
    if(result.success){
        closeDeleteProductConfirmModal()
        openNotificationModal('Success', 'Product deleted successfuly !')
    }else{
        openNotificationModal('Error', result.message)
    }
}

function openEditModal(productId){
    document.getElementById('edit-modal').style.display = 'flex'
    document.getElementById('edit-name').value = document.getElementById('product-' + productId + '-name').textContent
    document.getElementById('edit-barcode').value = document.getElementById('product-' + productId + '-barcode').textContent.replace('Barcode: ', '').trim()
    document.getElementById('edit-price').value = document.getElementById('product-' + productId + '-price').textContent.replace('Price: ', '').replace(' DA', '').trim()
    document.getElementById('edit-stock').value = document.getElementById('product-' + productId + '-stock').textContent.replace('Stock: ', '').trim()
    document.getElementById('edit-cost').value = document.getElementById('product-' + productId + '-cost').textContent.replace('Cost: ', '').replace(' DA', '').trim()
    document.getElementById('edit-modal').setAttribute('data-product-id', productId)
}

async function view_products(){
    const name_filter = document.getElementById('search-product-name').value
    const barcode_filter = document.getElementById('search-product-barcode').value
    const start_date_filter = document.getElementById('filter-start-date').value
    const end_date_filter = document.getElementById('filter-end-date').value
    const result = await pywebview.api.stock.fetch_products(name_filter || null, barcode_filter || null, start_date_filter || null, end_date_filter || null)
    const products_list = document.getElementById('products-list')
    if (result.success){
        const products = result.data.products
        products_list.innerHTML = ''
        const products_list_html = products.map(p => {
            return `
            <div class="product-card" id="product-${p.id}">
                <div class="product-info">
                    <div class="product-name" id="product-${p.id}-name">${p.name}</div>
                    <div class="product-details">
                        <span id="product-${p.id}-barcode">Barcode: ${p.barcode}</span>
                        <span id="product-${p.id}-price">Price: ${p.price.toFixed(2)} DZD</span>
                        <span id="product-${p.id}-stock">Stock: ${p.stock}</span>
                        <span id="product-${p.id}-cost">Cost: ${p["cost-price"].toFixed(2)} DZD</span>
                        <span id="product-${p.id}-date">Created at: ${p["created-at"].split('T')[0]}</span>
                    </div>
                </div>
                <div class="product-actions">
                    <button class="primary-btn" onclick="openEditModal(${p.id})">Edit</button>
                    <button class="danger-btn" onclick="openDeleteProductConfirmModal(${p.id})">Delete</button>
                </div>
            </div>
            `
        })
        if (products_list_html.length > 0){

            products_list.innerHTML = products_list_html.join('')
        }else{
            products_list.innerHTML = 
            `
            <p style="color:#fff; text-align:center; margin-top:40px;">
            Empty
            </p>
            `
        }
    }else{
        openNotificationModal('Error', result.message)
    }
}

function closeEditModal(){
    document.getElementById('edit-modal').style.display = 'none'
    view_products()
}
async function saveProductEdit(event){
    event.preventDefault()
    event.stopPropagation()
    const productId = document.getElementById('edit-modal').getAttribute('data-product-id')
    const name = document.getElementById('edit-name').value
    const barcode = document.getElementById('edit-barcode').value
    const price = document.getElementById('edit-price').value
    const stock = document.getElementById('edit-stock').value
    const cost = document.getElementById('edit-cost').value

    const result = await pywebview.api.stock.edit_product(productId, barcode, name, price, stock, cost)

    if(result.success){
        closeEditModal()
        openNotificationModal('Success', 'Product update successfuly !')
    }else{
        openNotificationModal('Error', result.message)
    }

    document.getElementById('edit-modal').setAttribute('data-product-id', '')


}
