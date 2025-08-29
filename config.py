"""
설정 관리 모듈
Streamlit 세션 상태 초기화 및 페이지 설정을 담당합니다.
"""
import streamlit as st
import os

# 상수 정의
UPLOAD_DIRECTORY = "uploads"
PAGE_TITLE = "Assistants API 챗봇"
PAGE_ICON = "🤖"

def ensure_upload_directory():
    """업로드 디렉토리가 존재하는지 확인하고 없으면 생성"""
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

def configure_page():
    """Streamlit 페이지 기본 설정"""
    st.set_page_config(
        page_title=PAGE_TITLE, 
        page_icon=PAGE_ICON, 
        layout="wide"
    )

def initialize_session_state():
    """세션 상태 변수들을 초기화"""
    session_defaults = {
        "messages": [],
        "thread_id": None,
        "api_key": None,
        "assistant_id": None,
        "assistant_instructions": None,
        "vector_store_id": None,
        "assistant_name": None,
        "vector_store_name": None,
        "current_page": "api_key",
        "chat_input_key": 0
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def get_sidebar_menu_config():
    """사이드바 메뉴 설정을 반환"""
    return {
        "menu_items": ["사용 가이드", "API Key 설정", "Assistant 생성", "채팅", "정보 보기", "대화 종료"],
        "icons": ['book', 'bi bi-check2-all', 'upload', 'bi bi-robot', 'database', 'trash'],
        "menu_icon": "app-indicator",
        "default_index": 0,
        "styles": {
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "#2E8B57", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        }
    }
