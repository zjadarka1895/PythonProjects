import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def wczytaj_dane_z_pliku():
    file_path = "./acp_d.csv"
    df = pd.read_csv(file_path, delimiter=",")
    df["Data"] = pd.to_datetime(df["Data"])
    tab_zamkniecie = df["Zamkniecie"].to_numpy()
    daty = df["Data"]

    return tab_zamkniecie, daty


def wykres(argumenty, f1, f2, tytul, nazwa_oy1, nazwa_oy2, kolor, kupno=None, sprzedaz=None):

    plt.figure(figsize=(12, 6))
    plt.plot(argumenty, f1, label=nazwa_oy1, color=kolor)

    if f2 is not None:
        plt.plot(argumenty, f2, label=nazwa_oy2, color='#0084ff')

    if kupno is not None:
        plt.scatter(argumenty[kupno], f1[kupno], color='g', marker='o', label="Kupno")

    if sprzedaz is not None:
        plt.scatter(argumenty[sprzedaz], f1[sprzedaz], color='r', marker='o', label="Sprzedaz")

    #plt.xlabel("Data")
    plt.ylabel("Wartosci")
    plt.title(tytul+" \nZofia Krzeszowiec")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)

    plt.show()


def ema_n(wartosci, n):
    alpha = 2 / (n + 1)
    ema = [wartosci[0]]  # Pierwsza wartość EMA to pierwsza wartość EMA_N(0) = x0
    for i in range(1, len(wartosci)):
        ema.append(alpha * wartosci[i] + (1 - alpha) * ema[-1])
    return np.array(ema)


def licz_macd(tab_wartosci):
    ema_12 = ema_n(tab_wartosci, 12)
    ema_26 = ema_n(tab_wartosci, 26)
    macd = ema_12 - ema_26
    return macd

def licz_signal(wartosci_macd):
    signal = ema_n(wartosci_macd, 9)
    return signal

def punkty_przeciecia(macd, signal):
    kupno = []
    sprzedaz = []

    for i in range(1, len(macd)):
        if macd[i-1] < signal[i-1] and macd[i] > signal[i]:
            kupno.append(i)
        elif macd[i-1] > signal[i-1] and macd[i] < signal[i]:
            sprzedaz.append(i)

    return kupno, sprzedaz

def kup(ceny, punkt_kupna, portfel, posiadane_akcje):
    ile_moge_kupic = portfel / ceny[punkt_kupna]
    posiadane_akcje += ile_moge_kupic
    portfel -= ile_moge_kupic * ceny[punkt_kupna]
    return portfel, posiadane_akcje


def sprzedaj(ceny, punkt_sprzedazy, portfel, posiadane_akcje):
    print("Sprzedano: ", posiadane_akcje, "Cena: ", ceny[punkt_sprzedazy])
    portfel += posiadane_akcje * ceny[punkt_sprzedazy]
    posiadane_akcje = 0
    return portfel, posiadane_akcje


def symulacja_inwestowania(notowania, kiedy_kupic, kiedy_sprzedac, okresy):
    i = 0
    portfel = 0
    posiadane_akcje = 1000
    historia_kapitalu = []
    daty_transakcji = [okresy[kiedy_kupic[0]]]
    aktualny_kapital = notowania[kiedy_kupic[0]]*posiadane_akcje
    print(aktualny_kapital)
    historia_kapitalu.append(aktualny_kapital)
    tran_z_zyskiem = 0
    tran_ze_strata = 0

    for d in range(len(notowania)):
        if i < len(kiedy_kupic) and d == kiedy_kupic[i] and i!=0:
            portfel, posiadane_akcje = kup(notowania, kiedy_kupic[i], portfel, posiadane_akcje)

        if i < len(kiedy_sprzedac) and d == kiedy_sprzedac[i]:
            print("Dzień: ", okresy[d])
            portfel, posiadane_akcje = sprzedaj(notowania, kiedy_sprzedac[i], portfel, posiadane_akcje)
            daty_transakcji.append(okresy[d])
            aktualny_kapital = portfel + posiadane_akcje * notowania[d]
            zysk = aktualny_kapital - historia_kapitalu[-1]
            print("Zysk: ", zysk)
            if zysk>0:
                tran_z_zyskiem+=1
            else:
                tran_ze_strata+=1

            print("Kapitał: ", aktualny_kapital)
            historia_kapitalu.append(aktualny_kapital)
            i += 1

    return historia_kapitalu, daty_transakcji, tran_z_zyskiem, tran_ze_strata


# Wczytaj dane
wartosci_notowan, kol_daty = wczytaj_dane_z_pliku()

# Rysowanie notowań WIG20
#wykres(kol_daty, wartosci_notowan, None, "Notowania WIG20", None, "Kurs zamknięcia", "y")

# Oblicz MACD i rysuj wykres
macd_tab = licz_macd(wartosci_notowan)

signal_tab = licz_signal(macd_tab)
kupno, sprzedaz = punkty_przeciecia(macd_tab, signal_tab)

#wykres notowan z zaznaczonymi punktami kupna/sprzedazy
#wykres(kol_daty, wartosci_notowan, None, "Notowania WIG20", None, "Kurs zamknięcia", "y", kupno, sprzedaz)

# Rysowanie MACD i signal z punktami kupna/sprzedaży
#wykres(kol_daty, macd_tab, signal_tab, "Wykres MACD SIGNAL, WIG20", "MACD", "SIGNAL", '#fe7f00', kupno, sprzedaz)

fundusze, daty_sprzedazy, zysk, strata = symulacja_inwestowania(wartosci_notowan, kupno, sprzedaz, kol_daty)
print("Transakcje zakonczone zyskiem: ", zysk)
print("Transakcje zakonczone strata: ", strata)
wykres(daty_sprzedazy, fundusze, None, "Historia posiadanego kapitału", "Kapitał", None, "b")