import json
import http.server
import socketserver
import requests
import ast
from typing import Tuple
from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    @property
    def api_response(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            byte =post_data
            byte = byte.decode().replace("'", '"')
            bodyJson = json.loads(byte)
            print(bodyJson)
            responseCode =self.createComponent(bodyJson['project_id'])
            return responseCode
           
    def createComponent(self,project_id):
        data={"data[][attributes][layers][][reposition-tickets]":"true","data[][attributes][layers][][component-id]":"wjydnld"}
        header={'accept': 'application/json','X-PlanRadar-API-Key':'13d9f9c76c0733d30683e8b1c58717bff089e224a396a43d37874caa6a3cf7cd6c800116567b4a82b9da885a214676078192139a4d89cb711a1b604795956a9d365bd4147f753e42194c9f550277ab70'}
        component =requests.post('https://www.planradar.com/api/v1/1255753/projects/{0}/components'.format(project_id),data=data,headers=header)
        print(component.request.body)
        if component.status_code==200:
            response = json.loads(component.text)
            print(response['data'][0]['id'])
            self.createForm(response['data'][0]['id'],project_id)
            return component.status_code
        else:
            return component.status_code
        
    def createForm(self,componentId,project_id):
        header={'accept': 'application/json','Content-Type':'application/json','X-PlanRadar-API-Key':'13d9f9c76c0733d30683e8b1c58717bff089e224a396a43d37874caa6a3cf7cd6c800116567b4a82b9da885a214676078192139a4d89cb711a1b604795956a9d365bd4147f753e42194c9f550277ab70'}
        dataString='{"data":{"attributes":{"ticket-type-id":"jeplxl"}}}'
        requestJson =  ast.literal_eval(str(dataString))
        print(requestJson)
        form = requests.post("https://www.planradar.com/api/v1/1255753/projects/{0}/ticket_types_project".format(project_id),data=dataString,headers=header)
        print({form.request.body})
        if form.status_code==200:
            response = json.loads(form.text)
            print(response['data']['id'])
            self.createTicket(project_id,componentId,response['data']['id'])
        else:
            print(form.status_code)
            return form.status_code

    def createTicket(self,project_id,ComponentId,TicketId):
        data='{"data":{"attributes":{"subject":"Task","ticket-type-id":"{TicketId}","status-id":1,"component-id":"{ComponentId}","priority-id": 1,"uuid": "b2b07dcb-638e-4c20-9b6b-b55f19163b2a"}}}'
        header={'accept': 'application/json','X-PlanRadar-API-Key':'13d9f9c76c0733d30683e8b1c58717bff089e224a396a43d37874caa6a3cf7cd6c800116567b4a82b9da885a214676078192139a4d89cb711a1b604795956a9d365bd4147f753e42194c9f550277ab70'}
        Ticket =requests.post('https://www.planradar.com/api/v1/1255753/projects/{0}/tickets'.format(project_id),data=data,headers=header)
        print(Ticket.request.body)
        if Ticket.status_code==200:
            Ticket = json.loads(Ticket.text)
            print(Ticket.status_code)
            return Ticket.status_code
        else:
            print(Ticket.status_code)
            return Ticket.status_code
        
    def do_POST(self):
        if self.path == '/createTicket':
            response = self.api_response
            self.send_header("Content-Type", "application/json")
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            if response == 200:
                self.send_response(200,"Ticket Create Successfully")
                print("Ticket Create Successfully")
            else:
                self.send_response(500,"Something went wrong")
                print("someting went wrong")
                print(f"Error: {response}")


if __name__ == "__main__":
    PORT = 22
    my_server = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
    print(f"Server started at {PORT}")
    my_server.serve_forever()