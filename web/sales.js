document.addEventListener('DOMContentLoaded', function(){
    setTimeout(function() {
        init_page()
        fetch_sales()
    }, 350)
})
function init_page() {
    const profit_card = document.getElementById('profit-card')
    const sales_filters = document.getElementById('sales-filters')
    if(state.current_user.role !== "ADMIN"){
        profit_card.style.display = 'none'
        sales_filters.style.display = 'none'
    }else{
        profit_card.style.display = 'block'
        sales_filters.style.display = 'block'    
    }
    document.getElementById('sales-start-date').value = state.filters.sales.start_date
    document.getElementById('sales-end-date').value = state.filters.sales.end_date
}

function toggleSaleDetails(saleId){
    document.getElementById('sale-details-' + saleId).classList.toggle('collapsed')
}

function openRefundModal(sale_id, item_id, name, qty, price){
    document.getElementById('refund-modal').style.display = 'flex'
    const sale_id_element = document.getElementById('refund-modal-sale-id')
    const product_name_element = document.getElementById('refund-modal-product-name')
    const max_quantity_element = document.getElementById('refund-modal-max-qty')
    const refund_amount_element = document.getElementById('refund-total-amount')
    const max_restock_quantity_element = document.getElementById('restock-modal-max-qty')
    const refund_quantity_element = document.getElementById('refund-quantity-input')
    
    refund_amount_element.setAttribute('data-price', price)
    sale_id_element.textContent = sale_id
    product_name_element.textContent = name
    max_quantity_element.textContent = qty
    refund_amount_element.textContent = refund_quantity_element.value * price
    max_restock_quantity_element.textContent = qty
    
    
    document.getElementById('refund-process-form').setAttribute('data-item-id', item_id)
}
function closeRefundModal(){
    document.getElementById('refund-modal').style.display = 'none'
}
async function performRefund(){
    const item_id = document.getElementById('refund-process-form').getAttribute('data-item-id')
    const restock_qty = document.getElementById('restock-quantity-input').value
    const refund_qty = document.getElementById('refund-quantity-input').value
    const result = await pywebview.api.sales.refund_item(item_id, parseInt(refund_qty), parseInt(restock_qty))
    if(!result.success)
        openNotificationModal('Error !', result.message)
    closeRefundModal()
}
function QtyCheck(){
    const restock_quantity_element = document.getElementById('restock-quantity-input')
    const refund_quantity_element = document.getElementById('refund-quantity-input')
    const max_quantity_element = document.getElementById('refund-modal-max-qty')
    const refund_amount_element = document.getElementById('refund-total-amount')
    const max_quantity = parseInt(max_quantity_element.textContent)
    const restock_quantity = parseInt(restock_quantity_element.value)
    const refund_quantity = parseInt(refund_quantity_element.value)
    const price = parseFloat(refund_amount_element.getAttribute('data-price'))
    
    if(restock_quantity>max_quantity || refund_quantity > max_quantity){
        restock_quantity_element.value = max_quantity
        refund_quantity_element.value = max_quantity
    }
    
    if (restock_quantity > refund_quantity)
        restock_quantity_element.value = refund_quantity_element.value
    
    refund_amount_element.textContent = refund_quantity_element.value * price
    
    document.getElementById('refund-process-form').setAttribute('data-refund-qty', refund_quantity)
    document.getElementById('refund-process-form').setAttribute('data-restock-qty', restock_quantity)
}

async function fetch_sales() {
    const start_date = document.getElementById('sales-start-date')
    const end_date = document.getElementById('sales-end-date')
    const revenue = document.getElementById('total-revenue')
    const profit = document.getElementById('total-profit')
    const salesCount = document.getElementById('total-sales')

    if(state.current_user.role === "ADMIN"){
        state.filters.sales = {}
        state.filters.sales.start_date = document.getElementById('sales-start-date').value
        state.filters.sales.end_date = document.getElementById('sales-end-date').value
        await pywebview.api.state.set_state(state)
    }


    const result = await pywebview.api.sales.list_sales(null, start_date.value, end_date.value);
    const salesListElement = document.getElementById('sales-list');
    const refundsListElement = document.getElementById('refunds-list');
    if (!result.success) {
        openNotificationModal('Error', result.message);
        return;
    }
    const salesData = result.data.sales;
    if(Object.values(salesData).length === 0){
        salesListElement.innerHTML = `<p style="color:#fff; text-align:center; margin-top:40px;">No Sales Found</p>`;
        return
        
    }
    const allSalesHTML = Object.values(salesData).map(sale => {
        const itemsHTML = sale.items.map(item => {
            return (item['product-id'] !== null)?`
                <div class="sale-item">
                    <span>${item.name || 'Product Unknown'}</span>
                    <span>Qty: ${item.quantity}</span>
                    <span>Prix unité: ${item['unit-price'].toFixed(2)} DZD</span>
                    <span>Prix: ${item.subtotal.toFixed(2)} DZD</span>
                    ${(item.refunded < item.quantity)?
                    `
                    <span style="color:var(--danger); font-weight:medium;">Refunded ${item.refunded}</span>
                    <button class="danger-btn" style="font-size:100%;" onclick="openRefundModal(${sale.sale.id}, ${item.id}, '${item.name}', ${item.quantity}, ${item["unit-price"]})">Refund</button>
                    `:`
                    <span style="color:var(--danger); grid-column:6; font-weight:medium;">Refunded</span>
                    `}
                    
                </div>
            `:`
                <div class="sale-item">
                    <span>${item.name || 'Product Unknown'}</span>
                    <span>Qty: ${item.quantity}</span>
                    <span>Prix unité: ${item['unit-price'].toFixed(2)} DZD</span>
                    <span>Prix: ${item.subtotal.toFixed(2)} DZD</span>
                </div>
            `
        }).join('');

        return `
        <div class="sale-card" id="sale-${sale.sale.id}">
            <div class="sale-header" onclick="toggleSaleDetails(${sale.sale.id})">
                <div class="sale-info">
                    <span class="sale-id">Sale #${sale.sale.id}</span>
                    <span class="sale-date">${sale.sale["created-at"].split('T')[0]}</span>
                    <span class="sale-date">${sale.sale["created-at"].split('T')[1].split(':')[0]}:${sale.sale["created-at"].split('T')[1].split(':')[1]}</span>
                </div>
                <div class="sale-total">${sale.sale["total-price"].toFixed(2)} DZD</div>
                <span class="dropdown-arrow">▼</span>
            </div>
            <div class="sale-details collapsed" id="sale-details-${sale.sale.id}">
                ${itemsHTML}
            </div>
        </div>
        `;
    });
    salesListElement.innerHTML = allSalesHTML.join('');
    let revenue_amount = 0;
    let spend_amount = 0;
    let sales_count = 0;

    const totalData = Object.values(result.data.sales).reduce((acc, saleData) => {
    
    const sale = saleData.sale; 
    const items = saleData.items;

    acc.sales_count += 1;

    acc.revenue += parseFloat(sale["total-price"]) || 0;

    const saleCost = items.reduce((costAcc, item) => {
        return costAcc + item["cost-price"] * item.quantity;
    }, 0);

    acc.spend += saleCost;

    return acc;
    
    }, { revenue: 0, spend: 0, sales_count: 0 });


    revenue_amount = totalData.revenue;
    spend_amount = totalData.spend;
    sales_count = totalData.sales_count;

    const profit_amount = revenue_amount - spend_amount;
    revenue.textContent = revenue_amount
    profit.textContent = profit_amount
    salesCount.textContent = sales_count


    const refunds_result = await pywebview.api.sales.list_refunds();

    if(!refunds_result.success){
        openNotificationModal('Error', result.message);
        return
    }
    
    
    const refunds_list = refunds_result.data.refunds
    
    if(refunds_list.length === 0){
        refundsListElement.innerHTML = `<p style="color:#fff; text-align:center; margin-top:40px;">No Refunds Found</p>`;
        return   
    }
    const refunds_elements = refunds_list.map(refund => {
        return `
        <div class="sale-card" id="refund-${refund.id}">
            <div class="sale-header">
                <div class="sale-info">
                    <span class="sale-id">#${refund.id}</span>
                    <span class="sale-id">${refund.name}</span>
                    <span class="sale-date">${refund["created-at"].split('T')[0]}</span>
                    <span class="sale-date">${refund["created-at"].split('T')[1].split(':')[0]}:${refund["created-at"].split('T')[1].split(':')[1]}</span>
                </div>
                <div class="sale-total">${refund['quantity-refunded']}</div>
                <div class="sale-total">${parseFloat(refund['unit-price'] * refund['quantity-refunded']).toFixed(2)} DZD</div>
            </div>
        </div>
        `
    })

    refundsListElement.innerHTML = refunds_elements.join('')

}


function clearSalesFilters(){
    const start_date = document.getElementById('sales-start-date')
    const end_date = document.getElementById('sales-end-date')
    start_date.value = ''
    end_date.value = ''
    fetch_sales()


}
