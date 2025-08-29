"""
채팅 페이지 모듈
"""
import streamlit as st
from openai import OpenAI
from openai_client import (
    create_message, StreamlitEventHandler, stream_assistant_response
)

def render_chat_page():
    """채팅 페이지 렌더링"""
    st.title(f"✅ {st.session_state.assistant_name or 'Assistant'}와의 채팅")
    
    if not st.session_state.api_key:
        st.error("API Key 설정 창에서 API Key를 먼저 생성해주세요!")
    elif not st.session_state.assistant_id:
        st.error('Assistant 생성 창에서 Assistant를 먼저 생성해주세요!')
    else:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=st.session_state.api_key)
        
        # Initialize chat input key if not exists
        if "chat_input_key" not in st.session_state:
            st.session_state.chat_input_key = 0

        # 채팅 입력창 (상단에 고정)
        st.markdown("---")
        prompt = st.text_input("메시지를 입력하세요:", key=f"chat_input_{st.session_state.chat_input_key}")
        st.markdown("---")
        
        # 채팅 내역을 보여줄 컨테이너
        chat_container = st.container()
        
        # 채팅 내역 표시
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # 사용자 입력 처리
        if prompt:
            # 사용자 메시지 표시
            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # 메시지 생성
            create_message(client, st.session_state.thread_id, prompt)
            
            # Assistant 응답을 위한 플레이스홀더 생성
            with chat_container:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    # 스트리밍 응답 처리
                    event_handler = StreamlitEventHandler(message_placeholder)
                    
                    # 스트리밍 실행 및 응답 받기
                    final_response = stream_assistant_response(
                        client, st.session_state.thread_id, 
                        st.session_state.assistant_id, event_handler
                    )
                    
                    # 완성된 응답을 세션 상태에 저장
                    if final_response:
                        st.session_state.messages.append({"role": "assistant", "content": final_response})
            
            # Increment the input key to clear the input field
            st.session_state.chat_input_key += 1
            st.rerun()
