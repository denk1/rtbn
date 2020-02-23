from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rtbn.models import Person
from rtbn.data import fill_new_line
from django.core.paginator import Paginator


def index(request):
    persons = Person.objects.all()[:5]
    return render(request, 'index.html', {'persons_update': persons})


@login_required
def data_input(request):
    return render(request, 'data_input.html')


def persons_listing(request):
    persons_list = Person.objects.all()
    paginator = Paginator(persons_list, 25)
    page = request.GET.get('page')
    is_new_item = request.POST.get('is_new_item')
    if is_new_item is not None and int(is_new_item) == 1:
        fill_new_line(request.POST)
    persons = paginator.get_page(page)
    return render(request,'persons_list.html', {'persons': persons})


def searching(requiest):
    searching_type = requiest.GET.get('type')
    return render(requiest, 'search.html', {'searching_type': searching_type})

