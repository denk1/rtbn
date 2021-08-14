from django.db.models import Q
from django.http import JsonResponse


def get_tree_items(item, query_set):
    item_queryset_result = query_set.objects.none()
    if item != None:
        item_queryset = query_set.objects.filter(pk=item.id)

        item_queryset_result |= item_queryset
        if len(item_queryset) != 0 and item_queryset[0].get_parent is not None:
            while item_queryset:
                above_item = query_set.objects.filter(
                    Q(pk=item_queryset[0].get_parent.id)).exclude(above_war_unit=None)
                item_queryset_result |= above_item
                item_queryset = above_item
    return item_queryset_result


def get_items(request, query_set, data_dict):
    if request.is_ajax():
        term = request.POST.get('term')
        parent_id = request.POST.get('parent_id')
        print('term is %s' % term)
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
