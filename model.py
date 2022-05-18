import random
import json

STEVILO_DOVOLJENIH_NAPAK = 10

PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "o"
NAPACNA_CRKA = "-"

ZACETEK = "S"
ZMAGA = "W"
PORAZ = "X"

DATOTEKA_Z_BESEDAMI = "besede.txt"
DATOTEKA_S_STANJEM = "stanje.json"

class Igra:

    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        self.crke = [] if crke is None else crke

    def napacne_crke(self):
        return [crka for crka in self.crke if crka not in self.geslo]

    def pravilne_crke(self):
        return [crka for crka in self.crke if crka in self.geslo]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def zmaga(self):
        return all([crka in self.crke for crka in self.geslo])

    def poraz(self):
        return self.stevilo_napak() >= STEVILO_DOVOLJENIH_NAPAK

    def pravilni_del_gesla(self):
        s = ""
        for crka in self.geslo:
            if crka in self.crke:
                s += crka + " "
            else:
                s += "_ "
        return s.strip()

    def nepravilni_ugibi(self):
        return " ".join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        else:
            self.crke.append(crka)
            if crka in self.geslo:
                if self.zmaga():
                    return ZMAGA
                else:
                    return PRAVILNA_CRKA
            else:
                if self.poraz():
                    return PORAZ
                else:
                    return NAPACNA_CRKA

with open(DATOTEKA_Z_BESEDAMI, encoding="utf-8") as f:
    bazen_besed = [vrstica.strip().upper() for vrstica in f]

def nova_igra():
    return Igra(random.choice(bazen_besed))

class Vislice:

    def __init__(self):
        self.igre = {}
        self.datoteka_s_stanjem = DATOTEKA_S_STANJEM

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        id_igre = self.prost_id_igre()
        igra = nova_igra()
        self.igre[id_igre] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return id_igre

    def ugibaj(self, id_igre, crka):
        self.nalozi_igre_iz_datoteke()
        igra, _ = self.igre[id_igre]
        stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, stanje)
        self.zapisi_igre_v_datoteko()

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as f:
            igre = {id_igre: (igra.geslo, igra.crke, stanje)
                for id_igre, (igra, stanje) in self.igre.items()}
            json.dump(igre, f)

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, "r", encoding="utf-8") as f:
            igre = json.load(f)
            self.igre = {int(id_igre): (Igra(geslo, crke), stanje)
                for id_igre, (geslo, crke, stanje) in igre.items()}