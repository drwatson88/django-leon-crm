# coding: utf-8


# create_unit_extra = {
#     'header': {
#         'create': 'Добавление',
#         'update': 'Просмотр/Редактирование',
#         'delete': 'Удаление'
#     },
#     'master': {
#         'main_buttons': [
#             {
#                 'key': 'back',
#                 'href': '#',
#                 'title': 'Назад'
#             },
#             {
#                 'key': 'save',
#                 'href': '#',
#                 'title': 'Сохранить'
#             }
#         ],
#         'slave_buttons': {}
#     }
# }


create_unit_extra = {
    'master': {
        'header': 'Добавление',
        'main_buttons': {
            'items': [
                {
                    'key': 'back',
                    'css_class': 'back',
                    'href': '#',
                    'title': 'Назад'
                },
                {
                    'key': 'save',
                    'css_class': 'save',
                    'href': '#',
                    'title': 'Сохранить'
                }],
        },
        'slave_buttons': {
            'meta': {
                'title': 'Добавить'
            }
        }
    },
    'slave': {
        'header': 'Добавление',
        'main_buttons': {
            'meta': {
                'title': 'Добавить',
                'key': 'add',
                'css_class': 'add'
            }
        }
    }
}
