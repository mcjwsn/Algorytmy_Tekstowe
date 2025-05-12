# <p align="center">Algorytmy tekstowe</p>
## <p align="center">Maciej Wisniewski wtorek 13.15 A</p>
# <p align="center">Laboratorium 4 - Wyszukiwanie wzorców (2)</p>
### <p align="center"> Zadanie 1 Algorytm Shift-Or </p>

```python
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

def shift_or(text: str, pattern: str) -> list[int]:
    """
    Implementacja algorytmu Shift-Or do wyszukiwania wzorca.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
    """

    m = len(pattern)
    n = len(text)
    

    if m == 0 or m > n: return []
    if m == n: return [0] if text == pattern else []

    result = []
    masks = make_mask(pattern) # zwracamy maski patternu
    state = ~0 # wszystkie bity ustawiamy na 1
    match_bit = 1 << (m - 1) #Tworzy maskę, która ma ustawiony tylko najbardziej znaczący bit, jesli sie zmieni to znalazlo pattern

    for i in range(n):

        state = (state << 1) | masks[ord(text[i])] # przeuwamy bit w lewo i patrzymy czy pattern sie zachowuje
        # Sprawdzenie, czy znaleziono dopasowanie
        # jesli najbardziej znaczy bit matcha jest 0 to znalazl dopasowanie w tekscie
        if (state & match_bit) == 0:
            # Jesli najbardziej znaczacy bit w state jest ustawiony na 0 -> dopasowalo sie prefiks o m
            match_pos = i - m + 1
            
            if match_pos >= 0: # poczatkowa pozycja jest dodatnia
                if text[match_pos:match_pos+m] == pattern: result.append(match_pos)
    
    return result
```

### <p align="center"> Zadanie 2 Przybliżone wyszukiwanie wzorca </p>
```python
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
```


### <p align="center"> Zadanie 3 Odległość Levenshteina </p>
```python
def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if not s1: return len(s2) # edge case
    if not s2: return len(s1)

    n1 = len(s1)
    n2 = len(s2)

    dp = [[0 for _ in range(n2+1)] for _ in range(n1+1)]

    for i in range(n1+1): dp[i][0] = i # usuwanie i znakow

    for i in range(1,n2+1): dp[0][i] = i # wstawianie j znakow
    # dp[i][j] to minimalna liczba operacji wstaw,suun,zmien potrzebna do zmiany pierwszych i znakow z s1 w pierwsze j znakow z s2.
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,   dp[i][j - 1] + 1,  dp[i - 1][j - 1] + cost)  # usunięcie, wstaw, zmien
        
    return dp[n1][n2]
```

### <p align="center"> Zadanie 4 Algorytm Aho-Corasick </p>
```python
from collections import deque
from typing import List, Tuple, Optional, Dict

class AhoCorasickNode:
    def __init__(self):
        # tworzenie węzła
        self.transitions: Dict[str, 'AhoCorasickNode'] = {} # przejscie
        
        self.failure_link: Optional['AhoCorasickNode'] = None # inny wezle w przypadku braku dopasowanai
        
        self.output: List[str] = [] # konczace sie na tym wezle


class AhoCorasick:
    def __init__(self, patterns: List[str]):

        self.patterns = [p for p in patterns if p] # usuwanie pustych
        self.root = AhoCorasickNode()
        
        # budwoanie struktry
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        for pattern in self.patterns: # kadzy wzorzec do drzewa
            current_node = self.root

            for char in pattern: # kazdy znak do drzewa
                if char not in current_node.transitions: current_node.transitions[char] = AhoCorasickNode()
                current_node = current_node.transitions[char]
            # dodajemy wzorzec do listy wyjsc dla ostatniego wezla
            current_node.output.append(pattern)

    def _build_failure_links(self):
        queue = deque() # kolejka do bfsa
        
        # lacze awaryjne dla wezlow
        for char, node in self.root.transitions.items():
            node.failure_link = self.root
            queue.append(node)
        
        # BFS
        while queue:
            current_node = queue.popleft()
            
            # dla przejść
            for char, child_node in current_node.transitions.items():
                queue.append(child_node)
                
                # lacze awaryjne dla dziecka
                failure_node = current_node.failure_link
                
                # szukamy wezla pod lacze awaryjne
                while failure_node is not self.root and char not in failure_node.transitions: failure_node = failure_node.failure_link
                # jesli przejscie dla znaku istnieje, ustawiamy lacze, jesli nie wskazujemy korzen
                if char in failure_node.transitions:
                    child_node.failure_link = failure_node.transitions[char]
                else:
                    child_node.failure_link = self.root
                
                # wyjscie przez lacze awaryjne
                child_node.output += child_node.failure_link.output

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        results = []
        if not self.patterns: return results
        
        current_node = self.root
        
        for i, char in enumerate(text):
            # znajdzie przejscie
            while current_node is not self.root and char not in current_node.transitions: current_node = current_node.failure_link
            
            # jesli jest, przejdz do wezla
            if char in current_node.transitions:
                current_node = current_node.transitions[char]
                
                # czy w tym wezle koczy sie wzorzec
                for pattern in current_node.output:
                    # znadjuejmy pozycje poczatkowa
                    start_index = i - len(pattern) + 1
                    results.append((start_index, pattern))
        
        return results
```


### <p align="center"> Zadanie 5 Wyszukiwanie wzorców dwuwymiarowych </p>
```python
def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    results = [] 
    text_len = len(text_column) 

    # przechodzimy po wzorcach
    for col_idx, pattern_col in enumerate(pattern_columns):
        pattern_len = len(pattern_col) 

        if pattern_len == 0 or pattern_len > text_len: continue

        # przesun wzorzec po tekscie
        for pos in range(text_len - pattern_len + 1):
            # czy fragment pasuje
            if text_column[pos:pos+pattern_len] == pattern_col: results.append((pos, col_idx)) # dodaj pozycje,index 

    return results


def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    if not text or not pattern or len(text) == 0 or len(pattern) == 0:  return []
    text_height = len(text)
    text_width = len(text[0]) 
    pattern_height = len(pattern)
    pattern_width = len(pattern[0]) 

    if pattern_height > text_height or pattern_width > text_width: return []

    results = [] 

    # mozliwe pozycje startowe wierszy
    for i in range(text_height - pattern_height + 1):
        # mozliwe pozycje startowe kolumn
        for j in range(text_width - pattern_width + 1):
            match = True 

            for pi in range(pattern_height):
                if text[i + pi][j:j + pattern_width] != pattern[pi]: # porwnianie wiersz z fragmentem tekstu
                    match = False 
                    break 
            
            # czy wiersze pasuja
            if match: results.append((i, j)) # Dodajemy pozycje lewego gornego

    return results
```


