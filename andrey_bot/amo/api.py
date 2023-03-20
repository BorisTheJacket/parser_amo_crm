import requests
from amo.models.lead import Lead
from amo.models.contact import Contact
from amo.models.links import LinksList

class Api():
    URL = 'https://infohylsru.amocrm.ru/' 
    session = None

    def __init__(self):
        payload = {
            "USER_LOGIN": "oldrowdy666@gmail.com",
            "USER_HASH": "07e15843a72f773c146cb58a0f43717b59eadabf"
        }

        session = requests.session()
        session.post(self.URL + 'private/api/auth.php', data=payload)
        
        self.session = session
            
    def get_lead(self, lead_id): # Если ответ 204 - скорее всего у контакта нет сделки.
        resp = self.session.get(f'{self.URL}/api/v4/leads/{lead_id}')
        if resp.status_code != 200:
            if resp.status_code == 204:
                print(f'{lead_id} нет сделки')
            else:
                print(resp.status_code)
                raise Exception('Попытка загрузить поля пользователя завершилось с ошибкой')
        else:
            print(resp.status_code)    
            return Lead(resp.json())



    def get_companies(self):
        resp = self.session.get(f'{self.URL}/api/v4/companies', params={})
        if resp.status_code == 200:    
            return resp.json()
        return None

    def get_contacts_by_email(self, e_mail):
        resp = self.session.get(f'{self.URL}/api/v4/contacts', params={'query': e_mail})
        if resp.status_code == 204:
            return []
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception('Вызов API завершился с ошибкой')
        
        json_response = resp.json()

        list_of_contacts  = [Contact(x) for x in json_response['_embedded']['contacts']]
        return list_of_contacts

    def get_lead_by_account_id(self, id):
        resp = self.session.get(f'{self.URL}/api/v4/leads', params={'filetr[account_id]': id})
        if resp.status_code != 200:
            raise Exception('Вызов API завершился с ошибкой')
        return resp.json()        
    
    def get_contact_links(self, id):
        resp = self.session.get(f'{self.URL}/api/v4/contacts/{id}/links')
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception('Вызов API завершился с ошибкой')
        return LinksList(resp.json())
    

    def get_lead_fields_by_id(self):
        resp = self.session.get(f'{self.URL}api/v4/leads/custom_fields')    
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception('Попытка загрузить поля пользователя завершилось с ошибкой')
        return resp.json()

    def get_user_by_id(self, id):
        resp = self.session.get(f'{self.URL}/api/v4/users/{id}')
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception('Попытка загрузить пользователя по ID завершилось с ошибкой')
        return(resp.json())
    

    

    