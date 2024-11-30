import os
from collections import defaultdict, Counter
from difflib import get_close_matches

class SearchEngine:
    def __init__(self):
        self.index = defaultdict(list)  # Index inversé
        self.document_word_counts = defaultdict(Counter)  # Compte des mots dans chaque document

    def index_document(self, doc_id, content):
        words = content.lower().split()
        for word in words:
            self.index[word].append(doc_id)
        self.document_word_counts[doc_id].update(words)

    def search(self, query, operator="ET", fuzzy=False):
        query_words = query.lower().split()
        results = None

        for word in query_words:
            if fuzzy:
                similar_words = self.find_similar_words(word)
                matching_docs = set(
                    doc_id for similar_word in similar_words for doc_id in self.index.get(similar_word, [])
                )
            else:
                matching_docs = set(self.index.get(word, []))

            if results is None:
                results = matching_docs
            elif operator == "ET":
                results.intersection_update(matching_docs)
            elif operator == "OU":
                results.update(matching_docs)

        return self.rank_results(query_words, results) if results else []

    def rank_results(self, query_words, results):
        relevance_scores = {}
        for doc_id in results:
            relevance_scores[doc_id] = sum(
                self.document_word_counts[doc_id][word] for word in query_words if word in self.document_word_counts[doc_id]
            )
        ranked_results = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in ranked_results]

    def find_similar_words(self, word, cutoff=0.8):
        return get_close_matches(word, self.index.keys(), n=5, cutoff=cutoff)
