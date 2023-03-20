
class Contact():

    def __init__(self, json_data) -> None:
        self.json_data = json_data

    def get_account_id(self):
        return self.json_data['account_id']

    def __repr__(self):
        return f'name: {self.json_data[""]} КРАСАВЧИК'

    def get_id(self):
        return self.json_data['id']