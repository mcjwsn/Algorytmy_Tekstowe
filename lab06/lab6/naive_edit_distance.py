def naive_edit_distance(s1: str, s2: str) -> int:
    if not s1: return len(s2)
    if not s2: return len(s1)
    # przerabiamy s1 w s2
    if s1[-1] == s2[-1]: return naive_edit_distance(s1[:-1],s2[:-1]) # takie same znaki
    else:
        return min(
            naive_edit_distance(s1,s2[:-1])+1, # wstawiamy do s1 na koniec ostatni znak z s2
            naive_edit_distance(s1[:-1],s2)+1, # usuniecie ostatniego znaku z s1
            naive_edit_distance(s1[:-1],s2[:-1]) + 1) # wymiana znaku
  

def naive_edit_distance_with_operations(s1: str, s2: str) -> tuple[int, list[str]]:
    if not s1: return len(s2), ['INSERT'] * len(s2)
    if not s2: return len(s1), ['DELETE'] * len(s1)
    
    if s1[-1] == s2[-1]:
        dist, ops = naive_edit_distance_with_operations(s1[:-1], s2[:-1])
        return dist, ops + ['MATCH']
    else:
        d1, o1 = naive_edit_distance_with_operations(s1, s2[:-1]) # INSERT
        d2, o2 = naive_edit_distance_with_operations(s1[:-1], s2) # DELETE
        d3, o3 = naive_edit_distance_with_operations(s1[:-1], s2[:-1]) # REPLACE

        if d1 <= min(d2,d3):
            return d1 + 1, o1 + ['INSERT']
        elif d2 <= min(d1,d3):
            return d2 + 1, o2 + ['DELETE']
        else:
            return d3 + 1, o3 + ['REPLACE']