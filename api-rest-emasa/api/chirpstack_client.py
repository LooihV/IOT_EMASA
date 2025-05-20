import requests

#Consumo de la api de chirpstack applications, gateways, device-profile, devices device activation, update users

class ChirpstackApiClient:
    def __init__(self, base_url, jwt_token):
        self.base_url = base_url.rstrip('/')
        self.headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
    }
        
        
    def handle_response(self, response):
        if response.ok:
            return response.json()
        else: raise Exception(f"[{response.status_code}]{response.text}")
        
        
    def register_gateway(self,gateway_data):
        url = f"{self.base_url}/api/gateways"
        return self.handle_response(requests.post(url,json={"gateway":gateway_data},headers=self.headers))
    
    
    def list_gateway(self,tenant_id=None,limit=100):
        url = f"{self.base_url}/api/gateways?limit={limit}"
        if tenant_id:
            url += f"&tenant_id={tenant_id}"
        return self.handle_response(requests.get(url,headers=self.headers))
    
    
    def update_gateway(self, gateway_id,gateway_data):
        url = f"{self.base_url}/api/gateways/{gateway_id}"
        return self.handle_response(requests.put(url,json={"gateway":gateway_data},headers=self.headers))
    
        
    def delete_gateway(self, gateway_id):
        url = f"{self.base_url}/api/gateways/{gateway_id}"
        return self.handle_response(requests.delete(url,headers=self.headers))

    
    def create_device_profile(self, profile_data):
        url = f"{self.base_url}/api/device-profiles"
        return self.handle_response(requests.post(url,json={"deviceProfile":profile_data},headers=self.headers))
    
    
    def update_device_profile(self, profile_id,profile_data):
        url = f"{self.base_url}/api/device-profiles/{profile_id}"
        return self.handle_response(requests.put(url,json={"deviceProfile":profile_data},headers=self.headers))
    
    
    def delete_device_profile(self, profile_id):
        url = f"{self.base_url}/api/device-profiles/{profile_id}"
        return self.handle_response(requests.delete(url,headers=self.headers))
    
    
    def list_devpro_algorit(self):
        url = f"{self.base_url}/api/device-profiles/adr-algorithms"
        return self.handle_response(requests.get(url,headers=self.headers))
    
    
    def create_application(self,application_data):
        url = f"{self.base_url}/api/applications"
        return self.handle_response(requests.post(url,json={"application":application_data},headers=self.headers))
    
    
    def list_application(self, tenant_id=None, limit=100, offset=0, search=""):
        url = f"{self.base_url}/api/applications?limit={limit}&offset={offset}&search={search}"
        if tenant_id:
            url += f"&tenant_id={tenant_id}"
        return self.handle_response(requests.get(url,headers=self.headers))
    
    
    def update_application(self, application_id,application_data):
        url = f"{self.base_url}/api/applications/{application_id}"
        return self.handle_response(requests.put(url,json={"application":application_data},headers=self.headers))
    
    
    def delete_application(self, application_id):
        url = f"{self.base_url}/api/applications/{application_id}"
        return self.handle_response(requests.delete(url,headers=self.headers))
    
    
    def create_mqqt_certificate(self, application_id):
        url = f"{self.base_url}/api/applications/{application_id}/integrations/mqtt/certificate"
        return self.handle_response(requests.post(url,headers=self.headers))
    
    
    def create_device(self,device_data):
        url = f"{self.base_url}/api/devices"
        return self.handle_response(requests.post(url,json={"device":device_data},headers=self.headers))
    
    
    def get_device(self,dev_eui):
        url = f"{self.base_url}/api/devices/{dev_eui}"
        return self.handle_response(requests.get(url,headers=self.headers))
    
    
    def update_device(self, dev_eui,device_data):
        url = f"{self.base_url}/api/devices/{dev_eui}"
        return self.handle_response(requests.put(url,json={"device":device_data},headers=self.headers))
    
    
    def delete_device(self, dev_eui):
        url = f"{self.base_url}/api/devices/{dev_eui}"
        return self.handle_response(requests.delete(url,headers=self.headers))
    
    
    def activate_device(self, dev_eui, activation_data):
        url = f"{self.base_url}/api/devices/{dev_eui}/activate"
        return self.handle_response(requests.post(url, json={"deviceActivation": activation_data}, headers=self.headers))

    
    def get_device_activation(self, dev_eui):
        url = f"{self.base_url}/api/devices/{dev_eui}/activation"
        return self.handle_response(requests.get(url,headers=self.headers))
    
    
    def update_user(self, user_id, user_data):
        url = f"{self.base_url}/api/users/{user_id}"
        return self.handle_response(requests.put(url,json={"user":user_data},headers=self.headers))