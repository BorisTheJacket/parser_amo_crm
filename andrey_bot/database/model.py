EMAILS_KEY = 'current_emails'

class State():
    def __init__(self, user_id, data={}) -> None:
        self.user_id = user_id 
        self.data = data

    def add_email(self, email: str, contact_id: str, lead_id: str):
        if EMAILS_KEY not in self.data:
            self.data[EMAILS_KEY] = {}
        self.data[EMAILS_KEY][email] = {
            'contact_id': contact_id,
            'lead_id': lead_id
        }
    
    def all_emails(self):
        return self.data[EMAILS_KEY]

        