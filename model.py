import random

STEVILO_DOVOLJENIH_NAPAK = 10

PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "o"
NAPACNA_CRKA = "-"

ZACETEK = "S"
ZMAGA = "W"
PORAZ = "X"

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

with open("besede.txt", encoding="utf-8") as f:
    bazen_besed = [vrstica.strip().upper() for vrstica in f]

def nova_igra():
    return Igra(random.choice(bazen_besed))

class Vislice:

    def __init__(self):
        self.igre = {}

    def prost_id_igre(self):
        if len(self.igre) == 0:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        id_igre = self.prost_id_igre()
        igra = nova_igra()
        self.igre[id_igre] = (igra, ZACETEK)
        return id_igre

    def ugibaj(self, id_igre, crka):
        igra, _ = self.igre[id_igre]
        stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, stanje)