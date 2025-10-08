# Privacy-Preserving Image Hash System
## Complete Implementation Guide

---

## 📋 PROJECT OVERVIEW

**What You're Building:**
A system that can identify similar/identical images without storing the actual images - critical for CSAM detection while preserving privacy.

**Core Concept:**
- Images → Perceptual Hashes (fingerprints)
- Store only hashes, never original images
- Match similar images even with minor modifications (crops, filters, compression)
- Fast matching at scale

**Real-World Use:**
- NCMEC, IWF, and Thorn all use variations of this technology
- Microsoft's PhotoDNA is based on similar principles
- Critical for detecting known CSAM without storing illegal content

---

## 🎯 PROJECT GOALS

**Primary Goals:**
1. Generate perceptual hashes from images
2. Store hashes in searchable database
3. Find similar images via hash matching
4. Demonstrate performance at scale
5. Show privacy preservation

**What This Demonstrates:**
- Understanding of CSAM detection technology
- Python expertise
- Database design
- Performance optimization
- Privacy-preserving techniques
- Production-ready code quality

---

## 🏗️ ARCHITECTURE

### **High-Level Flow:**

```
Image Upload → Hash Generation → Database Storage → Similarity Search
     ↓              ↓                   ↓                  ↓
  (binary)      (64-bit int)      (indexed DB)      (Hamming distance)
```

### **Components:**

1. **Hash Generator** - Creates perceptual hashes
2. **Storage Layer** - Database for hash storage
3. **Matching Engine** - Finds similar hashes
4. **API Layer** - RESTful API for interaction
5. **CLI Tool** - Command-line interface
6. **Web UI** (optional) - Simple demo interface

---

## 🛠️ TECHNICAL STACK

### **Core Libraries:**

```python
# Hashing
imagehash==4.3.1          # Perceptual hashing algorithms
Pillow==10.2.0            # Image processing

# Storage
sqlalchemy==2.0.25        # Database ORM
psycopg2-binary==2.9.9    # PostgreSQL driver (or sqlite3)

# API
fastapi==0.109.0          # Modern Python API framework
uvicorn==0.27.0           # ASGI server
pydantic==2.5.3           # Data validation

# Performance
numpy==1.26.3             # Numerical computing
redis==5.0.1              # Caching (optional)

# Testing
pytest==7.4.4             # Testing framework
pytest-asyncio==0.23.3    # Async testing
```

### **Why These Choices:**

- **ImageHash**: Industry-standard library, implements multiple algorithms
- **FastAPI**: Modern, async, automatic API docs, type hints
- **PostgreSQL**: Production-grade, good indexing for similarity search
- **SQLAlchemy**: ORM makes database operations clean

---

## 📁 PROJECT STRUCTURE

```
image-hash-system/
├── src/
│   ├── __init__.py
│   ├── hasher/
│   │   ├── __init__.py
│   │   ├── generator.py      # Hash generation logic
│   │   └── algorithms.py     # Different hash algorithms
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py       # Database models
│   │   └── repository.py     # Data access layer
│   ├── matcher/
│   │   ├── __init__.py
│   │   └── similarity.py     # Similarity search logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   └── routes.py         # API endpoints
│   └── cli/
│       ├── __init__.py
│       └── commands.py       # CLI interface
├── tests/
│   ├── __init__.py
│   ├── test_hasher.py
│   ├── test_matcher.py
│   └── test_api.py
├── data/
│   ├── sample_images/        # Test images (benign)
│   └── .gitkeep
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── ETHICS.md             # Important!
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── LICENSE
```

---

## 💻 IMPLEMENTATION - STEP BY STEP

### **Phase 1: Hash Generation (Days 1-2)**

#### **File: `src/hasher/generator.py`**

```python
"""
Image hash generation using multiple perceptual hashing algorithms.
"""
from typing import Optional, Dict
from PIL import Image
import imagehash
import io


class ImageHasher:
    """Generate perceptual hashes from images."""
    
    ALGORITHMS = {
        'phash': imagehash.phash,      # Perceptual hash (most common)
        'dhash': imagehash.dhash,      # Difference hash (fast)
        'ahash': imagehash.average_hash,  # Average hash (simple)
        'whash': imagehash.whash,      # Wavelet hash (robust)
    }
    
    def __init__(self, hash_size: int = 8):
        """
        Initialize hasher.
        
        Args:
            hash_size: Size of hash (8 = 64-bit hash)
        """
        self.hash_size = hash_size
    
    def generate_hash(
        self, 
        image_data: bytes, 
        algorithm: str = 'phash'
    ) -> str:
        """
        Generate hash from image data.
        
        Args:
            image_data: Raw image bytes
            algorithm: Hashing algorithm to use
            
        Returns:
            Hash as hexadecimal string
        """
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        # Load image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Generate hash
        hash_func = self.ALGORITHMS[algorithm]
        hash_value = hash_func(image, hash_size=self.hash_size)
        
        return str(hash_value)
    
    def generate_all_hashes(self, image_data: bytes) -> Dict[str, str]:
        """Generate hashes using all algorithms."""
        return {
            algo: self.generate_hash(image_data, algo)
            for algo in self.ALGORITHMS.keys()
        }
    
    def hash_distance(self, hash1: str, hash2: str) -> int:
        """
        Calculate Hamming distance between two hashes.
        
        Returns:
            Number of differing bits (0 = identical)
        """
        h1 = imagehash.hex_to_hash(hash1)
        h2 = imagehash.hex_to_hash(hash2)
        return h1 - h2  # Hamming distance
```

#### **Why This Design:**
- Multiple algorithms for different use cases
- Accepts raw bytes (works with any image source)
- Returns string hashes (easy to store/compare)
- Hamming distance for similarity

---

### **Phase 2: Database Storage (Days 3-4)**

#### **File: `src/storage/database.py`**

```python
"""
Database models for hash storage.
"""
from sqlalchemy import Column, String, Integer, DateTime, Index, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class ImageHash(Base):
    """Image hash record."""
    
    __tablename__ = 'image_hashes'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Hash values (different algorithms)
    phash = Column(String(16), nullable=False, index=True)
    dhash = Column(String(16), index=True)
    ahash = Column(String(16), index=True)
    whash = Column(String(16), index=True)
    
    # Metadata
    source = Column(String(255))  # Where image came from
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Optional: Store hash as integer for faster comparison
    phash_int = Column(BigInteger, index=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_phash', 'phash'),
        Index('idx_timestamp', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<ImageHash(id={self.id}, phash={self.phash[:8]}...)>"


class MatchResult(Base):
    """Record of hash matches."""
    
    __tablename__ = 'match_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_hash_id = Column(Integer, nullable=False)
    matched_hash_id = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)  # Hamming distance
    algorithm = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_query', 'query_hash_id'),
        Index('idx_distance', 'distance'),
    )
```

#### **File: `src/storage/repository.py`**

```python
"""
Data access layer for hash operations.
"""
from typing import List, Optional, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base, ImageHash, MatchResult


class HashRepository:
    """Repository for hash storage and retrieval."""
    
    def __init__(self, database_url: str):
        """
        Initialize repository.
        
        Args:
            database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_hash(
        self, 
        hashes: Dict[str, str], 
        source: Optional[str] = None
    ) -> int:
        """
        Store image hashes.
        
        Args:
            hashes: Dictionary of algorithm -> hash
            source: Optional source identifier
            
        Returns:
            ID of stored hash record
        """
        session = self.Session()
        try:
            hash_record = ImageHash(
                phash=hashes.get('phash'),
                dhash=hashes.get('dhash'),
                ahash=hashes.get('ahash'),
                whash=hashes.get('whash'),
                source=source,
                phash_int=int(hashes.get('phash', '0'), 16)
            )
            session.add(hash_record)
            session.commit()
            return hash_record.id
        finally:
            session.close()
    
    def find_similar(
        self, 
        query_hash: str, 
        algorithm: str = 'phash',
        threshold: int = 10
    ) -> List[tuple]:
        """
        Find similar hashes.
        
        Args:
            query_hash: Hash to search for
            algorithm: Which algorithm's hashes to search
            threshold: Maximum Hamming distance
            
        Returns:
            List of (id, hash, distance) tuples
        """
        session = self.Session()
        try:
            # Get all hashes for this algorithm
            column = getattr(ImageHash, algorithm)
            all_hashes = session.query(
                ImageHash.id, 
                column
            ).all()
            
            # Calculate distances
            import imagehash
            query_h = imagehash.hex_to_hash(query_hash)
            
            results = []
            for hash_id, stored_hash in all_hashes:
                if stored_hash:
                    stored_h = imagehash.hex_to_hash(stored_hash)
                    distance = query_h - stored_h
                    if distance <= threshold:
                        results.append((hash_id, stored_hash, distance))
            
            # Sort by distance
            results.sort(key=lambda x: x[2])
            return results
            
        finally:
            session.close()
    
    def get_hash_count(self) -> int:
        """Get total number of stored hashes."""
        session = self.Session()
        try:
            return session.query(ImageHash).count()
        finally:
            session.close()
```

---

### **Phase 3: Similarity Matching (Day 5)**

#### **File: `src/matcher/similarity.py`**

```python
"""
Similarity matching engine.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class MatchResult:
    """Result of a similarity search."""
    hash_id: int
    hash_value: str
    distance: int
    similarity_score: float  # 0-1, higher is more similar
    
    @classmethod
    def from_tuple(cls, hash_id: int, hash_value: str, distance: int):
        # Convert distance to similarity score (0-64 bits)
        similarity = 1 - (distance / 64.0)
        return cls(hash_id, hash_value, distance, similarity)


class SimilarityMatcher:
    """Find similar images via hash matching."""
    
    def __init__(self, repository):
        self.repository = repository
    
    def find_matches(
        self,
        query_hash: str,
        algorithm: str = 'phash',
        threshold: int = 10,
        limit: int = 10
    ) -> List[MatchResult]:
        """
        Find similar hashes.
        
        Args:
            query_hash: Hash to search for
            algorithm: Hashing algorithm
            threshold: Max Hamming distance (0-64)
            limit: Max results to return
            
        Returns:
            List of match results, sorted by similarity
        """
        results = self.repository.find_similar(
            query_hash, 
            algorithm, 
            threshold
        )
        
        # Convert to MatchResult objects
        matches = [
            MatchResult.from_tuple(hash_id, hash_val, dist)
            for hash_id, hash_val, dist in results[:limit]
        ]
        
        return matches
    
    def classify_match(self, distance: int) -> str:
        """
        Classify match quality based on distance.
        
        Hamming distance interpretation:
        - 0-5: Identical or near-identical
        - 6-10: Very similar (minor edits)
        - 11-15: Similar (cropped/filtered)
        - 16-20: Possibly similar
        - 21+: Different
        """
        if distance <= 5:
            return "identical"
        elif distance <= 10:
            return "very_similar"
        elif distance <= 15:
            return "similar"
        elif distance <= 20:
            return "possibly_similar"
        else:
            return "different"
```

---

### **Phase 4: REST API (Days 6-7)**

#### **File: `src/api/main.py`**

```python
"""
FastAPI application for image hash system.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

from ..hasher.generator import ImageHasher
from ..storage.repository import HashRepository
from ..matcher.similarity import SimilarityMatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(
    title="Image Hash System API",
    description="Privacy-preserving image similarity detection",
    version="1.0.0"
)

# Initialize components
hasher = ImageHasher()
repository = HashRepository("postgresql://localhost/image_hashes")
matcher = SimilarityMatcher(repository)


# Response models
class HashResponse(BaseModel):
    hash_id: int
    phash: str
    dhash: Optional[str]
    ahash: Optional[str]
    whash: Optional[str]
    message: str


class MatchResponse(BaseModel):
    hash_id: int
    hash_value: str
    distance: int
    similarity_score: float
    classification: str


class SearchResponse(BaseModel):
    query_hash: str
    matches: List[MatchResponse]
    total_matches: int


# Endpoints
@app.post("/hash/upload", response_model=HashResponse)
async def upload_and_hash(
    file: UploadFile = File(...),
    source: Optional[str] = None
):
    """
    Upload image and generate hashes.
    
    The image itself is NOT stored, only the hash.
    """
    try:
        # Read image data
        image_data = await file.read()
        
        # Generate all hashes
        hashes = hasher.generate_all_hashes(image_data)
        
        # Store hashes
        hash_id = repository.store_hash(hashes, source)
        
        logger.info(f"Stored hash {hash_id} from {file.filename}")
        
        return HashResponse(
            hash_id=hash_id,
            phash=hashes['phash'],
            dhash=hashes.get('dhash'),
            ahash=hashes.get('ahash'),
            whash=hashes.get('whash'),
            message="Image hashed and stored successfully"
        )
        
    except Exception as e:
        logger.error(f"Error hashing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hash/search", response_model=SearchResponse)
async def search_similar(
    file: UploadFile = File(...),
    algorithm: str = Query("phash", regex="^(phash|dhash|ahash|whash)$"),
    threshold: int = Query(10, ge=0, le=64),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Search for similar images.
    
    Upload an image and find similar images in the database.
    """
    try:
        # Read and hash image
        image_data = await file.read()
        query_hash = hasher.generate_hash(image_data, algorithm)
        
        # Find matches
        matches = matcher.find_matches(
            query_hash,
            algorithm,
            threshold,
            limit
        )
        
        # Format response
        match_responses = [
            MatchResponse(
                hash_id=m.hash_id,
                hash_value=m.hash_value,
                distance=m.distance,
                similarity_score=m.similarity_score,
                classification=matcher.classify_match(m.distance)
            )
            for m in matches
        ]
        
        return SearchResponse(
            query_hash=query_hash,
            matches=match_responses,
            total_matches=len(match_responses)
        )
        
    except Exception as e:
        logger.error(f"Error searching: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    return {
        "total_hashes": repository.get_hash_count(),
        "algorithms": list(ImageHasher.ALGORITHMS.keys())
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### **Phase 5: CLI Tool (Day 8)**

#### **File: `src/cli/commands.py`**

```python
"""
Command-line interface for hash system.
"""
import click
from pathlib import Path
from ..hasher.generator import ImageHasher
from ..storage.repository import HashRepository
from ..matcher.similarity import SimilarityMatcher


@click.group()
def cli():
    """Image Hash System CLI"""
    pass


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--algorithm', '-a', default='phash', 
              help='Hashing algorithm')
def hash_image(image_path, algorithm):
    """Generate hash from image file."""
    hasher = ImageHasher()
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    hash_value = hasher.generate_hash(image_data, algorithm)
    click.echo(f"Hash ({algorithm}): {hash_value}")


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--source', '-s', help='Source identifier')
def batch_hash(directory, source):
    """Hash all images in a directory."""
    hasher = ImageHasher()
    repository = HashRepository("postgresql://localhost/image_hashes")
    
    directory = Path(directory)
    image_files = list(directory.glob('*.jpg')) + \
                  list(directory.glob('*.png'))
    
    with click.progressbar(image_files, label='Hashing images') as files:
        for img_file in files:
            with open(img_file, 'rb') as f:
                image_data = f.read()
            
            hashes = hasher.generate_all_hashes(image_data)
            repository.store_hash(hashes, source or str(img_file))
    
    click.echo(f"Hashed {len(image_files)} images")


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--threshold', '-t', default=10, help='Distance threshold')
def find_similar(image_path, threshold):
    """Find similar images."""
    hasher = ImageHasher()
    repository = HashRepository("postgresql://localhost/image_hashes")
    matcher = SimilarityMatcher(repository)
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    query_hash = hasher.generate_hash(image_data)
    matches = matcher.find_matches(query_hash, threshold=threshold)
    
    if not matches:
        click.echo("No matches found")
        return
    
    click.echo(f"\nFound {len(matches)} matches:\n")
    for match in matches:
        click.echo(f"ID: {match.hash_id}")
        click.echo(f"Distance: {match.distance}")
        click.echo(f"Similarity: {match.similarity_score:.2%}")
        click.echo(f"Classification: {matcher.classify_match(match.distance)}")
        click.echo("---")


if __name__ == '__main__':
    cli()
```

---

### **Phase 6: Testing (Days 9-10)**

#### **File: `tests/test_hasher.py`**

```python
"""
Tests for hash generation.
"""
import pytest
from PIL import Image
import io
from src.hasher.generator import ImageHasher


def create_test_image(size=(100, 100), color='red'):
    """Create a simple test image."""
    img = Image.new('RGB', size, color)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def test_hash_generation():
    """Test basic hash generation."""
    hasher = ImageHasher()
    image_data = create_test_image()
    
    hash_value = hasher.generate_hash(image_data)
    
    assert isinstance(hash_value, str)
    assert len(hash_value) == 16  # 64-bit hash = 16 hex chars


def test_identical_images_produce_same_hash():
    """Identical images should have identical hashes."""
    hasher = ImageHasher()
    image_data = create_test_image()
    
    hash1 = hasher.generate_hash(image_data)
    hash2 = hasher.generate_hash(image_data)
    
    assert hash1 == hash2


def test_similar_images_have_small_distance():
    """Similar images should have low Hamming distance."""
    hasher = ImageHasher()
    
    # Create two similar images
    img1_data = create_test_image(color='red')
    img2_data = create_test_image(color=(255, 10, 10))  # Slightly different red
    
    hash1 = hasher.generate_hash(img1_data)
    hash2 = hasher.generate_hash(img2_data)
    
    distance = hasher.hash_distance(hash1, hash2)
    
    # Should be similar but not identical
    assert 0 < distance < 15


def test_different_images_have_large_distance():
    """Very different images should have high Hamming distance."""
    hasher = ImageHasher()
    
    img1_data = create_test_image(color='red')
    img2_data = create_test_image(color='blue')
    
    hash1 = hasher.generate_hash(img1_data)
    hash2 = hasher.generate_hash(img2_data)
    
    distance = hasher.hash_distance(hash1, hash2)
    
    assert distance > 10


def test_all_algorithms():
    """Test all hashing algorithms."""
    hasher = ImageHasher()
    image_data = create_test_image()
    
    all_hashes = hasher.generate_all_hashes(image_data)
    
    assert 'phash' in all_hashes
    assert 'dhash' in all_hashes
    assert 'ahash' in all_hashes
    assert 'whash' in all_hashes
```

---

## 📊 PERFORMANCE OPTIMIZATION

### **Indexing Strategy:**

```python
# Add to database.py for faster searches
from sqlalchemy import Index, func

class ImageHash(Base):
    # ... existing code ...
    
    # Additional indexes for performance
    __table_args__ = (
        # B-tree index for exact matches
        Index('idx_phash_btree', 'phash'),
        
        # Integer index for faster distance calculations
        Index('idx_phash_int', 'phash_int'),
        
        # Composite index for filtered searches
        Index('idx_source_timestamp', 'source', 'timestamp'),
    )
```

### **Caching Layer (Optional):**

```python
# Add Redis caching for frequent queries
import redis
import json

class CachedHashRepository(HashRepository):
    """Repository with Redis caching."""
    
    def __init__(self, database_url: str, redis_url: str):
        super().__init__(database_url)
        self.redis = redis.from_url(redis_url)
        self.cache_ttl = 3600  # 1 hour
    
    def find_similar(self, query_hash: str, **kwargs):
        """Find similar with caching."""
        # Check cache
        cache_key = f"similar:{query_hash}:{kwargs}"
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # Query database
        results = super().find_similar(query_hash, **kwargs)
        
        # Cache results
        self.redis.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(results)
        )
        
        return results
```

---

## 📈 BENCHMARKING

#### **File: `benchmark.py`**

```python
"""
Performance benchmarking.
"""
import time
from pathlib import Path
from src.hasher.generator import ImageHasher
from src.storage.repository import HashRepository
from src.matcher.similarity import SimilarityMatcher


def benchmark_hashing(num_images=1000):
    """Benchmark hash generation speed."""
    hasher = ImageHasher()
    
    # Create test image
    from PIL import Image
    import io
    img = Image.new('RGB', (800, 600), 'blue')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    image_data = buf.getvalue()
    
    start = time.time()
    for _ in range(num_images):
        hasher.generate_hash(image_data)
    elapsed = time.time() - start
    
    print(f"Hashed {num_images} images in {elapsed:.2f}s")
    print(f"Rate: {num_images/elapsed:.0f} images/second")


def benchmark_search(num_hashes=10000, num_queries=100):
    """Benchmark search performance."""
    repository = HashRepository("postgresql://localhost/image_hashes")
    matcher = SimilarityMatcher(repository)
    
    # Assume database has num_hashes already
    print(f"Searching {num_hashes} hashes...")
    
    query_hash = "a" * 16  # Dummy hash
    
    start = time.time()
    for _ in range(num_queries):
        matcher.find_matches(query_hash, threshold=10)
    elapsed = time.time() - start
    
    print(f"Performed {num_queries} searches in {elapsed:.2f}s")
    print(f"Rate: {num_queries/elapsed:.0f} searches/second")


if __name__ == "__main__":
    print("=== Hash Generation Benchmark ===")
    benchmark_hashing(1000)
    
    print("\n=== Search Benchmark ===")
    benchmark_search(10000, 100)
```

---

## 🔒 ETHICS & PRIVACY

#### **File: `docs/ETHICS.md`**

```markdown
# Ethics and Privacy Considerations

## Purpose

This system is designed for **educational purposes** to demonstrate 
privacy-preserving image similarity detection technology.

## Privacy-by-Design

1. **No Image Storage**: Only perceptual hashes are stored, never images
2. **Irreversible Hashes**: Cannot reconstruct images from hashes
3. **Limited Metadata**: Minimal metadata collection
4. **Access Controls**: Database access should be restricted

## Intended Use

✅ **Appropriate Uses:**
- Educational demonstration of CSAM detection technology
- Research into perceptual hashing algorithms
- Building trust & safety infrastructure
- Portfolio demonstration for job applications

❌ **Inappropriate Uses:**
- Actual CSAM detection (requires legal authority)
- Surveillance without consent
- Privacy violation
- Any illegal activity

## Legal Considerations

- This system does NOT have NCMEC database access
- Should NOT be used for actual CSAM detection
- Using this with actual CSAM is ILLEGAL
- Consult legal counsel before production use

## Responsible Development

If developing this for production use:
1. Work with legal counsel
2. Coordinate with NCMEC/law enforcement
3. Implement proper access controls
4. Have trauma support for reviewers
5. Follow all applicable laws

## Data Handling

- Use only benign test images (landscapes, objects, etc.)
- Never use sensitive personal images