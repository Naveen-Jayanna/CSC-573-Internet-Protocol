import socket
import time
import struct

EXP_TIME = 30 # time in seconds to collect packets

class Protocols:
    ICMP = 1
    TCP = 6
    IPV4 = 8
    UDP = 17
    DNS_PORT = 53
    HTTP_PORT = 80
    HTTPS_PORT = 443
    QUIC_PORT1 = 80
    QUIC_PORT2 = 443

def collect_samples(sampling_time):
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    current_time = time.time()
    packet_list = []
    while time.time() < current_time + sampling_time:
        pkt, addr = conn.recvfrom(65535)
        packet_list.append(pkt)
    return packet_list

def ethernet_hdr(data):
    dest_mac, src_mac, protocol = struct.unpack("! 6s 6s H", data[:14])
    return socket.htons(protocol), data[14:]

def ipv4_hdr(data):
    version_hdr_len = data[0]
    header_len = (version_hdr_len & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return proto, data[header_len:]

def tcp_hdr(data):
    src_port, dest_port, sequence, ack, offset_resvd_flgs = struct.unpack('! H H L L H', data[:14])
    offset = (offset_resvd_flgs >> 12) * 4
    return src_port, dest_port, data[offset:]

def udp_hdr(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, data[8:]

def dump_results(results):
    with open('sniffer_njayann.csv', 'w') as f:
        f.write('protocol,count\n')
        for k,v in results.items():
            f.write(k + ','+ str(v) +'\n')
        f.close()   
            
def main():
    packet_list = collect_samples(EXP_TIME) # time to collect packets in secs

    #create list of protocols
    protocols = ('ip', 'tcp', 'udp', 'dns', 'icmp', 'http', 'https', 'quic')

    #create the dictionary
    results = dict.fromkeys(protocols)

    for proto in results:
        results[proto] = 0

    for p in packet_list:
        protocol, data = ethernet_hdr(p)

        if protocol == Protocols.IPV4: 
            ip_proto, ip_data = ipv4_hdr(data)
            results['ip'] += 1
        
            if ip_proto == Protocols.ICMP:
                results['icmp'] += 1
                
            if ip_proto == Protocols.TCP:   
                results['tcp'] += 1
                src, dst, tcp_data = tcp_hdr(ip_data)

                if len(tcp_data) > 0:
                    if (src == Protocols.HTTP_PORT or dst == Protocols.HTTP_PORT): 
                        results['http'] += 1

                    if (src == Protocols.HTTPS_PORT or dst == Protocols.HTTPS_PORT):  
                        results['https'] += 1
                            
            if ip_proto == Protocols.UDP:
                results['udp'] += 1
                src, dst, udp_data = udp_hdr(ip_data)

                if len(udp_data) > 0:
                    if (src == Protocols.DNS_PORT or dst == Protocols.DNS_PORT):   
                        results['dns'] += 1

                    if (src == Protocols.QUIC_PORT1 or dst == Protocols.QUIC_PORT1):  
                        results['quic'] += 1
                    
                    if (src == Protocols.QUIC_PORT2 or dst == Protocols.QUIC_PORT2):  
                        results['quic'] += 1

    dump_results(results)

if __name__ == "__main__":
    main()
