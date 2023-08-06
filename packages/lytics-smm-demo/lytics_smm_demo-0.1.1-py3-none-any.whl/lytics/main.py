import requests
import json

api_url = "https://lytics.lol/api/v2"

class Lytics:
    def __init__(self, api_key):
        self.api_key = api_key

    
    def services(self):
        payload = {
            'key': self.api_key,
            'action': 'services'
        }
        try:
            resp = requests.post(api_url, json=payload)
            clean_json = json.dumps(resp.json(), indent=4, ensure_ascii=False)
            return clean_json
        
        except Exception as e:
            raise Exception(str(e))    
        

    def balance(self):
        payload = {
            'key': self.api_key,
            'action': 'balance'
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))    
        

    def order(self, service_id, **kwargs):
        payload = {
            'key': self.api_key,
            'action': 'add',
            'service': service_id,
        }
        try:
            payload.update(kwargs)
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))


    def status(self, order_id):
        payload = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))    
 

    def multi_status(self, order_ids: list):
        payload = {
            'key': self.api_key,
            'action': 'status',
            'orders': ",".join(str(x) for x in order_ids)
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))    


    def refill(self, order_id):
        payload = {
            'key': self.api_key,
            'action': 'refill',
            'order': order_id 
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))


    def multi_refill(self, order_ids):
        payload = {
            'key': self.api_key,
            'action': 'refill',
            'orders': ",".join(str(x) for x in order_ids) 
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))


    def refill_status(self, refill_id):
        payload = {
            'key': self.api_key,
            'action': 'refill_status',
            'order': refill_id
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))


    def multi_refill_status(self, refill_ids):
        payload = {
            'key': self.api_key,
            'action': 'refill_status',
            'order': ",".join(str(x) for x in refill_ids) 
        }
        try:
            resp = requests.post(api_url, json=payload)
            return resp.json()
        
        except Exception as e:
            raise Exception(str(e))