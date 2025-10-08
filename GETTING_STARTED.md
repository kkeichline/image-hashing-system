# Getting Started with Implementation

Welcome! This guide will help you implement the Image Hash System step-by-step.

## 📋 Prerequisites Check

Before you start, make sure you have:
- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] A code editor (VS Code recommended)
- [ ] Basic understanding of Python classes and functions
- [ ] Familiarity with SQL/databases (helpful but not required)

## 🎯 Implementation Order

Follow these phases in order. Each builds on the previous one.

---

## Phase 1: Hash Generation (Start Here!)

**Goal:** Implement the `ImageHasher` class to generate perceptual hashes from images.

**Files to implement:**
- `src/hasher/generator.py`

**What to do:**

1. **Implement `__init__` method:**
   ```python
   def __init__(self, hash_size: int = 8):
       self.hash_size = hash_size
   ```

2. **Implement `generate_hash` method:**
   - Check if algorithm is valid
   - Load image using `Image.open(io.BytesIO(image_data))`
   - Convert to RGB if needed: `image.convert('RGB')`
   - Get hash function: `hash_func = self.ALGORITHMS[algorithm]`
   - Generate hash: `hash_value = hash_func(image, hash_size=self.hash_size)`
   - Return as string: `return str(hash_value)`

3. **Implement `generate_all_hashes` method:**
   - Loop through `self.ALGORITHMS.keys()`
   - Call `generate_hash()` for each algorithm
   - Return dictionary

4. **Implement `hash_distance` method:**
   - Convert hashes to hash objects: `imagehash.hex_to_hash(hash1)`
   - Calculate distance: `h1 - h2` (this gives Hamming distance)
   - Return the distance

**Test it:**
```bash
# Create a simple test
python3 << 'EOF'
from PIL import Image
import io
from src.hasher.generator import ImageHasher

# Create test image
img = Image.new('RGB', (100, 100), 'red')
buf = io.BytesIO()
img.save(buf, format='PNG')
image_data = buf.getvalue()

# Hash it
hasher = ImageHasher()
hash_value = hasher.generate_hash(image_data)
print(f"Hash: {hash_value}")
print(f"Length: {len(hash_value)}")
EOF
```

**Learning resources:**
- [ImageHash documentation](https://github.com/JohannesBuchner/imagehash)
- [PIL/Pillow documentation](https://pillow.readthedocs.io/)

---

## Phase 2: Database Storage

**Goal:** Store hashes in a database and retrieve them.

**Files to implement:**
- `src/storage/database.py`
- `src/storage/repository.py`

**What to do:**

1. **In `database.py`, define `ImageHash` model:**
   ```python
   id = Column(Integer, primary_key=True, autoincrement=True)
   phash = Column(String(16), nullable=False, index=True)
   dhash = Column(String(16), index=True)
   # ... add other columns
   ```

2. **Implement `HashRepository.__init__`:**
   ```python
   self.engine = create_engine(database_url)
   Base.metadata.create_all(self.engine)
   self.Session = sessionmaker(bind=self.engine)
   ```

3. **Implement `store_hash` method:**
   ```python
   session = self.Session()
   try:
       hash_record = ImageHash(
           phash=hashes.get('phash'),
           # ... other fields
       )
       session.add(hash_record)
       session.commit()
       return hash_record.id
   finally:
       session.close()
   ```

4. **Implement `find_similar` method:**
   - Query all hashes
   - Calculate distance for each
   - Filter by threshold
   - Sort by distance
   - Return results

**Test it:**
```bash
python3 << 'EOF'
from src.storage.repository import HashRepository

repo = HashRepository("sqlite:///test.db")
hash_id = repo.store_hash({
    'phash': 'a1b2c3d4e5f6g7h8'
})
print(f"Stored hash with ID: {hash_id}")
print(f"Total hashes: {repo.get_hash_count()}")
EOF
```

**Learning resources:**
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [SQLAlchemy ORM documentation](https://docs.sqlalchemy.org/en/14/orm/)

---

## Phase 3: Similarity Matching

**Goal:** Find similar images based on hash comparison.

**Files to implement:**
- `src/matcher/similarity.py`

**What to do:**

1. **Implement `MatchResult.from_tuple`:**
   ```python
   similarity = 1 - (distance / 64.0)
   return cls(hash_id, hash_value, distance, similarity)
   ```

2. **Implement `SimilarityMatcher.find_matches`:**
   - Call `self.repository.find_similar()`
   - Convert results to `MatchResult` objects
   - Limit results
   - Return list

3. **Implement `classify_match`:**
   ```python
   if distance <= 5:
       return "identical"
   elif distance <= 10:
       return "very_similar"
   # ... etc
   ```

**Test it:**
```bash
python3 << 'EOF'
from src.matcher.similarity import SimilarityMatcher
from src.storage.repository import HashRepository

repo = HashRepository("sqlite:///test.db")
matcher = SimilarityMatcher(repo)

# Assuming you have stored hashes
matches = matcher.find_matches("a1b2c3d4e5f6g7h8", threshold=10)
for match in matches:
    print(f"Match: {match.hash_id}, Distance: {match.distance}")
EOF
```

---

## Phase 4: REST API

**Goal:** Create API endpoints for the system.

**Files to implement:**
- `src/api/main.py`

**What to do:**

1. **Initialize components (after imports):**
   ```python
   hasher = ImageHasher()
   repository = HashRepository("sqlite:///image_hashes.db")
   matcher = SimilarityMatcher(repository)
   ```

2. **Implement `/hash/upload` endpoint:**
   ```python
   image_data = await file.read()
   hashes = hasher.generate_all_hashes(image_data)
   hash_id = repository.store_hash(hashes, source)
   return HashResponse(...)
   ```

3. **Implement `/hash/search` endpoint:**
   ```python
   image_data = await file.read()
   query_hash = hasher.generate_hash(image_data, algorithm)
   matches = matcher.find_matches(query_hash, algorithm, threshold, limit)
   # Format and return results
   ```

4. **Implement `/stats` endpoint:**
   ```python
   return {
       "total_hashes": repository.get_hash_count(),
       "algorithms": list(ImageHasher.ALGORITHMS.keys())
   }
   ```

**Test it:**
```bash
# Start the server
python -m uvicorn src.api.main:app --reload

# In another terminal, test it
curl http://localhost:8000/health
curl http://localhost:8000/stats

# Open in browser
open http://localhost:8000/docs
```

**Learning resources:**
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic models](https://pydantic-docs.helpmanual.io/)

---

## Phase 5: Command Line Interface

**Goal:** Create CLI commands for easy interaction.

**Files to implement:**
- `src/cli/commands.py`

**What to do:**

1. **Implement `hash_image` command:**
   ```python
   hasher = ImageHasher()
   with open(image_path, 'rb') as f:
       image_data = f.read()
   hash_value = hasher.generate_hash(image_data, algorithm)
   click.echo(f"Hash ({algorithm}): {hash_value}")
   ```

2. **Implement `batch_hash` command:**
   - Use `Path(directory).glob('*.jpg')` to find images
   - Use `click.progressbar()` for progress indication
   - Hash and store each image

3. **Implement `find_similar` command:**
   - Hash the query image
   - Use matcher to find similar
   - Display results with click.echo()

**Test it:**
```bash
python -m src.cli.commands hash-image path/to/image.jpg
python -m src.cli.commands --help
```

**Learning resources:**
- [Click documentation](https://click.palletsprojects.com/)

---

## Phase 6: Testing

**Goal:** Write tests to ensure everything works.

**Files to implement:**
- `tests/test_hasher.py`
- `tests/test_storage.py`
- `tests/test_matcher.py`
- `tests/test_api.py`

**What to do:**

1. **Install test dependencies:**
   ```bash
   pip install pytest pytest-asyncio httpx
   ```

2. **Uncomment test code** and implement test logic

3. **Run tests:**
   ```bash
   pytest tests/ -v
   pytest tests/test_hasher.py -v
   ```

**Learning resources:**
- [Pytest documentation](https://docs.pytest.org/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 🐛 Debugging Tips

1. **Import errors:**
   - Make sure you're in the project root
   - Use `python -m` to run modules: `python -m src.api.main`

2. **Database errors:**
   - Start with SQLite: `sqlite:///test.db`
   - Check if tables are created: `Base.metadata.create_all(engine)`

3. **Hash generation errors:**
   - Verify image is valid
   - Check image mode (convert to RGB)
   - Print intermediate values

4. **API errors:**
   - Check FastAPI logs in terminal
   - Use `/docs` endpoint to test interactively
   - Add print statements to debug

---

## 📚 Additional Resources

### Python Concepts:
- [Python Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Async/Await](https://docs.python.org/3/library/asyncio.html)

### Project Concepts:
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Perceptual Hashing](http://www.phash.org/)
- [RESTful APIs](https://restfulapi.net/)

---

## ✅ Completion Checklist

- [ ] Phase 1: Hash generation works
- [ ] Phase 2: Database storage works
- [ ] Phase 3: Similarity matching works
- [ ] Phase 4: API endpoints work
- [ ] Phase 5: CLI commands work
- [ ] Phase 6: Tests pass
- [ ] Documentation updated
- [ ] Code is clean and commented

---

## 🎉 Next Steps

Once you've completed the implementation:

1. **Optimize performance:**
   - Add caching with Redis
   - Implement BK-tree for faster search
   - Add database indexes

2. **Add features:**
   - Batch upload API
   - Hash deletion
   - Search history
   - Web UI

3. **Deploy:**
   - Use Docker Compose
   - Deploy to cloud (Heroku, AWS, etc.)
   - Add monitoring

4. **Portfolio:**
   - Write a blog post about what you learned
   - Add to your portfolio/resume
   - Share on GitHub

---

## ❓ Need Help?

- Read the TODO comments in each file
- Check the documentation in `docs/`
- Review the project guide in `image-hash-project.md`
- Search for specific error messages
- Break problems into smaller steps

**Good luck and happy coding! 🚀**
