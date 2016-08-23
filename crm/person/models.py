# coding: utf-8

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Bank(models.Model):

    title = models.CharField(verbose_name='Наименование банка', max_length=255)
    inn = models.CharField(verbose_name='ИНН', max_length=255)
    kpp = models.CharField(verbose_name='КПП', max_length=255)
    checking_account = models.CharField(verbose_name='Расчетный счет', max_length=255)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=255)

    def __str__(self):
        return '{}||{}'.format(self.title, self.checking_account)

    class Meta:
        verbose_name = u'bank'
        verbose_name_plural = u'banks'
        ordering = (u'title',)


class OrgType(models.Model):

    name = models.CharField(verbose_name='Тип организации', primary_key=True, max_length=255)
    official = models.CharField(verbose_name='Наименование типа организации', max_length=255)

    def __str__(self):
        return self.official

    class Meta:
        verbose_name = u'org type'
        verbose_name_plural = u'org types'
        ordering = (u'name',)


class Org(models.Model):

    title = models.CharField(verbose_name='Наименование организации', max_length=255)
    inn = models.CharField(verbose_name='ИНН', max_length=255)
    kpp = models.CharField(verbose_name='КПП', max_length=255)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=255)
    legal_address = models.CharField(verbose_name='Юридический адрес', max_length=255)
    actual_address = models.CharField(verbose_name='Фактический адрес', max_length=255)
    org_type = models.ForeignKey(OrgType, verbose_name='Тип организации', max_length=255)
    bank = models.ForeignKey(Bank, verbose_name='Банк', max_length=255)
    checking_account = models.CharField(verbose_name='Расчетный счет', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=255)
    email = models.EmailField(verbose_name='Эл. почта', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'org'
        verbose_name_plural = "org's"
        ordering = ('title',)


class OrgEmployee(models.Model):

    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255)
    role = models.CharField(verbose_name='Должность', max_length=255, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=255)
    email = models.EmailField(verbose_name='Эл. почта', max_length=255)
    org = models.ForeignKey(Org, verbose_name='Наименование организации')
