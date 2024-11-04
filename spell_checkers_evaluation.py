import pandas as pd
import time
from sklearn.metrics import precision_score, recall_score, accuracy_score

# Load results
try:
    existing_results = pd.read_csv('spell_checker_results.csv')
    evaluated_checkers = existing_results['Spell Checker'].tolist()
except FileNotFoundError:
    existing_results = pd.DataFrame()
    evaluated_checkers = []

# Evaluation metrics functions
def calculate_classifying_metrics(y_true, y_pred):
    #Precision, recall, and accuracy
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    return precision, recall, accuracy

def evaluate_spell_checker(y_true, y_pred, suggestions, elapsed_time, word_count):
    precision, recall, accuracy = calculate_classifying_metrics(y_true, y_pred)
    errors = sum(y_true != y_pred) / len(y_true) * 100
    top_7_errors = sum(true_word not in suggs[:7] for true_word, suggs in zip(y_true, suggestions)) / len(y_true) * 100
    fixed = sum((y_true == y_pred) & (y_true != '')) / sum(y_true != '') * 100
    top_7_fixed = sum(true_word in suggs[:7] for true_word, suggs in zip(y_true, suggestions)) / len(y_true) * 100
    broken = sum((y_true != '') & (y_pred != y_true)) / sum(y_true != '') * 100
    speed = word_count / elapsed_time if elapsed_time > 0 else 0

    return {
        "Precision": precision,
        "Recall": recall,
        "Accuracy": accuracy,
        "Errors Percent": errors,
        "Top 7 Errors Percent": top_7_errors,
        "Fix Rate": fixed,
        "Top 7 Fix Rate": top_7_fixed,
        "Broken Percent": broken,
        "Speed (words/sec)": speed
    }

# Spell checker implementations
def spell_checker_pyspellchecker(word_list):
    from spellchecker import SpellChecker

    spell = SpellChecker()
    predictions = []
    suggestions = []

    for word in word_list:
        corrected = spell.correction(word)
        predictions.append(corrected if corrected else word)
        candidates = spell.candidates(word)
        suggestions.append(list(candidates) if candidates else [word])

    return predictions, suggestions

def spell_checker_textblob(word_list):
    from textblob import Word

    predictions = []
    suggestions = []

    for word in word_list:
        blob_word = Word(word)
        corrected = blob_word.correct()
        predictions.append(str(corrected) if corrected else word)
        suggs = [s[0] for s in blob_word.spellcheck()[:7]]
        suggestions.append(suggs if suggs else [word])

    return predictions, suggestions

def spell_checker_hunspell(word_list):
    import hunspell

    hspell = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
    predictions = []
    suggestions = []

    for word in word_list:
        if hspell.spell(word):
            predictions.append(word)
            suggestions.append([word])
        else:
            suggs = hspell.suggest(word)
            predictions.append(suggs[0] if suggs else word)
            suggestions.append(suggs if suggs else [word])

    return predictions, suggestions

def spell_checker_jamspell(word_list):
    import jamspell

    corrector = jamspell.TSpellCorrector()
    corrector.LoadLangModel('en.bin')

    predictions = []
    suggestions = []

    for word in word_list:

        corrected = corrector.FixFragment(word)
        predictions.append(corrected if corrected else word)
        
        suggs = corrector.GetCandidates([word], 0)
        suggestions.append(suggs if suggs else [word])

    return predictions, suggestions

def spell_checker_autocorrect(word_list):
    from autocorrect import Speller

    spell = Speller()
    predictions = []
    suggestions = []

    for word in word_list:
        corrected = spell(word)
        predictions.append(corrected if corrected else word)
        suggestions.append([corrected] if corrected else [word])

    return predictions, suggestions

def main():

    data = pd.read_csv('dataset.csv')
    
    y_true = data['correct']
    incorrect_words = data['incorrect']
    
    spell_checkers = [
        ("PySpellChecker", spell_checker_pyspellchecker),
        ("TextBlob", spell_checker_textblob),
        ("Hunspell", spell_checker_hunspell),
        ("Jamspell", spell_checker_jamspell),
        ("Autocorrect", spell_checker_autocorrect),
    ]

    new_results = []

    # Evaluate spell checkers
    for checker_name, checker_func in spell_checkers:
        if checker_name not in evaluated_checkers:
            print(f"Evaluating {checker_name}...")
            
            start_time = time.time()
            y_pred, suggestions = checker_func(incorrect_words)
            elapsed_time = time.time() - start_time
            
            print(f"Completed {checker_name} in {elapsed_time:.2f} seconds.")

            result = evaluate_spell_checker(y_true, y_pred, suggestions, elapsed_time, len(incorrect_words))
            result['Spell Checker'] = checker_name
            result['Completion Time (seconds)'] = elapsed_time
            new_results.append(result)

    if not existing_results.empty:
        combined_results = pd.concat([existing_results, pd.DataFrame(new_results)], ignore_index=True)
    else:
        combined_results = pd.DataFrame(new_results)

    combined_results.to_csv('spell_checker_results.csv', index=False)
    print("Results have been saved to spell_checker_results.csv")

if __name__ == "__main__":
    main()
