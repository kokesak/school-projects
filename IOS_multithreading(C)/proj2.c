#include <stdio.h>
#include <stdlib.h>
#include "proj2.h"

// makro pro vystupni soubor
#define NAME "proj2.out"

int rid_number,         // interni pocitadlo ridera
	action_id,          // cislo provadene akce
    riders_at_stop_id,  // pocet rideru na zastavce
	remaining_rid_id,   // pocet zbyvajicich rideru
	kapacita_id,        // kapacita autobusu
	nastoupenych_id;    // pocet nastoupenych rideru do autobusu

int R,          // argumenty: R = argv[1] - pocet cestujicich
    C,          //            C = argv[2] - kapacita autobusu
    ART,        //            ART = argv[3] - doba uspani mezi tvorbou procesu
    ABT;        //            ABT = argv[4] - doba simulace autobusu

int *action = NULL,
	*riders_at_stop = NULL,
	*remaining_rid = NULL,
	*kapacita = NULL,
	*nastoupenych = NULL;


sem_t *sem_mutex = NULL,        // mutex, pro provadeni elemtarnich akci
      *sem_riders = NULL,       // aby hlavni proces skoncil az po skonceni vsech rideru a busu
      *sem_get_in = NULL,       // signal mozneho nastoupeni do autobusu
      *sem_bus_empty = NULL,    // bus je prazdny - vyloyil cestujici
      *sem_bus_arrival = NULL,  // bus je v zastavce - nesmi vstoupit proces
      *sem_bus_depart = NULL,   // cestujici nastoupili do autobusu -> muze odjet
      *sem_ride_end = NULL,     // bus dojel, rider muze vystoupit
      *sem_finish_rider = NULL; // ukonceni rideru

FILE *file_out = NULL;

// vytvoreni semaforu
void set_semaphores()
{

	if ((sem_mutex = sem_open("/xlitwo00_mutex", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_finish_rider = sem_open("/xlitwo00_finish_rider", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_riders = sem_open("/xlitwo00_riders", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_get_in = sem_open("/xlitwo00_get_in", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        fprintf(stderr, "chyba pri vytvareni semaforu\n");
        close_resources();
        exit(1);
    }

    if ((sem_bus_empty = sem_open("/xlitwo00_bus_empty", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_bus_arrival = sem_open("/xlitwo00_bus_arrival", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_bus_depart = sem_open("/xlitwo00_bus_depart", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

	if ((sem_ride_end = sem_open("/xlitwo00_ride_end", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
	{
		fprintf(stderr, "chyba pri vytvareni semaforu\n");
		close_resources();
		exit(1);
	}

}

// vytvoreni sdilenych promennych
void set_shared()
{
	if ((action_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
        close_resources();
        exit(1);
    }

	if ((riders_at_stop_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((remaining_rid_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((kapacita_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((nastoupenych_id = shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT | 0666)) == -1)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((action = shmat(action_id, NULL, 0)) == NULL)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((riders_at_stop = shmat(riders_at_stop_id, NULL, 0)) == NULL)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((remaining_rid = shmat(remaining_rid_id, NULL, 0)) == NULL)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((kapacita = shmat(kapacita_id, NULL, 0)) == NULL)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

	if ((nastoupenych = shmat(nastoupenych_id, NULL, 0)) == NULL)
    {
        fprintf(stderr, "chyba pri vytvareni sdilene promenne\n");
		close_resources();
		exit(1);
    }

}

// uzavreni semaforu a zbaveni se sdilenych promennych
void close_resources()
{
	sem_close(sem_mutex);
	sem_close(sem_riders);
	sem_close(sem_get_in);
	sem_close(sem_bus_empty);
	sem_close(sem_bus_arrival);
	sem_close(sem_bus_depart);
	sem_close(sem_ride_end);
	sem_close(sem_finish_rider);

    sem_unlink("/xlitwo00_mutex");
    sem_unlink("/xlitwo00_riders");
    sem_unlink("/xlitwo00_get_in");
    sem_unlink("/xlitwo00_bus_empty");
    sem_unlink("/xlitwo00_bus_arrival");
    sem_unlink("/xlitwo00_bus_depart");
	sem_unlink("/xlitwo00_ride_end");
	sem_unlink("/xlitwo00_finish_rider");

	shmdt(action);
	shmdt(riders_at_stop);
	shmdt(remaining_rid);
	shmdt(kapacita);
	shmdt(nastoupenych);

	shmctl(action_id, IPC_RMID, NULL);
	shmctl(riders_at_stop_id, IPC_RMID, NULL);
	shmctl(remaining_rid_id, IPC_RMID, NULL);
	shmctl(kapacita_id, IPC_RMID, NULL);
	shmctl(nastoupenych_id, IPC_RMID, NULL);


}

// radnom cislo pro uspani
int rand_value(int max)
{
	if (max == 0)
		return 0;
	return rand() % max;
}



void rider()
{


	// rider zacne
	sem_wait(sem_mutex);
		fprintf(file_out, "%d \t: RID %d \t: start\n", (*action)++, rid_number);
	sem_post(sem_mutex);

	// rider se pokusi vstoupit na zastavku
	sem_wait(sem_bus_arrival);
		sem_wait(sem_mutex);
			fprintf(file_out, "%d \t: RID %d \t: enter: %d \n", (*action)++, rid_number, ++(*riders_at_stop));
		sem_post(sem_mutex);
	sem_post(sem_bus_arrival);

	// rider ceka az ho pusti bus
	sem_wait(sem_get_in);

	sem_wait(sem_mutex);
		fprintf(file_out, "%d \t: RID %d \t: boarding \n", (*action)++, rid_number);
		(*riders_at_stop)--;
		(*nastoupenych)++;

        // kontrola jestli je bus plny
		if( (*nastoupenych) == (*kapacita) || (*riders_at_stop) == 0)
        {
            sem_post(sem_bus_depart); // bus plny -> rider vysle zpravu ze muze odjet
        }
        else
        {
            sem_post(sem_get_in); // bus neni plny -> zbudi dalsiho na zastavce
        }

    sem_post(sem_mutex);

    // ceka na konec jizdy -> vystup
    sem_wait(sem_ride_end);

	// zmensi pocet odbavenych rideru a vystoupenych
	sem_wait(sem_mutex);
		(*remaining_rid)--;
        (*nastoupenych)--;
    sem_post(sem_mutex);

    if((*nastoupenych) == 0)
    {
        // vzbudi autobus pro pokracovani v jizde
        sem_post(sem_bus_empty);
    }
    else
    {
        // zbudi dalsiho cestujiciho aby vystoupil
        sem_post(sem_ride_end);
    }

    // ceka az vystoupi vsichni vystoupi a dostane od busu povoleni pro konec
    sem_wait(sem_finish_rider);

    // rider se ukonci
    sem_wait(sem_mutex);
        fprintf(file_out, "%d \t: RID %d \t: finish \n", (*action)++, rid_number);
    sem_post(sem_mutex);


	exit (0);


}


void bus()
{
    // bus zacne
	sem_wait(sem_mutex);
		fprintf(file_out, "%d \t: BUS \t\t: start\n", (*action)++);
	sem_post(sem_mutex);

	// bus bude cyklicky jezdit na zastavky dokud nebude pocet zbyvajich procesu = 0
	while( (*remaining_rid) != 0)
	{

        // bus prijede na zastavku, nemuzou nastupovat dalsi rideri
		sem_wait(sem_bus_arrival);

		sem_wait(sem_mutex);
			fprintf(file_out, "%d \t: BUS \t\t: arrival\n", (*action)++);
		sem_post(sem_mutex);

		if( (*riders_at_stop) > 0 )
		{
			sem_wait(sem_mutex);
				fprintf(file_out, "%d \t: BUS \t\t: start boarding: %d \n", (*action)++, (*riders_at_stop) );
            sem_post(sem_mutex);

            // kdzy je pocet rideru na zastavce mensi jak kapacita, tak umele snizim kapacitu busu pro tuto jizdu
            if( (*kapacita) > (*riders_at_stop) )
            {
                (*kapacita) = (*riders_at_stop);
            }
            else
            {
                (*kapacita) = C;    // nastaveni na puvodni hodnotu
            }

            // uvolneni mista do autobusu pro 1 process
            sem_post(sem_get_in);

            // ceka az bude moc odjet - rideri nastoupi
			sem_wait(sem_bus_depart);

			sem_wait(sem_mutex);
				fprintf(file_out, "%d \t: BUS \t\t: end boarding: %d \n", (*action)++, (*riders_at_stop) );
			sem_post(sem_mutex);
		}

        // bus odjede ze zastavky
		sem_wait(sem_mutex);
			fprintf(file_out, "%d \t: BUS \t\t: depart \n", (*action)++);
            sem_post(sem_bus_arrival);
		sem_post(sem_mutex);

        // simulace jizdy
		usleep(rand_value(ABT) * 1000);

		sem_wait(sem_mutex);
			fprintf(file_out, "%d \t: BUS \t\t: end \n", (*action)++ );
		sem_post(sem_mutex);

        if( (*nastoupenych) != 0)
        {
                // vzbudi jednoho cestujiciho
				sem_post(sem_ride_end);

                // ceka az rideri vystoupi
                sem_wait(sem_bus_empty);

                //umozni ukoncit vystoupenym riderum
                for(int i = 0; i < (*kapacita); i++)
                    sem_post(sem_finish_rider);
        }

    }


    sem_wait(sem_mutex);
        fprintf(file_out, "%d \t: BUS \t\t: finish\n", (*action)++);
    sem_post(sem_mutex);

    exit (0);

}

// kontrola argumentu
int arguments(int argc, char *argv[])
{
    if(argc != 5)
        return -1;

    char *endptr;

    R = (int) strtol(argv[1], &endptr, 10);
    if (*endptr != '\0' || R <= 0)
       return -1;

    C = (int) strtol(argv[2], &endptr, 10);
    if (*endptr != '\0' || C <= 0)
       return -1;

    ART = (int) strtol(argv[3], &endptr, 10);
    if (*endptr != '\0' || (ART < 0 || ART > 1000))
       return -1;

    ABT = (int) strtol(argv[4], &endptr, 10);
    if (*endptr != '\0' || (ABT < 0 || ABT > 1000))
       return -1;

    return 0;

}



int main(int argc, char *argv[])
{

    int value = arguments(argc, argv);  // osetreni argumentu

    if(value == -1)
    {
        fprintf(stderr, "spatne zadane argumenty\n");
        exit(1);
    }

	if ((file_out = fopen(NAME, "w")) == NULL)
	{
		fprintf(stderr, "chyba pri otevirani souboru\n");
		exit(1);
	}

	set_shared();
	set_semaphores();


    srand(time(NULL));  // seed pro funkci rand()

    (*action) = 1;
	(*riders_at_stop) = 0;
	(*remaining_rid) = R;
	(*nastoupenych) = 0;
	(*kapacita) = C;

	// vycisteni vystupnich souboru
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
	setbuf(file_out, NULL);

	pid_t bus_proc = 0;
	pid_t rid_proc = 0;
	pid_t gen_proc = 0;
	pid_t main_proc = fork();


	// chyba pri forku
	if (main_proc < 0)
	{
		fprintf(stderr, "chyba main forku.\n");
		close_resources();
		kill(0, SIGKILL);
	}
	else if (main_proc == 0)    // proces, abych mohl na konci ukoncit main az po vsech ostatnich procesech
	{
		gen_proc = fork();      // proces pro generovani

		if (gen_proc < 0)
		{
			fprintf(stderr, "chyba genratoru forku.\n");
			close_resources();
			kill(0, SIGKILL);
		}
		else if (gen_proc == 0)  // generovani rideru
		{
			for (int i = 0; i < R; i++)
			{

				usleep(rand_value(ART) * 1000);
				rid_proc = fork();

				if (rid_proc < 0)
				{
					fprintf(stderr, "chyba pri tvorbe ridera (fork error).\n");
					close_resources();
					kill(0, SIGKILL);
				}
				else if (rid_proc == 0)
				{
					rid_number = i + 1; // identifikator ridera
					rider();
				}

			}

			for (int i = 0; i < R; i++) // cekani na konec rideru
				{
                    wait(NULL);
                    sem_post(sem_riders);
                }
            exit(0);
		}
		else // parent proces pro gen busu
		{

				if (bus_proc < 0)
				{
					fprintf(stderr, "chyba pri tvorbe busu (chyba fork).\n");
					close_resources();
					kill(0, SIGKILL);
				}
				else if (bus_proc == 0)
				{
						bus();
				}
				wait(NULL);         // cekani na konce busu
                sem_post(sem_riders);
				exit(0);
		}
	}

	for(int i = 0; i < R+1;i++)     // kontrola skoncenych procesu
        sem_wait(sem_riders);

   	fclose(file_out);
	close_resources();
	return 0;
	}



