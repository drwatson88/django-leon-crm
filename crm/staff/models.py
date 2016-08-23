# coding: utf-8

from django.db import models


class Role(models.Model):

    name = models.CharField(verbose_name='Роль', max_length=255, primary_key=True)
    official = models.CharField(verbose_name='Наименование роли', max_length=255)


class Rights(models.Model):

    name = models.CharField(verbose_name='Контроллер раздела',
                            max_length=255, primary_key=True)
    official = models.CharField(verbose_name='Наименование контроллера раздела',
                                max_length=255)


class RightsGroup(models.Model):

    name = models.CharField(verbose_name='Группа прав', max_length=255,
                            primary_key=True)
    official = models.CharField(verbose_name='Наименование группы прав',
                                max_length=255)
    rights = models.ManyToManyField(Rights, verbose_name='Доступные контроллеры разделов')


class StaffGroup(models.Model):

    name = models.CharField(verbose_name='Группа сотрудников', max_length=255,
                            primary_key=True)
    official = models.CharField(verbose_name='Наименование типа группы сотрудников',
                                max_length=255)
    rights_group = models.ManyToManyField(RightsGroup, verbose_name='Группа прав')


class Staff(models.Model):

    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=255)
    email = models.EmailField(verbose_name='Эл. почта', max_length=255)
    staff_group = models.ManyToManyField(StaffGroup, verbose_name='Группа сотрудников')
