from django.db.models import Q
from django.http import JsonResponse


def get_tree_items(item, query_set, dict_filter):
    item_queryset_result = query_set.objects.none()
    if item != None:
        item_queryset = query_set.objects.filter(pk=item.id)

        item_queryset_result |= item_queryset
        if len(item_queryset) != 0 and item_queryset[0].get_parent is not None:
            while item_queryset:
                above_item = query_set.objects.filter(
                    Q(pk=item_queryset[0].get_parent.id)).exclude(**dict_filter)
                item_queryset_result |= above_item
                item_queryset = above_item
    return item_queryset_result


def get_items(request, query_set, data_dict):
    if request.is_ajax():
        term = request.POST.get('term')
        parent_id = request.POST.get('parent_id')
        print('term is %s' % term.encode('utf-8'))
        print('parent_id is %s' % parent_id)
        if term is not None:
            keys_list = list(data_dict.keys())
            data_dict[keys_list[0]] = parent_id
            data_dict[keys_list[1]] = term
            regions = query_set.objects.all().filter(**data_dict)
            response_content = list(regions.values())
            return JsonResponse(response_content, safe=False)


def add_item(request, query_set, data_dict):
    id = -1
    id_parent = None
    if request.method == 'POST':
        keys_list = list(data_dict.keys())
        d = request.POST.dict()
        if "" != d['parent_item']:
            id_parent = d['parent_item']
        parent_item = query_set.objects.all().filter(id=id_parent).first()
        data_dict[keys_list[0]] = parent_item
        data_dict[keys_list[1]] = d['text']
        region = query_set.objects.create(**data_dict)
        region.save()
        id = region.id
        print(id)
        print(type(id))
    return JsonResponse({'result': True, 'id': id}, safe=False)


def get_data_by_name(request, table_name):
    if request.is_ajax():
        term = request.POST.get('term')
        print('the term is  %s' % term.encode('utf-8'))
        if term is not None:
            result = table_name.objects.all().filter(
                name__icontains=term
            )
            response_content = list(result.values())
            return JsonResponse(response_content, safe=False)


def add_data_with_name(request, table_name):
    d = -1
    if request.method == 'POST':
        d = request.POST.dict()
        item = table_name.objects.create(name=d['text'])
        item.save()
        print('the new id of calling team is %s' % item.id)
        id = item.id
    return JsonResponse({'result': True, 'id': id}, safe=False)


def delete_objects_from_formset(formset):
    for item in formset.deleted_objects:
        item.delete()


def save_formset_with_person(formset, person):
    formset_items = formset.save(commit=False)
    for item in formset_items:
        item.person = person
        item.save()
    delete_objects_from_formset(formset)
    formset.save_m2m()


def from_queryset_to_str(queryset):
    str_result = ''
    for item in queryset.order_by('level'):
        if item.get_parent is not None:
            str_result += ' ' + item.get_parent.name
    return str_result
