from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django_webtest import WebTest

from .models import Menu, Item, Ingredient


class MenuModelTests(WebTest):
    def test_menu_creation(self):
        menu = Menu.objects.create(
            season='Summer 2018',
            expiration_date='2018-08-31'
        )
        menu.save()
        user = User.objects.create_user('temporary',
                                        'temporary@example.com',
                                        'temporary')
        item = menu.items.create(name="Ramune",
                                 description="Has a marble",
                                 chef=user)
        item.save()
        ingredient = item.ingredients.create(name='chocolate')
        ingredient.save()
        today = timezone.now().date()
        self.assertEqual(menu.season, 'Summer 2018')
        self.assertEqual(menu.created_date, today)
        self.assertEqual(menu.expiration_date, '2018-08-31')
        self.assertEqual(menu.season, str(menu))
        self.assertEqual(menu.items.get(pk=item.pk), item)
        self.assertEqual(item.name, "Ramune")
        self.assertEqual(item.description, "Has a marble")
        self.assertEqual(item.chef, user)
        self.assertEqual(item.name, str(item))
        self.assertEqual(item.ingredients.get(pk=ingredient.pk), ingredient)
        self.assertEqual(ingredient.name, "chocolate")
        self.assertEqual(ingredient.name, str(ingredient))


class MenuViewTests(WebTest):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(name="Kahlua")
        self.ingredient2 = Ingredient.objects.create(name="half-and-half")
        self.ingredient3 = Ingredient.objects.create(name="Coca-Cola")
        self.ingredient4 = Ingredient.objects.create(name="vodka")
        self.ingredient5 = Ingredient.objects.create(name="heavy cream")
        self.ingredient6 = Ingredient.objects.create(name="vermouth")
        self.user = User.objects.create_user('temporary',
                                             'temporary@example.com',
                                             'temporary')
        self.item1 = Item.objects.create(
            name="Black cow",
            description="Favorite drink of Donald Fagen",
            chef=self.user,
            standard=True
        )
        self.item1.save()
        self.item2 = Item.objects.create(
            name="White Russian",
            description="Favorite drink of the Big Lebowski",
            chef=self.user
        )
        self.item2.save()
        self.item3 = Item.objects.create(
            name="Vodka martini",
            description="Favorite drink of James Bond",
            chef=self.user
        )
        self.item3.save()
        self.item1.ingredients.add(self.ingredient1, self.ingredient2,
                                   self.ingredient3)
        self.item2.ingredients.add(self.ingredient1, self.ingredient4,
                                   self.ingredient5)
        self.item3.ingredients.add(self.ingredient4, self.ingredient6)
        self.menu1 = Menu.objects.create(
            season="Winter 2017",
            expiration_date="2018-02-28"

        )
        self.menu1.save()
        self.menu1.items.add(self.item1, self.item2)
        self.menu2 = Menu.objects.create(
            season="Spring 2018"
        )
        self.menu2.save()
        self.menu2.items.add(self.item2, self.item3)
        self.menu3 = Menu.objects.create(
            season="Summer 2016",
            expiration_date="2016-08-31"
        )
        self.menu3.save()
        self.menu3.items.add(self.item1, self.item3)

    def test_menu_list(self):
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu1.season)
        self.assertContains(resp, self.menu2.season)
        self.assertNotContains(resp, self.menu3.season)

    def test_menu_detail(self):
        resp = self.client.get(reverse('menu:menu_detail',
                                       kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, 'Winter 2017')
        self.assertContains(resp, 'Black cow')
        self.assertContains(resp, 'White Russian')
        self.assertContains(resp, 'February 28, 2018')

    def test_item_detail(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertContains(resp, 'Black cow')
        self.assertContains(resp, 'Favorite drink of Donald Fagen')
        self.assertContains(resp, 'temporary')
        self.assertContains(resp, 'This item is available year-round.')

    def test_item_detail_no_item(self):
        resp = self.client.get(reverse('menu:item_detail',
                                       kwargs={'pk': 4}))
        self.assertEqual(resp.status_code, 404)

    def test_create_new_menu_invalid(self):
        resp = self.client.post(reverse('menu:menu_new'),
                                {'created_date': date.today(),
                                 'season': '',
                                 'items': '',
                                 'expiration_date': 'tomorrow'})
        self.assertEqual(200, resp.status_code)
        self.assertFormError(resp, 'form', 'season',
                             ['This field is required.'])
        self.assertFormError(resp, 'form', 'items',
                             ['"" is not a valid value for a primary key.'])
        self.assertFormError(resp, 'form', 'expiration_date',
                             ['Enter a valid date.'])

    def test_create_new_menu_valid(self):
        form = self.app.get(reverse('menu:menu_new')).form
        form['created_date'] = date.today()
        form['season'] = 'Spring 2018'
        form['items'] = '1'
        form['expiration_date'] = '2018-05-01'
        resp = form.submit()
        new_menu = Menu.objects.last()
        self.assertRedirects(resp, new_menu.get_absolute_url())

    def test_edit_menu(self):
        form = self.app.get(reverse('menu:menu_edit', kwargs={'pk': 1})).form
        form['season'] = 'Summer 2018'
        resp = form.submit()
        edited_menu = Menu.objects.get(pk=1)
        self.assertEqual(edited_menu.season, 'Summer 2018')
        self.assertEqual(edited_menu.expiration_date.strftime("%Y-%m-%d"),
                         '2018-02-28')
        self.assertEqual(list(edited_menu.items.all()),
                         [Item.objects.get(pk=1), Item.objects.get(pk=2)])
        self.assertRedirects(resp, reverse('menu:menu_list'))
