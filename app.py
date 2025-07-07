import streamlit as st
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt

# Load your sales data
df = pd.read_csv("sales_data.csv")

# Set your API key securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page title
st.title("💬 Chat with Your Sales Data (Gen AI + Streamlit)")

# User input
user_question = st.text_input("Ask a question about your sales data:")

if user_question:
    with st.spinner("Thinking..."):
        prompt = f"""
You are a Python assistant. Convert the user's question into a one-line pandas code that works on the following DataFrame.
Only return the single line of code. No explanation. No comments.

Data:
{df.head().to_string(index=False)}

User question: {user_question}
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You return clean pandas code only."},
                {"role": "user", "content": prompt}
            ]
        )

        generated_code = response.choices[0].message.content.strip()

        st.markdown("**🔧 GPT-Generated Code:**")
        st.code(generated_code, language='python')

        try:
            result = eval(generated_code, {"df": df})

            st.markdown("**📊 Result:**")
            st.dataframe(result)

            if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
                try:
                    st.bar_chart(result)
                except:
                    pass

        except Exception as e:
            st.error(f"⚠️ Error executing code: {e}")
