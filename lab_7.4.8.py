with open("text.txt", "w", encoding="utf-8") as f:
    f.write("даний великий текст українською мовою\n")
    f.write("ми будемо замінювати слова і видаляти зайве\n")

with open("replace.txt", "w", encoding="utf-8") as f:
    f.write("текст код\n")
    f.write("мовою програмування\n")

with open("delete.txt", "w", encoding="utf-8") as f:
    f.write("даний\n")
    f.write("ми\n")
    f.write("зайве\n")


class SentenceError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Sentence:
    def __init__(self, data=""):
        if isinstance(data, Sentence):
            self.words = data.words.copy()
        elif isinstance(data, list):
            self.words = data.copy()
        elif isinstance(data, str):
            self.words = data.split()
        else:
            self.words = []

    def __str__(self):
        return f"Об'єкт Sentence. Кількість слів: {len(self.words)}. Зміст: {' '.join(self.words)}"

    def __len__(self):
        return len(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def __setitem__(self, index, value):
        if not isinstance(value, str):
            raise SentenceError(f"Неприпустима операція: слово має бути рядком (str), отримано {type(value).__name__}.")
        self.words[index] = value

    def __add__(self, other):
        if not isinstance(other, (Sentence, str)):
            raise SentenceError(
                f"Неприпустимий тип правого операнда для операції '+': {type(other).__name__}. Очікується Sentence або str.")

        new_sentence = Sentence(self)
        if isinstance(other, Sentence):
            new_sentence.words.extend(other.words)
        elif isinstance(other, str):
            new_sentence.words.append(other)
        return new_sentence

    def __sub__(self, other):
        if not isinstance(other, (Sentence, str)):
            raise SentenceError(
                f"Неприпустимий тип правого операнда для операції '-': {type(other).__name__}. Очікується Sentence або str.")

        new_sentence = Sentence(self)
        if isinstance(other, Sentence):
            new_sentence.words = [w for w in new_sentence.words if w not in other]
        elif isinstance(other, str):
            new_sentence.words = [w for w in new_sentence.words if w != other]
        return new_sentence

    def __contains__(self, item):
        return item in self.words


try:
    with open("text.txt", "r", encoding="utf-8") as f:
        main_text = f.read()

    s = Sentence(main_text)

    with open("replace.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                old_word = parts[0]
                new_word = parts[1]
                for i in range(len(s)):
                    if s[i] == old_word:
                        s[i] = new_word

                # Демонстрація помилки 1: розкоментуйте рядок нижче, щоб перевірити
                 #s[i] = 123

    # Видалення слів
    with open("delete.txt", "r", encoding="utf-8") as f:
        words_to_delete = Sentence(f.read())

    s = s - words_to_delete

    # Демонстрація помилки 2: розкоментуйте рядок нижче, щоб перевірити
    # s = s - 456

    print(f"Загальна кількість слів відкоригованого тексту: {len(s)}")
    print(s)

except SentenceError as e:
    print(f"Зловлено виключення: {e}")
except Exception as e:
    print(f"Виникла інша помилка: {e}")