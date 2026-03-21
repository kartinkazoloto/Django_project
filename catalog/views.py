from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')


# def contacts(request):
#     return render(request, 'contacts.html')


def contacts(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'contacts.html')
