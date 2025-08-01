class Node:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.start = -1
        self.end = -1
        self.id = -1
        self.suffix_start = -1

class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"
        self.n = len(self.text)
        self.root = Node() # root 
        self.root.suffix_link = self.root
        self.active_node = self.root # aktulany aktywny
        self.active_edge = 0 # idx w tekscie nowego znaku
        self.active_length = 0 # len dopasowania
        self.remainder = 0 # dodanie sufixow w bierzacej fazie
        self.global_end = -1
        self.node_count = 0
        self.build_tree()

    def get_edge_length(self, node):
        if node.end == -1: return self.global_end - node.start + 1 # konczy sie globalu
        else: return node.end - node.start + 1 # konczy sie na wezle

    def walk_down(self, node): # skip / count, przesuwamy jesli active_length jest większe lub równe długości bieżącej krawędzi.
        edge_length = self.get_edge_length(node)
        if self.active_length >= edge_length:
            self.active_edge += edge_length
            self.active_length -= edge_length
            self.active_node = node # aktywnym wezlem staje sie dziecko
            return True # zeszlismy nizej 
        return False # nie, active_point jest na krawedzi

    def new_node(self, start, end=None): # nowy wezel
        node = Node()
        node.start = start
        if end is None: node.end = -1 
        else: node.end = end
        node.id = self.node_count
        self.node_count += 1
        return node

    def build_tree(self):
        for i in range(self.n): # przetwarzanie i-tego chara
            self.global_end = i # wydluzamy wszystkie
            self.remainder += 1 # nowy suffix do dodania
            last_new_node = None # ostatnio utworzony wezel wewnetrzny, umozliwia ustawienie lacza sufixowego
            
            while self.remainder > 0:  
                if self.active_length == 0: self.active_edge = i 
                
                #czy z active_node wychodzi krawedz zaczynajaca się od znaku text[self.active_edge]
                current_char_for_edge = self.text[self.active_edge]

                if current_char_for_edge not in self.active_node.children:
                    # nie ma krawedzi zaczynajacej się od current_char_for_edge.
                    leaf = self.new_node(i) 
                    leaf.suffix_start = i - self.remainder + 1 
                    self.active_node.children[current_char_for_edge] = leaf
                    
                    if last_new_node is not None:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                else:
                    next_node = self.active_node.children[current_char_for_edge]
                    
                    # skip/count
                    if self.walk_down(next_node):
                        continue 

                    # active_point jest gdzies na krawedzi do next_node.
                    if self.text[next_node.start + self.active_length] == self.text[i]:
                        # znak pasuje 
                        if last_new_node is not None and self.active_node != self.root:
                            last_new_node.suffix_link = self.active_node
                            last_new_node = None
                        
                        self.active_length += 1
                        break 

                    # Znak nie pasuje. Musimy split.
                    
                    split_end = next_node.start + self.active_length - 1 
                    split_node = self.new_node(next_node.start, split_end)
                    
                    self.active_node.children[current_char_for_edge] = split_node
                
                    leaf = self.new_node(i) 
                    leaf.suffix_start = i - self.remainder + 1
                    split_node.children[self.text[i]] = leaf 
                    
                    next_node.start += self.active_length 
                    split_node.children[self.text[next_node.start]] = next_node 

                    if last_new_node is not None: last_new_node.suffix_link = split_node
                    
                    last_new_node = split_node
                
                self.remainder -= 1
                
                if self.active_node == self.root and self.active_length > 0:
                    # jesli jestesmy w korzeniu i active_length > 0,to znaczy, ze przetwarzalismy sufiks S = cX
                    # nastepny sufiks to X.
                    self.active_length -= 1
                    # active_edge musi teraz wskazywać na poczatek sufiksu X.
                    self.active_edge = i - self.remainder + 1 
                elif self.active_node != self.root:
                    # wezel z lacza
                    if self.active_node.suffix_link is not None:
                        self.active_node = self.active_node.suffix_link
                    else:
                        self.active_node = self.root

    def get_all_substrings_with_positions(self):
        substrings = {}
        self._dfs_substrings(self.root, "", substrings)
        return substrings

    def find_pattern(self, pattern: str) -> list[int]:
        if not pattern:
            return []
        
        current_node = self.root
        pattern_pos = 0 # 
        pattern_len = len(pattern)
        
        while pattern_pos < pattern_len:
            char_to_match = pattern[pattern_pos] 
            
            # czy z current_node krawedz zaczyna sie od char_to_match
            if char_to_match not in current_node.children: return []
            
            next_node = current_node.children[char_to_match] # Wwezel
            edge_len = self.get_edge_length(next_node) 
            compare_len = min(edge_len, pattern_len - pattern_pos) 
            
            edge_text_segment = self.text[next_node.start : next_node.start + compare_len]
            pattern_segment = pattern[pattern_pos : pattern_pos + compare_len]
            
            if edge_text_segment != pattern_segment: return [] 
            
            pattern_pos += compare_len
            current_node = next_node
 
        positions = []
        self._collect_leaves(current_node, positions) 
        return sorted(list(set(positions))) 

    def _collect_leaves(self, node, positions):
        if not node.children: #nie ma dzieci to jest lisciem
            start_pos = node.suffix_start 
            if start_pos != -1: 
                positions.append(start_pos)
        else:
            for child in node.children.values():
                self._collect_leaves(child, positions)

    def _get_leaf_suffix_start(self, leaf_node): return leaf_node.suffix_start

    def print_tree(self, node=None, depth=0, edge_char=""):
        if node is None:
            node = self.root
            print("Drzewo sufiksów:")
        
        if node != self.root:
            edge_str = self.text[node.start:node.start + self.get_edge_length(node)]
            suffix_info = f" (suffix_start: {node.suffix_start})" if node.suffix_start != -1 else ""
            print("  " * depth + f"--({edge_char})-- [{edge_str}] (id: {node.id}){suffix_info}")
        
        for char, child in sorted(node.children.items()): self.print_tree(child, depth + 1, char)

def test_suffix_tree():
    print("=== TESTY DRZEWA SUFIKSÓW ===\n")
    
    # Test 1: Prosty tekst
    print("Test 1: Tekst 'banana'")
    tree1 = SuffixTree("banana")
    print(f"Szukanie 'ana': {tree1.find_pattern('ana')} (oczekiwane: [1, 3])")
    print(f"Szukanie 'nan': {tree1.find_pattern('nan')} (oczekiwane: [2])")
    print(f"Szukanie 'a': {tree1.find_pattern('a')} (oczekiwane: [1, 3, 5])")
    print(f"Szukanie 'banana': {tree1.find_pattern('banana')} (oczekiwane: [0])")
    print(f"Szukanie 'xyz': {tree1.find_pattern('xyz')} (oczekiwane: [])")
    print()
    
    # Test 2: Tekst z powtórzeniami
    print("Test 2: Tekst 'abcabxabcd'")
    tree2 = SuffixTree("abcabxabcd")
    print(f"Szukanie 'abc': {tree2.find_pattern('abc')} (oczekiwane: [0, 6])")
    print(f"Szukanie 'ab': {tree2.find_pattern('ab')} (oczekiwane: [0, 3, 6])")
    print(f"Szukanie 'x': {tree2.find_pattern('x')} (oczekiwane: [5])")
    print()
    
    # Test 3: Tekst z wszystkimi identycznymi znakami
    print("Test 3: Tekst 'aaaaa'")
    tree3 = SuffixTree("aaaaa")
    print(f"Szukanie 'a': {tree3.find_pattern('a')} (oczekiwane: [0, 1, 2, 3, 4])")
    print(f"Szukanie 'aa': {tree3.find_pattern('aa')} (oczekiwane: [0, 1, 2, 3])")
    print(f"Szukanie 'aaa': {tree3.find_pattern('aaa')} (oczekiwane: [0, 1, 2])")
    print()
    
    # Test 4: Długi tekst
    print("Test 4: Dłuższy tekst")
    long_text = "the quick brown fox jumps over the lazy dog"
    tree4 = SuffixTree(long_text)
    print(f"Szukanie 'the': {tree4.find_pattern('the')} (oczekiwane: [0, 31])")
    print(f"Szukanie 'o': {tree4.find_pattern('o')} (oczekiwane: [12, 17, 26, 41])")
    print(f"Szukanie 'fox': {tree4.find_pattern('fox')} (oczekiwane: [16])")
    print()
    
    # Test 5: Weryfikacja manualnie
    print("Test 5: Prosty tekst 'abab'")
    tree5 = SuffixTree("abab")
    print(f"Szukanie 'a': {tree5.find_pattern('a')} (oczekiwane: [0, 2])")
    print(f"Szukanie 'b': {tree5.find_pattern('b')} (oczekiwane: [1, 3])")
    print(f"Szukanie 'ab': {tree5.find_pattern('ab')} (oczekiwane: [0, 2])")
    print(f"Szukanie 'ba': {tree5.find_pattern('ba')} (oczekiwane: [1])")
    print()

if __name__ == "__main__":
    test_suffix_tree()

    print("\n=== STRUKTURA DRZEWA DLA 'banana' ===")
    tree = SuffixTree("banana")
    tree.print_tree()