from testproject.menu.models import Menu
menu, created = Menu.objects.get_or_create(name='main_menu', slug='main_menu')