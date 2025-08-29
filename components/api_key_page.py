"""
API Key 설정 페이지 모듈
"""
import streamlit as st
from openai_client import validate_api_key

def render_api_key_page():
    """API Key 설정 페이지 렌더링"""
    st.title("✅ API Key 설정")
    
    if st.session_state.api_key:
        st.success("API Key가 이미 설정되어 있습니다!")
    else:
        api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")
        if api_key:
            if validate_api_key(api_key):
                st.session_state.api_key = api_key
                st.success("API Key가 성공적으로 설정되었습니다!")
