
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