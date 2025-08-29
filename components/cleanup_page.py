"""
리소스 정리 페이지 모듈
"""
import streamlit as st
import time
from openai import OpenAI
from cleanup_manager import cleanup_all_resources, reset_session_state

def render_cleanup_page():
    """리소스 정리 페이지 렌더링"""
    st.title("🗑️ 대화 종료 및 정리")
    
    if not st.session_state.api_key:
        st.error("API Key가 설정되지 않았습니다.")
        return
    
    # 현재 생성된 리소스 상태 표시
    st.markdown("### 📊 현재 생성된 리소스")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Assistant**")
        if st.session_state.assistant_name:
            st.success(f"✅ {st.session_state.assistant_name}")
        else:
            st.info("❌ 생성되지 않음")
            
        st.markdown("**Vector Store**")
        if st.session_state.vector_store_name:
            st.success(f"✅ {st.session_state.vector_store_name}")
        else:
            st.info("❌ 생성되지 않음")
    
    with col2:
        st.markdown("**채팅 메시지**")
        if st.session_state.messages:
            st.success(f"✅ {len(st.session_state.messages)}개 메시지")
        else:
            st.info("❌ 메시지 없음")
            
        st.markdown("**Thread ID**")
        if st.session_state.thread_id:
            st.success(f"✅ {st.session_state.thread_id[:20]}...")
        else:
            st.info("❌ 생성되지 않음")
    
    st.markdown("---")
    
    # 정리할 항목들 설명
    st.markdown("### ⚠️ 정리될 항목들")
    st.markdown("""
    다음 항목들이 **OpenAI 플랫폼에서 완전히 삭제**됩니다:
    
    - 🤖 **Assistant**: 생성된 AI 어시스턴트
    - 📚 **Vector Store**: 업로드된 파일들의 검색 인덱스
    - 📄 **Files**: 업로드된 모든 파일들
    - 💬 **Chat History**: 모든 대화 기록
    - 🧵 **Thread**: 대화 스레드
    
    **주의**: 이 작업은 되돌릴 수 없습니다!
    """)
    
    # 정리 실행 버튼
    st.markdown("---")
    
    if any([st.session_state.assistant_id, st.session_state.vector_store_id, st.session_state.messages]):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🗑️ 모든 리소스 정리하기", 
                        type="primary", 
                        use_container_width=True,
                        help="OpenAI 플랫폼의 모든 생성된 리소스를 삭제합니다"):
                
                st.markdown("### 🔄 정리 진행 상황")
                
                try:
                    client = OpenAI(api_key=st.session_state.api_key)
                    
                    with st.spinner("리소스 정리 중..."):
                        cleanup_results = cleanup_all_resources(client)
                    
                    # 결과 표시
                    st.markdown("### 📋 정리 결과")
                    
                    if cleanup_results['errors']:
                        st.error("일부 리소스 정리 중 오류가 발생했습니다:")
                        for error in cleanup_results['errors']:
                            st.error(f"- {error}")
                    
                    if (cleanup_results['assistant'] or 
                        cleanup_results['vector_store'] or 
                        cleanup_results['files']):
                        
                        st.success("🎉 리소스 정리가 완료되었습니다!")
                        
                        # 세션 상태 초기화
                        reset_session_state()
                        
                        st.info("💡 세션이 초기화되었습니다. 새로운 Assistant를 생성할 수 있습니다.")
                        
                        # 3초 후 가이드 페이지로 이동
                        with st.empty():
                            for i in range(3, 0, -1):
                                st.info(f"🔄 {i}초 후 가이드 페이지로 이동합니다...")
                                time.sleep(1)
                        
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"정리 중 오류가 발생했습니다: {str(e)}")
    
    else:
        st.info("🔍 정리할 리소스가 없습니다.")
