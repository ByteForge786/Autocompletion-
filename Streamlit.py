import streamlit as st
from typing import List
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search_prefix(self, prefix: str) -> List[str]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        return self._dfs(node, prefix)

    def _dfs(self, node: TrieNode, prefix: str) -> List[str]:
        results = []
        if node.is_end:
            results.append(prefix)
        
        for char, child_node in node.children.items():
            results.extend(self._dfs(child_node, prefix + char))
        
        return results

# Initialize Trie with your knowledge base
trie = Trie()
knowledge_base = [
    "apple", "application", "apply",
    "banana", "bandana",
    "cat", "category",
    # Add more words/phrases from your knowledge base
]

for word in knowledge_base:
    trie.insert(word)

# Streamlit interface
st.title("Autocomplete with Custom Knowledge Base")

# Initialize session state
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""
if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = time.time()

# Text input
user_input = st.text_input("Start typing:", key="user_input")

# Autocomplete logic
if user_input and (user_input != st.session_state.last_input or time.time() - st.session_state.last_update_time > 2):
    completions = trie.search_prefix(user_input)
    st.session_state.last_input = user_input
    st.session_state.last_update_time = time.time()
    
    # Display autocomplete suggestions
    if completions:
        suggestion = st.selectbox("Autocomplete suggestions:", completions)
        if st.button("Use Suggestion"):
            st.session_state.user_input = suggestion
            st.experimental_rerun()

# Handle Tab key press
if st.session_state.user_input != st.session_state.last_input:
    st.session_state.last_input = st.session_state.user_input
    completions = trie.search_prefix(st.session_state.user_input)
    if completions:
        st.session_state.user_input = completions[0]
    st.experimental_rerun()
