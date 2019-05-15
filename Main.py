from Sniffer import Sniffer
from Sender import Sender
from AttackerCalc import AttackerCalc
from FeaturesCalc import FeaturesCalc
from PacketFilter import PacketFilter
from MTADownloader import MTADownloader
from CSV import CSV
from Network import Network
from Iface import Iface
from scapy.all import *
import time
import os, signal, sys
import gym
import gym_DRLMal


def callback_sniffer(*args, **kwargs):
    pkt = args[0]
    featuresCalc = kwargs.get("features_calc")
    list_of_packets = kwargs.get("packets")
    csv = kwargs.get('csv_obj')
    filter_1 = kwargs.get("filter")[0]
    filter_2 = kwargs.get("filter")[1]
    if((filter_2.check_packet_filter(pkt) or filter_1.check_packet_filter(pkt)) is True):
        list_of_packets.append(pkt)
    if(len(list_of_packets) >= featuresCalc.get_min_window_size()):
        features = featuresCalc.compute_features(list_of_packets)
        csv.add_row(features)
        list_of_packets.clear()
    else:
        pass
    pass

mta = MTADownloader()
if(mta.check_if_file_with_links_exists() is False):
    mta.get_links_for_download_pcaps()
reader = open("pcaps_link.txt", "r")
f = reader.readlines()
mta.download_pcap([f[0]])
'''
ENV_NAME = 'DRLMal-v0'
env = gym.make(ENV_NAME)
attacker = AttackerCalc(pcap="good.pcap")
#ip_to_consider = ['10.0.2.15']#attacker.compute_attacker()
ip_to_ignore = env.get_network().get_all_ips()
flow_type = "legitimate"
filter_1 = PacketFilter(ip_whitelist_filter=[], ip_blacklist_filter=ip_to_ignore, IPv4=True, TCP=True, UDP=False)
filter_2 = PacketFilter(ip_whitelist_filter=[], ip_blacklist_filter=ip_to_ignore, IPv4=True, TCP=False, UDP=True)
iface_sender = Iface("mal-eth0")
iface_sniffer = Iface("s0-eth2")
iface_sender.set_mtu(2500)
iface_sniffer.set_mtu(2500)
featuresCalc = FeaturesCalc(flow_type=flow_type, min_window_size=10)
csv = CSV(file_name="features_" + flow_type, folder_name="Features")
csv_2 = CSV(file_name="features_legitimate_1", folder_name="Features")
csv_2.open_csv()
print (csv_2.get_number_of_rows())
csv_2.read_row(0)

csv.create_empty_csv()
csv.add_row(featuresCalc.get_features_name())
argument = {"features_calc": featuresCalc, "packets": [], 'filter': [filter_1, filter_2], 'csv_obj': csv}

sniffer = Sniffer(iface_sniffer, callback_prn=callback_sniffer, callback_prn_kwargs=argument)
sniffer.start()
while(sniffer.get_started_flag() is False):
    pass
sender = Sender(iface_sender, fast=True, verbose=False, time_to_wait=10)
sender.send('good.pcap')
sniffer.stop()
csv.close_csv()
'''