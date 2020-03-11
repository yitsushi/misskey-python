class Singleton(type):
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._inst[cls]


class Permissions(metaclass=Singleton):
    __permissions = [
        "read:account",
        'read:blocks',
        'read:drive',
        'read:favorites',
        'read:following',
        'read:messaging',
        'read:mutes',
        'read:notifications',
        'read:reactions',
        'read:pages',
        'read:page-likes',
        'read:user-groups',

        'write:blocks',
        'write:drive',
        'write:favorites',
        'write:following',
        'write:messaging',
        'write:mutes',
        'write:notes',
        'write:notifications',
        'write:reactions',
        'write:pages',
        'write:page-likes',
        'write:user-groups',
        'write:votes',
        "write:account",
    ]

    def is_valid(self, value):
        return value in self.__permissions

    def all(self):
        return self.__permissions

    def all_read(self):
        return [x for x in self.__permissions if x.startswith('read:')]

    def all_write(self):
        return [x for x in self.__permissions if x.startswith('write:')]
