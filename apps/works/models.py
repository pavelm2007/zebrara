# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext as _

from sorl.thumbnail.fields import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from model_utils.managers import PassThroughManager
from mptt.models import MPTTModel, TreeForeignKey
from flatpages.models import FlatPage

from common.models import Pos_Act
from common.utils import simple_upload_to


__all__ = [
    'Service',
    'Work',
    'WorkMedia',
    'Example',
    'ExampleMedia',

]


class MixinQuerySet(QuerySet):
    def active_list(self):
        return self.filter(is_active=True)


class Service(MPTTModel, Pos_Act):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Услуга')
    name = models.CharField(u'Название', max_length=255)
    short_text = models.TextField(u'Короткий текст', blank=True)
    text = models.TextField(u'Описание', blank=True)
    price = models.ForeignKey(FlatPage, blank=True, null=True)
    image = ImageField(u'Логотип', upload_to=simple_upload_to('image', 'service_logo'), blank=True)

    class Meta:
        ordering = ['tree_id', 'lft']
        #ordering = ['position', 'name', ]
        verbose_name = u'Услуга'
        verbose_name_plural = u'Услуги'

    objects = models.Manager()
    filters = PassThroughManager.for_queryset_class(MixinQuerySet)()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_example_list_url(self):
        return ('works:example_service_list', (), {'pk': self.pk, })

    def has_example(self):
        qs = self.work_set.filter(is_active=True).filter(is_example=True)
        if qs:
            return True
        return False

        #@models.permalink
    #def get_absolute_url(self):
    #    return

    def thumbnail(self, width=264, height=64):
        if self.image:
            thumbnail = get_thumbnail(self.image, str(width) + 'x' + str(height))
            img_resize_url = unicode(thumbnail.url)
            html = '<a style="height:%spx; display:block" class="image-picker" href="%s">' \
                   '<img src="%s" alt="%s" width="%s" height="%s" />' \
                   '</a>'
            return html % (height, self.image.url, img_resize_url, self.name, thumbnail.width, thumbnail.height)

        return '<img src="http://placehold.it/264x64" alt="False">'

    thumbnail.short_description = u'Лого раздела'
    thumbnail.allow_tags = True


class Work(Pos_Act, models.Model):
    service = models.ForeignKey(Service, verbose_name=u'Услуга')
    name = models.CharField(u'Название', max_length=255, blank=True)
    short_text = models.CharField(u'Короткое описание', max_length=50, blank=True)
    text = models.TextField(u'Описание', blank=True)
    image = ImageField(u'Изображение', blank=True, upload_to=simple_upload_to('image', path='works'))
    date = models.DateField(u'Дата реализации проекта', blank=True, null=True)
    is_work = models.BooleanField(u'Публиковать в работах', default=True)
    is_example = models.BooleanField(u'Публиковать в примерах', default=False)

    objects = models.Manager()
    filters = PassThroughManager.for_queryset_class(MixinQuerySet)()

    class Meta:
        ordering = ['position', '-id', 'name', 'date', ]
        verbose_name = u'Работа'
        verbose_name_plural = u'Работы'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('works:work_detail', (), {'pk': self.pk, })

    def thumbnail(self, width=64, height=64):
        if self.image:
            thumbnail = get_thumbnail(self.image, str(width) + 'x' + str(height))
            img_resize_url = unicode(thumbnail.url)
            html = '<a style="height:%spx; display:block" class="image-picker" href="%s">' \
                   '<img src="%s" alt="%s" width="%s" height="%s" />' \
                   '</a>'
            return html % (height, self.image.url, img_resize_url, self.name, thumbnail.width, thumbnail.height)

        return '<img src="http://placehold.it/64x64" alt="False">'

    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True


class Example(Pos_Act, models.Model):
    service = models.ForeignKey(Service, verbose_name=u'Услуга')
    name = models.CharField(u'Название', max_length=255, blank=True)
    text = models.TextField(u'Описание', blank=True)
    image = ImageField(u'Изображение', blank=True, upload_to=simple_upload_to('image', path='service_example'))
    date = models.DateField(u'Дата реализации проекта', blank=True, null=True)

    objects = models.Manager()
    filters = PassThroughManager.for_queryset_class(MixinQuerySet)()

    class Meta:
        ordering = ['position', 'name', 'date', ]
        verbose_name = u'Пример'
        verbose_name_plural = u'Примеры'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('works:example_detail', (), {'pk': self.pk, })

    def get_images(self):
        return self.example_media.filter(is_active=True)


class WorkMedia(Pos_Act, models.Model):
    work = models.ForeignKey(Work, related_name='work_media', verbose_name=u'Работа')
    title = models.CharField(u'Заголовок', max_length=30, blank=True, null=True)
    image = ImageField(u'Изображение', upload_to="work_media/", blank=True)
    is_main = models.BooleanField(default=False)

    object = models.Manager()
    filters = PassThroughManager.for_queryset_class(MixinQuerySet)()

    class Meta:
        ordering = ('position',)
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

# copy main image into the product object
# this signal is disabled during the import process
@receiver(post_save, sender=WorkMedia)
def work_image(sender, instance, **kwargs):
    if bool(instance.image) is False:
        instance.delete()
        return False

    if instance.is_main:
        # removing is_main flag from all images
        for work_image in instance.work.work_media.all():
            if work_image.pk != instance.pk:
                work_image.is_main = False
                work_image.save()

        # making this image as main
        instance.work.image = instance.image
        instance.work.save()
    else:
        if instance.work.work_media.count() == 1:
            instance.is_main = True
            # call this signal again
            instance.save()


@receiver(post_delete, sender=WorkMedia)
def work_image_delete(sender, instance, **kwargs):
    if instance.is_main:
        try:
            work = instance.work
        except Work.DoesNotExist:
            return False

        if work.work_media.exclude(image=None).count() > 0:
            work_image = work.work_media.exclude(image=None).all()[0]
            work_image.is_main = True
            work_image.save()
        else:
            work.image = None
            work.save()


class ExampleMedia(Pos_Act, models.Model):
    example = models.ForeignKey(Example, related_name='example_media', verbose_name=u'Пример')
    title = models.CharField(u'Заголовок', max_length=30, blank=True, null=True)
    image = ImageField(u'Изображение', upload_to="example_media/", blank=True)
    is_main = models.BooleanField(default=False)

    object = models.Manager()
    filters = PassThroughManager.for_queryset_class(MixinQuerySet)()

    class Meta:
        ordering = ('position',)
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

# copy main image into the product object
# this signal is disabled during the import process
@receiver(post_save, sender=ExampleMedia)
def example_image(sender, instance, **kwargs):
    if bool(instance.image) is False:
        instance.delete()
        return False

    if instance.is_main:
        # removing is_main flag from all images
        for example_image in instance.example.example_media.all():
            if example_image.pk != instance.pk:
                example_image.is_main = False
                example_image.save()

        # making this image as main
        instance.example.image = instance.image
        instance.example.save()
    else:
        if instance.example.example_media.count() == 1:
            instance.is_main = True
            # call this signal again
            instance.save()


@receiver(post_delete, sender=ExampleMedia)
def example_image_delete(sender, instance, **kwargs):
    if instance.is_main:
        try:
            example = instance.example
        except Example.DoesNotExist:
            return False

        if example.example_media.exclude(image=None).count() > 0:
            example_image = example.example_media.exclude(image=None).all()[0]
            example_image.is_main = True
            example_image.save()
        else:
            example.image = None
            example.save()
