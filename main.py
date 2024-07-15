import streamlit as st
import pandas as pd
import random

random.seed(42)

st.title('Data Tagging App')
df = pd.read_csv('questions.csv')

# Initialize session state for num
if 'index' not in st.session_state:
    st.session_state['index'] = 0

if 'gpt_score' not in st.session_state:
    st.session_state['gpt_score'] = 1
if 'mixtral_score' not in st.session_state:
    st.session_state['mixtral_score'] = 1
if 'qwen_score' not in st.session_state:
    st.session_state['qwen_score'] = 1
if 'llama_score' not in st.session_state:
    st.session_state['llama_score'] = 1

def update_score(score: int, model: str):
    st.session_state[f'{model}_score'] = score

# Function to increment the claim number
def increment_claim():
    df.loc[num, 'gpt_score'] = st.session_state['gpt_score']
    df.loc[num, 'mixtral_score'] = st.session_state['mixtral_score']
    df.loc[num, 'qwen_score'] = st.session_state['qwen_score']
    df.loc[num, 'llama_score'] = st.session_state['llama_score']

    st.session_state['gpt_score'] = 1
    st.session_state['mixtral_score'] = 1
    st.session_state['qwen_score'] = 1
    st.session_state['llama_score'] = 1
    df.to_csv('questions.csv', index=False)

    print(df.head())
    st.session_state['index'] += 1

# Get the current claim number
num = st.session_state['index']

if num < len(df):
    # Display the current claim
    st.title(f"Claim #{num + 1} of {len(df)}")
    st.write(df.iloc[num]['claim'])
    st.divider()
    answers = []
    for col in ['gpt', 'qwen', 'mixtral', 'llama']:
        answers.append({'model': col, 'answer': df.iloc[num][f"{col}_answer"]})
    random.shuffle(answers)
    for index, answer in enumerate(answers):
        st.write(answer['answer'])
        rating = st.slider('Rate this claim between 1 and 10', min_value=1, max_value=10, step=1, key=str(answer['model']))
        if rating:
            update_score(rating, answer['model'])
        st.divider()
    
    # Button to go to the next claim
    # st.button('Next', on_click=increment_claim)
    if st.button('Next', on_click=increment_claim):
        st.experimental_rerun()
        
        # JavaScript to scroll to top after button click
        scroll_to_top_script = """
        <script>
            window.scrollTo({top: 0});
        </script>
        """
        st.markdown(scroll_to_top_script, unsafe_allow_html=True)
else:
    st.write("Download the CSV file to see the results and send to Yonatan")
    st.download_button(
        label="Download Results",
        data=df.to_csv(index=False),
        file_name='results.csv',
        mime='text/csv'
    )
