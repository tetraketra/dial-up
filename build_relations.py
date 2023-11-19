import collections as cl
import json
import copy
import multiprocessing as mp

num_to_let: dict[str, list[str]] = { '2': ['a', 'b', 'c'], '3': ['d','e','f'], '4': ['g','h','i'], '5': ['j','k','l'], '6': ['m','n','o'], '7': ['p','q','r','s'], '8': ['t','u','v'], '9': ['w','x','y','z'] }
let_to_num: dict[str, str]       = { 'a': '2', 'b': '2', 'c': '2', 'd': '3', 'e': '3', 'f': '3', 'g': '4', 'h': '4', 'i': '4', 'j': '5', 'k': '5', 'l': '5', 'm': '6', 'n': '6', 'o': '6', 'p': '7', 'q': '7', 'r': '7', 's': '7', 't': '8', 'u': '8', 'v': '8', 'w': '9', 'x': '9', 'y': '9', 'z': '9' }


def word_to_encoded(word: str) -> str:
    return "".join([let_to_num[letter] for letter in word])
        

def words_to_encodings(word_list: list[str]) -> dict[str, list[str]]: # dict[encoding, words_that_map_to_that_encoding]

    print(f"Started encoding {len(word_list[0])}-letter words.")
    
    encodings: dict[str, list[str]] = cl.defaultdict(lambda: list())

    for word in word_list:
        encoding: str = word_to_encoded(word)
        encodings[encoding].append(word)
        
    print (f"Finished encoding {len(word_list[0])}-letter words.")
    return dict(encodings)


def get_words_from_file(file_path: str) -> list[str]:
    with open(file_path, 'r') as f:
        words = json.loads(f.read())
        words = [word['word'] for word in words]

    return words


if __name__ == "__main__":  
    
    file_format = "{}-letter-words.json"
    files = [file_format.format(i) for i in range(2, 16)]

    with mp.Pool(13) as p:
        word_list: list[str] = p.map(get_words_from_file, files)
        encodings_list: dict[str, list[str]] = p.map(words_to_encodings, word_list)

    all_encodings: dict[str, list[str]] = copy.deepcopy(num_to_let)
    for encoding in encodings_list:
        all_encodings.update(encoding)

    with open("word_list.json", 'w') as f:
        json.dump(all_encodings, f)