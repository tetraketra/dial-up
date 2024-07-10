# 📞 Dial-Up 📞

Command-line [en/de]coder for an unnamed nondeterministic phone-dialpad-based code.
Supports punctuation, variable capitalization, and messages of arbitrary length.
This app is intentionally built to use no dependencies. 
You do not need to build an environment.

---

# 🏗️ Project Structure 🏗️
```html
dial-up
├── words
│   └── # The base words the app uses to build its corpus.
├── dial_up.py       # The app. Run as script.
├── pyproject.toml   # Linting config.
├── requirements.txt # Empty ^.^
│
│=─ word_list.json   # App corpus. Built when needed.
└=─ log.txt          # App log. Built when needed.
```

---

# 🛠️ Run Process 🛠️
```sh
git clone https://github.com/tetraketra/dial-up
cd dial-up

python3 dial_up.py # Expects 3.11 but should work on some earlier versions.

```
