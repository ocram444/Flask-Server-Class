#Object oriented Flask server
from flask import Flask
from flask import send_from_directory #(optional) For example handler only
import os



class Server(object):
    """Server class to host requests"""
    #init the server
    def __init__(self, **configs):
        self.app = Flask(__name__)
        self.configs(**configs)
        self.num_requests = 0

    #change server configs
    def configs(self, **configs):
        for key, value in configs.items():
            self.app.config[key] = value

    #add an request to the server
    def add_request(self, request):
        self.num_requests += 1                               #increment the number of requests
        handler_wrapper = f"func{self.num_requests}"         #give the function a unique name
        setattr(self, handler_wrapper, request.handler)      #create a self.attribute that stores the handler function with the unique name
        self.app.add_url_rule(request.route, handler_wrapper, getattr(self, handler_wrapper), methods=[request.mode]) #add the request to the server
                
    #run the server
    def run(self, **kwargs):
        self.app.run(**kwargs)
    

class RequestHandler(object):
    """request class to store and handle requests"""
    #init the request
    def __init__(self, route = "/", mode = "GET", handler = None):
        self.route = route      #url of the request (/home, /controlPanel, ...)
        self.mode = mode        #mode of the request (GET, POST, PUT, DELETE)
        if handler == None:     #default handler
            self.handler = self.default_handler
        else:                   #handler function
            self.handler = handler

    #default handler function
    def default_handler(self):
        return "Default handler. Hello World!"
    

#export Server and RequestHandler classes
__all__ = ["Server", "RequestHandler"]





#example web server instance
if __name__ == "__main__":

    #example handlers
    def send_static_file():
        #static file to serve: ./index.html
        path = "./"
        filename = "index.html"
        print("Server side: serving index.html")
        return send_from_directory(path, filename)

    def test_handler():
        print("Server side: serving thest handler string")
        return "test handler"

    def post_test_handler():
        print("Server side: post test handler called")
        return "Front end: post test handler called"

    #example server
    server = Server()

    configs = {"DEBUG": False,}
    server.configs(**configs)

    action1 = RequestHandler(route="/", mode="GET", handler=test_handler)
    action2 = RequestHandler(route="/test", mode="GET", handler=send_static_file)
    action3 = RequestHandler(route="/test", mode="POST", handler=post_test_handler)
    server.add_request(action1)  # localhost:420/        ->  will return "test handler"
    server.add_request(action2)  # localhost:420/test    ->  will return the ./index.html file
    server.add_request(action3)  # localhost:420/test    ->  will print "post test handler called" to the console when a POST request is made to localhost:420/test

    server.run(host="localhost", port=420)