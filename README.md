# ayg-text-editor

ayg-text-editor is a Python-based text editor that highlights misspelled or scrambled words in real-time as you type. It uses an unscrambling algorithm to automatically correct the highlighted words and replaces them with the correct versions.

## Features
- **Real-time Word Correction**: Detects and corrects scrambled or misspelled words as you type.
- **Word Highlighting**: Highlights incorrect words in red for easy identification.
- **Basic Text Editor Functionalities**: Create, open, save, and edit text files.
- **Multithreading**: Ensures smooth and responsive text editing and word correction.

## How It Works
1. **Highlighting**: The application highlights words that are not found in the English words corpus provided by NLTK.
2. **Queue-Based Correction**: The highlighted word is placed in a queue, where a separate thread processes it to find the correct word using an unscrambling algorithm.
3. **Replacement**: Once the correct word is found, it replaces the highlighted word in the text editor.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Kasmik004/ayg-text-editor
    cd ayg-text-editor
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the NLTK words corpus:
    ```python
    python -m nltk.downloader words
    ```

5. Run the application:
    ```bash
    python editor.py
    ```

## Usage

- **Creating a New File**: Select `File > New` to create a new text document.
- **Opening a File**: Select `File > Open` to open an existing text document.
- **Saving a File**: Select `File > Save` to save the current document.
- **Checking Text**: The application will automatically highlight and correct scrambled or misspelled words as you type.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

