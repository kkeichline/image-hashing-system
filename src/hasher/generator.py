"""
Image hash generation using multiple perceptual hashing algorithms.

TODO: Implement the ImageHasher class with the following methods:
- __init__(hash_size=8)
- generate_hash(image_data, algorithm='phash')
- generate_all_hashes(image_data)
- hash_distance(hash1, hash2)

Refer to the project guide for implementation details.
"""

from typing import Optional, Dict
from PIL import Image
import imagehash
import io


class ImageHasher:
    """Generate perceptual hashes from images."""

    ALGORITHMS = {
        "phash": imagehash.phash,  # Perceptual hash (most common)
        "dhash": imagehash.dhash,  # Difference hash (fast)
        "ahash": imagehash.average_hash,  # Average hash (simple)
        "whash": imagehash.whash,  # Wavelet hash (robust)
    }

    def __init__(self, hash_size: int = 8):
        """
        Initialize hasher.

        Args:
            hash_size: Size of hash (8 = 64-bit hash)

        TODO: Store the hash_size parameter
        """
        pass

    def generate_hash(self, image_data: bytes, algorithm: str = "phash") -> str:
        """
        Generate hash from image data.

        Args:
            image_data: Raw image bytes
            algorithm: Hashing algorithm to use

        Returns:
            Hash as hexadecimal string

        TODO:
        1. Validate the algorithm is in ALGORITHMS
        2. Load image from bytes using PIL
        3. Convert to RGB if needed
        4. Generate hash using the selected algorithm
        5. Return hash as string
        """
        pass

    def generate_all_hashes(self, image_data: bytes) -> Dict[str, str]:
        """
        Generate hashes using all algorithms.

        TODO: Loop through ALGORITHMS and generate hash for each
        """
        pass

    def hash_distance(self, hash1: str, hash2: str) -> int:
        """
        Calculate Hamming distance between two hashes.

        Returns:
            Number of differing bits (0 = identical)

        TODO:
        1. Convert hex strings to hash objects
        2. Calculate Hamming distance (use the - operator)
        3. Return the distance
        """
        pass
