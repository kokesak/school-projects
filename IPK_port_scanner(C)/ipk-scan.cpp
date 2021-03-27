#include <sys/types.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <errno.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <net/ethernet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <pcap.h>
#include <string.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <signal.h>
//#include <sys/types.h>
#include <time.h>
#include <ctype.h>
#include <netinet/ip_icmp.h>
#include <netdb.h>
#include <vector>

//#define __BYTE_ORDER __BIG_ENDIAN


// exit code 5 = wrong ip adress/domain name
// exit code 4 = wrong arguments syntax
// exit code 3 = port number out of range
// exit code 2 = no interface found
// exit code 1 = socket error, filter compile error, sending error


pcap_t *handle;
bool resend = false;

using namespace std;

struct pseudohdr {
    u_int32_t src_addr;
    u_int32_t dst_addr;
    u_int8_t padding;
    u_int8_t proto;
    u_int16_t length;
};

struct data_4_checksum {
    struct pseudohdr pshd;
    struct tcphdr tcphdr;
    char payload[1024];
};

struct data_4_checksum_UDP {
    struct pseudohdr pshd;
    struct udphdr udphdr;
    char payload[1024];
};


// Vypocet checksum
// Kod prevzat z:
// https://stackoverflow.com/questions/14088274/raw-socket-linux-send-receive-a-packet
// Datum: 30.12.2012
unsigned short comp_chksum(unsigned short *addr, int len) {
    long sum = 0;

    while (len > 1) {
        sum += *(addr++);
        len -= 2;
    }

    if (len > 0)
        sum += *addr;

    while (sum >> 16)
        sum = ((sum & 0xffff) + (sum >> 16));

    sum = ~sum;

    return ((u_short) sum);

}
//

void alarm_handler(int sig)
{
    pcap_breakloop(handle);
    //printf("Packet havent arrived in time \n");
    resend = true;
}


void tcp_handler(u_char *args, const struct pcap_pkthdr* header, const u_char* packet) 
{

    struct ether_header *eptr;
    eptr = (struct ether_header *) packet;
    struct iphdr *ip_packet_recv = (struct iphdr *)(packet + sizeof(struct ether_header));
    struct tcphdr *tcp_packet_recv = (struct tcphdr *)(packet + sizeof(struct ether_header) + (ip_packet_recv->ihl*4));


    if(tcp_packet_recv->ack == 1 && tcp_packet_recv->syn == 1){
        printf("%d/tcp\t open \n",ntohs(tcp_packet_recv->source));
        return;
    }
    else if (tcp_packet_recv->ack == 1 && tcp_packet_recv->rst == 1) {
        printf("%d/tcp\t closed \n",ntohs(tcp_packet_recv->source));
        return;
    }
    else{
        printf("Unexpected combination of flags recieved, Port %d TCP\n", ntohs(tcp_packet_recv->source));
        return;
    }
    return;
}

void udp_handler(u_char *args, const struct pcap_pkthdr* header, const u_char* packet) 
{

    struct ether_header *eptr;
    eptr = (struct ether_header *) packet;
    struct iphdr *ip_packet_recv = (struct iphdr *)(packet + sizeof(struct ether_header));
    struct icmp *icmp_packet_recv = (struct icmp *)(packet + sizeof(struct ether_header) + (ip_packet_recv->ihl*4));
    struct udphdr *udp_packet_recv = (struct udphdr *)(packet + sizeof(struct ether_header) + (ip_packet_recv->ihl*4) + sizeof(struct icmp));

    //printf("ICMP CODE %d \n", icmp_packet_recv->icmp_code);
    if(icmp_packet_recv->icmp_code == 3){
        printf("%d/udp\t closed \n", ntohs(udp_packet_recv->dest));
    }
    else{
        printf("Unexpected code recieved, Port %d UDP \n", ntohs(udp_packet_recv->dest));
    }

    return;
}

int main(int argc, char *argv[]) {

    srand(time(0));
    int sock, bytes, on = 1;
    char buffer[1024];

    struct iphdr *ip;
    struct tcphdr *tcp;
    struct udphdr *udp;
    struct sockaddr_in to;
    struct pseudohdr pseudoheader;
    struct data_4_checksum tcp_chk_construct;
    struct data_4_checksum_UDP udp_chk_construct;

    bool tcp_enable,udp_enable = false;

    // nahrazeni -pt a -pu paramteru za jendopismene -t a -u pro funkci getopt
    for(int i = 1; i < argc; i++){
        if (strcmp(argv[i], "-pt") == 0){
            strcpy(argv[i], "-t");
            tcp_enable = true;
        }
        else if(strcmp(argv[i], "-pu") == 0){   
            strcpy(argv[i], "-u");
            udp_enable = true; 
        }

        
    }

    if(tcp_enable == false && udp_enable == false){
        cerr << "-pt or -pu not set" << endl;
        exit(4);
    }

    char ip_destination[50];
    int adr_index;
    // zjisteni mista, kde se nachazi argument pro ip adresu / domenove jmeno
    for(int i = 1; i < argc; i++){
        
        if ((argv[i][0]) == '-'){
            i++;

        }
        else
        {
           strcpy(ip_destination, argv[i]);
           adr_index = i;
           break;
        }  
    }

    int opt;
    bool interface_enable = false;
    char interface_name[40];
    vector<int> tcp_array;
    vector<int> udp_array;
    while ((opt = getopt(argc,argv,"i:t:u:")) != EOF)
        switch(opt)
        {
            case 'i': 
                interface_enable = true; 

                strcpy(interface_name, optarg);
                break;
            case 't': 
            {
                int i = 0;
                int letter_start = 0;
                bool dash_found = false;
                bool last_number = false;
                int dash_index;
                while(optarg[i] != '\0'){
                    if(optarg[i] == ',' || optarg[i+1] == '\0'){
                        if (optarg[i+1] == '\0')
                            last_number = true;
                        if(!dash_found){
                            char number[5] = "";
                            int pos = 0;
                            if(!last_number){
                                for(int k = letter_start; k < i; k++){
                                number[pos] = optarg[k];
                                pos++; 
                                }
                            }
                            else{
                                for(int k = letter_start; k <= i; k++){
                                number[pos] = optarg[k];
                                pos++; 
                                }
                        }
                        //cout << atoi(number) << " number\n"; 
                        if(atoi(number) < 1 || atoi(number) > 65535){
                            cerr << "Port number out of range" << endl;
                            exit(3);
                        }
                        tcp_array.push_back(atoi(number));
                        letter_start = i+1;
                        }
                        else if(dash_found){
                            char number_start[5] = "";
                            char number_end[5] = "";
                            int pos = 0;
                            if(!last_number){
                                for(int k = letter_start; k < dash_index; k++){
                                number_start[pos] = optarg[k];
                                pos++; 
                                }
                                pos = 0;
                                for(int k = dash_index + 1; k < i; k++){
                                number_end[pos] = optarg[k];
                                pos++; 
                                }
                            }
                            else{
                                for(int k = letter_start; k < dash_index; k++){
                                number_start[pos] = optarg[k];
                                pos++; 
                                }
                                pos = 0;
                                for(int k = dash_index + 1; k <= i; k++){
                                number_end[pos] = optarg[k];
                                pos++; 
                                }
                        }
                        //cout << atoi(number) << " number\n";
                        for(int j = atoi(number_start); j <= atoi(number_end); j++){
                            if(j < 1 || j > 65535){
                                cerr << "Port number out of range" << endl;
                                exit(3);
                            }
                            tcp_array.push_back(j);
                        } 
                        dash_found = false;
                        letter_start = i+1;
                        }
                    }
                    else if(optarg[i] == '-'){
                        if(dash_found){
                            cerr << "Error while parsing arguments" << endl;
                            exit(4);
                        }
                        dash_found = true;
                        dash_index = i;
                    }
                    i++;
                }

                /*for(int i = 0; i<5; i++){
                    tcp_array.push_back(i);
                }*/
                /*for(int i = 0; i<tcp_array.size(); i++){
                    printf("%d \n", tcp_array[i]);
                }*/
                break;
            }
            case 'u': 
            {
                int i = 0;
                int letter_start = 0;
                bool dash_found = false;
                bool last_number = false;
                int dash_index;
                while(optarg[i] != '\0'){
                    if(optarg[i] == ',' || optarg[i+1] == '\0'){
                        if (optarg[i+1] == '\0')
                            last_number = true;
                        if(!dash_found){
                            char number[5] = "";
                            int pos = 0;
                            if(!last_number){
                                for(int k = letter_start; k < i; k++){
                                number[pos] = optarg[k];
                                pos++; 
                                }
                            }
                            else{
                                for(int k = letter_start; k <= i; k++){
                                number[pos] = optarg[k];
                                pos++; 
                                }
                        }
                        //cout << atoi(number) << " number\n"; 
                        if(atoi(number) < 1 || atoi(number) > 65535){
                            cerr << "Port number out of range" << endl;
                            exit(3);
                        }
                        udp_array.push_back(atoi(number));
                        letter_start = i+1;
                        }
                        else if(dash_found){
                            char number_start[5] = "";
                            char number_end[5] = "";
                            int pos = 0;
                            if(!last_number){
                                for(int k = letter_start; k < dash_index; k++){
                                number_start[pos] = optarg[k];
                                pos++; 
                                }
                                pos = 0;
                                for(int k = dash_index + 1; k < i; k++){
                                number_end[pos] = optarg[k];
                                pos++; 
                                }
                            }
                            else{
                                for(int k = letter_start; k < dash_index; k++){
                                number_start[pos] = optarg[k];
                                pos++; 
                                }
                                pos = 0;
                                for(int k = dash_index + 1; k <= i; k++){
                                number_end[pos] = optarg[k];
                                pos++; 
                                }
                        }
                        //cout << atoi(number) << " number\n";
                        for(int j = atoi(number_start); j <= atoi(number_end); j++){
                            if(j < 1 || j > 65535){
                                cerr << "Port number out of range" << endl;
                                exit(3);
                            }
                            udp_array.push_back(j);
                        } 
                        dash_found = false;
                        letter_start = i+1;
                        }
                    }
                    else if(optarg[i] == '-'){
                        if(dash_found){
                            cerr << "Error while parsing arguments" << endl;
                            exit(4);
                        }
                        dash_found = true;
                        dash_index = i;
                    }
                    i++;
                }

                break;
            }
            case '?': printf("unknown value %d\n",optopt); break;
            default:  break;
        }

    

    
    

    pcap_if_t *alldevsp;
    char *error_buffer;

    
    if(pcap_findalldevs(&alldevsp, error_buffer))
    {
        cerr << "Error while finding interface" << endl;
        exit(2);
    }

    if(interface_enable){
        while(alldevsp != nullptr){
            if(strcmp(alldevsp->name, interface_name) == 0){
                break;
            }
            else{
                alldevsp = alldevsp->next;
            }
        }
        
        if (alldevsp == nullptr) {
            cerr << "Error while finding interface" << endl;
            exit(2);
        }
    }
    else{
        while(alldevsp != nullptr){
            //alldevsp->flags == 55
            if(strcmp(alldevsp->name, "lo") == 0){
                alldevsp = alldevsp->next;
            }
            else{
                break;
            }
            
        }
        
        if (alldevsp == nullptr) {
            cerr << "Error while finding interface" << endl;
            exit(2);
        }
    }

    struct hostent *dst_host_addr = gethostbyname(ip_destination);
    if(dst_host_addr == nullptr){
        cerr << "Error while translating given destination address " << endl;
        exit(5);
    }
    struct in_addr dst_addr_in;
    dst_addr_in.s_addr = *(u_long *) (dst_host_addr->h_addr_list[0]);
    strcpy(ip_destination, inet_ntoa(dst_addr_in));
    printf("Interesting ports on %s (%s)\n", argv[adr_index], ip_destination);
    printf("PORT \t STATE \n");
    

    const u_char *packet;
    struct pcap_pkthdr packet_header;
    int packet_count_limit = 1;
    int timeout_limit = 50; /* In milliseconds */



    handle = pcap_open_live(
            alldevsp->name,
            BUFSIZ,
            packet_count_limit,
            timeout_limit,
            error_buffer
    );

    if(handle == NULL){
        cerr << "Handle error"<< endl;
        exit(99);
    }

    

    // ziskani ip adresy interfaceu
    // ziskani destination ip adresy
    // Kod prevzat z:
    // https://www.binarytides.com/c-program-to-get-ip-address-from-interface-name-on-linux/
    // Datum: 17.03.2012
    // Autor: Silver Moon
    int fd;
	struct ifreq ifr;
	
	fd = socket(AF_INET, SOCK_DGRAM, 0);

	//Type of address to retrieve - IPv4 IP address
	ifr.ifr_addr.sa_family = AF_INET;

	//Copy the interface name in the ifreq structure
	strncpy(ifr.ifr_name , alldevsp->name , IFNAMSIZ-1);

	ioctl(fd, SIOCGIFADDR, &ifr);

	close(fd);
    char *ip_int_adr = inet_ntoa(( (struct sockaddr_in *)&ifr.ifr_addr )->sin_addr);
    //



    if(tcp_enable){
        sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
        if (sock == -1) {
            cerr << "error while creating socket()" << endl;
            exit(1);
        }

        if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) == -1) {
            cerr << "error during setsockopt()" << endl;
            exit(1);
        }


        // Naplneni hlavicky ip, tcp
        // Cast kodu prevzata z:
        // https://stackoverflow.com/questions/14088274/raw-socket-linux-send-receive-a-packet
        // Datum: 30.12.2012
        ip = (struct iphdr*) buffer;
        tcp = (struct tcphdr*) (buffer + sizeof(struct iphdr));

        int iphdrlen = sizeof(struct iphdr);
        int tcphdrlen = sizeof(struct tcphdr);
        int datalen = 0;

        ip->frag_off = 0;
        ip->version = 4;
        ip->ihl = 5;
        ip->tot_len = htons(iphdrlen + tcphdrlen);
        ip->id = 0;
        ip->ttl = 40;
        ip->protocol = IPPROTO_TCP;
        ip->saddr = inet_addr(ip_int_adr);
        ip->daddr = inet_addr(ip_destination);
        ip->check = 0;

        tcp->source     = htons(43345);
        tcp->doff       = 5;
        tcp->ack_seq    = 0;
        tcp->ack        = 0;
        tcp->psh        = 0;
        tcp->rst        = 0;
        tcp->urg        = 0;
        tcp->syn        = 1;
        tcp->fin        = 0;
        tcp->window     = htons(65535);
        tcp->check      = 0;

        pseudoheader.src_addr = ip->saddr;
        pseudoheader.dst_addr = ip->daddr;
        pseudoheader.padding = 0;
        pseudoheader.proto = ip->protocol;
        pseudoheader.length = htons(tcphdrlen + datalen);

        tcp_chk_construct.pshd = pseudoheader;



        //tcp->check = (checksum >> 8) | (checksum << 8);

        to.sin_addr.s_addr = ip->daddr;
        to.sin_family = AF_INET;


        struct bpf_program fcode;
        bpf_u_int32 NetMask;
        //char filter[]="src 216.58.201.100";

        
        char filter[] = "tcp and dst port 43345 and src ";
        // pridani ip_destination na konec filter stringu
        strcat(filter, ip_destination);


        if(pcap_compile(handle, &fcode, filter, 1, NetMask) < 0){
            cerr << "error while compiling filter" << endl;
            exit(1);
        }
        
        //set the filter
        if(pcap_setfilter(handle, &fcode) < 0){
            cerr << "error while setting filter" << endl;
            exit(1);
        }

        for(int packet_number = 0; packet_number < tcp_array.size(); packet_number++){

            tcp->dest       = htons(tcp_array[packet_number]);
            tcp->seq        = htons(rand() % 65535);
            tcp->check      = 0;

            tcp_chk_construct.tcphdr = *tcp;

            unsigned short checksum = comp_chksum((unsigned short*) &tcp_chk_construct, sizeof(struct pseudohdr) + tcphdrlen + datalen);

            tcp->check = comp_chksum((unsigned short*) &tcp_chk_construct,
                sizeof(struct pseudohdr) + tcphdrlen + datalen);

            to.sin_port = tcp->dest;

            bytes = sendto(sock, buffer, ntohs(ip->tot_len), 0, (struct sockaddr*) &to, sizeof(to));
            if (bytes == -1) {
                cerr << "packet not sent, function sendto()" << endl;
                exit(1);
            }
            alarm(2);
            signal(SIGALRM, alarm_handler);
            pcap_loop(handle, 1, tcp_handler, NULL);
            // reset alarmu
            alarm(0);
            
            if(resend){
                tcp->dest       = htons(tcp_array[packet_number]);
                tcp->seq        = htons(rand() % 65535);
                tcp->check      = 0;

                tcp_chk_construct.tcphdr = *tcp;

                tcp->check = comp_chksum((unsigned short*) &tcp_chk_construct,
                        sizeof(struct pseudohdr) + tcphdrlen + datalen);
                to.sin_port = tcp->dest;


                bytes = sendto(sock, buffer, ntohs(ip->tot_len), 0, (struct sockaddr*) &to, sizeof(to));

                if (bytes == -1) {
                    cerr << "packet not sent, function sendto()" << endl;
                    exit(1);
                }
                alarm(2);
                signal(SIGALRM, alarm_handler);

                pcap_loop(handle, 1, tcp_handler, NULL);
                alarm(0);
                resend = false;
                printf("%d/tcp\t filtered \n",ntohs(tcp->dest));

            }
        }

        close(sock);
    }

    if(udp_enable){

        sock = socket(AF_INET, SOCK_RAW, IPPROTO_UDP);
        if (sock == -1) {
            cerr << "error while creating socket()" << endl;
            exit(1);
        }

        if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) == -1) {
            cerr << "error during setsockopt()" << endl;
            exit(1);
        }
        
        ip = (struct iphdr*) buffer;
        udp = (struct udphdr*) (buffer + sizeof(struct iphdr));

        int udphdrlen = sizeof(struct udphdr);
        int iphdrlen = sizeof(struct iphdr);
        int datalen = 0;
        
        ip->frag_off = 0;
        ip->version = 4;
        ip->ihl = 5;
        ip->tot_len = htons(iphdrlen + udphdrlen);
        ip->id = 0;
        ip->ttl = 40;
        ip->protocol = IPPROTO_UDP;
        ip->saddr = inet_addr(ip_int_adr);
        ip->daddr = inet_addr(ip_destination);
        ip->check = 0;

        udp->source     = htons(43346);
        udp->len        = htons(8);


        pseudoheader.src_addr = ip->saddr;
        pseudoheader.dst_addr = ip->daddr;
        pseudoheader.padding = 0;
        pseudoheader.proto = ip->protocol;
        pseudoheader.length = htons(udphdrlen + datalen);

        udp_chk_construct.pshd = pseudoheader;
        

        to.sin_addr.s_addr = ip->daddr;
        to.sin_family = AF_INET;


        struct bpf_program fcode;
        bpf_u_int32 NetMask;

        char filter_icmp[] = "icmp and src ";
        strcat(filter_icmp, ip_destination);
        if(pcap_compile(handle, &fcode, filter_icmp, 1, NetMask)<0){
            cerr << "error while compiling filter" << endl;
            exit(1);
        }
        
        //set the filter
        if(pcap_setfilter(handle, &fcode)<0){
             cerr << "error while setting filter" << endl;
            exit(1);
        }

        for(int packet_number = 0; packet_number < udp_array.size(); packet_number++){
            
            udp->dest       = htons(udp_array[packet_number]);
            udp->check      = 0;

            udp_chk_construct.udphdr = *udp;

            udp->check = comp_chksum((unsigned short*) &udp_chk_construct,
                sizeof(struct pseudohdr) + udphdrlen + datalen);

            to.sin_port = udp->dest;


            bytes = sendto(sock, buffer, ntohs(ip->tot_len), 0, (struct sockaddr*) &to, sizeof(to));

            if (bytes == -1) {
                cerr << "packet not sent, function sendto()" << endl;
                exit(1);
            }

            alarm(2);
            signal(SIGALRM, alarm_handler);

            pcap_loop(handle, 1, udp_handler, NULL);
            alarm(0);

            int resend_udp = 0;
            while(resend){
                resend_udp++;

                udp->dest       = htons(udp_array[packet_number]);
                udp->check      = 0;


                udp_chk_construct.udphdr = *udp;

                udp->check = comp_chksum((unsigned short*) &udp_chk_construct,
                    sizeof(struct pseudohdr) + udphdrlen + datalen);
                
                to.sin_port = udp->dest;

                bytes = sendto(sock, buffer, ntohs(ip->tot_len), 0, (struct sockaddr*) &to, sizeof(to));

                if (bytes == -1) {
                    cerr << "packet not sent, function sendto()" << endl;
                    exit(1);
                }

                alarm(2);
                signal(SIGALRM, alarm_handler);

                pcap_loop(handle, 1, tcp_handler, NULL);
                alarm(0);
                if(resend_udp == 2){
                    resend = false;
                    printf("%d/udp\t open \n",ntohs(udp->dest));
                }

            }
    
        }

        close(sock);
    }

    return 0;
}