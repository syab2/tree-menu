from django import template
from menu.models import Menu, MenuItem
from django.db.models import Prefetch


register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu = Menu.objects.prefetch_related(
        Prefetch('items', queryset=MenuItem.objects.select_related('parent').order_by('id'), to_attr='prefetched_items')).get(name=menu_name)

    menu_items = menu.prefetched_items
    active_items = set()

    for item in menu_items:
        if item.get_url() == current_url:
            active_items.add(item.id)
            parent = item.parent
            while parent:
                active_items.add(parent.id)
                parent = parent.parent

    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append({
                    'item': item,
                    'children': children,
                    'is_active': item.id in active_items,
                    'has_active_child': any(child['is_active'] or child['has_active_child'] for child in children)
                })
        return tree

    menu_tree = build_tree(menu_items)
    return {
        'menu': menu,
        'menu_tree': menu_tree,
        'current_url': current_url,
        'menu_name': menu_name
    }   
