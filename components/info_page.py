"""
정보 보기 페이지 모듈
"""
import streamlit as st

def render_info_page():
    """정보 보기 페이지 렌더링"""
    st.title("✅ 정보 보기")
    st.markdown(f"""
        ### 📘 저장소(vector_store)
        - {st.session_state.vector_store_name or '아직 없어요!'}
            - vector_store는 안전하게 보관됩니다.
        
        ### 📙 도우미(assistant)
        - {st.session_state.assistant_name or '아직 없어요!'}
            - assistant는 안전하게 보관됩니다.
        
        ### 📗작성한 프롬프트(instructions)
        """)
    st.code(st.session_state.assistant_instructions or '아직 작성하지 않았어요!')
