import streamlit as st
from textblob import TextBlob
import language_tool_python

# ------------------ Cached Grammar Tool ------------------

@st.cache_resource
def load_grammar_tool():
"""Load LanguageTool only once to avoid re-downloading each time."""
    return language_tool_python.LanguageTool('en-US')

# ------------------ Spell & Grammar Module ------------------

class SpellCheckerModule:
def **init**(self):
self.spell_check = TextBlob("")
self.grammar_tool = load_grammar_tool()

```
def correct_spell(self, text):
    words = text.split()
    corrected_words = []
    mistakes = 0
    for word in words:
        corrected_word = str(TextBlob(word).correct())
        if corrected_word.lower() != word.lower():
            mistakes += 1
        corrected_words.append(corrected_word)
    return " ".join(corrected_words), mistakes

def correct_grammar(self, text):
    try:
        matches = self.grammar_tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        foundmistakes = [match.ruleId for match in matches]
        foundmistakes_count = len(foundmistakes)
        return foundmistakes, foundmistakes_count, corrected_text
    except Exception as e:
        st.error("⚠️ Grammar checking failed. Please try again later.")
        return [], 0, text
```

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Grammar & Spelling Checker", layout="wide")
st.title("📝 Grammar & Spelling Checker")
st.markdown("Enhance your writing with AI-powered grammar and spelling correction! ✨")

st.markdown("### Choose Input Method")
option = st.radio("Select input type:", ["Type Text", "Upload File"], horizontal=True)

user_text = ""

if option == "Type Text":
user_text = st.text_area("Enter your text below:", height=200)
else:
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
if uploaded_file is not None:
user_text = uploaded_file.read().decode("utf-8")
st.text_area("File Content:", user_text, height=200, label_visibility="collapsed")

st.markdown("---")
st.markdown("### Select Check Option")

check_option = st.radio(
"Choose what you want to check:",
["🔤 Spelling Check", "🧩 Grammar Check", "✅ Both"],
horizontal=True
)

if st.button("🚀 Check Text"):
if user_text.strip() == "":
st.warning("⚠️ Please enter or upload some text first.")
else:
obj = SpellCheckerModule()
corrected_text = user_text
spelling_mistakes = grammar_mistakes = 0

```
    if check_option == "✅ Both":
        corrected_text, spelling_mistakes = obj.correct_spell(corrected_text)
        mistakes, grammar_mistakes, grammar_result = obj.correct_grammar(corrected_text)
        corrected_text = grammar_result

    elif check_option == "🔤 Spelling Check":
        corrected_text, spelling_mistakes = obj.correct_spell(corrected_text)

    elif check_option == "🧩 Grammar Check":
        mistakes, grammar_mistakes, grammar_result = obj.correct_grammar(corrected_text)
        corrected_text = grammar_result

    # Layout: Two columns (Original | Corrected)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🧾 Original Text")
        st.text_area("Original text:", user_text, height=250)
    with col2:
        st.subheader("✨ Corrected Text")
        st.text_area("Corrected text:", corrected_text, height=250)

    # Results Summary
    st.markdown("---")
    st.subheader("📊 Results Summary")

    colA, colB, colC = st.columns(3)
    colA.metric("Spelling Mistakes", spelling_mistakes)
    colB.metric("Grammar Mistakes", grammar_mistakes)
    total = spelling_mistakes + grammar_mistakes
    colC.metric("Total Issues Found", total)

    st.success("✅ Text checked successfully!")
```

st.markdown("---")
st.caption("Developed by Ahad Raza | NLP Project Practice")

