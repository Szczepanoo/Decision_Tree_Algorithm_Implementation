################################################################################################################
# LAB 1
# Odczyt danych

def wykryj_separator(linia):
    """
    Wykrywa separator, znajdując pierwszy znak niealfanumeryczny i
    budując z niego ciąg takich samych znaków.
    """
    if not linia:
        return None

    i = 0
    # znaki uznawane za część liczby (np. -, ., e)
    while i < len(linia) and (linia[i].isalnum() or linia[i] in ['+', '-', '.', 'e', 'E']):
        i += 1

    if i == len(linia):
        return None  # bez separatora → whitespace

    sep_char = linia[i]
    separator = sep_char

    j = i + 1
    while j < len(linia) and linia[j] == sep_char:
        separator += linia[j]
        j += 1

    return separator


def split_by_separator(text, separator):
    """
    Dzieli tekst po separatorze bez użycia regex.
    Obsługuje separatory wieloznakowe.
    """
    if separator is None:
        return text.split()

    wynik = []
    buff = ""
    i = 0
    n = len(separator)

    while i < len(text):
        if text[i:i+n] == separator:
            wynik.append(buff)
            buff = ""
            i += n
        else:
            buff += text[i]
            i += 1

    wynik.append(buff)
    return wynik


def konwertuj_wartosc(v):
    """
    Zamienia tekst na int, float lub pozostawia jako string.
    Kolejność prób:
    1. int
    2. float
    3. string
    """
    # próba int
    try:
        return int(v)
    except ValueError:
        pass

    # próba float
    try:
        return float(v)
    except ValueError:
        pass

    # pozostaje string
    return v


def wczytaj_tabele_decyzyjna(nazwa_pliku, separator=None):
    dane = []

    with open(nazwa_pliku, "r", encoding="utf-8") as f:
        linie = [l.strip() for l in f if l.strip()]

    if not linie:
        return [], []

    if separator is None:
        separator = wykryj_separator(linie[0])

    for linia in linie:
        elementy = split_by_separator(linia, separator)
        # konwersja typów
        elementy = [konwertuj_wartosc(e) for e in elementy]
        dane.append(elementy)

    atrybuty = [wiersz[:-1] for wiersz in dane]
    decyzje = [wiersz[-1] for wiersz in dane]
    return atrybuty, decyzje


def policz_wartosci_atrybutow(atrybuty):
    wartosci = []
    liczba_kol = len(atrybuty[0])
    for kol in range(liczba_kol):
        wartosci.append(set(w[kol] for w in atrybuty))
    return wartosci


def policz_wystapienia_wartosci(atrybuty):
    wyst = []
    liczba_kol = len(atrybuty[0])
    for kol in range(liczba_kol):
        sl = {}
        for w in atrybuty:
            sl[w[kol]] = sl.get(w[kol], 0) + 1
        wyst.append(sl)
    return wyst


def liczba_mozliwych_wartosci(atrybuty):
    """
    Zwraca listę liczb: ile różnych wartości ma każdy atrybut.
    Przykład: [2, 3, 2, 1]
    """
    wynik = []
    liczba_kol = len(atrybuty[0])

    for kol in range(liczba_kol):
        unikalne = set(w[kol] for w in atrybuty)
        wynik.append(len(unikalne))

    return wynik


def wystapienia_wartosci(atrybuty):
    """
    Zwraca listę słowników:
    [{wartość: liczba}, {wartość: liczba}, ...]
    Jeden słownik na atrybut.

    Przykład:
    [
        {0: 3, 1: 2},
        {"zielony": 2, "czerwony": 1, "niebieski": 1},
        ...
    ]
    """
    wynik = []
    liczba_kol = len(atrybuty[0])

    for kol in range(liczba_kol):
        sl = {}
        for w in atrybuty:
            val = w[kol]
            sl[val] = sl.get(val, 0) + 1
        wynik.append(sl)

    return wynik


################################################################################################################
# LAB 2
# Wynaczanie Entropii

import math


def log2_approx(x, epsilon=1e-12):
    """
    Przybliżenie logarytmu w bazie 2 dla x > 0
    """
    if x <= 0:
        return 0.0  # bezpieczeństwo
    n = 0
    while x >= 2:
        x /= 2
        n += 1
    while x < 1:
        x *= 2
        n -= 1
    # Teraz x w [1,2), przybliżenie log2(1+y) ~ y - y^2/2 + y^3/3 ...
    y = x - 1
    term = y
    result = 0.0
    k = 1
    while abs(term) > epsilon:
        result += term / k
        k += 1
        term *= -y
    return n + result


def entropia(wystapienia):
    """
    Liczy entropię na podstawie słownika {wartość: liczba_wystąpień}.
    Wzór: I(P) = - sum(pi * log2(pi)) dla wszystkich i
    """
    total = sum(wystapienia.values())
    if total == 0:
        return 0.0

    ent = 0.0
    for count in wystapienia.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return ent


# Funkcja informacyjna
def info_atrybutu(atrybuty, decyzje):
    """
    Liczy Info(X, T) dla każdego atrybutu X w tabeli atrybutów względem decyzji.
    Zwraca listę wartości Info(X_i, T) dla wszystkich kolumn.
    """
    liczba_kol = len(atrybuty[0])
    total = len(atrybuty)
    wyniki = []

    for kol in range(liczba_kol):
        # grupowanie obiektów po wartościach atrybutu
        grupy = {}
        for i, w in enumerate(atrybuty):
            val = w[kol]
            if val not in grupy:
                grupy[val] = []
            grupy[val].append(decyzje[i])

        # liczenie Info dla atrybutu: suma (|Ti|/|T| * entropia(Ti))
        info = 0.0
        for podzbior in grupy.values():
            # obliczamy entropię dla podzbioru decyzji Ti
            wyst = {}
            for d in podzbior:
                wyst[d] = wyst.get(d, 0) + 1
            ent = entropia(wyst)
            info += (len(podzbior) / total) * ent
        wyniki.append(info)

    return wyniki


################################################################################################################
# LAB 3
# Przyrost informacji

def przyrost_informacji(atrybuty, decyzje):
    """
    Liczy Gain(X, T) = Info(T) - Info(X, T) dla każdego atrybutu.
    Zwraca listę wartości przyrostu informacji.
    """
    # entropia wszystkich decyzji
    wyst_dec = {}
    for d in decyzje:
        wyst_dec[d] = wyst_dec.get(d, 0) + 1
    info_T = entropia(wyst_dec)

    # Info(X, T) dla każdego atrybutu
    info_XT = info_atrybutu(atrybuty, decyzje)

    # Gain(X, T)
    gain = [info_T - val for val in info_XT]
    return gain


# Zrównoważony przyrost informacji (GainRatio)

def split_info(atrybuty):
    """
    Liczy SplitInfo(X, T) dla każdego atrybutu X.
    """
    liczba_kol = len(atrybuty[0])
    total = len(atrybuty)
    wyniki = []

    for kol in range(liczba_kol):
        # liczymy liczność każdej wartości atrybutu
        sl = {}
        for w in atrybuty:
            val = w[kol]
            sl[val] = sl.get(val, 0) + 1

        # entropia podziału według atrybutu
        ent = 0.0
        for count in sl.values():
            if count > 0:
                p = count / total
                ent -= p * math.log2(p)
        wyniki.append(ent)
    return wyniki


def gain_ratio(atrybuty, decyzje):
    """
    Liczy GainRatio(X, T) = Gain(X, T) / SplitInfo(X, T) dla każdego atrybutu.
    """
    gain = przyrost_informacji(atrybuty, decyzje)
    split = split_info(atrybuty)

    # unikamy dzielenia przez zero
    gain_ratio_list = []
    for g, s in zip(gain, split):
        if s == 0:
            gain_ratio_list.append(0.0)
        else:
            gain_ratio_list.append(g / s)
    return gain_ratio_list


################################################################################################################
# LAB 3

def podziel_dane(atrybuty, decyzje, idx_atrybutu):
    """
    Zwraca słownik:
      wartość_atrybutu -> (lista_atrybutów_potomka, lista_decyzji_potomka)
    """
    wyniki = {}
    for w, d in zip(atrybuty, decyzje):
        val = w[idx_atrybutu]
        if val not in wyniki:
            wyniki[val] = ([], [])
        wyniki[val][0].append(w)
        wyniki[val][1].append(d)
    return wyniki


def policz_wystapienia(lista):
    wynik = {}
    for x in lista:
        if x not in wynik:
            wynik[x] = 0
        wynik[x] += 1
    return wynik


def buduj_drzewo(atrybuty, decyzje, poziom=0):
    """
    Rekurencyjna budowa drzewa zgodnie z pseudokodem:
    - oblicz GainRatio
    - wybierz najlepszy podział
    - jeśli max GainRatio == 0 → STOP (liść)
    - w przeciwnym razie buduj poddrzewa
    """

    print("\n" + "="*60)
    print(f"POZIOM {poziom} – liczba obiektów: {len(atrybuty)}")
    print("="*60)

    # 1. Entropia
    ent = entropia(policz_wystapienia(decyzje))
    print(f"Info(T) = {ent:.6f}")

    # 2. Gain
    gain = przyrost_informacji(atrybuty, decyzje)
    for i, g in enumerate(gain, 1):
        print(f"Gain(a{i}, T) = {g:.6f}")

    # 3. SplitInfo
    splitinfo = split_info(atrybuty)
    for i, s in enumerate(splitinfo, 1):
        print(f"SplitInfo(a{i}, T) = {s:.6f}")

    # 4. GainRatio
    gr = gain_ratio(atrybuty, decyzje)
    for i, r in enumerate(gr, 1):
        print(f"GainRatio(a{i}, T) = {r:.6f}")

    # 5. Kryterium stopu – brak poprawy
    najlepszy = max(gr)
    if najlepszy == 0.0:
        print("KONIEC – wszystkie GainRatio = 0.0 → Tworzymy liść.")
        # zwracamy klasę większościową
        klasa = max(set(decyzje), key=decyzje.count)
        print(f"Liść → klasa: {klasa}")
        return

    # 6. Wybór najlepszego atrybutu
    idx_best = gr.index(najlepszy)
    print(f"\nNajlepszy podział: a{idx_best+1}, GainRatio = {najlepszy:.6f}")

    # 7. Dzielenie danych na podzbiory
    potomkowie = podziel_dane(atrybuty, decyzje, idx_best)

    # 8. Rekurencyjne zejście po każdym potomku
    for val, (atr_p, dec_p) in potomkowie.items():
        print(f"\n-- Wartość {val} → {len(atr_p)} obiektów")
        buduj_drzewo(atr_p, dec_p, poziom + 1)


################################################################################################################
# WIZUALIZACJA

# Prosta klasa węzła drzewa
class Node:
    def __init__(self, nazwa=None, dzieci=None, liść=False, klasa=None):
        self.nazwa = nazwa  # nazwa atrybutu
        self.dzieci = dzieci or {}  # słownik: wartość -> Node
        self.liść = liść
        self.klasa = klasa  # klasa decyzyjna, jeśli liść


# Funkcja budująca drzewo i zwracająca strukturę Node
def buduj_drzewo_struktura(atrybuty, decyzje):
    if not atrybuty or not decyzje:
        return None

    # Kryterium stopu – wszystkie decyzje są takie same
    if len(set(decyzje)) == 1:
        return Node(liść=True, klasa=decyzje[0])

    # Obliczamy GainRatio
    gr = gain_ratio(atrybuty, decyzje)
    najlepszy = max(gr)
    if najlepszy == 0:
        klasa = max(set(decyzje), key=decyzje.count)
        return Node(liść=True, klasa=klasa)

    idx_best = gr.index(najlepszy)
    nazwa_atrybutu = f"a{idx_best + 1}"

    potomkowie = podziel_dane(atrybuty, decyzje, idx_best)
    dzieci = {}
    for val, (atr_p, dec_p) in potomkowie.items():
        dzieci[val] = buduj_drzewo_struktura(atr_p, dec_p)

    return Node(nazwa=nazwa_atrybutu, dzieci=dzieci)


def drukuj_drzewo_tekstowo(node, poziom=0, wartosc_krawedzi=None):
    """
    Rekurencyjne drukowanie drzewa w konsoli.
    node – obiekt Node
    poziom – głębokość drzewa (wcięcia)
    wartosc_krawedzi – wartość atrybutu, która prowadzi do tego węzła
    """
    prefix = "    " * poziom
    if wartosc_krawedzi is not None:
        prefix += f"[{wartosc_krawedzi}] -> "

    if node.liść:
        print(f"{prefix}LIŚĆ: {node.klasa}")
    else:
        print(f"{prefix}Atrybut: {node.nazwa}")
        for val, child in node.dzieci.items():
            drukuj_drzewo_tekstowo(child, poziom + 1, val)

################################################################################################################
# PRZYKŁAD UŻYCIA

#pliki = ["Rozszerzona_breast+cancer/breast-cancer.data","tab1_1.txt","tab1_2.txt"]

pliki = ["tab1_1.txt","tab1_2.txt"]

for nazwa in pliki:
    print("=" * 60)
    print(f"Przetwarzanie pliku: {nazwa}")
    print("=" * 60)

    atrybuty, decyzje = wczytaj_tabele_decyzyjna(nazwa)

    print("Atrybuty:")
    for w in atrybuty:
        print(w)

    print("\nLiczba możliwych wartości każdego atrybutu:")
    print(liczba_mozliwych_wartosci(atrybuty))

    print("\nWystąpienia każdej wartości:")
    wyniki = wystapienia_wartosci(atrybuty)
    for i, sl in enumerate(wyniki, start=1):
        print(f"Atrybut a{i}: {sl}")

    print("\nEntropia wartości decyzyjnych:")
    ent_dec = entropia(dict((d, decyzje.count(d)) for d in set(decyzje)))
    print(f"Info(T) = {ent_dec:.6f}")

    print("\n[OPCJONALNE] Entropia dla każdego atrybutu:")
    for i, sl in enumerate(wyniki, start=1):
        ent = entropia(sl)
        print(f"Info(A{i}) = {ent:.6f}")

    print("\nInfo(X, T) dla każdego atrybutu:")
    info_wszystkie = info_atrybutu(atrybuty, decyzje)
    for i, info_val in enumerate(info_wszystkie, start=1):
        print(f"Info(a{i}, T) = {info_val:.6f}")

    print("\nPrzyrost informacji dla każdego atrybutu (Gain):")
    gain_wszystkie = przyrost_informacji(atrybuty, decyzje)
    for i, g in enumerate(gain_wszystkie, start=1):
        print(f"Gain(a{i}, T) = {g:.6f}")

    print("\nSplitInfo dla każdego atrybutu:")
    splitinfo_wszystkie = split_info(atrybuty)
    for i, s in enumerate(splitinfo_wszystkie, start=1):
        print(f"SplitInfo(a{i}, T) = {s:.6f}")

    print("\nZrównoważony przyrost informacji (GainRatio) dla każdego atrybutu:")
    gr_wszystkie = gain_ratio(atrybuty, decyzje)
    for i, gr in enumerate(gr_wszystkie, start=1):
        print(f"GainRatio(a{i}, T) = {gr:.6f}")

    print("\n\n### REKURENCYJNA BUDOWA DRZEWA ###")
    buduj_drzewo(atrybuty, decyzje)

    print("\n Wizualizacja:", nazwa)
    drukuj_drzewo_tekstowo(buduj_drzewo_struktura(atrybuty, decyzje))

    print("\n")  # odstęp między plikami
