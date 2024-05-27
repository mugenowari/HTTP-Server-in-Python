import socket
import sys
hostName = "localhost"
serverPort = 8123

def start_server(host=hostName, port=serverPort):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    # homeFile= open('index.html', 'rb')
    print(f"Servidor iniciado em {host}:{port}. Aguardando conexões...")
    
    while True:
        connection, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        
        request = (connection.recv(1024)).decode('utf-8')

        string_list = request.split(' ')     # Split request from spaces
        method = string_list[0] # First string is a method
        requesting_file = string_list[1] #Second string is request file
        
        myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here       
     
        myfile = myfile.lstrip('/')
        if(myfile == ''):
            myfile = 'index.html'    # Load index file as default

        try:
            file = open(myfile,'rb') # open file , r => read , b => byte format
            response = file.read()
            file.close()
 
            header = 'HTTP/1.1 200 OK\n'
 
            if(myfile.endswith(".jpg")):
                mimetype = 'image/jpg'
            elif(myfile.endswith(".css")):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'
 
            header += 'Content-Type: '+str(mimetype)+'\n\n'
 
        except Exception as e:
            header = ('HTTP/1.1 404 Not Found\n\n')
            response = ('''<html>
                          <body>
                            <center>
                             <h3>Error 404: File not found</h3>
                             <p>Python HTTP Server</p>
                            </center>
                          </body>
                        </html>'''.encode('utf-8'))

        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)

        print('Client request ',requesting_file)

        connection.close()
        

start_server()
