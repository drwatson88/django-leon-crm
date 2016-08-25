# coding: utf-8

import sys
import os
import argparse


CATEGORY_SITE_IMAGE = 'upload_crm/demo/image.jpg'
PRODUCT_IMAGE = 'upload_crm/demo/image.jpg'


def args():
    parser = argparse.ArgumentParser(description='Generate test '
                                                 'objects for catalog demo')
    parser.add_argument('PROJECT_PATH', nargs='+', help='PROJECT_PATH help')
    return parser.parse_args()


def main(project_dir):
    project_dir = project_dir or u'/'.join(os.getcwd().split(u'/')[:-3])
    sys.path.append(project_dir)
    sys.path.append(os.path.join(project_dir, u'apps'))
    os.environ[u'DJANGO_SETTINGS_MODULE'] = u'settings'

    import django
    django.setup()

    from mixer.backend.django import mixer, Mixer
    from person.models import Org, OrgEmployee, Bank, OrgType
    from order.models import Order, OrderStatus

    # Create OrgType
    i = 0
    for k, v in {'client': 'Клиент',
                 'provider': 'Поставщик',
                 'seller': 'Продавец',
                 'branch': 'Филиал'}.items():
        OrgType(name=k, official=v).save()
        i += 1

    # Create Bank
    i = 0
    for bank in [('ООО "Банк1"', 'INN23452365236',
                  'KPP23452365236', '45555555555',
                  'OGRN23452365236'),
                 ('ООО "пРИБАЛТ"', 'INN234523235236',
                  'KPP2345232355236', '345325235',
                  'OGRN23451243365236')]:
        Bank(title=bank[0], inn=bank[1], kpp=bank[2],
             checking_account=bank[3], ogrn=bank[4]).save()
        i += 1

    # Create OrderStatus
    i = 0
    for status in [('go', 'go'),
                   ('last', 'last')]:
        OrderStatus(name=status[0], official=status[1]).save()
        i += 1


if __name__ == '__main__':
    args = args()
    main(args.PROJECT_PATH[0])
