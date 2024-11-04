# Spell Checker Evaluation

This project evaluates and compares various spell checkers using a dataset made by Wikipedia editors.

## Dataset

The dataset used for this evaluation is sourced from the [Wikipedia dataset](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html). The dataset contains pairs of correctly spelled words and their corresponding misspellings.

### Dataset Format

- Each correct word is preceded by a dollar sign `$` and followed by its misspellings, each in a new line, without duplicates.
- If a spelling or misspelling contains a space, it is replaced by an underscore (e.g., `light_year`).
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

"The script `scripts/generate_dataset.py` processes the dataset by reading from `data/raw/data.txt` and generating a CSV file `data/raw/dataset.csv` with pairs of correct and incorrect words. It uses the dataset format as described above."

### Evaluation Script

The script evaluates various spell checkers, including PySpellChecker, TextBlob, Hunspell, Jamspell, and Autocorrect. 

## Usage

1. **Prepare Dataset**: Ensure that `data/raw/data.txt` is present. Run `scripts/generate_dataset.py` to generate `data/raw/dataset.csv`.

2. **Run Evaluations**: Execute `scripts/spell_checkers_evaluation.py` to evaluate all spell checkers. The results will be saved to `data/processed/spell_checker_results.csv`.

## Documentation

### Metrics

- **Accuracy**: Number of correct predictions (both true positives and true negatives) divided by the total number of predictions.

- **Precision**: Number of true positive results divided by the total number of positive predictions(true positives + false positives). A higher precision indicates fewer false positives.

- **Recall**: Number of true positive results divided by the total number of actual positives(true positives + false negatives). A higher recall indicates fewer false negatives.


- **Errors Percent**: The percentage of words that remain incorrect after spell checking.

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

### Results Summary

The evaluation results indicate different levels of performance among the spell checkers:

- **Efficiency**: 
  - **Jamspell** demonstrated the highest speed at 371.94 words/sec, making it significantly faster than other checkers.
  - **Autocorrect** showed good speed at 35.62 words/sec, followed by Hunspell at 22.71 words/sec.
  - **PySpellChecker** and **TextBlob** were the slowest, processing around 4 words/sec.

- **Effectiveness**:
  - **Hunspell** performed best with 75.6% accuracy and the highest fix rate, along with an impressive 90.3% top 7 fix rate.
  - **PySpellChecker** showed good performance with 73.7% accuracy and 84% top 7 fix rate.
  - **TextBlob** had the lowest performance with 61.4% accuracy.

- **Error Handling**:
  - **Hunspell** had the lowest error rate at 24.4% and best top 7 errors at 9.7%.
  - **TextBlob** showed the highest error rate at 38.6% and high top 7 errors at 29.8%.
  - **Autocorrect** had identical error and top 7 error rates (31.4%), suggesting limited suggestion capabilities.

### Analysis of Strengths and Weaknesses

- **PySpellChecker**:
  - **Strengths**: Good accuracy (73.7%) and reasonable suggestion quality (84% top 7 fix rate)
  - **Weaknesses**: Very slow processing speed (4.45 words/sec)
  - **Best for**: Applications where speed is not critical but accuracy is important

- **TextBlob**:
  - **Strengths**: Limited strengths in current evaluation
  - **Weaknesses**: Lowest accuracy (61.4%), slow speed (4.07 words/sec), high error rate (38.6%)
  - **Best for**: May need significant improvements before production use

- **Hunspell**:
  - **Strengths**: Best accuracy (75.6%), excellent suggestion quality (90.3% top 7 fix rate), good speed
  - **Weaknesses**: Relatively few compared to others
  - **Best for**: General-purpose spell checking where reliability is key

- **Jamspell**:
  - **Strengths**: Exceptional speed (371.94 words/sec), good suggestion quality (85.9% top 7 fix rate)
  - **Weaknesses**: Moderate accuracy (66.8%)
  - **Best for**: High-speed applications where some accuracy trade-off is acceptable

- **Autocorrect**:
  - **Strengths**: Decent speed (35.62 words/sec)
  - **Weaknesses**: Moderate accuracy (68.6%), limited suggestion capabilities
  - **Best for**: Simple spell-checking tasks where speed is more important than accuracy

### Challenges

The technical challenges encountered during this project were centered around dependency and spell checkers installation. Setting up Jamspell proved demanding as it required specific versions of SWIG and additional configuration steps. Hunspell also presented challenges, needing proper installation of dependencies. The selection of appropriate evaluation metrics was also considered to ensure a comprehensive evaluation of the spell checkers' performance.