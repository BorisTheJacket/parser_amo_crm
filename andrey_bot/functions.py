import datetime



def milisec_to_date(milisec):
    return datetime.datetime.fromtimestamp(milisec).strftime("%d.%b.%Y")

def serchig_through_field_list(field_list, item):
    for element in field_list:
        if element['field_name'] == item:
            if element['values'][0]['value'].isdigit():
                return int(element['values'][0]['value'])
            else:
                return element['values'][0]['value']