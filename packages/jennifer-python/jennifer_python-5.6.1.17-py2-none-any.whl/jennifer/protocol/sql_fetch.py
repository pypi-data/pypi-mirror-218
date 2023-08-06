from .profile_data import PiData


class PiSqlFetch(PiData):
    def __init__(self, o, count):
        PiData.__init__(self, o)

        self.type = PiData.TYPE_SQL_FETCH
        self.end_time = 0
        self.end_cpu = 0
        self.count = count

    def get_type(self):
        return self.type
