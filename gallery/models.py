import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    """
    Generate a random alphanumeric string.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Style(models.Model):
    """
    A model representing a tattoo style.
    """
    name = models.CharField("Название", max_length=250, db_index=True)
    slug = models.SlugField("URL", max_length=250,
                            unique=True, null=False, editable=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        """
        Meta information for the Style model.
        """
        ordering = ('name',)
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Save the current instance to the database.
        """

        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        return super(Style, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery:style-list', args=[str(self.slug)])


class Tattoo(models.Model):
    """
    A model representing a tattoo.
    """
    style = models.ForeignKey(
        Style, on_delete=models.CASCADE, related_name='tattoos')
    title = models.CharField("Название", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", max_length=250)
    image = models.ImageField(
        "Изображение", upload_to='tattoos/tattoos/%Y/%m/%d')
    # tags = models.ManyToManyField('Tag', blank=True, related_name='tattoos')
    available = models.BooleanField("Доступно", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        # ordering = ('name',)
        verbose_name = 'Тату'
        verbose_name_plural = 'Тату'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery:tattoo-detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        return super(Tattoo, self).save(*args, **kwargs)


class TattooManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of tattoo objects filtered by availability.
        """
        return super(TattooManager, self).get_queryset().filter(available=True)


class TattooProxy(Tattoo):

    objects = models.Manager()

    class Meta:
        proxy = True
        verbose_name = 'Тату'
        verbose_name_plural = 'Тату'
