import copy
import json
import multiprocessing as mp
import os
from collections import defaultdict
from enum import Enum

PUNCTUATION_TRANSMAP = str.maketrans("", "", "'\"~!@#$%^&*()_+\{\}|:<>?/,.;")

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
    handlers=[logging.FileHandler("log.txt")],
)

from typing import NewType  # noqa: E402

CodeWordMapToWords = NewType("CodeMap", dict[str, list[str]])
""" e.g. `{"1234": ["BEAR", "HERE", "LEFT"]}` """

# ================================================================================


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


def words_to_codes(word_list: list[str]) -> CodeWordMapToWords:  # type: ignore
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

    encodings: dict[str, list[str]] = defaultdict(lambda: list())

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


def chunk_words(strings: list[str], max_length: int) -> list[list[str]]:
    """
    Chunk a list of words into groupings of a given text length.
    For example, `chunk_words(["abcd", "ac", "asdf"], 7) -> [["abcd", "ac"], ["asdf"]]]`.

    Parameters
    ----------
    strings : list[str]
        Your list of words.
    max_length : int
        The maximum

    Returns
    -------
    chunks : list[list[str]]
        Groupings of a given text length.
    """
    chunks: list[list[str]] = []
    current_chunk: list[str] = []

    for string in strings:
        if sum(map(len, current_chunk)) + len(string) > max_length:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(string)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


if __name__ == "__main__":
    # Build relations/world_list if necessary.
    if not os.path.exists(os.path.join(".", "word_list.json")):
        build_relations()
        logging.info("Built relations (`word_list.json`) from scratch")

    # Fetch word_list.
    with open("word_list.json", "r") as f:
        encodings: CodeWordMapToWords = defaultdict(lambda: list(), json.loads(f.read()))  # type: ignore
        encodings: dict[str, list[str]]  # Because VS Code doesn't like NewType for some reason.
        logging.info("Loaded encodings.")
        logging.info(f"{len(encodings)} total codes.")
        logging.info(f"{len([word for group in encodings.values() for word in group])} total words.")

    # Ask for mode, encoding or decoding.
    class Modes(Enum):  # Inner scope is okay. This is only used right here.
        ENCODE = 1
        DECODE = 2

    prompt = "\nSelect a mode, encoding or decoding [1, 2]: "
    while (mode := int(input(prompt))) not in [m.value for m in Modes]:
        logging.error(f"User selected invalid mode number: {mode}")
        print("Invalid mode.")

    mode_num_to_name = {v: n for n, v in [(m.name, m.value) for m in Modes]}
    logging.info(f"Mode selected: {mode_num_to_name[mode]}")

    # Encode:
    if mode == Modes.ENCODE.value:
        print("Enter text: ", end="")
        text: str = input().strip().lower()
        text_encoded: str = "".join([(LET2NUM[char] if char.isalpha() else char) for char in text])
        print(f"\nEncoded text: {text_encoded}")

        logging.info(f"Generated translation for text: {text}")
        logging.info(f"Translation: {text_encoded}")

    # Decode:
    elif mode == Modes.DECODE.value:
        # Translation(s):
        code: str = input("Enter code: ")
        code_words: list[str] = code.strip().replace("-", " ").translate(PUNCTUATION_TRANSMAP).split(" ")
        code_words_options: list[str] = [encodings[code] for code in code_words]
        translator: dict[str, dict[str, list[str] | int]] = {  # Disgusting type hint.
            cw: {"options": cwo, "options_n": cwo_n}
            for cw, cwo, cwo_n in zip(code_words, code_words_options, [*map(len, code_words_options)])
        }

        logging.info(f"Generated translations for code: {code}")
        logging.info(f"Translations: {translator}")

        # Guard:
        if code_words[0][0].isalpha():
            logging.error(f"User entered invalid code: {mode}")
            print("Invalid input. Numbers and punctuation only please.")

        # Print Translation(s):
        print("")
        for chunk in chunk_words(code_words, 40):
            print(" ".join(chunk))

            max_options: int = max(translator[word]["options_n"] for word in chunk)  # Height of translation chunk.
            for row in range(max_options):
                translation_chunk_line: list[str] = [
                    (translator[word]["options"][row] if row < translator[word]["options_n"] else " " * len(word))
                    for word in chunk
                ]
                print(" ".join(translation_chunk_line))

        # Add missing word(s) (if any):
        missing_words: list[str] = [cw for cw, cwo in zip(code_words, code_words_options) if len(cwo) == 0]
        logging.info(f"Translation had {len(missing_words)} missing words.")

        if missing_words:  # Code words without translation options.
            words_added: int = 0

            print(f"\nThere were {len(missing_words)} code word(s) with no English equivalent.")
            print("Would you like to provide translations for them? [y/n]: ", end="")
            if input().lower() == "y":
                logging.info("User decided to add missing words.")

                for code_word in missing_words:
                    print(f'\nEnter translations for "{code_word}", or leave blank to skip: ', end="")
                    word: str = input().replace(" ", "").strip().lower().translate(PUNCTUATION_TRANSMAP)

                    if not word:
                        logging.info("User skipped adding missing words.")
                        continue

                    if (code := word_to_code(word)) != code_word:
                        print(f'Invalid translation ("{code_word}" != "{code}"). Skipped.')
                        logging.error("User provided invalid translation. Skipped.")
                        continue

                    if word not in encodings[code_word]:
                        logging.info(f'User added missing word, ("{word}" == "{code_word}").')
                        encodings[code_word].append(word)
                        words_added += 1
                        continue

            if words_added:
                with open("word_list.json", "w") as f:
                    json.dump(encodings, f)

                txt = f"\nWord list has been updated with {words_added} new words."
                logging.info(txt)
                print(txt)

        # Add extra words (if any):
        print("\nWould you like to add any additional words to the corpus? [y/n]: ", end="")
        if input().lower() == "y":
            words_added: int = 0

            while True:  # Adding new words.
                print("\nEnter word, or leave blank to stop: ", end="")
                word: str = input().strip().lower().translate(PUNCTUATION_TRANSMAP)

                if not word:
                    logging.info("User skipped adding new words.")
                    break

                code_word: str = word_to_code(word)

                if word not in encodings[code_word]:
                    logging.info(f'User added new word, ("{word}" == "{code_word}").')
                    encodings[code_word].append(word)
                    words_added += 1
                else:
                    logging.error(f'User attempted to add word already in corpus, ("{word}" == "{code_word}").')
                    print("This word is already in the corpus!")

            if words_added:
                with open("word_list.json", "w") as f:
                    json.dump(encodings, f)

                txt = f"\nWord list has been updated with {words_added} new words."
                logging.info(txt)
                print(txt)
