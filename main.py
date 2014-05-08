'''
Created on 7 mai 2014

@author: Victor Talpaert
'''

import logging, SocketServer, robot

# parameters:
log_path = '/var/log/rebound/simple_test_server.log'  # make sure this file exists
host = '0.0.0.0'  # '0.0.0.0' means listening on every IP address
channel = 233

# All the info will be written in the same log, even when info comes from other scripts
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.debug('======== STARTING SCRIPT ===========')

class Server(SocketServer.TCPServer):
    def __init__(self, server_address, handlerClass):
        self.host = host
        self.channel = channel
        SocketServer.TCPServer.allow_reuse_address = True
        try :
            SocketServer.TCPServer.__init__(self, server_address, handlerClass)
        except IOError as details:
            logging.error('Server : socket.error : {}'.format(details))
        
        logging.info('Server : RPi library : {}'.format(robot.GPIO))
        if robot.GPIO is None :
            self.robo = robot.BaseRobot()
        else :
            self.robo = robot.Robot()


class Handler(SocketServer.BaseRequestHandler):
    # Instantiated once per connection        
    def handle(self):
        logging.info('Handler : {} is connected'.format(self.client_address))
        while True:
            self.order = self.request.recv(256).strip()
            if not self.order: break
            logging.info('Handler : Order is ##%s##' % self.order)
            self.server.robo.execute(self.order)
        self.request.close()
        logging.info('Handler : {} is disconnected'.format(self.client_address))


if __name__ == '__main__':
    print 'log can be found at ' + log_path
    logging.debug('Main : Starting server')
    sServer = Server((host, channel), Handler)
    logging.info('Main : Ready to serve on {}'.format(sServer.server_address))
    try :
        sServer.serve_forever()
    except KeyboardInterrupt as details :
        sServer.server_close()
        logging.info('Main : closing server ({})'.format(details))
    finally:
        logging.info('Main : SocketServer stopped serving')
