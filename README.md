# Image Hash System

A privacy-preserving image similarity detection system using perceptual hashing. This project demonstrates the core technology used in CSAM detection systems like PhotoDNA, while maintaining privacy by never storing actual images.

## 🎯 Project Purpose

This is an **educational project** that demonstrates:
- How perceptual hashing works
- Privacy-preserving image similarity detection
- The technology behind trust & safety systems
- Production-ready code architecture

**⚠️ Important:** This is for learning purposes only. See [ETHICS.md](docs/ETHICS.md) for responsible use guidelines.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for development)
- Virtual environment tool (venv, conda, etc.)

### Installation

1. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up database** (PostgreSQL example)
```bash
# Create database
createdb image_hashes

# Or use SQLite for development (no setup needed)
# The system will create a SQLite file automatically
```

4. **Set environment variables** (optional)
```bash
export DATABASE_URL="postgresql://localhost/image_hashes"
# or
export DATABASE_URL="sqlite:///image_hashes.db"
```

## 📖 Usage

### Option 1: REST API

1. **Start the API server**
```bash
python -m uvicorn src.api.main:app --reload
```

2. **Access the interactive API docs**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. **Upload and hash an image**
```bash
curl -X POST "http://localhost:8000/hash/upload" \
  -F "file=@path/to/image.jpg" \
  -F "source=test"
```

4. **Search for similar images**
```bash
curl -X POST "http://localhost:8000/hash/search?threshold=10" \
  -F "file=@path/to/query.jpg"
```

### Option 2: Command Line Interface

```bash
# Hash a single image
python -m src.cli.commands hash-image path/to/image.jpg

# Hash all images in a directory
python -m src.cli.commands batch-hash path/to/directory/

# Find similar images
python -m src.cli.commands find-similar path/to/query.jpg --threshold 10
```

### Option 3: Python Library

```python
from src.hasher.generator import ImageHasher
from src.storage.repository import HashRepository
from src.matcher.similarity import SimilarityMatcher

# Initialize components
hasher = ImageHasher()
repository = HashRepository("sqlite:///image_hashes.db")
matcher = SimilarityMatcher(repository)

# Hash an image
with open('image.jpg', 'rb') as f:
    image_data = f.read()
    hashes = hasher.generate_all_hashes(image_data)
    hash_id = repository.store_hash(hashes, source='test')

# Find similar images
query_hash = hasher.generate_hash(image_data)
matches = matcher.find_matches(query_hash, threshold=10)

for match in matches:
    print(f"Match: {match.hash_id}, Distance: {match.distance}")
```

## 🏗️ Project Structure

```
image-hashing-system/
├── src/
│   ├── hasher/          # Hash generation
│   ├── storage/         # Database operations
│   ├── matcher/         # Similarity matching
│   ├── api/             # REST API
│   └── cli/             # Command-line interface
├── tests/               # Test files
├── docs/                # Documentation
├── data/                # Sample images (not included)
├── docker/              # Docker configuration
└── requirements.txt     # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_hasher.py
```

## 🐳 Docker Deployment

```bash
# Start all services (PostgreSQL + Redis + API)
cd docker
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📚 Documentation

- [API Documentation](docs/API.md) - REST API endpoints and usage
- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Ethics & Privacy](docs/ETHICS.md) - **Important guidelines for responsible use**

## 🔧 Configuration

### Database Options

**SQLite (Development)**
```python
DATABASE_URL = "sqlite:///image_hashes.db"
```

**PostgreSQL (Production)**
```python
DATABASE_URL = "postgresql://user:password@localhost/image_hashes"
```

### Hashing Algorithms

- `phash` (Perceptual Hash) - Default, most robust
- `dhash` (Difference Hash) - Fastest
- `ahash` (Average Hash) - Simplest
- `whash` (Wavelet Hash) - Most accurate

### Similarity Thresholds

- **0-5**: Identical or near-identical images
- **6-10**: Very similar (minor edits)
- **11-15**: Similar (crops, filters)
- **16-20**: Possibly similar
- **21+**: Different images

## 🎓 Learning Path

This project is structured to help you learn step-by-step:

1. **Phase 1: Hash Generation** (`src/hasher/`)
   - Learn about perceptual hashing algorithms
   - Implement image preprocessing
   - Calculate hash distances

2. **Phase 2: Storage** (`src/storage/`)
   - Design database schema
   - Implement repository pattern
   - Learn SQLAlchemy ORM

3. **Phase 3: Matching** (`src/matcher/`)
   - Implement similarity search
   - Learn about Hamming distance
   - Optimize search performance

4. **Phase 4: API** (`src/api/`)
   - Build REST API with FastAPI
   - Learn async Python
   - Implement proper error handling

5. **Phase 5: CLI** (`src/cli/`)
   - Build command-line tools
   - Learn Click framework
   - Create user-friendly interfaces

6. **Phase 6: Testing** (`tests/`)
   - Write unit tests
   - Integration testing
   - Performance benchmarking

## ⚖️ Legal & Ethical Notice

**READ THIS CAREFULLY:**

1. This system is for **educational purposes only**
2. Do NOT use with actual CSAM - that is ILLEGAL
3. Use only benign test images (landscapes, objects, etc.)
4. See [docs/ETHICS.md](docs/ETHICS.md) for full guidelines
5. For production use, consult legal counsel and coordinate with NCMEC

## 📝 TODO List for Implementation

The code structure is set up with skeleton code and TODO comments. You need to implement:

### Core Functionality
- [ ] Complete `ImageHasher.generate_hash()` method in `src/hasher/generator.py`
- [ ] Complete `ImageHasher.hash_distance()` method
- [ ] Define database columns in `src/storage/database.py`
- [ ] Implement `HashRepository.store_hash()` in `src/storage/repository.py`
- [ ] Implement `HashRepository.find_similar()`
- [ ] Implement `SimilarityMatcher.find_matches()` in `src/matcher/similarity.py`
- [ ] Complete API endpoints in `src/api/main.py`
- [ ] Implement CLI commands in `src/cli/commands.py`

### Testing
- [ ] Write tests for hash generation in `tests/test_hasher.py`
- [ ] Write tests for database operations
- [ ] Write tests for API endpoints
- [ ] Add performance benchmarks

Each file has detailed TODO comments and hints to guide your implementation!

## 📞 Learning Resources

### Technical Resources:
- [Perceptual Hashing Overview](http://www.phash.org/)
- [ImageHash Library Docs](https://github.com/JohannesBuchner/imagehash)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

### Trust & Safety Resources:
- [NCMEC](https://www.missingkids.org/)
- [Thorn](https://www.thorn.org/)
- [IWF](https://www.iwf.org.uk/)

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project demonstrates concepts used in:
- Microsoft PhotoDNA
- Facebook PDQ
- Other trust & safety systems

Built for educational purposes to understand how these critical systems work.

---

**Questions?** Review the documentation in the `docs/` folder, especially [ETHICS.md](docs/ETHICS.md).

**Ready to learn?** Start with Phase 1 - implement the hash generation in `src/hasher/generator.py`!
