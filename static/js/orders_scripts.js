window.addEventListener('load', () => {

    let quantity, price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost

    let quantity_arr = []
    let price_arr = []

    let total_forms = parseInt($('input#id_orderitems-TOTAL_FORMS').val());
    console.log(total_forms);

    let order_total_cost = parseFloat($('span.order_total_cost').text().replace(',', '.')) || 0;
    let order_total_quantity = parseInt($('span.order_total_quantity').text()) || 0;
    console.log(order_total_cost);
    console.log(order_total_quantity);


    for (let i = 0; i < total_forms; i++) {
        quantity_arr.push(parseInt($(`#id_orderitems-${i}-quantity`).val()));
        price_arr.push(parseFloat($(`.orderitems-${i}-price`).text().replace(',', '.') || 0))
    }

    console.log(quantity_arr)
    console.log(price_arr)
    $('.order_form').on('click', 'input[type=number]',  e=>{
        let target = e.target;

        orderitem_num = parseInt(target.name.split('-')[1]);
        if (price_arr[orderitem_num]) {
            let orderitem_price = price_arr[orderitem_num];
            delta_quantity = parseInt(target.value) - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = target.value;
            orderSummaryUpdate(orderitem_price, delta_quantity);
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]',  e=>{
        let target = e.target;

        orderitem_num = parseInt(target.name.split('-')[1]);
        if (price_arr[orderitem_num]) {
            if (target.checked) {
                delta_quantity = -quantity_arr[orderitem_num]
                $(`#id_orderitems-${orderitem_num}-quantity`).prop('disabled', true)
                $(`#id_orderitems-${orderitem_num}-product`).prop('disabled', true)
            } else {
                delta_quantity = quantity_arr[orderitem_num]
                $(`#id_orderitems-${orderitem_num}-quantity`).prop('disabled', false)
                $(`#id_orderitems-${orderitem_num}-product`).prop('disabled', false)
            }
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    $('.order_form').on('change', 'select.form-control', e => {
        let target = e.target;
        let product_pk = target.value;
        let row = parseInt(target.name.split('-')[1])

        $.ajax({
            url: `/orders/get_product_price/${product_pk}`,
            success: data => {
                $('.td3>span').filter((num, el) => num === row).text(`${data.price.replace('.', ',')} руб`);
                recalcArrays();
                recalcTotalCost();
            }
        })
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost));
        order_total_quantity += delta_quantity;

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_cost.toFixed(2).replace('.', ','));
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
        added: recalcArrays
    })

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.split('-')[1]);
        delta_quantity = -quantity_arr[orderitem_num] || 0;
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    function recalcArrays() {
        let total_forms = parseInt($('input#id_orderitems-TOTAL_FORMS').val());
        console.log(total_forms);

        quantity_arr = [];
        price_arr = [];
        for (let i = 0; i < total_forms; i++) {
            quantity_arr.push(parseInt($(`#id_orderitems-${i}-quantity`).val() || 0));
        }
        $('.td3>span').each((num, el) => price_arr.push(parseFloat($(el).text().replace(',', '.'))));
    }

    function recalcTotalCost() {
        let total_cost = 0;
        for (let i = 0; i < price_arr.length; i++) {
            total_cost += price_arr[i] * quantity_arr[i];
        }
        $('span.order_total_cost').text(total_cost.toFixed(2).replace('.', ','));
    }

})