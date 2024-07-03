import tkinter as tk
from tkinter import filedialog, messagebox
import nltk
from nltk.corpus import words
import queue
import threading
from itertools import permutations

# Ensure the words corpus is downloaded
nltk.download("words")
word_list = set(words.words())


def unscramble(word):
    valid_words = set()
    for perm in ["".join(p) for p in permutations(word)]:
        if perm.lower() in word_list:
            valid_words.add(perm)
            break
    return valid_words.pop() if valid_words else None


class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ayg-text-editor")

        self.text_area = tk.Text(self.window, wrap=tk.WORD)
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)
        self.text_area.bind("<space>", self.check_current_word)

        self.create_menu()

        self.q = queue.Queue()
        self.q_answer = queue.Queue()
        self.stop_event = threading.Event()

        self.worker_thread = threading.Thread(target=self.run_unscramble)
        self.worker_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Check Text", command=self.check_text)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file:
            self.window.title(f"ayg-text-editor - {file}")
            self.text_area.delete(1.0, tk.END)
            with open(file, "r") as file_handler:
                self.text_area.insert(tk.INSERT, file_handler.read())

    def save_file(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file:
            with open(file, "w") as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window.title(f"ayg-text-editor - {file}")

    def check_text(self):
        text_content = self.text_area.get("1.0", tk.END).strip()
        words_in_text = text_content.split()
        incorrect_words = [
            word for word in words_in_text if word.lower() not in word_list
        ]

        if incorrect_words:
            messagebox.showinfo(
                "Incorrect Words",
                f"Incorrect words found: {', '.join(incorrect_words)}",
            )
        else:
            messagebox.showinfo("Correct Words", "All words are correct!")

    def check_current_word(self, event=None):
        cursor_index = self.text_area.index(tk.INSERT)
        text_content = self.text_area.get("1.0", cursor_index).split()
        if text_content:
            current_word = text_content[-1]
            if current_word.lower() not in word_list:
                self.highlight_word(cursor_index, len(current_word))
                self.q.put((current_word, cursor_index))
            else:
                self.remove_highlight(cursor_index, len(current_word))

    def highlight_word(self, cursor_index, word_length):
        start_index = f"{cursor_index} - {word_length}c"
        end_index = cursor_index
        self.text_area.tag_add("incorrect", start_index, end_index)
        self.text_area.tag_config("incorrect", foreground="red")

    def remove_highlight(self, cursor_index, word_length):
        start_index = f"{cursor_index} - {word_length}c"
        end_index = cursor_index
        self.text_area.tag_remove("incorrect", start_index, end_index)

    def run_unscramble(self):
        while True:
            original_word, cursor_index = self.q.get()
            if original_word is None:
                break
            corrected_word = unscramble(original_word)
            self.q_answer.put((original_word, corrected_word, cursor_index))
            self.q.task_done()
            self.update_text_area()

    def update_text_area(self):
        while not self.q_answer.empty():
            original_word, corrected_word, cursor_index = self.q_answer.get()
            if corrected_word is not None:
                word_start_index = self.text_area.search(
                    original_word, cursor_index, backwards=True, stopindex="1.0"
                )
                if word_start_index:
                    word_end_index = f"{word_start_index} + {len(original_word)}c"
                    self.text_area.delete(word_start_index, word_end_index)
                    self.text_area.insert(word_start_index, corrected_word)
                    self.remove_highlight(cursor_index, len(corrected_word))

    def on_closing(self):
        self.stop_event.set()
        self.q.put((None, None))
        self.worker_thread.join()
        self.window.destroy()


if __name__ == "__main__":
    text_editor = TextEditor()
