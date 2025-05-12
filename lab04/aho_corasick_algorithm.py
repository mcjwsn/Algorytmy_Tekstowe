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