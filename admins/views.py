from django.shortcuts import render

# Create your views here.


def index(request):
    ctx = {
        'header': 'Административная панель'
    }
    return render(request, 'admins/base.html', ctx)


