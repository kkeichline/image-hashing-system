# Architecture Documentation

## System Overview

The Image Hash System is a privacy-preserving image similarity detection system that uses perceptual hashing to identify similar images without storing the actual images.

## High-Level Architecture

```
┌─────────────┐
│   Client    │
│ (CLI/API)   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  ┌──────────┐  ┌────────────────┐  │
│  │ Upload   │  │ Search Similar │  │
│  │ Endpoint │  │   Endpoint     │  │
│  └──────────┘  └────────────────┘  │
└──────┬──────────────────┬───────────┘
       │                  │
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   Hasher    │    │   Matcher   │
│   Module    │    │   Module    │
└──────┬──────┘    └──────┬──────┘
       │                  │
       └──────────┬───────┘
                  ▼
          ┌─────────────┐
          │  Repository │
          │   (Storage) │
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │  Database   │
          │ (PostgreSQL)│
          └─────────────┘
```

## Component Details

### 1. Hasher Module (`src/hasher/`)

**Purpose:** Generate perceptual hashes from images

**Components:**
- `generator.py`: Main hashing logic
  - `ImageHasher` class
  - Supports multiple algorithms (pHash, dHash, aHash, wHash)
  - Handles image loading and preprocessing

**Key Algorithms:**

1. **pHash (Perceptual Hash)** - DEFAULT
   - Most robust to image modifications
   - Uses DCT (Discrete Cosine Transform)
   - Good for detecting similar images with edits

2. **dHash (Difference Hash)**
   - Fastest algorithm
   - Based on gradient differences
   - Good for identical/near-identical detection

3. **aHash (Average Hash)**
   - Simplest algorithm
   - Based on average pixel values
   - Less robust but very fast

4. **wHash (Wavelet Hash)**
   - Most robust to geometric transformations
   - Uses Haar wavelet transform
   - Slowest but most accurate

**Hash Properties:**
- 64-bit hash (8x8 grid)
- Represented as 16-character hex string
- Hamming distance for comparison (0-64)

### 2. Storage Module (`src/storage/`)

**Purpose:** Persist hashes and provide data access

**Components:**

1. **`database.py`**: SQLAlchemy Models
   - `ImageHash`: Stores hash values and metadata
   - `MatchResult`: Stores search results (optional)

2. **`repository.py`**: Data Access Layer
   - `HashRepository` class
   - CRUD operations for hashes
   - Similarity search implementation

**Database Schema:**

```sql
-- image_hashes table
CREATE TABLE image_hashes (
    id SERIAL PRIMARY KEY,
    phash VARCHAR(16) NOT NULL,
    dhash VARCHAR(16),
    ahash VARCHAR(16),
    whash VARCHAR(16),
    phash_int BIGINT,  -- For faster comparisons
    source VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_phash ON image_hashes(phash);
CREATE INDEX idx_phash_int ON image_hashes(phash_int);
CREATE INDEX idx_timestamp ON image_hashes(timestamp);

-- match_results table (optional)
CREATE TABLE match_results (
    id SERIAL PRIMARY KEY,
    query_hash_id INTEGER NOT NULL,
    matched_hash_id INTEGER NOT NULL,
    distance INTEGER NOT NULL,
    algorithm VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Matcher Module (`src/matcher/`)

**Purpose:** Find similar images based on hash comparisons

**Components:**
- `similarity.py`: Matching logic
  - `SimilarityMatcher` class
  - `MatchResult` dataclass
  - Match classification

**Matching Process:**
1. Query database for all hashes
2. Calculate Hamming distance for each
3. Filter by threshold
4. Sort by distance (most similar first)
5. Classify match quality

**Match Classification:**
- **Identical** (0-5 bits): Same or near-same image
- **Very Similar** (6-10 bits): Minor edits, filters
- **Similar** (11-15 bits): Crops, compression
- **Possibly Similar** (16-20 bits): Significant changes
- **Different** (21+ bits): Unrelated images

### 4. API Module (`src/api/`)

**Purpose:** RESTful API for system interaction

**Components:**
- `main.py`: FastAPI application
  - Upload endpoint
  - Search endpoint
  - Stats endpoint
  - Health check

**Technology:**
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

**Features:**
- Automatic OpenAPI documentation
- Type validation
- Async support
- Error handling

### 5. CLI Module (`src/cli/`)

**Purpose:** Command-line interface

**Components:**
- `commands.py`: Click-based CLI
  - `hash-image`: Hash a single image
  - `batch-hash`: Hash directory of images
  - `find-similar`: Search for similar images

**Usage:**
```bash
# Hash single image
python -m src.cli.commands hash-image image.jpg

# Hash directory
python -m src.cli.commands batch-hash ./images/

# Find similar
python -m src.cli.commands find-similar query.jpg --threshold 10
```

## Data Flow

### Upload Flow

```
1. Client uploads image
   ↓
2. API receives file bytes
   ↓
3. Hasher generates all hashes
   ↓
4. Repository stores hashes
   ↓
5. Return hash ID and values
```

### Search Flow

```
1. Client uploads query image
   ↓
2. API receives file bytes
   ↓
3. Hasher generates query hash
   ↓
4. Matcher searches repository
   ↓
5. Calculate distances for all hashes
   ↓
6. Filter by threshold
   ↓
7. Sort and limit results
   ↓
8. Return matches with scores
```

## Performance Considerations

### Hashing Performance
- **Speed**: ~1000-5000 hashes/second (depends on image size)
- **Bottleneck**: Image I/O and decoding
- **Optimization**: Use smaller hash sizes for faster processing

### Search Performance
- **Linear Search**: O(n) - Compare against all hashes
- **Current Implementation**: Suitable for 10K-100K hashes
- **Bottleneck**: Hamming distance calculation

### Scaling Strategies

#### For 100K+ Hashes:
1. **Database Indexing**
   - B-tree index on hash values
   - Integer representation for faster comparison

2. **Caching**
   - Redis for frequent queries
   - Cache search results

3. **Approximate Search**
   - Use BK-trees for faster similarity search
   - Trade accuracy for speed

#### For 1M+ Hashes:
1. **Sharding**
   - Partition hashes across databases
   - Parallel search

2. **Approximate Nearest Neighbors**
   - Use FAISS or Annoy
   - Reduce search space

3. **Hybrid Approach**
   - First pass: Fast approximate search
   - Second pass: Precise distance calculation

## Security Considerations

### Current Implementation
⚠️ **Not production-ready** - Missing critical security features

### Required for Production:

1. **Authentication**
   - API key authentication
   - OAuth 2.0 support
   - Rate limiting per user

2. **Authorization**
   - Role-based access control
   - Audit logging
   - Access restrictions

3. **Input Validation**
   - File type validation
   - Size limits
   - Malware scanning

4. **Data Protection**
   - Encryption at rest
   - Encryption in transit (HTTPS)
   - Secure database connections

5. **Rate Limiting**
   - Prevent abuse
   - DDoS protection
   - Cost control

## Deployment Architecture

### Development
```
┌──────────────┐
│   Local Dev  │
│              │
│  FastAPI +   │
│  SQLite      │
└──────────────┘
```

### Production
```
┌─────────────┐     ┌──────────────┐
│  Load       │────▶│   API        │
│  Balancer   │     │   Servers    │
│  (nginx)    │     │   (multiple) │
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │              │
            ┌───────▼────┐  ┌──────▼─────┐
            │ PostgreSQL │  │   Redis    │
            │  (Primary) │  │   (Cache)  │
            └────────────┘  └────────────┘
```

## Monitoring & Observability

### Metrics to Track:
- Hash generation rate
- Search latency
- Database query time
- Cache hit rate
- API response times
- Error rates

### Logging:
- All API requests
- Hash operations
- Search queries
- Errors and exceptions

### Health Checks:
- Database connectivity
- Cache availability
- Disk space
- Memory usage

## Future Enhancements

### Short-term:
- [ ] Batch upload API
- [ ] Result pagination
- [ ] Hash deletion endpoint
- [ ] Better error messages

### Medium-term:
- [ ] BK-tree for faster search
- [ ] Redis caching layer
- [ ] Metrics dashboard
- [ ] Batch processing queue

### Long-term:
- [ ] Multi-region deployment
- [ ] Real-time matching
- [ ] Machine learning similarity
- [ ] Video hash support

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock external dependencies
- Test edge cases

### Integration Tests
- Test component interactions
- Test database operations
- Test API endpoints

### Performance Tests
- Benchmark hash generation
- Benchmark search performance
- Load testing

### Security Tests
- Input validation
- SQL injection prevention
- File upload security

## Development Setup

See README.md for detailed setup instructions.

## References

- [ImageHash Library](https://github.com/JohannesBuchner/imagehash)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Perceptual Hashing Paper](http://www.phash.org/)
