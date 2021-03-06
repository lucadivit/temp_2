from mininet.net import Mininet
from mininet.node import Controller, Node
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.clean import Cleanup
import os

class Network():

    def __init__(self, ip_net="192.0.2.0/24"):

        self.ip_net = ip_net
        self.network = None
        self.host_mal = None
        self.host_leg = None
        self.switch = None
        self.controller = None
        self.gateway = None

    def create_default_network(self):
        self.set_mininet_network(Mininet(controller=Controller, ipBase=self.get_ip_net()))
        self.get_mininet_network().addController('c0')
        # Il flag "inNamespace=False" non crea un namespace per l'interfaccia di rete dell'host che di solito viene fatto di default.
        # Questo permette di vedere l'interfaccia anche dalla Main shell e non solo da quella dell'host stesso.
        self.set_host_mal(self.get_mininet_network().addHost('mal', inNamespace=False))
        self.set_host_leg(self.get_mininet_network().addHost('leg', inNamespace=False))
        self.set_switch(self.get_mininet_network().addSwitch('s0'))
        self.set_gateway(self.get_mininet_network().addNAT('n0'))
        self.get_gateway().configDefault()
        self.get_mininet_network().addLink(self.get_host_mal(), self.get_switch())
        self.get_mininet_network().addLink(self.get_host_leg(), self.get_switch())
        self.get_mininet_network().addLink(self.get_switch(), self.get_gateway())


    def get_all_ips(self):
        ips = []
        for node in self.get_mininet_network().keys():
            ip = self.get_mininet_network().getNodeByName(node).IP()
            if(ip in ips):
                pass
            else:
                ips.append(ip)
        return ips

    def get_host_interface(self, host):
        return host.defaultIntf()

    def start_network(self):
        self.get_mininet_network().start()

    def stop_network(self):
        self.get_mininet_network().stop()

    def clean_network(self):
        c = Cleanup()
        c.cleanup()

    def cli_network(self):
        CLI(self.get_network())

    def set_gateway(self, gateway):
        self.gateway = gateway

    def get_gateway(self):
        return self.gateway

    def set_controller(self, controller):
        self.controller = controller

    def get_controller(self):
        return self.controller

    def set_switch(self, switch):
        self.switch = switch

    def get_switch(self):
        return self.switch

    def set_host_mal(self, host):
        self.host_mal = host

    def get_host_mal(self):
        return self.host_mal

    def set_host_leg(self, host):
        self.host_leg = host

    def get_host_leg(self):
        return self.host_leg

    def set_ip_net(self, ip_net):
        self.ip_net = ip_net

    def get_ip_net(self):
        return self.ip_net

    def set_mininet_network(self, network):
        self.network = network

    def get_mininet_network(self):
        return self.network