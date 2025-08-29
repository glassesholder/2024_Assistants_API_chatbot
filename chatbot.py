"""
Assistants API 챗봇봇 애플리케이션
리팩토링된 모듈들을 통합하여 실행합니다.
"""
import streamlit as st
from streamlit_option_menu import option_menu

# 모듈 임포트
from config import configure_page, initialize_session_state, ensure_upload_directory, get_sidebar_menu_config
from components.guide_page import render_guide_page
from components.api_key_page import render_api_key_page
from components.assistant_creation_page import render_assistant_creation_page
from components.chat_page import render_chat_page
from components.info_page import render_info_page
from components.cleanup_page import render_cleanup_page

# 초기 설정
configure_page()
initialize_session_state()
ensure_upload_directory()

# 사이드바 메뉴 설정
def setup_sidebar():
    """사이드바 메뉴 설정 및 페이지 선택 처리"""
    with st.sidebar:
        
        menu_config = get_sidebar_menu_config()
        choice = option_menu(
            "", 
            menu_config["menu_items"],
            icons=menu_config["icons"],
            menu_icon=menu_config["menu_icon"],
            default_index=menu_config["default_index"],
            styles=menu_config["styles"]
        )
        
        # 페이지 매핑
        page_mapping = {
            "사용 가이드": "guide",
            "API Key 설정": "api_key", 
            "Assistant 생성": "assistant_creation",
            "채팅": "chat",
            "정보 보기": "info",
            "대화 종료": "cleanup"
        }
        
        if choice in page_mapping:
            st.session_state.current_page = page_mapping[choice]
        
        return choice

# 사이드바 설정
choice = setup_sidebar()

# 페이지 라우팅
def render_current_page():
    """현재 선택된 페이지를 렌더링"""
    page = st.session_state.current_page
    
    if page == "guide":
        render_guide_page()
    elif page == "api_key":
        render_api_key_page()
    elif page == "assistant_creation":
        render_assistant_creation_page()
    elif page == "chat":
        render_chat_page()
    elif page == "info":
        render_info_page()
    elif page == "cleanup":
        render_cleanup_page()
    else:
        render_guide_page()  # 기본 페이지

# 메인 애플리케이션 실행
if __name__ == "__main__":
    render_current_page()