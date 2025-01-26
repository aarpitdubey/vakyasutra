import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


SYSTEM_TEMPLATE = '''

    Below is a draft text that may be poorly worded.  
Your goal is to:  
- Properly redact the draft text  
- Convert the draft text to a specified tone  
- Convert the draft text to a specified dialect  

### Here are some examples of different Tones:  
- **Standard**: The project has been completed successfully, meeting all required criteria and deadlines. The team’s effort was commendable and consistent throughout the process.  
- **Fluency**: The team smoothly completed the project, adhering to all requirements and deadlines. Their dedication and teamwork made the entire process seamless and efficient.  
- **Natural**: We wrapped up the project on time and met all the requirements! Everyone on the team worked together so well to make it happen.  
- **Formal**: We are pleased to announce the successful completion of the project, which adhered to all stipulated requirements and deadlines. The team demonstrated commendable effort and diligence throughout.  
- **Academic**: The project was executed within the established parameters, achieving compliance with the prescribed criteria and deadlines. This outcome highlights the team’s exceptional proficiency and commitment.  
- **Simple**: The project is finished. We did everything we needed to and got it done on time.  
- **Creative**: Imagine a clock ticking down as a team races against time, crafting brilliance at every step. With every deadline met and every detail perfected, the project’s completion marks a tale of dedication and triumph.  
- **Expand**: The project was not just completed but also exceeded expectations. Each team member put in significant effort to ensure we met the deadlines while maintaining exceptional quality. This accomplishment is a testament to our collective dedication and hard work.  
- **Shorten**: The project is done successfully, on time, and as required.  
- **Custom**: [Describe the desired tone here, e.g., motivational, empathetic, humorous, etc.] You can specify any desired tone, such as motivational, empathetic, humorous, or others. For example:  
  - **Motivational**: "You’ve done an incredible job! This project’s success is proof of your hard work and dedication. Keep pushing boundaries, and even greater achievements await."  
  - **Empathetic**: "We understand the challenges you faced during this project, and we deeply appreciate the effort you put in. Your hard work and resilience have led to a fantastic result."  
  - **Humorous**: "Well, look at that—we finished the project, and no one had to bribe the coffee machine! Fantastic teamwork, everyone. Let’s keep the streak going."  


### Here are some examples of words in different dialects:  
- **American**: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield  
- **British**: chips, candyfloss, flat, rubbish, biscuit, green fingers, car park, trousers, windscreen  

### Example Sentences from each dialect:  
- **American**: The project has been completed successfully, meeting all required criteria and deadlines. The team’s effort was commendable and consistent throughout the process.  
- **British**: The project has been completed successfully, adhering to all specified criteria and timelines. The team’s performance was exemplary and unwavering throughout the endeavour.  

### Instructions:  
Please start the redaction with a warm introduction. Add the introduction if you need to.  

Below is the draft text, tone, and dialect:  
DRAFT: {draft}  
TONE: {tone}  
DIALECT: {dialect}  

YOUR {dialect} RESPONSE:  

'''

# Prompt Template variables definition
PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["tone", "dialect", "draft"],
    template=SYSTEM_TEMPLATE,
)

_ = load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# LLM and Key loading Function
def load_LLM(OPENAI_API_KEY):
    """Logic for loading the chain you want to use should go here."""
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7, openai_api_key=OPENAI_API_KEY)
    return llm

# Page title and header
st.set_page_config(page_title="Paraphrase your text")
st.header("Paraphrase your text")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Paraphrase your text in different styles.")

with col2:
    st.write("Subscribe to [aarpitdubey](https://www.linkedin.com/in/aarpitdubey/)")


# #Input OpenAI API Key
# st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = OPENAI_API_KEY
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Enter the text you want to re-write")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 1000:
    st.write("Please enter a shorter text. The maximum length is 1000 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your redaction to have?',
        ('Standard', 'Fluency', 'Natural', 'Formal', 'Academic', 'Simple', 'Creative', 'Expand', 'Shorten'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(OPENAI_API_KEY=openai_api_key)

    prompt_with_draft = PROMPT_TEMPLATE.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    # st.write(improved_redaction)

     # Access the content of the AIMessage object
    content_only = improved_redaction.content

    # Display the content only
    st.write(content_only)
