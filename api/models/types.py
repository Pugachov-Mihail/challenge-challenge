import sqlalchemy.types as types


class Choise(types.TypeDecorator):
    impl = types.String

    def __init__(self, choise, **kwargs):
        self.choise: dict = choise
        super(Choise, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        return [v for k, v in self.choise.items() if value == k][0]

    def process_result_value(self, value, dialect):
        return [v for k, v in self.choise.items() if value == v][0]
