from scapy.all import *
from progress.bar import Bar
import time


class Sender():

    mtu = 2500

    def __init__(self, interface, end_pcap_callback=None, fast=False, verbose=False, time_to_wait=5):
        self.interface = interface
        self.end_pcap_callback = end_pcap_callback
        self.fast = fast
        self.verbose = verbose
        self.time_to_wait = time_to_wait

    def send(self, pcap):
        self.check_mtu()
        pkts = rdpcap(pcap)
        pkts_totali = len(pkts)
        index = 0
        print('\n' + "Inizio invio di " + pcap + '\n')
        time.sleep(self.get_time_to_wait())
        bar = Bar("Invio in corso", max=pkts_totali)
        if self.get_fast() is False:
            for pkt in pkts:
                if index == 0:
                    try:
                        sendp(pkt, iface=self.get_interface().get_interface_name(), verbose=0)
                        if self.get_verbose() is True:
                            print("\n" + "Inviato pacchetto " + str(index + 1) + "/" + str(pkts_totali) + "/n")
                    except:
                        print("\n" + "Pacchetto " + str(index + 1) + "/" + str(pkts_totali) + " saltato." + "\n")
                else:
                    delay = pkt.time - pkts[index - 1].time
                    if self.get_verbose() is True:
                        print("\n" + "Attendo " + str(delay) + "\n")
                    time.sleep(delay)
                    try:
                        sendp(pkt, iface=self.get_interface().get_interface_name(), verbose=0)
                        if self.get_verbose() is True:
                            print("\n" + "Inviato pacchetto " + str(index + 1) + "/" + str(pkts_totali) + "/n")
                    except:
                        print("\n" + "Pacchetto " + str(index + 1) + "/" + str(pkts_totali) + " saltato." + "\n")
                index += 1
                bar.next()
        else:
            for pkt in pkts:
                try:
                    sendp(pkt, iface=self.get_interface().get_interface_name(), verbose=0)
                except:
                    print("\n" + "Pacchetto " + str(index + 1) + "/" + str(pkts_totali) + " saltato." + "\n")
                index += 1
                bar.next()
        time.sleep(self.get_time_to_wait())
        bar.finish()
        print('\n' + "Inviati " + str(index) + " di " + str(pkts_totali) + " pacchetti.\n")
        return

    def check_mtu(self):
        default_mtu = self.get_interface().get_mtu()
        if(self.mtu > default_mtu):
            print("\nLa tua MTU e' " + str(default_mtu) + ". Si consiglia di portarla a 2500.\n")
        else:
            pass
        return

    def set_time_to_wait(self, time_to_wait):
        self.time_to_wait = time_to_wait

    def get_time_to_wait(self):
        return self.time_to_wait

    def set_interface(self, interface):
        self.interface = interface

    def get_interface(self):
        return self.interface

    def set_verbose(self, val):
        self.verbose = val

    def get_verbose(self):
        return self.verbose

    def set_fast(self, fast):
        self.fast = fast

    def get_fast(self):
        return self.fast
