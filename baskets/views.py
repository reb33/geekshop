from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
from django.template.loader import render_to_string

from baskets.models import Basket
from products.models import Product


@login_required
def basket_add(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=user, product=product)

    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user, product=product, quantity=1)
    products = Product.objects.all()
    ctx = {'products': products}
    result = render_to_string('includes/card.html', ctx)
    return JsonResponse({'result': result})


@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    print(f'{basket_id} {quantity}')
    if request.is_ajax():
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        ctx = {'baskets': baskets}
        result = render_to_string('baskets/profile_baskets.html', ctx)
        return JsonResponse({'result': result})
