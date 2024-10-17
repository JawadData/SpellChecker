from collections import defaultdict, Counter
import re
import string
import math

class NgramLanguageModel_2:
    def __init__(self):
        self.bigram_counts = defaultdict(int)
        self.vocabulary = set()
        self.k = 0.01
        self.resultats = None
        self.word_freq = None
        self.train = None
        self.test = None
        self.ngram_size =2
        self.autocomplete_words = []
        self.autocomplete_vocab = set()

    def prepare_data(self, infile):

        try:
          
            with open(infile, "r", encoding="utf-8") as file:
                sentences = [
                    re.sub(
                        r'[{}0-9]'.format(re.escape(string.punctuation)),
                        '',
                        sentence.strip().lower()
                    )
                    for sentence in file.readlines() if sentence.strip()
                ]
        except FileNotFoundError:
            print("Fichier non trouvé ou impossible à lire.")

            sentences = [
                re.sub(
                    r'[{}0-9]'.format(re.escape(string.punctuation)),
                    '',
                    infile.strip().lower()
                )
            ]

        for sentence in sentences:
            self.autocomplete_words.extend(sentence.split())
        self.autocomplete_vocab = set(self.autocomplete_words)

        processed_sentences = ["<s> " + sent + " </s>" for sent in sentences]

        words = [word for sentence in processed_sentences for word in sentence.split()]
        self.word_freq = Counter(words)
        words = [word if self.word_freq[word] > 0 else "<UNK>" for word in words]
        self.vocabulary = set(words)

        self.train_text = ' '.join(words)

    def train_model(self, infile=""):

        self.prepare_data(infile)

        words = self.train_text.split()
        for i in range(len(words) - self.ngram_size + 1):
            bigram = tuple(words[i:i+2])
            self.bigram_counts[bigram] += 1

        self.results = {}

        print("Bigrammes comptés :")
        for bigram, count in self.bigram_counts.items():
            first_word = bigram[0]
            
            count_first_word = self.word_freq[first_word]
            probability = (count + self.k) / (count_first_word + self.k * len(self.vocabulary))
            log_probability = math.log(probability)
            self.results[bigram] = {'Probabilité': probability, 'Log Probabilité': log_probability}

        return self.results

    def delete_letter(self, word):
   
        delete_l = []
        split_l = [(word[:c], word[c:]) for c in range(len(word))]
        for a, b in split_l:
            if b:
                delete_l.append(a + b[1:])
        return delete_l

    def substituate_letter(self, word):
  
        letters = 'abcdefghijklmnopqrstuvwxyz'
        replace_l = []
        split_l = [(word[:c], word[c:]) for c in range(len(word))]

        replace_l = [
            a + l + (b[1:] if len(b) > 1 else '')
            for a, b in split_l if b
            for l in letters
        ]
        replace_set = set(replace_l)
        replace_set.discard(word)  
        replace_l = sorted(list(replace_set))
        return replace_l

    def insert_letter(self, word):

        letters = 'abcdefghijklmnopqrstuvwxyz'
        insert_l = []
        split_l = [(word[:c], word[c:]) for c in range(len(word)+1)]
        insert_l = [a + l + b for a, b in split_l for l in letters]
        return insert_l

    def edits1(self, word, allow_switches=True):

        edits1_set = set()

        edits1_set.update(self.delete_letter(word))
        if allow_switches:
            edits1_set.update(self.substituate_letter(word))
            edits1_set.update(self.insert_letter(word))

        return edits1_set

    def edits2(self, word, allow_switches=True):

        edits2_set = set()

        edit_one = self.edits1(word, allow_switches=allow_switches)
        for w in edit_one:
            if w:
                edit_two = self.edits1(w, allow_switches=allow_switches)
                edits2_set.update(edit_two)

        return edits2_set

    def candidates_without_probabilities(self, word):

        suggestions_1 = self.edits1(word).intersection(self.autocomplete_vocab)
        suggestions_2 = self.edits2(word).intersection(self.autocomplete_vocab)

        suggestions = list(suggestions_1.union(suggestions_2))
        return suggestions
    
    def correct_spelling_with_same_letter(self, word, candidates):
        word = word.lower()
   
        filtered_candidates = [w for w in candidates if w.startswith(word[0])]
        return filtered_candidates

    def autocorrect_with_probabilities(self, input_text, candidates):

        if not self.results:
            print("Aucun modèle entraîné. Utilisez train_model d'abord.")
            return None

        words = input_text.split()

        if len(words) < self.ngram_size:
            print("Pas assez de mots pour former un n-gramme.")
            return None

        n_gram = tuple(words[-2:])

        candidates_probabilities = {}
        for candidate in candidates:
            current_n_gram = (n_gram[0], candidate)
            if current_n_gram in self.results:
                candidates_probabilities[candidate] = self.results[current_n_gram]['Probabilité']

        if not candidates_probabilities:
            print("Aucun candidat trouvé dans les résultats.")
            return None

        best_candidate = max(candidates_probabilities, key=candidates_probabilities.get)
        return best_candidate

