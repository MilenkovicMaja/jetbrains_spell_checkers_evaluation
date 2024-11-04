import pandas as pd
from typing import Dict, List
import random

def get_dict_from_spelling_file(file_path: str) -> Dict[str, List[str]]:
    spelling_dict = {}
    current_word = None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('$'):
                current_word = line[1:]  # Remove the $ sign
                spelling_dict[current_word] = []
            elif current_word:
                spelling_dict[current_word].append(line)
                
    return spelling_dict

def create_dataset(spelling_dict: Dict[str, List[str]], num_samples: int = 1000, correct_as_incorrect_ratio: float = 0.1) -> pd.DataFrame:
    correct_words = []
    incorrect_words = []
    
    words = list(spelling_dict.keys())
    
    for _ in range(num_samples):
        chosen_word = random.choice(words)
        if random.random() < correct_as_incorrect_ratio:
            correct_words.append(chosen_word)
            incorrect_words.append(chosen_word)
        else:

            misspellings = list(spelling_dict[chosen_word])
            correct_words.append(chosen_word)
            if misspellings:
                incorrect_words.append(random.choice(misspellings))
            else:
                incorrect_words.append(chosen_word)
    
    dataset = pd.DataFrame({
        'correct': correct_words,
        'incorrect': incorrect_words
    })
    
    return dataset

def main():
    file_path = 'data/raw/data.txt'
    
    try:
        spelling_dict = get_dict_from_spelling_file(file_path)  
        dataset = create_dataset(spelling_dict)
        dataset.to_csv('dataset.csv', index=False)
        
    except FileNotFoundError:
        print(f"Error: Could not find file at {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
