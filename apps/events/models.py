# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.db.models import permalink, Q
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete

from model_utils.managers import PassThroughManager
from sorl.thumbnail import ImageField
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail.shortcuts import get_thumbnail

from common.models import Pos_Act
from common.utils import simple_upload_to


# Create your models here.

__all__ = [
    'Event',
    'EventMedia',
]


class PostQuerySet(QuerySet):
    def live(self):
        return self.filter(status=self.model.LIVE_STATUS).filter(published__lte=datetime.now())


class Event(Pos_Act, models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, u'Опубликовано'),
        (DRAFT_STATUS, u'В работе'),
        (HIDDEN_STATUS, u'Скрыто'),
    )

    title = models.CharField(u'Заголовок', max_length=255)
    slug = models.SlugField(editable=True, unique=True)
    published = models.DateTimeField(u'Дата публикации', default=datetime.now())
    short_text = models.TextField(u'Анонс', blank=True, null=True)
    text = models.TextField(u'Текст')
    image = models.ImageField(u'Главное фото', upload_to=simple_upload_to('image'), blank=True, null=True)
    status = models.IntegerField(u'Статус', choices=STATUS_CHOICES, default=LIVE_STATUS)

    objects = models.Manager()
    object_filter = PassThroughManager.for_queryset_class(PostQuerySet)()

    class Meta:
        ordering = ('position', '-published', 'title', )
        verbose_name = u'Событие'
        verbose_name_plural = u'События'

    def __unicode__(self):
        return u'%s' % (self.title)

    @permalink
    def get_absolute_url(self):
        return ('events:detail', (), {'slug': self.slug, })

    def get_images(self):
        return self.event_media.filter(is_active=True)

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '200x100', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = (u'Главное фото')
    admin_thumbnail.allow_tags = True


class EventMedia(Pos_Act, models.Model):
    event = models.ForeignKey(Event, related_name='event_media', verbose_name=u'Новость')
    title = models.CharField(u'Заголовок', max_length=30, blank=True, null=True)
    image = ImageField(u'Изображение', upload_to="event/", blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ('position',)
        verbose_name = u'Фото'
        verbose_name_plural = u'Фото'

# copy main image into the product object
# this signal is disabled during the import process
@receiver(post_save, sender=EventMedia)
def event_image(sender, instance, **kwargs):
    if bool(instance.image) is False:
        instance.delete()
        return False

    if instance.is_main:
        # removing is_main flag from all images
        for event_image in instance.event.event_media.all():
            if event_image.pk != instance.pk:
                event_image.is_main = False
                event_image.save()

        # making this image as main
        instance.event.image = instance.image
        instance.event.save()
    else:
        if instance.event.event_media.count() == 1:
            instance.is_main = True
            # call this signal again
            instance.save()


@receiver(post_delete, sender=EventMedia)
def event_image_delete(sender, instance, **kwargs):
    if instance.is_main:
        try:
            event = instance.event
        except Event.DoesNotExist:
            return False

        if event.event_media.exclude(image=None).count() > 0:
            event_image = event.event_media.exclude(image=None).all()[0]
            event_image.is_main = True
            event_image.save()
        else:
            event.image = None
            event.save()
