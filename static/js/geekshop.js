window.addEventListener('load', ()=> {
    $('.basket-list').on('change', 'input.form-control',e=>{
        let input = e.target;
        let urlEdit = input.attributes['data-url-edit'].value;
        let p = urlEdit.split('/').filter(s=>s.length>0);
        let [url, basket_id, quantity] = [p.slice(0, -2).join('/'), p.slice(-2, -1)[0], p.slice(-1)[0]];
        let new_quantity = input.value;
        if (quantity !== new_quantity) {
            $.ajax(
                {
                    url: `/${url}/${basket_id}/${new_quantity}`,
                    success: function (data) {
                        $('.basket-list').html(data.result);
                    },
                });
            e.preventDefault();
        }
    })

    $('.card_add_basket').on('click', 'button[type=button]', e=>{
        let input = e.target;
        let urlAdd = input.attributes['data-href'].value;
        $.ajax({
            url: urlAdd,
            // success: data=>{
            //     $('.card_add_basket').html(data.result);
            // }
        });
        e.preventDefault();
    })

    $('.products_pagination').on('click', 'button.page-link', e=>{
        let input = e.target;
        let urlPage = input.attributes['data-href'].value;
        $.ajax({
            url: urlPage,
            success: data=>{
                $('.card_add_basket').html(data.result);
            }
        });
        e.preventDefault();
    })
})