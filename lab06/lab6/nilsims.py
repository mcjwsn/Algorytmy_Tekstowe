import hashlib
from typing import List, Tuple


class NilsimsHash:
    """Klasa implementująca algorytm Nilsimsa."""

    def __init__(self):
        """Inicjalizuje hash Nilsimsa."""
        self.hash_size = 256  # 256-bitowy hash
        self.bucket_count = self.hash_size * 2

    def _rolling_hash(self, text: str) -> List[int]:
        """
        Oblicza rolling hash dla tekstu.

        Zwraca listę hashów MD5 trigramów.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista wartości rolling hash
        """
        trigrams = self._trigrams(text)
        return [
            int(hashlib.md5(tri.encode('utf-8')).hexdigest(), 16)
            for tri in trigrams
        ]

    def _trigrams(self, text: str) -> List[str]:
        """
        Generuje trigramy z tekstu.

        Args:
            text: Tekst do przetworzenia

        Returns:
            Lista trigramów
        """
        text = text.lower()
        return [text[i:i+3] for i in range(len(text) - 2)]

    def compute_hash(self, text: str) -> bytes:
        """
        Oblicza hash Nilsimsa dla tekstu.

        Args:
            text: Tekst do zahashowania

        Returns:
            256-bitowy hash jako bytes
        """
        buckets = [0] * self.bucket_count
        hashes = self._rolling_hash(text)

        for h in hashes:
            for i in range(self.hash_size):
                bit = (h >> i) & 1
                if bit:
                    buckets[i] += 1
                else:
                    buckets[i] -= 1

        fingerprint = 0
        for i in range(self.hash_size):
            if buckets[i] >= 0:
                fingerprint |= (1 << i)

        return fingerprint.to_bytes(self.hash_size // 8, byteorder='big')

    def compare_hashes(self, hash1: bytes, hash2: bytes) -> float:
        """
        Porównuje dwa hashe Nilsimsa i zwraca stopień podobieństwa.

        Args:
            hash1: Pierwszy hash
            hash2: Drugi hash

        Returns:
            Stopień podobieństwa w zakresie [0, 1]
        """
        if len(hash1) != len(hash2):
            raise ValueError("Hashy muszą mieć tę samą długość")

        dist = sum(bin(b1 ^ b2).count("1") for b1, b2 in zip(hash1, hash2))
        return 1 - dist / self.hash_size


def nilsims_similarity(text1: str, text2: str) -> float:
    """
    Oblicza podobieństwo między dwoma tekstami używając algorytmu Nilsimsa.

    Args:
        text1: Pierwszy tekst
        text2: Drugi tekst

    Returns:
        Stopień podobieństwa w zakresie [0, 1]
    """
    hasher = NilsimsHash()
    hash1 = hasher.compute_hash(text1)
    hash2 = hasher.compute_hash(text2)
    return hasher.compare_hashes(hash1, hash2)


def find_similar_texts(target: str, candidates: List[str], threshold: float = 0.7) -> List[Tuple[int, float]]:
    """
    Znajduje teksty podobne do tekstu docelowego.

    Args:
        target: Tekst docelowy
        candidates: Lista kandydatów
        threshold: Próg podobieństwa

    Returns:
        Lista krotek (indeks, podobieństwo) dla tekstów powyżej progu
    """
    hasher = NilsimsHash()
    target_hash = hasher.compute_hash(target)

    results = []
    for i, candidate in enumerate(candidates):
        candidate_hash = hasher.compute_hash(candidate)
        similarity = hasher.compare_hashes(target_hash, candidate_hash)
        if similarity >= threshold:
            results.append((i, similarity))

    return results
