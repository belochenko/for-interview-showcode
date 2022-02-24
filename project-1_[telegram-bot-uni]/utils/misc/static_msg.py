import json


class Map(dict):
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.__dict__ = self


def message_loader():
    """
    Processing json dict file 'msg.json' to access from class attribute
    :return Map(messages_store):
    """
    with open('data/msg.json', encoding='utf-8') as f:
        messages_store = json.load(f)

        return Map(messages_store)


def major_loader():
    """
    Processing json dict file 'msg.json' to access from class attribute
    :return Map(major_store):
    """
    with open('data/major.json', encoding='utf-8') as f:
        major_store = json.load(f)

        return Map(major_store)


maj = major_loader()
msg = message_loader()
