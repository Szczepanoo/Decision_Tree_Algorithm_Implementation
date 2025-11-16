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




# PRZYKŁAD UŻYCIA

pliki = ["dane1.txt", "dane2.txt", "dane3.txt"]

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

    print("\n")  # odstęp między plikami

