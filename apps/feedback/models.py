# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.template import loader
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils.encoding import smart_str, smart_unicode

# Create your models here.

__all__ = [
    'Feedback',
]


class Feedback(models.Model):
    name = models.CharField(u'ваше имя', max_length=255)
    phone = models.CharField(u'Телефон', max_length=255, blank=True, null=True)
    email = models.CharField(u'E-mail', max_length=255)
    title = models.CharField(u'Тема', max_length=255, blank=True, null=True)
    comment = models.TextField(u'комментарий')
    created = models.DateTimeField(u'Отправлено', auto_now_add=True)

    class Meta:
        ordering = ('id', )
        verbose_name = u'Обратная связь'
        verbose_name_plural = u'Обратная связь'

    def __unicode__(self):
        return u'%s' % (self.name)


#@receiver(post_save, sender=Feedback)
#def FeedbackSubmit(sender, instance, **kwargs):
#    feedback = instance
#    #managers = [manager[1] for manager in settings.MANAGERS]
#    #mail_title = u'Новый отзыв - %s' % feedback.title
#    mail_message = loader.render_to_string('feedback/message.txt', {'object': feedback, })
#    #send_mail(mail_title, mail_message, settings.DEFAULT_FROM_MAIL, [managers])
#    managers = [manager[1] for manager in settings.MANAGERS]
#    subject = smart_unicode(u'Форма обратной связи ' +feedback.__unicode__())
#    send_mail(subject, mail_message, settings.DEFAULT_FROM_MAIL,managers)