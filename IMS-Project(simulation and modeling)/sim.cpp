#include <stdio.h>
#include <string.h>

#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;

#define ARGERR do {cerr << "Spatne argumenty!\n" << POMOC << endl; tiskni_pomoc(); return 1;}while(0)

// Soucinitel tepelne vodivosti
const map<string, float> MATERIALY = {{"polystyren", 0.04},
                                      {"cihla", 0.17},
                                      {"beton", 1.29},
                                      {"drevo", 0.18},
                                      {"mineralni_vlna", 0.079},
                                      {"ocel", 50},
                                      {"cement", 1.16},
                                      {"eps", 0.037},
                                      {"celuloza", 0.039}
                                      };

const float TEPLOTY[] = {12.5, 7.4, 2.4, -1.0, -7.1, -1.2, 2.6, 7.3, 12.4};
const string TEPLOTY_MESIC[] = {"zari", "rijen", "list", "pros", "leden", "unor", "brez", "duben", "kvet"};

const string POMOC = "Pouziti: ./sim [-t vnitrni_teplota] [-w sirka_domu vyska_domu delka_domu][-m [material1 material1_tloustka] ...]";

void tiskni_pomoc()
{
    cout << POMOC << endl;
    map<string, float>::const_iterator it = MATERIALY.begin();
    string tisk = "Dostupne materialy: ";
    tisk += it->first;
    while (++it != MATERIALY.end())
    {
        tisk += ", ";
        tisk += it->first;
    }
    cout << tisk << endl;
}

double hodnota_co2(string material){
    if(material == "cihla"){
        return 1496;
    }
    else if (material == "polystyren"){
        return 2415;
    }
    else if (material == "beton"){
        return 227;
    }
    else if (material == "drevo"){
        return -704.5;
    }
    else if (material == "mineralni_vlna"){
        return 66;
    }
    else if (material == "ocel"){
        return 2588;
    }
    else if (material == "cement"){
        return 2160;
    }
    else if (material == "eps"){
        return 50.3;
    }
    else if (material == "celuloza"){
        return 50.3;
    }
    else{
        return 0;
    }
    
    
}

int main(int argc, char *argv[])
{
    int teplota_uvnitr;
    double sirka, vyska, delka;
    string pouzite_materialy[10];
    int arr_idx = 0;
    double suma_co2 = 0.0;

    // Soucinitel tepelne vodivosti; tloustka
    vector<pair<float, float>> materialy;

    for (int i = 0; i < argc; i++)
    {
        if (strcmp(argv[i], "-t") == 0)
        {
            if (++i >= argc) {ARGERR;}
            teplota_uvnitr = atoi(argv[i]);
        }
        else if (strcmp(argv[i], "-w") == 0)
        {
            if (++i >= argc) {ARGERR;}
            sirka = atof(argv[i]);
            if (++i >= argc) {ARGERR;}
            vyska = atof(argv[i]);
            if (++i >= argc) {ARGERR;}
            delka = atof(argv[i]);
        }        
        else if (strcmp(argv[i], "-m") == 0)
        {
            if (++i >= argc) {ARGERR;}
            map<string, float>::const_iterator it;
            while ((it = MATERIALY.find(string(argv[i]))) != MATERIALY.end())
            {
                pouzite_materialy[arr_idx] = string(argv[i]);
                arr_idx++;
                if (++i >= argc) {ARGERR;}
                materialy.push_back(make_pair(it->second, atof(argv[i])));
                if (i+1 >= argc) {break;}
                ++i;
            }
        }
        else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0)
        {
            tiskni_pomoc();
        }
    }
    cout << "Vnitrni teplota: " << teplota_uvnitr << endl;
    cout << "Sirka domu: " << sirka << " m Vyska domu: " << vyska << " m Delka domu: " << delka << " m" << endl;

    double R = 0;
    double Ri, Re, RT, U, S, HT, P;
    double CO2_z_materialu;

    S = 2 * sirka * vyska + 2 * delka * vyska;

    for (int i = 0; i < materialy.size(); i++)
    {
        CO2_z_materialu = S * materialy[i].second * hodnota_co2(pouzite_materialy[i]); 
        cout << "Zed: material c. " << i << " - " << pouzite_materialy[i] << ", tloustka: " << materialy[i].second << "m, soucinitel tepelne vodivosti: " << materialy[i].first << ", Vyprodukovanych CO2: " << CO2_z_materialu << " kg" << endl;
        R += materialy[i].second / materialy[i].first;
        suma_co2 += CO2_z_materialu;
    }
    cout << "Prace bagru na stvbe po dobu 15 dnu (6h denne): 1944 kg CO2" << endl;

    Ri = 0.13;
    Re = 0.04;
    RT = Ri + R + Re;

    cout << "Tepelny odpor R = " << R << " RT = " << RT << endl;
    U = 1/RT;
    cout << "Soucinitel prostupu tepla U = " << U << endl;
    cout << "Povrch zdi S = " << S << endl;
    HT = U * S;
    cout << "Merna ztrata prostupem tepla HT = " << HT << endl;
    double suma_energii = 0.0;
    double suma_emisi_plynu = 0.0;
    
    cout << "Mesic\tTepelna ztrata\tNa den\t\tEnergie na den\tCO2 na den" << endl;
    for (int i = 0; i < (sizeof(TEPLOTY) / sizeof(TEPLOTY[0])); i++)
    {
        P = HT * (teplota_uvnitr - TEPLOTY[i]);
        double vykon_den = P * 24 / 1000; // kWh
        double energie_den = P * 3600 * 24 / 10e6; // MJ
        double co2_den = vykon_den * 0.2; // kg
        cout << TEPLOTY_MESIC[i] << "\t" << P << " W\t"<< vykon_den <<" kWh\t" << energie_den << " MJ\t"<< co2_den << " kg"  << endl;
        suma_energii += energie_den * 30;
        suma_emisi_plynu += co2_den * 30;
    }
    
    cout << "Celkem CO2 vyprodukovanych behem stavby: " << suma_co2 + 1944.0 << " kg CO2" << endl;
    cout << "Celkem energie na vytapeni za rok: " << suma_energii << " MJ " << endl;
    cout << "Celkem CO2 vzniklych spalovanim zemniho plynu za rok: " << suma_emisi_plynu << " kg CO2" << endl;


    return 0;
}
