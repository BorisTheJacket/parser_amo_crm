from models.lead import Lead
from api import Api 
from files import save_file_json
from models.links import LinksList
import json
import datetime
from pandas import DataFrame


list_of_dicts = []
fields_name_list = ['Осталось оплатить','Тариф','Способ оплаты','Тип оплаты', 'Статус вн. рассрочки']
list_of_statuses = ['Рассрочка Тинькофф', 'МТС (от Тинькофф)', 'Ресурс Развития']


with open('F:/python/radiator_panel/andrey_bot/database/db.json','r', encoding='utf-8') as file:
    
    all_mail_address_dict = json.load(file)
    
    for mail_list in all_mail_address_dict:
        

        api = Api()

        for mail in all_mail_address_dict[mail_list]:
            data_dict = {}

            resp = api.get_contacts_by_email(mail)
            
            if len(resp) == 0:
                print("Не нашёл e-mail: ", mail)
                continue

            for contact in resp:
                
                lead_id = api.get_contact_links(contact.get_id())
                
                if lead_id.is_empty():
                    continue 

                lead = api.get_lead(lead_id.get_first_lead_id())

                lead_custom_fields = lead.get_custom_fields()

                data_dict['Менеджер'] = lead.get_responsable()
                data_dict['Ссылка на сделку'] = lead.get_lead_url()
                data_dict['Дата заявки'] = lead.get_creation_date()
                data_dict['Дата оплаты'] = lead.get_closed_date()
                if lead_custom_fields.is_exist('Осталось оплатить'):
                    data_dict['Стоимость курса'] = lead.get_price() + lead.get_custom_fields().get_value('Осталось оплатить')
                else:
                    data_dict['Стоимость курса'] = lead.get_price()
                data_dict['Приход ДС'] = ''
                status = lead.get_custom_fields().get_value('Способ оплаты')
                status_tip_oplaty = lead.get_custom_fields().get_value('Тип оплаты')
                if status in list_of_statuses:
                    data_dict['Статус'] = 'Брокер'
                else:
                    data_dict['Статус'] = status_tip_oplaty
                if lead.get_custom_fields().is_exist('Осталось оплатить'):
                    data_dict['К доплате'] = lead.get_custom_fields().get_value('Осталось оплатить')
                else:
                    data_dict['К доплате'] = 0

                list_of_dicts.append(data_dict)

            df = DataFrame(list_of_dicts)
            df.to_excel('Отчет.xlsx', sheet_name="sheet2", index=False)


        

