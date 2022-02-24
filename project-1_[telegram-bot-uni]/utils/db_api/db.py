class Ops:  # TODO

    @classmethod
    def is_user_exists(cls, phone_number=None, username=None) -> bool:
        """
        Check if user's phone number exists in DB
        :return: True if phone number exists in db and False if did not
        """
        assert phone_number is not None or username is not None

        if phone_number is not None:
            return cls.get_or_none(cls.phoneNumber == phone_number) is not None
        elif username is not None:
            return cls.get_on_none(cls.username == username) is not None

    @classmethod
    def find_by_phone_number(cls, phone_number: str):
        """
        Selects item from the DB and returns it in dict.
        """
        if cls.is_user_exists(cls, phone_number=phone_number):
            user = cls.select().where(cls.phoneNumber == phone_number).dicts()
            return user.get()
        else:
            return 'User is not exists'

    @classmethod
    def find_by_username(cls, username: str):
        """
        Selects item from the DB and returns it in dict.
        :return: dict
        """
        if cls.is_user_exists(cls, username=username):
            user = cls.select().where(cls.username == username).dicts()
            return user.get()
        else:
            return 'User is not exists'

    @classmethod
    def push_new_user(cls, user_data):
        cls.create(**user_data)
