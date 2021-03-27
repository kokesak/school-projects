Projekt je dostupný pro vyzkoušení na stránce http://www.stud.fit.vutbr.cz/~xhrusk26/ITU/

Sestavení/zprovoznění
Je třeba si stáhnout Unity Hub (https://unity3d.com/get-unity/download) nebo konkrétní verzi Unity. 
V obou případech je třeba být zaregistrován s Personal licencí (licence zdarma). V případě stáhnutí Unity Hub je třeba stáhnout v části Installs pomocí tlačítka Add 
nejnovější verzi Unity a poté vybrat moduly (platformy, na kterých lze projekt postavit a spustit.. nejlépe WebGL nebo Universal Windows Platform). 
Poté v části projects lze založit nový projekt pomocí tlačítka new. Tam se vybere 2D template, zvolí jméno projektu a kde bude uložen. Poté stačí kliknout pravým tlačítkem
v okně Project na Assets složku a zvolit Show in explorer. Tam následně tuto Assets složku smazat a vložit tam naši Assets složku (našeho odevzdaného projektu).

Druhou možností je, kdybychom náš projekt exportovali jako custom package. U nového projektu pak stačí zvolit vlevo nahoře Assets->Import Package->Custom Package...  a tam
zvolit ITU_package.unitypackage. 

U obou možností se sice všechny zdrojové soubory načtou do Assets složky, ale UI prvky se nebudou zobrazovat, jelikož je vyžadováno více závislostí než jsme schopni odevzdat.
Z toho důvodu máme celý projekt ke stáhnutí z odkazu https://drive.google.com/file/d/1RR6-gWyWnJ-vc6MLRaFp25WXHzoGBzJ9/view?usp=sharing , který stačí otevřít v Unity editoru
(nebo nahrát do složky s projektem).
