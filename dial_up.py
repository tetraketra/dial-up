import json
from collections import defaultdict

num_to_let: dict[str, list[str]] = { '2': ['a', 'b', 'c'], '3': ['d','e','f'], '4': ['g','h','i'], '5': ['j','k','l'], '6': ['m','n','o'], '7': ['p','q','r','s'], '8': ['t','u','v'], '9': ['w','x','y','z'] }
let_to_num: dict[str, str]       = { 'a': '2', 'b': '2', 'c': '2', 'd': '3', 'e': '3', 'f': '3', 'g': '4', 'h': '4', 'i': '4', 'j': '5', 'k': '5', 'l': '5', 'm': '6', 'n': '6', 'o': '6', 'p': '7', 'q': '7', 'r': '7', 's': '7', 't': '8', 'u': '8', 'v': '8', 'w': '9', 'x': '9', 'y': '9', 'z': '9' }


def word_to_encoded(word: str) -> str:
    return "".join([let_to_num[letter] for letter in word])


def chunk_words(strings: list[str], max_length: int):
    chunks = []
    current_chunk = []

    for string in strings:
        if sum(map(len, current_chunk)) + len(string) > max_length:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(string)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def encode_text(sentence: str) -> str:
    return [(let_to_num[char] if char.isalpha() else char) for char in sentence]


if __name__ == "__main__":
    
    with open("word_list.json", 'r') as f:
        encodings: dict[str, list] = defaultdict(lambda: list(), json.loads(f.read()))

    while (mode := int(input("Select a mode, encoding or decoding [1, 2]: "))) not in [1, 2]:
        print("Invalid mode.")
    
    if mode == 1:
        sentence = input("Enter text: ").strip().lower()
        encoded_sentence = encode_text(sentence)
        print(f"Encoded text: {''.join(encoded_sentence)}")

    elif mode == 2:
        code = input("Enter code: ").strip().replace("-", " ")
        for c in "'\"~!@#$%^&*()_+\{\}|:<>?/,.;":
            code = code.replace(c, "")

        code_words = code.split(" ")
        code_word_options = [encodings[word] for word in code_words] 
        code_word_num_options = list(map(len, code_word_options))
        code_words_translator = { cw:[cwo, cwno] for cw, cwo, cwno in zip(code_words, code_word_options, code_word_num_options) }

        print()
        chunks = chunk_words(code_words, 40)
        for chunk in chunks:
            print(" ".join(chunk))
            
            max_options = max(code_words_translator[word][1] for word in chunk)
            for row in range(max_options):
                print( " ".join( 
                    [ (code_words_translator[word][0][row] if row < code_words_translator[word][1] else " "*len(word)) for word in chunk]
                ) )

            print()


        missing_words = [cw for cw, cwo in zip(code_words, code_word_options) if cwo == []]
        if missing_words:

            words_added = 0
            if input("There were some code words with no English equivalent. \nWould you like to provide translations for them? [y/n]: ").lower() == 'y':

                for code_word in missing_words:

                    while True:

                        print()
                        translation = input(f"Enter translations for \"{code_word}\", or leave blank to skip: ").strip().lower()
                        if not translation.replace(" ", "").strip():
                            break
                        
                        for c in "'\"~!@#$%^&*()_+\{\}|:<>?/,.;":
                            translation = translation.replace(c, "")

                        if word_to_encoded(translation) != code_word:
                            print(f"Invalid translation (\"{code_word}\" != \"{word_to_encoded(translation)}\"). Please try again.")
                            continue

                        if translation not in encodings[code_word]:
                            encodings[code_word].append(translation)
                            words_added += 1
                            break

            if words_added:
                with open("word_list.json", 'w') as f:
                    json.dump(encodings, f)
                print()
                print(f"Word list has been updated with {words_added} new words.")

        print()
        if input("Would you like to add any additional words to the corpus? [y/n]: ").lower() == 'y':
            print()
            words_added = 0
            while True:

                word = input("Enter word, or leave blank to stop: ").strip().lower()
                if not word: break

                for c in "'\"~!@#$%^&*()_+\{\}|:<>?/,.;":
                    word = word.replace(c, "")
                code_word = word_to_encoded(word)

                if word not in encodings[code_word]:
                    encodings[code_word].append(word)
                    words_added += 1
                else:
                    print("This word is already in the corpus!")

            if words_added:
                with open("word_list.json", 'w') as f:
                    json.dump(encodings, f)
                print()
                print(f"Word list has been updated with {words_added} new words.")
            
            
            
            
        

    