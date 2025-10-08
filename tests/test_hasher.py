"""
Tests for hash generation.

TODO: Implement tests for the ImageHasher class.
"""

import pytest
from PIL import Image
import io

# TODO: Uncomment when ImageHasher is implemented
# from src.hasher.generator import ImageHasher


def create_test_image(size=(100, 100), color="red"):
    """
    Create a simple test image.

    This is a helper function to generate test images without
    needing actual image files.
    """
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_hash_generation():
    """
    Test basic hash generation.

    TODO:
    1. Create ImageHasher instance
    2. Generate test image
    3. Generate hash
    4. Assert hash is correct type and length
    """
    # hasher = ImageHasher()
    # image_data = create_test_image()
    # hash_value = hasher.generate_hash(image_data)
    # assert isinstance(hash_value, str)
    # assert len(hash_value) == 16  # 64-bit hash = 16 hex chars
    pass


def test_identical_images_produce_same_hash():
    """
    Identical images should have identical hashes.

    TODO:
    1. Create hasher
    2. Generate test image
    3. Hash the same image twice
    4. Assert hashes are identical
    """
    pass


def test_similar_images_have_small_distance():
    """
    Similar images should have low Hamming distance.

    TODO:
    1. Create two very similar images (slightly different colors)
    2. Hash both images
    3. Calculate distance
    4. Assert distance is small but not zero
    """
    pass


def test_different_images_have_large_distance():
    """
    Very different images should have high Hamming distance.

    TODO:
    1. Create two very different images (red vs blue)
    2. Hash both images
    3. Calculate distance
    4. Assert distance is large
    """
    pass


def test_all_algorithms():
    """
    Test all hashing algorithms.

    TODO:
    1. Generate test image
    2. Call generate_all_hashes()
    3. Assert all algorithm hashes are present
    """
    pass


def test_invalid_algorithm():
    """
    Test that invalid algorithm raises error.

    TODO:
    1. Try to generate hash with invalid algorithm
    2. Assert ValueError is raised
    """
    pass


def test_image_format_conversion():
    """
    Test that different image formats work correctly.

    TODO:
    1. Create images in different formats (JPEG, PNG, GIF)
    2. Hash each format
    3. Assert all succeed
    """
    pass


def test_hash_distance_calculation():
    """
    Test Hamming distance calculation.

    TODO:
    1. Create hasher
    2. Use known hash values
    3. Calculate distance
    4. Assert correct distance
    """
    pass


# Hint: You can run these tests with:
# pytest tests/test_hasher.py -v
