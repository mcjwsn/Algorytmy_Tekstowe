def hamming_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Hamminga między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Hamminga (liczba pozycji, na których znaki się różnią)
        Jeśli ciągi mają różne długości, zwraca -1
    """
    if len(s1) != len(s2): return -1
    
    distance = 0
    for c1, c2 in zip(s1, s2):
        if c1 != c2: distance += 1
    
    return distance


def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    return bool(m & set_nth_bit(n)) # konwersja kazdej liczby innej od 0 na true


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    if not len(pattern): return []

    masks = [~0 for _ in range(256)]  # wszystkie maski na same 1 

    for i, char in enumerate(pattern):  masks[ord(char)] &= ~(1 << i) 
    
    return masks


def fuzzy_shift_or(text: str, pattern: str, k: int = 2) -> list[int]:
    """
    Implementacja przybliżonego wyszukiwania wzorca przy użyciu algorytmu Shift-Or.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania
        k: Maksymalna dopuszczalna liczba różnic (odległość Hamminga)

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
        z maksymalnie k różnicami
    """
    if not pattern or k < 0 or len(pattern) > len(text): return [] # edgecasy

    m = len(pattern)
    n = len(text)
    
    masks = make_mask(pattern) # maski 
    
    states = [(1 << m) - 1] * (k + 1) # stany, na poczatku zaden nie pasuje
    results = []
    
    for i in range(n):
        old_states = states.copy() # zapamietujemy poprzednie stany
        states[0] = ((old_states[0] << 1) | 1) & masks[ord(text[i])] # nadpisz stan dla 0 bledow
        # Shift w lewo do następnego znaku wzorca, OR z 1 ustawia najmłodszy bit (poczatek dopasowania),
        # AND z maską znaku zeruje bity tam gdzie nie pasuja
        
        for j in range(1, k + 1):
            # zastapienie | usuniecie | wstawienie
            states[j] = (((old_states[j] << 1) & masks[ord(text[i])]) | (old_states[j-1] << 1) | ((old_states[j-1] << 2) | 1))

        for j in range(k + 1):
            #najstarszy bit (m-1) w stanie j jest 0 ( dopasowanie) i maska 10..0
            if not (states[j] & set_nth_bit(m-1)):
                results.append(i - m + 1) # dopasowanie na itej pozycji
                break

    return [pos for pos in results if pos >= 0] # tylko nieujmne startowe pozycje