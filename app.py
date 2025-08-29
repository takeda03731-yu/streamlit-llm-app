import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.title("専門家LLMチャットアプリ")
st.markdown("""
このアプリは、あなたの入力した質問や相談内容に対して、選択した分野の専門家になりきったAIが回答します。

1. 専門家の種類をラジオボタンで選択してください。
2. 下の入力欄に質問や相談内容を入力し、送信ボタンを押してください。
3. AIが専門家として回答します。
""")

expert_types = {
    "ITコンサルタント": "あなたは優秀なITコンサルタントです。分かりやすく、的確にアドバイスしてください。",
    "キャリアカウンセラー": "あなたは経験豊富なキャリアカウンセラーです。親身になって相談に乗り、前向きな助言をしてください。",
    "健康アドバイザー": "あなたは信頼できる健康アドバイザーです。科学的根拠に基づき、丁寧にアドバイスしてください。"
}

selected_expert = st.radio("専門家の種類を選択してください", list(expert_types.keys()))
user_input = st.text_area("質問・相談内容を入力してください", height=100)

def get_llm_response(input_text: str, expert_type: str) -> str:
    system_template = expert_types[expert_type]
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{input}")
    ])
    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run(input_text)
    return result

if st.button("送信"):
    if not user_input.strip():
        st.warning("質問・相談内容を入力してください。")
    else:
        with st.spinner("AIが回答中..."):
            answer = get_llm_response(user_input, selected_expert)
        st.markdown("#### 回答")
        st.write(answer)