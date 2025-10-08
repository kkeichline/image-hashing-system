# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
TODO: Implement authentication in production. Current implementation has no auth for development.

---

## Endpoints

### 1. Upload and Hash Image

Generate perceptual hashes from an uploaded image.

**Endpoint:** `POST /hash/upload`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file (JPEG, PNG, etc.)
  - `source`: (Optional) String identifier for the source

**Response:**
```json
{
  "hash_id": 123,
  "phash": "a1b2c3d4e5f6g7h8",
  "dhash": "1a2b3c4d5e6f7g8h",
  "ahash": "9i0j1k2l3m4n5o6p",
  "whash": "7q8r9s0t1u2v3w4x",
  "message": "Image hashed and stored successfully"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/hash/upload" \
  -F "file=@image.jpg" \
  -F "source=test_source"
```

---

### 2. Search for Similar Images

Find images similar to an uploaded image.

**Endpoint:** `POST /hash/search`

**Query Parameters:**
- `algorithm`: Hashing algorithm to use (default: `phash`)
  - Options: `phash`, `dhash`, `ahash`, `whash`
- `threshold`: Maximum Hamming distance (default: `10`, range: 0-64)
- `limit`: Maximum number of results (default: `10`, range: 1-100)

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file to search for

**Response:**
```json
{
  "query_hash": "a1b2c3d4e5f6g7h8",
  "matches": [
    {
      "hash_id": 123,
      "hash_value": "a1b2c3d4e5f6g7h8",
      "distance": 0,
      "similarity_score": 1.0,
      "classification": "identical"
    },
    {
      "hash_id": 456,
      "hash_value": "a1b2c3d4e5f6g7h9",
      "distance": 5,
      "similarity_score": 0.92,
      "classification": "very_similar"
    }
  ],
  "total_matches": 2
}
```

**Classification Levels:**
- `identical`: Distance 0-5 (identical or near-identical)
- `very_similar`: Distance 6-10 (minor edits, filters)
- `similar`: Distance 11-15 (cropped, compressed)
- `possibly_similar`: Distance 16-20 (significant changes)
- `different`: Distance 21+ (different images)

**Example:**
```bash
curl -X POST "http://localhost:8000/hash/search?algorithm=phash&threshold=10&limit=5" \
  -F "file=@search_image.jpg"
```

---

### 3. Get Statistics

Get system statistics about stored hashes.

**Endpoint:** `GET /stats`

**Response:**
```json
{
  "total_hashes": 1523,
  "algorithms": ["phash", "dhash", "ahash", "whash"]
}
```

**Example:**
```bash
curl "http://localhost:8000/stats"
```

---

### 4. Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Example:**
```bash
curl "http://localhost:8000/health"
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid algorithm specified"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing image: [error message]"
}
```

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Usage Examples

### Python Example
```python
import requests

# Upload and hash
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/hash/upload',
        files={'file': f},
        data={'source': 'my_app'}
    )
print(response.json())

# Search for similar
with open('search.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/hash/search',
        files={'file': f},
        params={
            'algorithm': 'phash',
            'threshold': 10,
            'limit': 5
        }
    )
print(response.json())
```

### JavaScript Example
```javascript
// Upload and hash
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('source', 'web_app');

const response = await fetch('http://localhost:8000/hash/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data);
```

---

## Rate Limiting

TODO: Implement rate limiting in production to prevent abuse.

Suggested limits:
- 100 requests per minute per IP for hash generation
- 50 requests per minute per IP for searches

---

## Best Practices

1. **Always check the health endpoint** before making requests
2. **Use appropriate thresholds** for your use case
   - Lower threshold (0-5) for exact matches
   - Medium threshold (5-15) for similar images
   - Higher threshold (15-25) for fuzzy matching
3. **Limit result size** to avoid overwhelming responses
4. **Cache results** when appropriate
5. **Handle errors gracefully** - network issues, invalid images, etc.

---

## TODO for Production

- [ ] Add authentication (API keys, OAuth)
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Add response caching
- [ ] Add batch upload endpoint
- [ ] Add hash deletion endpoint
- [ ] Add filtering by source/date
- [ ] Add pagination for large result sets
- [ ] Add WebSocket support for real-time matching
- [ ] Add metrics/monitoring endpoints
