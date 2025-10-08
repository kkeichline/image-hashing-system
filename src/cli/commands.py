"""
Command-line interface for hash system.

TODO: Implement CLI commands using Click:
- hash-image: Generate hash from a single image
- batch-hash: Hash all images in a directory
- find-similar: Find similar images

Refer to the project guide for command specifications.
"""

import click
from pathlib import Path

# TODO: Import your modules
# from ..hasher.generator import ImageHasher
# from ..storage.repository import HashRepository
# from ..matcher.similarity import SimilarityMatcher


@click.group()
def cli():
    """Image Hash System CLI"""
    pass


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--algorithm", "-a", default="phash", help="Hashing algorithm")
def hash_image(image_path, algorithm):
    """
    Generate hash from image file.

    TODO:
    1. Load image file
    2. Generate hash
    3. Print result
    """
    click.echo("TODO: Implement hash_image command")


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--source", "-s", help="Source identifier")
def batch_hash(directory, source):
    """
    Hash all images in a directory.

    TODO:
    1. Find all image files in directory
    2. Hash each image
    3. Store in database
    4. Show progress bar
    """
    click.echo("TODO: Implement batch_hash command")


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--threshold", "-t", default=10, help="Distance threshold")
def find_similar(image_path, threshold):
    """
    Find similar images.

    TODO:
    1. Load and hash query image
    2. Search for matches
    3. Display results with similarity scores
    """
    click.echo("TODO: Implement find_similar command")


if __name__ == "__main__":
    cli()
