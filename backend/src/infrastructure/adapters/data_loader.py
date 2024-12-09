import pandas as pd
from typing import List, Tuple
from ...domain.models.movie import Movie
from ...domain.models.producer import Producer
import os
import re


class CsvLoader:

    @staticmethod
    def _split_producers(producers_str: str) -> List[str]:
        """
        Split producer names considering different formats and combinations.
        Returns a list of individual producer names.
        """
        if not producers_str or pd.isna(producers_str):
            return []

        names = re.split(r",\s*and\s+|\s+and\s+|,\s*", producers_str)

        clean_names = []
        for name in names:
            name = name.strip()
            if not name:
                continue
            if name.endswith(" and"):
                name = name[:-4]

            clean_names.append(name.strip())

        return clean_names

    @staticmethod
    def load_movies(file_path: str) -> Tuple[List[Movie], List[Producer]]:
        absolute_path = f"/app/data/{file_path}"
        df = pd.read_csv(absolute_path, sep=';')
        movies = []
        all_producers = set()

        for _, row in df.iterrows():
            producer_names = CsvLoader._split_producers(row['producers'])

            movie = Movie(
                id=None,
                year=row['year'],
                title=row['title'],
                studios=row['studios'],
                winner=row['winner'] == 'yes',
                producers=[]  # TODO: POpulate Later
            )
            movies.append(movie)

            all_producers.update(producer_names)

        producers = [Producer(id=None, name=name) 
                    for name in sorted(all_producers) 
                    if name]

        for i, row in df.iterrows():
            movies[i].producer_names = CsvLoader._split_producers(row['producers'])

        return movies, producers

    @staticmethod
    def test_producer_splitting():
        """
        Test function to verify producer name splitting
        """
        test_cases = [
            "A. Kitman Ho, Julius R. Nasso and Steven Seagal",
            "Adam Sandler and Rob Schneider",
            "Adam Sandler and Tom Shadyac",
            "Adam Sandler, Chris Columbus, Mark Radcliffe and Allen Covert",
            "Albert S. Ruddy",
            "Alex Kurtzman, Chris Morgan, Sean Daniel and Sarah Bradshaw",
            "Alexander Salkind and Ilya Salkind",
            "Allan Carr",
            "Allen Covert, Jack Giarraputo, Heather Parry and Adam Sandler",
            "Andrew Bergman and Mike Lobell",
            "Ann Carli Avi Arad, Isaac Larian and Steven Paul"
        ]

        for test_case in test_cases:
            result = CsvLoader._split_producers(test_case)
            print(f"\nInput: {test_case}")
            print(f"Output: {result}")
