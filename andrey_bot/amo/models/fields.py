class Field():

    def __init__(self, json_data):
        self.json_data = json_data

    def value(self):
        custom_field_value = self.json_data['values'][0]['value']
        field_type = self.json_data['field_type']
        if field_type == 'numeric':
            return int(custom_field_value)
        elif field_type == 'date':
            return int(custom_field_value)
        elif field_type == 'select':
            return str(custom_field_value)
        else:
            return custom_field_value
        
class CustomFields():

    def __init__(self, json_data):
        self.fields_dict = {i['field_name']: Field(i) for i in json_data}

    def is_exist(self, name):
        return name in self.fields_dict.keys()

    def get_value(self, name):
        return self.fields_dict[name].value()