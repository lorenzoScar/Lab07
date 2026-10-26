import copy

from database.meteo_dao import MeteoDao
from model.situazione import Situazione


class Model:
    def __init__(self):
        #capire in che modo voglio salvare i dati
        self._mappa_umidita = None

    def get_umidita_media(self, mese):
        return MeteoDao.get_umidita_media(mese)

    def get_situazioni_meta_mese(self, mese):
        return MeteoDao.get_situazioni_meta_mese(mese)

    def get_sequenza_ottima(self, mese):
        #utput delle citta Torino, Milano... in una lista
        self.__sequenza_ottima = []
        #inizializzo a -1 perché il costo POTREBBE essere 0, -1 default per dire che non è impostato
        self.__costo_ottimo = -1
        #parziale, livello e situazioni meta mese
        #ricorsione parte da sequenza vuota
        self.__ricorsione_sequenza([], 0, self.get_situazioni_meta_mese(mese))
        return self.__sequenza_ottima, self.__costo_ottimo
    """il metodo restituisce il risultato migliore tra quelli esplorati che soddisfano i vincoli, 
    non necessariamente il migliore in assoluto se la ricorsione o i controlli di ammissibilità 
    escludono erroneamente alcune soluzioni."""

    def __ricorsione_sequenza(self, parziale: list[Situazione], livello: int, situazioni_mese: list[Situazione]):
        #fine ricorsione, caso base
        if len(parziale) == 15:
            # mi calcolo il costo
            costo = self.__calcola_costo(parziale)
            # ho due casi:
            # - caso costo minore = sostituisco soluzione
            # - non ho mai trovato una soluzione, questo è il primo
            if costo < self.__costo_ottimo or self.__costo_ottimo == -1:
                self.__costo_ottimo = costo
                self.__sequenza_ottima = copy.deepcopy(parziale)
                """
                ottengo un parziale di 15 situazioni! Situazione (localita, data, umidita
                """
        else: # CASO RICORSIVO
            for i in range(livello * 3, (livello + 1) * 3):
                # livello 0 -> range (0*3= 0, 0+1 *3= 3)
                # livello 1 -> range (1*3= 3, 1+1 *3= 6)
                # livello 2 -> range (6,9)
                # livello 3 -> range (9,12)
                # livello 4 -> range (12,15) = 3 possibili soluzioni per livello
                if self.__is_admissible(parziale, situazioni_mese[i]):
                    #verifico situazione, se ok aggiungo
                    parziale.append(situazioni_mese[i])
                    self.__ricorsione_sequenza(parziale, livello+1, situazioni_mese)
                    parziale.pop()
                """
                backtracking:
                scelgo a: 
                    scelgo d
                        scelgo g
                        torno indietro
                        scelgo h
                        torno indietro
                    torno indietro
                
                scelgo b:
                    ...
                
                """


    def __calcola_costo(self, sequenza: list[Situazione]) -> int:
        costo = 0
        costo += sequenza[0].umidita
        costo += sequenza[1].umidita

        if sequenza[0].localita != sequenza[1].localita:
            costo += 100

        #parto da indice 2 perché [0] e [1] le ho già "esaminate"
        for i in range(2, len(sequenza)):
            #sottosequenza di 3 elementi consecutivi
            sequenza_short = sequenza[i-2:i+1]
            costo += sequenza[i].umidita
            if sequenza_short[2].localita != sequenza[1].localita:
                costo += 100
            elif sequenza_short[2].localita != sequenza[0].localita:
                costo += 100

        return costo

    def __is_admissible(self, parziale: list[Situazione], situazione: Situazione) -> bool:
        #check che nessuna citta sia visitata piu di 6 volte
        visite = {"Milano": 0, "Genova": 0, "Torino": 0}
        if len(parziale) >= 6:
            for stop in parziale:
                visite[stop.localita] += 1
            visite[situazione.localita] += 1
            """
            print(list(visite.value())>6)
            for visita in visite.values():
                if visita > 6:
                    return False
            """
            if any(v > 6 for v in visite.values()):
                return False

        if len(parziale) >= 3:
            last_stop = parziale[-1].localita
            permanenza = 0
            for stop in parziale[-3:]:
                if stop.localita == last_stop:
                    permanenza += 1
            if permanenza < 3 and situazione.localita != last_stop:
                return False
            else:
                return True
        else:
            for stop in parziale:
                if stop.localita != situazione.localita:
                    return False
            return True
