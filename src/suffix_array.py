import numpy as np


class InvertedSuffixArray:
    def __init__(self):
        self.strings = []
        self.text = ""
        self.suffix_array = np.array([], dtype=np.int32)

    # -------------------------------
    # String inversion
    # -------------------------------
    def invert_string(self, s: str) -> str:
        return s[::-1]

    # -------------------------------
    # Insert: invert string and rebuild
    # -------------------------------
    def insert(self, word: str) -> None:
        word = self.invert_string(word)
        self.strings.append(word)
        self._rebuild_suffix_array()

    # -------------------------------
    # Build suffix array (O(n log n))
    # -------------------------------
    def _rebuild_suffix_array(self) -> None:
        # Concatenate all inverted strings with unique delimiters
        self.text = ""
        for i, s in enumerate(self.strings):
            # Use Unicode private-use characters as separators
            self.text += s + chr(0xE000 + i)

        # Generate and sort suffixes
        suffixes = [(self.text[i:], i) for i in range(len(self.text))]
        suffixes.sort()

        # Store indices in a NumPy array (sequential memory)
        self.suffix_array = np.array(
            [idx for _, idx in suffixes],
            dtype=np.int32
        )

    # -------------------------------
    # Search: binary search (O(m log n))
    # -------------------------------
    def search(self, pattern: str) -> bool:
        pattern = self.invert_string(pattern)
        left = self._lower_bound(pattern)

        if left >= len(self.suffix_array):
            return False

        start = self.suffix_array[left]
        return self.text[start:start + len(pattern)] == pattern

    # -------------------------------
    # Range search: binary search bounds
    # -------------------------------
    def range_search(self, pattern: str):
        pattern = self.invert_string(pattern)

        left = self._lower_bound(pattern)
        right = self._upper_bound(pattern)

        results = set()
        for i in range(left, right):
            start = self.suffix_array[i]
            suffix = self.text[start:]

            # Extract original word (before delimiter)
            for ch in suffix:
                if ord(ch) >= 0xE000:
                    break
            word = suffix[:suffix.index(ch)][::-1]
            results.add(word)

        return list(results)

    # -------------------------------
    # Delete: remove string and rebuild
    # -------------------------------
    def delete(self, word: str) -> None:
        word = self.invert_string(word)
        if word in self.strings:
            self.strings.remove(word)
            self._rebuild_suffix_array()

    # -------------------------------
    # Binary search helpers
    # -------------------------------
    def _lower_bound(self, pattern: str) -> int:
        lo, hi = 0, len(self.suffix_array)
        while lo < hi:
            mid = (lo + hi) // 2
            start = self.suffix_array[mid]
            if self.text[start:] < pattern:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def _upper_bound(self, pattern: str) -> int:
        lo, hi = 0, len(self.suffix_array)
        while lo < hi:
            mid = (lo + hi) // 2
            start = self.suffix_array[mid]
            if self.text[start:].startswith(pattern):
                lo = mid + 1
            else:
                hi = mid
        return lo

    # -------------------------------
    # Memory usage (bytes)
    # -------------------------------
    def memory_usage(self) -> int:
        text_bytes = len(self.text.encode("utf-8"))
        strings_bytes = sum(len(s.encode("utf-8")) for s in self.strings)
        array_bytes = self.suffix_array.nbytes

        return text_bytes + strings_bytes + array_bytes
