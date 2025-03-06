import streamlit as st
import random

# Setup the Streamlit app
st.set_page_config(page_title="🧩 Word Scramble Game", layout="wide", initial_sidebar_state="expanded")

# Word lists for each category with related icons
WORD_CATEGORIES = {
    "Vegetables": {"icon": "🥦", "words": ["tomato", "carrot", "potato", "onion", "spinach"]},
    "Animals": {"icon": "🐶", "words": ["tiger", "elephant", "giraffe", "monkey", "zebra"]},
    "Fruits": {"icon": "🍎", "words": ["banana", "apple", "mango", "cherry", "grape"]},
    "Countries": {"icon": "🌍", "words": ["canada", "germany", "brazil", "india", "france"]},
    "Colors": {"icon": "🎨", "words": ["red", "blue", "green", "yellow", "purple"]},
    "Sports": {"icon": "⚽", "words": ["football", "tennis", "cricket", "hockey", "golf"]},
    "Body Parts": {"icon": "🦵", "words": ["heart", "liver", "brain", "stomach", "lungs"]},
    "Clothes": {"icon": "👕", "words": ["shirt", "jeans", "jacket", "socks", "scarf"]},
    "Professions": {"icon": "👩‍⚕️", "words": ["doctor", "engineer", "teacher", "artist", "lawyer"]}
}

# Initialize session state variables
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "scrambled_word" not in st.session_state:
    st.session_state.scrambled_word = ""
if "original_word" not in st.session_state:
    st.session_state.original_word = ""
if "message" not in st.session_state:
    st.session_state.message = ""
if "show_correct_answer" not in st.session_state:
    st.session_state.show_correct_answer = False

# Function to scramble words
def scramble_word(word):
    return "".join(random.sample(word, len(word)))

# Function to start a new round
def new_word():
    category = st.session_state.selected_category
    word = random.choice(WORD_CATEGORIES[category]["words"])  # Pick a new random word
    st.session_state.original_word = word
    st.session_state.scrambled_word = scramble_word(word)
    st.session_state.message = ""  # Reset message
    st.session_state.show_correct_answer = False  # Reset correct answer display

# Function to start the game with a selected category
def start_game(category):
    st.session_state.selected_category = category
    new_word()

# **Page 1: Category Selection**
if st.session_state.selected_category is None:
    st.title("🧩 Word Scramble Game")
    st.header("Select a category to start ✨")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(3)  # Create three columns for buttons

    for i, (category, data) in enumerate(WORD_CATEGORIES.items()):  # Iterate over category dictionary
        with cols[i % 3]:  # Distribute buttons across columns
            if st.button(f"{data['icon']} {category}", use_container_width=True):  # Add icon to button text
                start_game(category)  # Start the game with the selected category
                st.rerun()  # Refresh Streamlit app to load the new category

# **Page 2: Game Page (Scrambled Word & Input Field)**
else:
    st.title(f"🔠 {st.session_state.selected_category} Word Scramble")

    # Show scrambled word
    st.subheader(f"🌀 Unscramble this: **{st.session_state.scrambled_word}**")

    # Custom styling for larger input field
    st.markdown(
        """
        <style>
        .big-input input {
            font-size: 24px !important;
            height: 50px !important;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input field for user answer (with larger size)
    user_input = st.text_input("🔤 Enter your answer:", key="user_input", help="Type your answer here")
    
    # Apply the custom CSS class
    st.markdown('<div class="big-input"></div>', unsafe_allow_html=True)

    if st.button("Submit Answer"):
        if user_input.lower() == st.session_state.original_word:
            st.session_state.message = "✅ Correct! Well done! 🎉"
            st.session_state.show_correct_answer = False  # Hide correct answer message
        else:
            st.session_state.message = "❌ Wrong! Try again. 😕"
            st.session_state.show_correct_answer = True  # Show correct answer
        st.rerun()

    # Display the message (Correct/Wrong)
    if st.session_state.message:
        st.markdown(f"### {st.session_state.message}")

    # Show correct answer if user got it wrong
    if st.session_state.show_correct_answer:
        st.warning(f"✅ The correct answer was: **{st.session_state.original_word}**")

    col1, col2 = st.columns([1, 1])

    # "Next" button to get another word from the same category
    with col1:
        if st.button("➡ Next Word"):
            new_word()
            st.rerun()

    # "Back to Categories" button
    with col2:
        if st.button("🔙 Back to Categories"):
            st.session_state.selected_category = None
            st.session_state.scrambled_word = ""
            st.session_state.original_word = ""
            st.session_state.message = ""
            st.session_state.show_correct_answer = False
            st.rerun()
