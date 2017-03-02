# coding: utf-8


class ListExtraConverter(object):

    def _convert_extra(self):
        self.extra['subtype'] = self.list_develop_extra['subtype']
        self.extra['filter'] = {
            'header': self.list_unit_extra['filter']['header'],
            'groups': [
                {
                    'items': group['items'],
                    'col_sizes': group['col_sizes']
                } for group in self.list_develop_extra['filter']['groups']
            ],
            'buttons': self.list_unit_extra['filter']['buttons']
        }


list_unit_extra = {
    'filter': {
        'header': 'Поиск',
        'buttons': [
            {
                'css_class': 'search',
                'href': '#',
                'title': 'Поиск'
            }
        ]
    }
}
