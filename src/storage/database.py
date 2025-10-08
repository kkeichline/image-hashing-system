"""
Database models for hash storage.

TODO: Implement SQLAlchemy models for:
- ImageHash table (stores hash values and metadata)
- MatchResult table (stores match history)

Refer to the project guide for table structure.
"""

from sqlalchemy import Column, String, Integer, DateTime, Index, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class ImageHash(Base):
    """
    Image hash record.

    TODO: Define columns:
    - id (primary key)
    - phash, dhash, ahash, whash (hash values)
    - source (where image came from)
    - timestamp
    - phash_int (integer representation for faster comparison)

    Don't forget to add indexes!
    """

    __tablename__ = "image_hashes"

    # TODO: Add columns here

    def __repr__(self):
        return f"<ImageHash(id={self.id})>"


class MatchResult(Base):
    """
    Record of hash matches.

    TODO: Define columns:
    - id (primary key)
    - query_hash_id
    - matched_hash_id
    - distance (Hamming distance)
    - algorithm
    - timestamp
    """

    __tablename__ = "match_results"

    # TODO: Add columns here
