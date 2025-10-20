import streamlit as st
from textblob import TextBlob
import language_tool_python

# ------------------ Cached Grammar Tool Loader ------------------ #
@st.cache_resource
def load_grammar_tool():
    return language_tool_python.LanguageTool('en-US')


# ------------------ Spell & Grammar Module ------------------ #
class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        # Load the grammar tool from cache
        self.grammar_tool = load_grammar_tool()

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
        matches = self.grammar_tool.check(text)
        corrected_text = language_tool_python.utils.correct(text, matches)
        foundmistakes = [match.ruleId for match in matches]
        foundmistakes_count = len(foundmistakes)
        return foundmistakes, foundmistakes_count, corrected_text


# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="Grammar & Spelling Checker", layout="wide")
st.markdown(
        """
        <h1 style="text-align:center;">📝 Grammar & Spelling Checker</h1>
       
        """,
        unsafe_allow_html=True,
    )
st.markdown("---")

# --- Two-column layout with border ---
col1, col_sep, col2 = st.columns([1, 0.02, 2])  # middle column is thin for the divider

# Add a vertical separator (border) between columns
st.markdown(
    """
    <style>
    .stColumn:nth-child(1) {
        border-right: 2px solid #ccc;  /* Green border */
        padding-right: 15px;
    }
    .stColumn:nth-child(2) {
        padding-left: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with col1:
   
    # Column heading describing its purpose
    st.markdown("### ⚙️ Configuration ")

    # Add a blockquote-style quote
    st.markdown(
        """
        <blockquote style='border-left: 4px solid #4CAF50; padding-left: 10px; color: #555; font-style: italic;'>
        “Customize how you want to check your text from here.”
        </blockquote>
        """,
        unsafe_allow_html=True
    )

    

    option = st.selectbox(
        "Select Input Method",  # empty string since label is already in markdown
        ["Type Text", "Upload File"],
        index=0
    )
    
   
    check_option = st.radio(
        "Choose Check Option",  # empty string since label is already in markdown
        ["Spelling Only", "Grammar Only", "Both"],
        horizontal=False
    )

    
    st.markdown("---")

    # Placeholder for summary metrics (filled after correction)
    summary_placeholder = st.empty()

with col_sep:
    # vertical separator
    st.markdown(
        """
        <div style='border-left: 2px solid #999; height: 100%; margin: 0 auto;'></div>
        """,
        unsafe_allow_html=True
    )
with col2:
    # Centered title and subtitle
    user_text = ""

    if option == "Type Text":
        user_text = st.text_area("Enter Your Text Below",height=200)
    else:
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
        if uploaded_file is not None:
            user_text = uploaded_file.read().decode("utf-8")
            st.text_area("File Content", user_text, height=200)

    st.markdown("")

    # Button to check text
    check_pressed = st.button(" Correct Text")

    # Result placeholders (appear after button click)
    result_area = st.container()

if check_pressed:
    if user_text.strip() == "":
        st.warning("⚠️ Please enter or upload some text first.")
    else:
        obj = SpellCheckerModule()
        corrected_text = user_text
        spelling_mistakes = grammar_mistakes = 0

        if check_option == "Both":
            corrected_text, spelling_mistakes = obj.correct_spell(corrected_text)
            mistakes, grammar_mistakes, grammar_result = obj.correct_grammar(
                corrected_text
            )
            corrected_text = grammar_result

        elif check_option == "Spelling Only":
            corrected_text, spelling_mistakes = obj.correct_spell(corrected_text)

        elif check_option == "Grammar Only":
            mistakes, grammar_mistakes, grammar_result = obj.correct_grammar(
                corrected_text
            )
            corrected_text = grammar_result

        # --- Update right column with results ---
        with result_area:
            st.markdown("---")
            st.markdown("### 🧾 Results")

            colA, colB = st.columns(2)
            with colA:
                st.subheader("Original Text")
                st.text_area("Original", user_text, height=250)
            with colB:
                st.subheader("Corrected Text")
                st.text_area("Corrected", corrected_text, height=250)

        # --- Update left column summary ---
        with summary_placeholder.container():
            st.markdown("### Results Summary")
            colA, colB, colC = st.columns(3)
            colA.metric("Spelling Mistakes", spelling_mistakes)
            colB.metric("Grammar Mistakes", grammar_mistakes)
            total = spelling_mistakes + grammar_mistakes
            colC.metric("Total Issues Found", total)
            st.success("Text checked successfully!")

st.markdown("---", unsafe_allow_html=True)
st.markdown(
    """
    <p style="text-align:center; font-size:14px; color:gray;">
    Developed by <b>Farhana Bibi</b> | NLP Project Practice
    </p>
    """,
    unsafe_allow_html=True,
)

















