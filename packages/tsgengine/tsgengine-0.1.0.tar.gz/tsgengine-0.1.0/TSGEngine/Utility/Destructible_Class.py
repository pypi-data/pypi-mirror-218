import weakref


class DestructibleClass:
    _alive = {}

    def __new__(cls):
        self = super().__new__(cls)
        self.__init__()
        self.class_type = cls
        if cls not in cls._alive:
            cls._alive[cls] = []
        DestructibleClass._alive[cls].append(self)

        return weakref.proxy(self)

    def destroy(self):
        self._alive[type(self)].remove(self)

    @classmethod
    def destroy_all_alive(cls):
        for alive_id in range(len(cls._alive[cls]), 0, -1):
            cls._alive[cls][alive_id-1].destroy()

        del cls._alive[cls]
