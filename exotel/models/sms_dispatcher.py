import requests
from xml.etree import ElementTree


class SMSDispatcher():
    BASE_INSPECTION_URL = "https://%s:%s@twilix.exotel.in"

    class Meta:
        app_label = 'exotel'

    def __init__(self,from_number,api_token):
        # TODO validate from_number
        self.from_number = from_number
        self.api_token = api_token
        self.exotel_POST_url = api_token.get_url()

    def send_one(self,to_number,body_text):
        payload = {"From":self.from_number,"To":to_number,"Body":body_text}
        response = requests.post(self.exotel_POST_url, data=payload)
        return self.get_message_from_response(response)

    def get_message_from_response(self,response):
        xml_response_message = response.text
        tree = ElementTree.fromstring(xml_response_message)
        message = ""
        if tree[0].tag == "RestException":
            message = "Sent Failed, RestException %s: %s" %(tree.find('.//Status').text,tree.find('.//Message').text)
        else:
            status = tree.find('.//Status').text
            to = tree.find('.//To').text
            url = tree.find('.//Uri').text
            inspection_url = self.BASE_INSPECTION_URL %(self.api_token.sid,self.api_token.token) + url
            message = "SMS request posted to Exotel. %s to %s. More info: %s" %(status,to, inspection_url)
        return message
