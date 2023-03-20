import json
import datetime
from amo.models.fields import CustomFields





class Lead():
    def __init__(self, json_data):
        self.json_data = json_data

    def __repr__(self):
        return f'name: {self.json_data["name"]}'

    def get_responsable(self):
        return self.json_data['responsible_user_id']
    
    def get_price(self):
        return self.json_data['price']
    
    def get_lead_url(self):
        return f'https://infohylsru.amocrm.ru/leads/detail/{self.json_data["id"]}'

    def _sec_to_date(self, item):
        return datetime.datetime.fromtimestamp(item).strftime("%d.%b.%Y")
    
    def get_creation_date(self):
        return self._sec_to_date(self.json_data['created_at'])
    
    def get_closed_date(self):
        return self._sec_to_date(self.json_data['closed_at'])
    
    def get_custom_fields(self):
        return CustomFields(self.json_data['custom_fields_values'])
    
    
