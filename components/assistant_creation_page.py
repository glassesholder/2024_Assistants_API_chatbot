"""
Assistant 생성 페이지 모듈
"""
import streamlit as st
import time
from openai import OpenAI
from openai_client import (
    create_vector_store, upload_files_to_vector_store, 
    create_assistant, create_thread
)
from file_manager import prepare_file_handles, close_file_handles, cleanup_files

def render_assistant_creation_page():
    """Assistant 생성 페이지 렌더링"""
    st.title("✅ Assistant 생성")
    
    if st.session_state.assistant_id:
        st.success("이미 생성한 Assistant가 있습니다! - 정보 보기에서 확인하기")
    else:
        try:
            client = OpenAI(api_key=st.session_state.api_key)
            
            st.write("파일을 업로드하세요")
            uploaded_files = st.file_uploader(
                "여러 파일을 선택하세요",
                accept_multiple_files=True
            )
            
            if uploaded_files:
                st.write(f"업로드된 파일 수: {len(uploaded_files)}")
                    
            vector_store_name = st.text_input("파일 저장소 이름을 입력하세요")
            assistant_name = st.text_input("Assistant 이름을 입력하세요")
            instructions = st.text_area("Assistant Instructions(역할)를 입력하세요", height=400)
            st.session_state.assistant_instructions = instructions
            model = st.selectbox("모델을 선택하세요", 
                            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"])
            temperature = st.slider("Temperature", 0.1, 1.0, 0.5)
            top_p = st.slider("Top P", 0.1, 1.0, 0.5)
            
            if st.button("Assistant 생성", key="btn_create_assistant", use_container_width=True) and uploaded_files:
                with st.spinner("Assistant를 생성중입니다..."):
                    try:
                        # Vector Store 생성
                        vector_store = create_vector_store(client, vector_store_name)
                        st.session_state.vector_store_id = vector_store.id
                        st.session_state.vector_store_name = vector_store_name
                        
                        # 파일 처리
                        file_handles = None
                        file_paths = []
                        
                        try:
                            file_handles, file_paths = prepare_file_handles(uploaded_files)
                            
                            # OpenAI에 파일 업로드
                            file_batch = upload_files_to_vector_store(
                                client, vector_store.id, file_handles
                            )
                            st.success(f"{len(uploaded_files)}개의 파일이 성공적으로 업로드되었습니다!")
                            
                        finally:
                            # 파일 핸들 닫기 및 로컬 파일 삭제
                            if file_handles:
                                close_file_handles(file_handles)
                            cleanup_files(file_paths)
                        
                        # Assistant 생성
                        assistant = create_assistant(
                            client, assistant_name, instructions, model, 
                            vector_store.id, temperature, top_p
                        )
                        
                        st.session_state.assistant_id = assistant.id
                        st.session_state.assistant_name = assistant_name
                        
                        # Thread 생성
                        thread = create_thread(client)
                        st.session_state.thread_id = thread.id
                        
                        st.success("Assistant가 성공적으로 생성되었습니다!")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
                        # 오류 발생시에도 파일 정리
                        if 'file_paths' in locals():
                            cleanup_files(file_paths)
        except Exception as e:
            st.error(f"API Key 설정 창에서 API Key를 먼저 생성해주세요!")
