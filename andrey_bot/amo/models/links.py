
class LinksList():

    def __init__(self, links):
        self.links = links

    def get_leads(self):
        leads = []
        for link in self.links:
            if link['to_entity_type'] == 'leads':
                leads.append(link)
        return leads

    def get_leads_ids(self):
        leads_ids = []
        for link in self.get_leads():
            leads_ids.append(link['to_entity_id'])
        return leads_ids
    
    def len(self):
        return len(self.links)
    
    def get_first_lead_id(self):
        result = None
        try:
            result = self.links['_embedded']['links'][0]['to_entity_id']
        finally:
            return result

    def is_empty(self):
        return len(self.links['_embedded']['links']) == 0

