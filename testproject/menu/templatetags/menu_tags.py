from django import template # type: ignore
from menu.models import Menu, MenuItem
from django.db.models import Prefetch # type: ignore


register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu = Menu.objects.prefetch_related(
        Prefetch('items', queryset=MenuItem.objects.select_related('parent').order_by('id'), to_attr='prefetched_items')).get(name=menu_name)

    menu_items = menu.prefetched_items
    active_items = set()
    active_item_parents = set() 
    
    for item in menu_items:
        if f'/menu/{item.get_url()}/' == current_url:
            active_items.add(item.id)
            parent = item.parent
            while parent:
                active_item_parents.add(parent.id)
                parent = parent.parent

    def build_tree(items, parent=None, level=0):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item, level+1)
                is_active = item.id in active_items
                tree.append({
                    'item': item,
                    'children': children,
                    'is_active': is_active,
                    'has_active_child': any(
                        child['is_active'] or child['has_active_child'] 
                        for child in children
                    ),
                    'level': level,
                    'should_expand': (is_active or item.id in active_item_parents or any(child['is_active'] for child in children))})
        return tree

    menu_tree = build_tree(menu_items)
    return {
        'menu': menu,
        'menu_tree': menu_tree,
        'current_url': current_url,
        'menu_name': menu_name
    }   
