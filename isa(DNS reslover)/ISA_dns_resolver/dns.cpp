#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <string.h>
#include <sys/socket.h>    
#include <arpa/inet.h> 
#include <netinet/in.h>
#include <unistd.h>
#include <iostream>
#include <netdb.h> 

using namespace std;

bool Recursion_desired = false;
bool Reversed_query = false;
bool Version6 = false;
bool DNS_server_set = false;
char DNS_server_address[100];
bool Port_set = false;
char Port_number[10] = "53";
bool Address_to_resolve_set = false;
unsigned char Address_to_resolve[100];


struct DNS_HEADER
{
    unsigned short id;      // identification number
 
    unsigned char rd :1;        // recursion desired
    unsigned char tc :1;        // truncated message
    unsigned char aa :1;        // authoritive answer
    unsigned char opcode :4;    // purpose of message
    unsigned char qr :1;        // query/response flag
 
    unsigned char rcode :4; // response code
    unsigned char z :3;     // its z! reserved
    unsigned char ra :1;    // recursion available
 
    unsigned short q_count;     // number of question entries
    unsigned short ans_count;   // number of answer entries
    unsigned short auth_count;  // number of authority entries
    unsigned short add_count;   // number of resource entries
};

struct QUESTION
{
    unsigned short qtype;
    unsigned short qclass;
};
 

unsigned char* ReadName (unsigned char*,unsigned char*,int*);
void change_address_to_dns_format (unsigned char*, unsigned char*);

/*
 *
 * Transfer shortened version of IPv6 address to full length
 * 
 * */
void ipv6_expander(char *address){
    struct in6_addr addr;
    inet_pton(AF_INET6,(char*)address,&addr);
    char str[40];

    sprintf(str,"%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x",
    (int)addr.s6_addr[0], (int)addr.s6_addr[1],
    (int)addr.s6_addr[2], (int)addr.s6_addr[3],
    (int)addr.s6_addr[4], (int)addr.s6_addr[5],
    (int)addr.s6_addr[6], (int)addr.s6_addr[7],
    (int)addr.s6_addr[8], (int)addr.s6_addr[9],
    (int)addr.s6_addr[10], (int)addr.s6_addr[11],
    (int)addr.s6_addr[12], (int)addr.s6_addr[13],
    (int)addr.s6_addr[14], (int)addr.s6_addr[15]);
    
    char reverse_ipv6[100];
    int index = 0;
    for(int i = 38; i>=0; i--){
        if(str[i] != ':'){
            reverse_ipv6[index] = str[i];
            reverse_ipv6[index + 1] = '.';
            index += 2;
        }

    }
    reverse_ipv6[64] = '\0';
    strcat((char*)reverse_ipv6,"ip6.arpa");    
    strcpy(address, reverse_ipv6);
}

void resolve(unsigned char *host)
{
    unsigned char buf[65536],*qname,*reader;
    int i, j, stop, s;
 
    struct sockaddr_in a;       // IPv4
    struct sockaddr_in6 aaaa;   // IPv6
 
    struct sockaddr_in dest;
 
    struct DNS_HEADER *dns = NULL;
    struct QUESTION *qinfo = NULL;
 
    s = socket(AF_INET , SOCK_DGRAM , IPPROTO_UDP); // UDP packet for DNS queries
 
    dest.sin_family = AF_INET;
    dest.sin_port = htons(atoi(Port_number));

    struct hostent *he;
    struct in_addr hostname;

    he = gethostbyname (DNS_server_address);
    if (he)
    {
        bcopy(*he->h_addr_list++, (char *) &hostname, sizeof(hostname));
        dest.sin_addr.s_addr = inet_addr(inet_ntoa(hostname));
    }
    else{
        fprintf(stderr, "Error when resloving dns server address\n");
        exit(1);
    }

    dns = (struct DNS_HEADER *)&buf;
 
    dns->id = (unsigned short) htons(getpid());
    dns->qr = 0;
    dns->opcode = 0;  
    dns->aa = 0;
    dns->tc = 0;
    if(Recursion_desired){
        dns->rd = 1;
    }
    else{
        dns->rd = 0;
    }
    dns->ra = 0;
    dns->z = 0;
    dns->rcode = 0;
    dns->q_count = htons(1);
    dns->ans_count = 0;
    dns->auth_count = 0;
    dns->add_count = 0;
    // Point to the query portion
    qname =(unsigned char*)&buf[sizeof(struct DNS_HEADER)];

    change_address_to_dns_format(qname, host);

    qinfo =(struct QUESTION*)&buf[sizeof(struct DNS_HEADER) + (strlen((const char*)qname) + 1)];

    if(Version6 && !Reversed_query){
        qinfo->qtype = htons(28);  
    }
    else if(Reversed_query){
        qinfo->qtype = htons(12);
    }
    else{
        qinfo->qtype = htons(1);
    }

    qinfo->qclass = htons(1);
    
    if(sendto(s,(char*)buf,sizeof(struct DNS_HEADER) + (strlen((const char*)qname)+1) + sizeof(struct QUESTION),0,(struct sockaddr*)&dest,sizeof(dest)) < 0)
    {
        fprintf(stderr, "Sending packet failed\n");
        exit(1);
    }
    
    // Timeout for recieving packet
    struct timeval timeout; 
    timeout.tv_sec = 2; 
    timeout.tv_usec = 0; 
    if (setsockopt (s, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(timeout)) < 0){ 
        fprintf(stderr, "Unknown internal error\n");
        exit(1);
    }

    // Receive the answer
    i = sizeof dest;
    if(recvfrom (s,(char*)buf , 65536 , 0 , (struct sockaddr*)&dest , (socklen_t*)&i ) < 0)
    {
        fprintf(stderr, "Receiving answer failed\n");
        exit(1);
    }
    
    switch(dns->rcode){
        case 1:
            fprintf(stderr, "Format error. \n");
            fprintf(stderr, "The name server was unable to interpret the query. \n");
            exit(1);
            break;
        case 2:
            fprintf(stderr, "Server failure. \n");
            fprintf(stderr, "The name server was unable to process this query due to a problem with the name server. \n");
            exit(1);
            break;
        case 3:
            fprintf(stderr, "Name Error. \n");
            fprintf(stderr, "Domain name referenced in the query does not exist. \n");
            exit(1);
            break;
        case 4:
            fprintf(stderr, "Not Implemented. \n");
            fprintf(stderr, "The name server does not support the requested kind of query. \n");
            exit(1);
            break;
        case 5:
            fprintf(stderr, "Refused. \n");
            fprintf(stderr, "The name server refuses to perform the specified operation for policy reasons. \n");
            exit(1);
            break;
        default:
            break;
    }
 
    
    reader = &buf[sizeof(struct DNS_HEADER)]; // move ahead of the dns header

    /* printf("XX:%d XX \n",dns->rcode);
    // cout << "READER" << endl;
    // for(int i = 0; i<512; i++){
    //    cout << hex << (int)reader[i] << " ";
    }*/

    // Start reading answers
    stop = 0;
    if(dns->aa == 0){
        printf("Authoritative: No, ");
    }
    else if(dns->aa == 1){
        printf("Authoritative: Yes, ");
    }

    if(dns->rd == 0){
        printf("Recursive: No, ");
    }
    else if(dns->rd == 1){
        printf("Recursive: Yes, ");
    }
    
    if(dns->tc == 0){
        printf("Truncated: No");
    }
    else if(dns->tc == 1){
        printf("Truncated: Yes");
    }
    // Question section
    printf("\nQuestion section (%d) \n", ntohs(dns->q_count));
    for(i=0;i<ntohs(dns->q_count);i++){
        int type, response_class;
        printf("    %s, ", ReadName(reader,buf,&stop));
        reader = reader + stop;
        type = (reader[0] << 8) + reader[1];
        if(type == 1){
            printf("A, ");
        }
        else if(type == 28){
            printf("AAAA, ");
        }
        else if(type == 12){
            printf("PTR, ");
        }

        response_class = (reader[2] << 8) + reader[3];
        if(response_class == 1)
            printf("IN");
        else if (response_class == 3)
            printf("CH");
        else if (response_class == 4)
            printf("HS");
       
    }
    reader = reader + 4;

    // Answer section
    printf("\nAnswer section (%d) \n", ntohs(dns->ans_count));
    for(i=0;i<ntohs(dns->ans_count);i++)
    {   
        int type, response_class, ttl, data_len;
        printf("    %s, ", ReadName(reader,buf,&stop));
        reader = reader + stop;

        type = (reader[0] << 8) + reader[1];
        if(type == 1){
            printf("A, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];
            printf("%d, ", ttl);
            string ip_adr = to_string(reader[10]) + "." + 
                            to_string(reader[11]) + "." + 
                            to_string(reader[12]) + "." +
                            to_string(reader[13]);
            cout << ip_adr << endl;

            reader = reader + 14;

        }
        else if(type == 5 || type == 12){
            if(type == 5){
                printf ("CNAME, ");
            }
            else if(type == 12){
                printf("PTR, ");
            }
            
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];

            printf("%d,",ttl);
            data_len = (reader[8] << 8) + reader[9];

            reader = reader + 10;
            
            int char_cnt = reader[0];

            int z = 0;

            u_char *cname;
            cname = ReadName(reader,buf,&stop);
            printf(" %s \n",cname);
            
            reader += data_len;
        }

        else if(type == 28){
            printf("AAAA, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];
            printf("%d, ", ttl);
            reader = reader + 10;
            
            struct in6_addr ipv6;
            for(int i = 0; i < 16; i=i+1){
                ipv6.s6_addr[i] = reader[i];
            }
            aaaa.sin6_addr = ipv6;

            char ipv6_addres[INET6_ADDRSTRLEN];
            inet_ntop(AF_INET6, &(aaaa.sin6_addr), ipv6_addres, INET6_ADDRSTRLEN);
            printf("%s \n", ipv6_addres);

            reader = reader + 16;
        }
    }
    
    // Authority section
    printf("Authority section (%d) \n", ntohs(dns->auth_count));

    for(i=0;i<ntohs(dns->auth_count);i++)
    {
        int type, response_class, ttl, data_len;
        printf("    %s, ", ReadName(reader,buf,&stop));

        reader = reader + stop;
        
        type = (reader[0] << 8) + reader[1];

        if(type == 2){
            printf ("NS, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];

            printf("%d,",ttl);
            data_len = (reader[8] << 8) + reader[9];

            reader = reader + 10;
            
            int char_cnt = reader[0];


            int z = 0;
            u_char *cname;
            cname = ReadName(reader,buf,&stop);
            printf(" %s \n",cname);
            
            reader += data_len;
        }
        else if(type == 6){
            printf ("SOA, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];

            printf("%d,",ttl);
            data_len = (reader[8] << 8) + reader[9];

            reader = reader + 10;
            
            int char_cnt = reader[0];


            int z = 0;
            u_char *cname;
            cname = ReadName(reader,buf,&stop);
            printf(" %s \n",cname);
            
            reader += data_len;
        }

    }
    
    // Additional sectio
    printf("Additional section (%d) \n", ntohs(dns->add_count));
    for(i=0;i<ntohs(dns->add_count);i++)
    {
        int type, response_class, ttl, data_len;
        printf("    %s, ", ReadName(reader,buf,&stop));
        reader = reader + stop;

        type = (reader[0] << 8) + reader[1];
        if(type == 1){
            printf("A, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];
            printf("%d, ", ttl);

            string ip_adr = to_string(reader[10]) + "." + 
                            to_string(reader[11]) + "." + 
                            to_string(reader[12]) + "." +
                            to_string(reader[13]);
            cout << ip_adr << endl;
            reader = reader + 14;
        }
        else if(type == 5 || type == 12){
            if(type == 5){
                printf ("CNAME, ");
            }
            else if(type == 12){
                printf("PTR, ");
            }
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];

            printf("%d,",ttl);
            data_len = (reader[8] << 8) + reader[9];

            reader = reader + 10;
            
            int char_cnt = reader[0];


            int z = 0;
            u_char *cname;
            cname = ReadName(reader,buf,&stop);
            printf(" %s \n",cname);
            
            reader += data_len;
           
        }

        else if(type == 28){
            printf("AAAA, ");
            response_class = (reader[2] << 8) + reader[3];
            if(response_class == 1)
                printf("IN, ");
            else if (response_class == 3)
                printf("CH, ");
            else if (response_class == 4)
                printf("HS, ");

            ttl = (reader[4] << 24) + (reader[5] << 16) + (reader[6] << 8) + reader[7];
            printf("%d, ", ttl);
            reader = reader + 10;
            
            struct in6_addr ipv6;
            for(int i = 0; i < 16; i=i+1){
                ipv6.s6_addr[i] = reader[i];
            }
            aaaa.sin6_addr = ipv6;

            char ipv6_addres[INET6_ADDRSTRLEN];
            inet_ntop(AF_INET6, &(aaaa.sin6_addr), ipv6_addres, INET6_ADDRSTRLEN);
            printf("%s \n", ipv6_addres);
            reader = reader + 16;
        }
    }
}

/*
 *
 * Reads data segment
 * Used from: https://www.binarytides.com/dns-query-code-in-c-with-winsock/
 * Author: Silver Moon, December 18, 2012
 * 
 * */
u_char* ReadName(unsigned char* reader,unsigned char* buffer,int* count)
{
    unsigned char *name;
    unsigned int p=0,jumped=0,offset;
    int i , j;
 
    *count = 1;
    name = (unsigned char*)malloc(256);
 
    name[0]='\0';
 
    while(*reader!=0)
    {
        if(*reader>=192)
        {
            offset = (*reader)*256 + *(reader+1)  - 0xc000; //- pointer
            reader = buffer + offset - 1;
            jumped = 1; // we have jumped to another location so counting wont go up!
        }
        else
        {
            name[p++]=*reader;
        }
 
        reader = reader+1;
 
        if(jumped==0)
        {
            *count = *count + 1; // if we havent jumped to another location then we can count up
        }
    }
 
    name[p]='\0'; // string complete
    if(jumped==1)
    {
        *count = *count + 1; // number of steps we actually moved forward in the packet
    }
 
    for(i=0;i<(int)strlen((const char*)name);i++) 
    {
        p=name[i];
        for(j=0;j<(int)p;j++) 
        {
            name[i]=name[i+1];
            i=i+1;
        }
        name[i]='.';
    }
    name[i-1]='\0';
    return name;
}

/*
 * 
 * Change address name to dns format
 * 
 * */
void change_address_to_dns_format(unsigned char* dns,unsigned char* host) {
    int lock = 0 , i;
    strcat((char*)host,".");
     
    for(i = 0 ; i < strlen((char*)host) ; i++) 
    {
        if(host[i]=='.') 
        {
            *dns++ = i-lock;
            for(;lock<i;lock++) 
            {
                *dns++=host[lock];
            }
            lock++; 
        }
    }
    *dns++='\0';
}

/*
 * 
 * Reverse IPv4 address for inverse querry
 * 
 * */
void reverse_ip_address(char* str){
    char tmp[strlen(str)];
    int index = 0;
    int count = 0;
    int k, i;
    int dot_found = 0;

    for(i = strlen(str)-1; i>=0; i--){
        if(dot_found == 3)
            break;
        if(str[i] == '.'){
            dot_found++;
            for(k = 0; k < count; k++){
                tmp[index] = str[(i+1)+k];
                index++;
            }
            count = 0;
            tmp[index] = '.';
            index++;
        }
        else{
            count = count + 1;
        }
    }
    i = 0;
    while(str[i] != '.'){
        tmp[index] = str[i];
        index++;
        i++;
    }
    strcpy(str, tmp);
    strcat((char*)str,".in-addr.arpa");
}

/*
 * 
 * Check if port argument is valid
 * 
 * */
void check_valid_port(char *str){
    for(int i = 0; i < strlen(str); i++){
        if(str[i] < '0' || str[i] > '9'){
            fprintf(stderr, "Invalid port number\n");
            exit(1);
        }
    }
    int port = atoi(str);

    if(port < 0 || port > 65535){
        fprintf(stderr, "Invalid port number\n");
        exit(1);
    }
    return;
}

/*
 * 
 * Checks if ip argument is valid (for -x option)
 * 
 * */
int isValidIpAddress(char *ipAddress)
{
    struct sockaddr_in sa;
    return (inet_pton(AF_INET, ipAddress, &(sa.sin_addr)));

}

int main(int argc, char *argv[]) {

    for(int i = 1; i < argc; i++){
        if(strcmp(argv[i], "-r") == 0)
            Recursion_desired = true;
        else if(strcmp(argv[i], "-x") == 0)
            Reversed_query = true;
        else if(strcmp(argv[i], "-6") == 0)
            Version6 = true;
        else if(strcmp(argv[i], "-p") == 0){
            if((i + 1) == argc){
                fprintf(stderr, "Argument -p needs value\n");
                return 1;
            }
            check_valid_port(argv[i+1]);
            Port_set = true;
            strcpy(Port_number,argv[i+1]);
            i++;
        }
        else if(strcmp(argv[i], "-s") == 0){
             if((i + 1) == argc){
                fprintf(stderr, "Argument -s needs value\n");
                return 1;
            }
            DNS_server_set = true;
            strcpy(DNS_server_address,argv[i+1]);
            i++;
        }
        else if (!Address_to_resolve_set){
            strcpy((char*)Address_to_resolve, argv[i]);
            Address_to_resolve_set = true;
        }
        else{
            fprintf(stderr, "Wrong syntax\n");
            return 1;
        }

    }

    if(DNS_server_set == false || Address_to_resolve_set == false){
        fprintf(stderr, "DNS server and address to resolve needs to be passed\n");
        exit(1);
    }

    if(Reversed_query){
        if(Version6){
            ipv6_expander((char*)Address_to_resolve);
        }
        else{
            if(isValidIpAddress((char*)Address_to_resolve) == 1){
                reverse_ip_address((char*)Address_to_resolve);
            }
            else{
                fprintf(stderr, "Wrong IPv4 address\n");
                return 1;
            }
        }
    }

    resolve(Address_to_resolve);
}