from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Style, Tattoo, TattooProxy


class TattooViewTest(TestCase):
    def test_get_tattoos(self):

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile(
            'test_image.gif', small_gif, content_type='image/gif')
        style = Style.objects.create(name='Style 1')
        tattoo_1 = Tattoo.objects.create(
            style=style,
            title='Tattoo 1',
            image=uploaded,
            slug='tattoo-1'
        )
        tattoo_2 = Tattoo.objects.create(
            style=style,
            title='Tattoo 2',
            image=uploaded,
            slug='tattoo-2'
        )

        response = self.client.get(reverse('gallery:tattoos'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tattoos']), 2)
        self.assertEqual(list(response.context['tattoos']), [
                         tattoo_1, tattoo_2])
        self.assertContains(response, tattoo_1)
        self.assertContains(response, tattoo_2)


class TattooDetailViewTest(TestCase):

    def test_get_tattoo_by_slug(self):
        # create a tattoo
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile(
            'test_image.gif', small_gif, content_type='image/gif')
        style = Style.objects.create(name='Style 1')
        tattoo = Tattoo.objects.create(
            style=style,
            title='Tattoo 1',
            image=uploaded,
            slug='tattoo-1'
        )

        # make a request to the tattoo detail view with the tattoo's slug
        response = self.client.get(
            reverse('gallery:tattoo-detail', args=[tattoo.slug]))

        # check that the response is successful
        self.assertEqual(response.status_code, 200)

        # check that the response contains the tattoo
        self.assertEqual(response.context['tattoo'], tattoo)
        self.assertEqual(response.context['tattoo'].slug, tattoo.slug)


class StyleListViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.style = Style.objects.create(
            name='Test Style', slug='test-style')
        self.tattoo = TattooProxy.objects.create(
            title='Test Tattoo',
            style=self.style,
            slug='test-tattoo',
            image=uploaded
        )

    def test_status_code(self):
        response = self.client.get(
            reverse('gallery:style-list', args=[self.style.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('gallery:style-list', args=[self.style.slug]))
        self.assertTemplateUsed(response, 'gallery/style_list.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('gallery:style-list', args=[self.style.slug]))
        self.assertEqual(response.context['style'], self.style)
        self.assertEqual(response.context['tattoos'][0], self.tattoo)
