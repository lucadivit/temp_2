from Sniffer import Sniffer
from Sender import Sender
from AttackerCalc import AttackerCalc
from FeaturesCalc import FeaturesCalc
from PacketFilter import PacketFilter
from MTADownloader import MTADownloader
from NeuralNetwork import NeuralNetwork
from LegitimateDownloader import LegitimateDownloader
from Agent import Agent
from CSV import CSV
from Network import Network
from Iface import Iface
from scapy.all import *
from callback import callback_sniffer
import time
import os, signal, sys
import gym
import gym_DRLMal

#Malware download send and train function definition
def malware_train(line):
    global malware_train_nb
    if(mta.check_if_link_is_in_downloaded_file(line) is False):
        pcap_file_name = mta.download_pcap([line])
        for pcap in pcap_file_name:
            if(pcap is not None):
                if(check_if_already_trained(pcap) is False):
                    attacker = AttackerCalc(pcap=mta.get_folder_name() + "/" + pcap)
                    ip_to_consider = attacker.compute_attacker()
                    flow_type = "malware"
                    filter_1.set_ip_whitelist_filter(ip_to_consider)
                    filter_2.set_ip_whitelist_filter(ip_to_consider)
                    filter_3.set_ip_whitelist_filter(ip_to_consider)
                    featuresCalc = FeaturesCalc(flow_type=flow_type, min_window_size=5)
                    csv = CSV(file_name="features_" + flow_type, folder_name="Features")
                    csv.create_empty_csv()
                    csv.add_row(featuresCalc.get_features_name())
                    argument = {"features_calc": featuresCalc, "packets": [], 'filter': [filter_1, filter_2, filter_3],
                                'csv_obj': csv}
                    sniffer = Sniffer(iface_sniffer, callback_prn=callback_sniffer, callback_prn_kwargs=argument)
                    sniffer.start()
                    while (sniffer.get_started_flag() is False):
                        pass
                    try:
                        sender = Sender(iface_sender, fast=False, verbose=False, time_to_wait=10)
                        sender.send(mta.get_folder_name() + "/" + pcap)
                        sniffer.stop()
                    except Exception as e:
                        print(e)
                    csv.close_csv()
                    env.set_csv(csv.get_folder_name() + "/" + csv.get_current_file_name())
                    agent.train_agent(steps=csv.get_number_of_rows() - 1, log_interval=csv.get_number_of_rows() - 1,
                                      verbose=2, nb_max_episode_steps=csv.get_number_of_rows() - 1)
                    malware_train_nb -= 1
                    trained_file.write(pcap + "\n")
                else:
                    print("\nPcap gia' utilizzato in passato. Saltato.\n")
            else:
                pass
    else:
        pass


#Legitimate send and train function definition
def legitimate_train(line):
    global legitimate_train_nb
    if(check_if_already_trained(line) is False):
        flow_type = "legitimate"
        filter_1.set_ip_whitelist_filter([])
        filter_2.set_ip_whitelist_filter([])
        filter_3.set_ip_whitelist_filter([])
        featuresCalc = FeaturesCalc(flow_type=flow_type, min_window_size=5)
        csv = CSV(file_name="features_" + flow_type, folder_name="Features")
        csv.create_empty_csv()
        csv.add_row(featuresCalc.get_features_name())
        argument = {"features_calc": featuresCalc, "packets": [], 'filter': [filter_1, filter_2, filter_3],
                    'csv_obj': csv}
        sniffer = Sniffer(iface_sniffer, callback_prn=callback_sniffer, callback_prn_kwargs=argument)
        sniffer.start()
        while (sniffer.get_started_flag() is False):
            pass
        try:
            sender = Sender(iface_sender, fast=False, verbose=False, time_to_wait=10)
            sender.send(lg.get_folder_name() + "/" + line)
            sniffer.stop()
        except Exception as e:
            print (e)
        csv.close_csv()
        env.set_csv(csv.get_folder_name() + "/" + csv.get_current_file_name())
        agent.train_agent(steps=csv.get_number_of_rows() - 1, log_interval=csv.get_number_of_rows() - 1,
                          verbose=2, nb_max_episode_steps=csv.get_number_of_rows() - 1)
        legitimate_train_nb -= 1
        trained_file.write(line + "\n")
    else:
        print("\nPcap gia' utilizzato in passato. Saltato.\n")



def check_if_already_trained(name):
    lines = trained_file_reader.readlines()
    trovato = False
    if(name.endswith("\n") is True):
        name.replace("\n", "")
    for line in lines:
        if (line.endswith("\n") is True):
            line = line.replace("\n", "")
        if(line == name):
            trovato=True
            break
    return trovato

times_to_train = 1
malware_train_nb = times_to_train
legitimate_train_nb = times_to_train

trained_file = open("trained.txt", "a+")
trained_file_reader = open("trained.txt", "r")

#Env, Agent and NN definition
ENV_NAME = 'DRLMal-v0'
env = gym.make(ENV_NAME)
nn = NeuralNetwork(input_shape=(1,) + env.observation_space.shape, output_dim=env.get_action_space().n)
model = nn.create_default_mlp_network()
agent = Agent(env=env, model=model, num_actions=env.get_action_space().n, batch_size=2)
agent.create_default_dqn_agent(nb_steps_warmup=5)

#Sender and Sniffer iface definition
ip_to_ignore = env.get_network().get_all_ips()
iface_sender = Iface("mal-eth0")
iface_sniffer = Iface("s0-eth2")
iface_sender.set_mtu(2500)
iface_sniffer.set_mtu(2500)

#Filters for pkts definition
filter_1 = PacketFilter(ip_whitelist_filter=[], ip_blacklist_filter=ip_to_ignore, IPv4=True, TCP=True,
                        UDP=False)
filter_2 = PacketFilter(ip_whitelist_filter=[], ip_blacklist_filter=ip_to_ignore, IPv4=True, TCP=False,
                        UDP=True)
filter_3 = PacketFilter(ip_whitelist_filter=[], ip_blacklist_filter=ip_to_ignore, IPv4=True, TCP=False,
                        UDP=False)

mta = MTADownloader()
lg = LegitimateDownloader()

if(mta.check_if_file_with_links_exists() is False):
    mta.get_links_for_download_pcaps()
mal_reader = open(mta.get_link_to_pcaps_file_name(), "r")
leg_reader = open(lg.get_file_name(), "r")
mal_file = mal_reader.readlines()
leg_file = leg_reader.readlines()

max_nb_of_pcaps = max(len(leg_file), len(mal_file))

for i in range(0, max_nb_of_pcaps):

    try:
        line_mal = mal_file[i]
        if(line_mal.endswith("\n") is True):
            line_mal = line_mal.replace("\n", "")
    except Exception as e:
        line_mal = None
        print(e)

    if(malware_train_nb > 0 and line_mal is not None):
        malware_train(line_mal)
    else:
        line_mal = None

    try:
        line_leg = leg_file[i]
        if(line_leg.endswith("\n") is True):
            line_leg = line_leg.replace("\n", "")
    except Exception as e:
        line_leg = None
        print(e)

    if(legitimate_train_nb > 0 and line_leg is not None):
        legitimate_train(line_leg)
    else:
        line_leg = None

    if((legitimate_train_nb <=0 and malware_train_nb <=0) or (line_leg is None and line_mal is None)):
        print ("\nAddestramento Completato\n")
        break