"""
Tests for the REST API.

TODO: Implement tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

# TODO: Uncomment when API is implemented
# from src.api.main import app

# client = TestClient(app)


def test_health_check():
    """
    Test the health check endpoint.

    TODO:
    1. Make GET request to /health
    2. Assert status 200
    3. Assert response contains "healthy"
    """
    # response = client.get("/health")
    # assert response.status_code == 200
    # assert response.json()["status"] == "healthy"
    pass


def test_get_stats():
    """
    Test the stats endpoint.

    TODO:
    1. Make GET request to /stats
    2. Assert status 200
    3. Assert response contains expected fields
    """
    pass


def test_upload_image():
    """
    Test uploading and hashing an image.

    TODO:
    1. Create test image
    2. POST to /hash/upload
    3. Assert status 200
    4. Assert response contains hash_id and hash values
    """
    pass


def test_upload_invalid_file():
    """
    Test uploading non-image file.

    TODO:
    1. Upload invalid file (text file)
    2. Assert appropriate error response
    """
    pass


def test_search_similar():
    """
    Test searching for similar images.

    TODO:
    1. Upload an image first
    2. Search with same image
    3. Assert match is found
    4. Assert distance is 0
    """
    pass


def test_search_with_threshold():
    """
    Test search with custom threshold.

    TODO:
    1. Upload multiple images
    2. Search with specific threshold
    3. Assert only matches within threshold returned
    """
    pass


def test_search_with_different_algorithm():
    """
    Test search using different algorithms.

    TODO:
    1. Upload image
    2. Search with dhash, ahash, whash
    3. Assert each works correctly
    """
    pass


def test_search_invalid_algorithm():
    """
    Test search with invalid algorithm.

    TODO:
    1. Try to search with invalid algorithm name
    2. Assert appropriate error response
    """
    pass


def test_upload_with_source():
    """
    Test uploading with source metadata.

    TODO:
    1. Upload with source parameter
    2. Assert hash stored with source
    """
    pass


# Hint: Run with: pytest tests/test_api.py -v
