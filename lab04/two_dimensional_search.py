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