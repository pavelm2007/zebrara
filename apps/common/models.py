# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail

from common.utils import simple_upload_to

__all__ = [
    'Photo',
    'Pos_Act',
    'SeoModel',
]


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    title = models.CharField(u'Название', max_length=255, blank=True)
    main_image = models.BooleanField(u'Заглавное изображение', default=False)
    image = models.ImageField(u'Изображение', upload_to=simple_upload_to('image'))

    class Meta:
        verbose_name = u'Изображение'
        verbose_name_plural = u'Изображения'

    def __unicode__(self):
        if self.title:
            return '%s' % (self.title)
        else:
            return '%s - %s' % (self.pk, self.image)


    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '200x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = (u'Изображение')
    admin_thumbnail.allow_tags = True


class SeoModel(models.Model):
    head_title = models.CharField(u'Заголовок окна браузера', max_length=255, blank=True)
    meta_description = models.CharField(u'[META] Описание', max_length=255, blank=True)
    meta_keywords = models.CharField(u'[META] Ключевые слова', max_length=255, blank=True)

    class Meta:
        abstract = True


class Pos_Act(models.Model):
    position = models.SmallIntegerField(u'Позиция', default=100)
    is_active = models.BooleanField(u'Видимость', default=True)

    class Meta:
        abstract = True
        ordering = ['position', 'id']


