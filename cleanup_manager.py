"""
OpenAI 리소스 정리 모듈
생성된 Assistant, Vector Store, Files 등을 삭제합니다.
"""
import streamlit as st
from openai import OpenAI
import time

def delete_assistant(client, assistant_id):
    """Assistant 삭제"""
    try:
        client.beta.assistants.delete(assistant_id)
        return True
    except Exception as e:
        st.error(f"Assistant 삭제 중 오류: {str(e)}")
        return False

def delete_vector_store(client, vector_store_id):
    """Vector Store 삭제"""
    try:
        client.beta.vector_stores.delete(vector_store_id)
        return True
    except Exception as e:
        st.error(f"Vector Store 삭제 중 오류: {str(e)}")
        return False

def get_vector_store_files(client, vector_store_id):
    """Vector Store에 연결된 파일 목록 조회"""
    try:
        files = client.beta.vector_stores.files.list(vector_store_id=vector_store_id)
        return [file.id for file in files.data]
    except Exception as e:
        st.error(f"파일 목록 조회 중 오류: {str(e)}")
        return []

def delete_file(client, file_id):
    """파일 삭제"""
    try:
        client.files.delete(file_id)
        return True
    except Exception as e:
        st.error(f"파일 삭제 중 오류 (ID: {file_id}): {str(e)}")
        return False

def cleanup_all_resources(client):
    """모든 OpenAI 리소스 정리"""
    cleanup_results = {
        'assistant': False,
        'vector_store': False,
        'files': [],
        'errors': []
    }
    
    try:
        # 1. Vector Store에서 파일 목록 가져오기 (Vector Store 삭제 전에 먼저)
        file_ids = []
        if st.session_state.vector_store_id:
            file_ids = get_vector_store_files(client, st.session_state.vector_store_id)
            st.write(f"삭제할 파일 수: {len(file_ids)}")
        
        # 2. 파일들 먼저 삭제 (Vector Store 삭제 전에)
        if file_ids:
            st.write("파일들 삭제 중...")
            for file_id in file_ids:
                if delete_file(client, file_id):
                    cleanup_results['files'].append(file_id)
                else:
                    cleanup_results['errors'].append(f"파일 삭제 실패: {file_id}")
            
            if cleanup_results['files']:
                st.success(f"✅ {len(cleanup_results['files'])}개의 파일이 삭제되었습니다.")
        
        # 3. Vector Store 삭제 (파일 삭제 후)
        if st.session_state.vector_store_id:
            st.write("Vector Store 삭제 중...")
            if delete_vector_store(client, st.session_state.vector_store_id):
                cleanup_results['vector_store'] = True
                st.success("✅ Vector Store가 삭제되었습니다.")
            else:
                cleanup_results['errors'].append("Vector Store 삭제 실패")
        
        # 4. Assistant 삭제 (마지막)
        if st.session_state.assistant_id:
            st.write("Assistant 삭제 중...")
            if delete_assistant(client, st.session_state.assistant_id):
                cleanup_results['assistant'] = True
                st.success("✅ Assistant가 삭제되었습니다.")
            else:
                cleanup_results['errors'].append("Assistant 삭제 실패")
        
        return cleanup_results
        
    except Exception as e:
        st.error(f"리소스 정리 중 예상치 못한 오류: {str(e)}")
        cleanup_results['errors'].append(str(e))
        return cleanup_results

def reset_session_state():
    """세션 상태 초기화"""
    keys_to_reset = [
        "messages", "thread_id", "assistant_id", "assistant_instructions",
        "vector_store_id", "assistant_name", "vector_store_name", "chat_input_key"
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            if key == "messages":
                st.session_state[key] = []
            elif key == "chat_input_key":
                st.session_state[key] = 0
            else:
                st.session_state[key] = None
    
    st.session_state.current_page = "guide"
