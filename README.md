# Spell Checker Evaluation

This project evaluates and compares various spell checkers using a dataset made by Wikipedia editors.

## Dataset

The dataset used for this evaluation is sourced from the [Wikipedia dataset](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html). The dataset contains pairs of correctly spelled words and their corresponding misspellings.

### Dataset Format

- Each correct word is preceded by a dollar sign `$` and followed by its misspellings, each in a new line, without duplicates.
- If a spelling or misspelling contains a space, it is replaced by an underscore (e.g., `a_lot`, `Christ_mas`).
- The dataset includes non-word misspellings as well as real-word errors.

#### Example Format

```
$correctword
misspelling1
misspelling2
...
```

## Installation

### Required Python Packages

```bash
pip install pandas
pip install scikit-learn
pip install pyspellchecker
pip install autocorrect
pip install textblob
```
After installing TextBlob, run the following command to download necessary resources:
```
python3 -m textblob.download_corpora
```
The installation instructions for TextBlob were found on the [TextBlob installation site](https://textblob.readthedocs.io/en/dev/install.html).

### Jamspell Installation

To install Jamspell, first install SWIG version 3:

```bash
wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz
tar -xvf swig-3.0.12.tar.gz
cd swig-3.0.12
./configure
make
sudo make install
```

Then, install Jamspell:

```bash
pip install jamspell
```

- Download the English model from the [Jamspell GitHub repository](https://github.com/bakwc/JamSpell?tab=readme-ov-file#download-models).

### Hunspell Installation

```bash
sudo apt-get install libhunspell-dev
pip install hunspell
sudo apt-get install hunspell-en-us
```
The dependencies for Hunspell are downloaded as described on [this GitHub page](https://github.com/postmodern/hunspell.cr?tab=readme-ov-file#installation).

## Scripts

### Data Preparation Script

The script `task.py` processes the dataset by reading from `data.txt` and generating a structured CSV file `dataset.csv` with pairs of correct and incorrect words. It uses the dataset format as described above.

### Evaluation Script

The script evaluates various spell checkers, including PySpellChecker, TextBlob, Hunspell, Jamspell, and Autocorrect. 

## Usage

1. **Prepare Dataset**: Ensure that `data.txt` is located in the same directory as the script. Run the script to generate `dataset.csv`.

2. **Run Evaluations**: Execute the `spell_checkers_evaluation.py` script to evaluate all spell checkers. The results are saved to `spell_checker_results.csv`.

## Documentation

### Metrics

- **Precision**: Number of true positive results divided by the total number of positive predictions(true positives + false positives). A higher precision indicates fewer false positives.

- **Recall**: Number of true positive results divided by the total number of actual positives(true positives + false negatives). A higher recall indicates fewer false negatives.

- **Accuracy**: Number of correct predictions (both true positives and true negatives) divided by the total number of predictions.

- **Errors Percent**: The percentage of words that remain incorrect after spell checking. It calculates the spell checker's failure rate in correcting misspellings.

- **Top 7 Errors Percent**: The percentage of misspelled words not corrected by one of the top 7 suggestions provided by the spell checker.

- **Fix Rate**: The percentage of misspelled words that were correctly fixed by the spell checker.

- **Top 7 Fix Rate**: The percentage of misspelled words corrected by one of the top 7 suggestions.

- **Broken Percent**: The percentage of originally correct words that were wrongly altered by the spell checker.

- **Speed (words/sec)**: The number of words processed by the spell checker per second.

### Tools


- **pandas**: For data manipulation and handling.
- **scikit-learn**: For evaluation metrics like precision, recall, and accuracy.
- **pyspellchecker**: A simple spell checker library.
- **autocorrect**: For automatic spelling correction.
- **textblob**: A library for natural language processing tasks.
- **jamspell**: For advanced spell checking using language models.
- **hunspell**: A spell checker and morphological analyzer library.
