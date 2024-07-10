import collections as cl
import copy
import json
import multiprocessing as mp
import os

NUM2LET: dict[str, list[str]] = {
    "2": ["a", "b", "c"],
    "3": ["d", "e", "f"],
    "4": ["g", "h", "i"],
    "5": ["j", "k", "l"],
    "6": ["m", "n", "o"],
    "7": ["p", "q", "r", "s"],
    "8": ["t", "u", "v"],
    "9": ["w", "x", "y", "z"],
}

LET2NUM: dict[str, str] = {
    "a": "2",
    "b": "2",
    "c": "2",
    "d": "3",
    "e": "3",
    "f": "3",
    "g": "4",
    "h": "4",
    "i": "4",
    "j": "5",
    "k": "5",
    "l": "5",
    "m": "6",
    "n": "6",
    "o": "6",
    "p": "7",
    "q": "7",
    "r": "7",
    "s": "7",
    "t": "8",
    "u": "8",
    "v": "8",
    "w": "9",
    "x": "9",
    "y": "9",
    "z": "9",
}

import logging  # noqa: E402

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)

from typing import NewType  # noqa: E402

CodeMap = NewType("CodeMap", dict[str, list[str]])
""" e.g. `{"1234": ["BEAR", "HERE", "LEFT"]}` """


def word_to_code(word: str) -> str:
    """
    Convert a word to its encoded equivalent.

    Parameters
    ----------
    word : str
        Your word.

    Returns
    -------
    encodedWord: str
        Your word, but encoded.
    """

    return "".join([LET2NUM[letter] for letter in word])


def words_to_codes(word_list: list[str]) -> CodeMap:
    """
    Generates code mappings for a list of words.
    Keys are `"1234"`-like codes.
    Values are all English words that map to that code.

    Parameters
    ----------
    word_list : list[str]
        List of words to generate code mappings for.

    Returns
    -------
    CodeMap: dict[str, list[str]]
        Mappoing from code to words which map to that code.
    """

    logging.info(f"Started encoding {len(word_list[0])}-letter words.")

    encodings: dict[str, list[str]] = cl.defaultdict(lambda: list())

    for word in word_list:
        encoding: str = word_to_code(word)
        encodings[encoding].append(word)

    logging.info(f"Finished encoding {len(word_list[0])}-letter words.")

    return dict(encodings)


def file_to_words(file_path: str) -> list[str]:
    """
    Extract all words from a `*-letter-words.json` file.

    Parameters
    ----------
    file_path : str
        The path to the file.

    Returns
    -------
    words: list[str]
        The words in the file.
    """
    
    with open(file_path, "r") as f:
        words = json.loads(f.read())
        words = [word["word"] for word in words]

    return words


def build_relations() -> None:
    """
    Build `word_list.json`.
    """
    file_format = "{}-letter-words.json"
    files = [os.path.join(".", "words", file_format.format(i)) for i in range(2, 16)]

    with mp.Pool(13) as p:
        word_list: list[str] = p.map(file_to_words, files)
        encodings_list: dict[str, list[str]] = p.map(words_to_codes, word_list)

    all_encodings: dict[str, list[str]] = copy.deepcopy(NUM2LET)
    for encoding in encodings_list:
        all_encodings.update(encoding)

    with open("word_list.json", "w") as f:
        json.dump(all_encodings, f)