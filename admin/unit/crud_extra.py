# coding: utf-8


class CrudExtraConverter(object):

    def _convert_extra(self):
        self.extra['master_form'] = {
            'header_pfx': self.unit_extra['master']['header_pfx'],
            'groups': [
                {
                    'items': group['items'],
                    'col_sizes': group['col_sizes'],
                    'slave_buttons': [
                        {
                            'title': self.unit_extra['master']['slave_buttons']['title'],
                            'css_class': group['items'][-1]
                        }
                    ] if group['slave_button'] else []
                } for group in self.develop_extra['master']['groups']
            ],
            'buttons': self.unit_extra['master']['main_buttons']
        }
        self.extra['subtype'] = self.develop_extra['subtype']

        self.extra['slave_form_s'] = [
            {
                'field': slave['field'],
                'header_pfx': self.unit_extra['slave']['header_pfx'],
                'groups': [
                    {
                        'items': group['items'],
                        'col_sizes': group['col_sizes'],
                        'slave_buttons': []
                    } for group in slave['groups']
                ],
                'buttons': [{
                    'title': button['title'],
                    'css_class': button['css_class'],
                    'href': slave['button']['href']
                            } for button in self.unit_extra['slave']['main_buttons']]
            } for slave in self.develop_extra['slave_s']
        ]


create_unit_extra = {
    'master': {
        'header_pfx': 'Добавление',
        'main_buttons': [
            {
                'css_class': 'back',
                'href': '#',
                'title': 'Назад'
            },
            {
                'css_class': 'save',
                'href': '#',
                'title': 'Сохранить'
            }
        ],
        'slave_buttons': {
            'title': 'Добавить'
        }
    },
    'slave': {
        'header_pfx': 'Добавление',
        'main_buttons': [
            {
                'css_class': 'add',
                'title': 'Добавить'
            }
        ]
    }
}