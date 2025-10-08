"""
Pytest configuration and shared fixtures.
"""

import pytest
import os


@pytest.fixture(scope="session")
def test_data_dir():
    """Directory for test data files."""
    return os.path.join(os.path.dirname(__file__), "test_data")


@pytest.fixture
def sample_image_path(test_data_dir):
    """
    Path to sample test image.

    TODO: Add actual test images to tests/test_data/ directory
    """
    return os.path.join(test_data_dir, "sample.jpg")


# Add more shared fixtures as needed
