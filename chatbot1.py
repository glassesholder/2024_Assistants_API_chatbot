import streamlit as st
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import time
from streamlit_option_menu import option_menu
import os

# 로컬 파일 저장 디렉토리 설정
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Streamlit 페이지 설정
st.set_page_config(page_title="중학교 수학 학습챗봇", page_icon="🤖", layout="wide")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "assistant_id" not in st.session_state:
    st.session_state.assistant_id = None
if "assistant_instructions" not in st.session_state:
    st.session_state.assistant_instructions = None
if "vector_store_id" not in st.session_state:
    st.session_state.vector_store_id = None
if "assistant_name" not in st.session_state:
    st.session_state.assistant_name = None
if "vector_store_name" not in st.session_state:
    st.session_state.vector_store_name = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "api_key"

# API 키 검증 함수
def validate_api_key(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        return True
    except Exception as e:
        st.error(f"잘못된 API_KEY 입니다. API_KEY를 다시 입력해주세요!")
        return False

# 파일 저장 함수
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIRECTORY, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# 파일 삭제 함수
def cleanup_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except Exception as e:
            st.warning(f"파일 삭제 중 오류 발생: {file_path}")

# 사이드바 메뉴 및 이미지
with st.sidebar:
    st.image("./logo.png", use_column_width=True)

    choice = option_menu("", ["사용 가이드","API Key 설정","Assistant 생성","채팅", "정보 보기"],
    icons=['book', 'bi bi-check2-all', 'upload','bi bi-robot', 'database'],
    menu_icon="app-indicator", default_index=0,
    styles={
    "container": {"padding": "4!important", "background-color": "#fafafa"},
    "icon": {"color": "#2E8B57", "font-size": "25px"},
    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
    "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

if choice=='API Key 설정':
    st.session_state.current_page = "api_key"
if choice=='사용 가이드':
    st.session_state.current_page = "guide"
if choice=='Assistant 생성':
    st.session_state.current_page = "assistant_creation"
if choice=='채팅':
    st.session_state.current_page = "chat"
if choice=='정보 보기':
    st.session_state.current_page = "info"

# 메인 컨텐츠 (가이드 페이지)
if st.session_state.current_page == "guide":
    st.title("✅ 사용 가이드")
    st.markdown("""
    ### 🎯 사용 방법
    1. **API Key 설정**
        - OpenAI API 키를 입력합니다.
        - API 키는 안전하게 보관됩니다.
    
    2. **Assistant 생성**
        - PDF 파일을 업로드합니다.
        - Vector Store 이름을 지정합니다.
        - Assistant 설정을 완료합니다.
        - Assistant를 생성합니다.
    
    3. **채팅**
        - Assistant 생성 후 채팅을 시작할 수 있습니다.
        - 실시간 스트리밍 응답을 받아볼 수 있습니다.
    
    ### ⚠️ 주의사항
    - 페이지를 새로고침하면 대화 내용이 초기화됩니다.
    - Assistant를 먼저 생성해야 채팅이 가능합니다.
    """)

elif st.session_state.current_page == "api_key":
    st.title("✅ API Key 설정")
    
    if st.session_state.api_key:
        st.success("API Key가 이미 설정되어 있습니다!")
    else:
        api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")
        if api_key:
            if validate_api_key(api_key):
                st.session_state.api_key = api_key
                st.success("API Key가 성공적으로 설정되었습니다!")

elif st.session_state.current_page == "assistant_creation":
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
                        vector_store = client.beta.vector_stores.create(
                            name=vector_store_name
                        )
                        st.session_state.vector_store_id = vector_store.id
                        st.session_state.vector_store_name = vector_store_name
                        
                        # 파일 저장 및 업로드
                        saved_files = []
                        file_paths = []  # 저장된 파일 경로 추적
                        file_handles = []  # 파일 핸들 추적
                        
                        try:
                            # 파일 저장
                            for uploaded_file in uploaded_files:
                                file_path = save_uploaded_file(uploaded_file)
                                file_paths.append(file_path)
                                file_handle = open(file_path, 'rb')
                                file_handles.append(file_handle)
                            
                            # OpenAI에 파일 업로드
                            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                                vector_store_id=vector_store.id,
                                files=file_handles
                            )
                            st.success(f"{len(uploaded_files)}개의 파일이 성공적으로 업로드되었습니다!")
                            
                        finally:
                            # 파일 핸들 닫기
                            for handle in file_handles:
                                handle.close()
                            # 로컬 파일 삭제
                            cleanup_files(file_paths)
                        
                        # Assistant 생성
                        assistant = client.beta.assistants.create(
                            name=assistant_name,
                            instructions=instructions,
                            model=model,
                            tools=[{"type": "file_search"}],
                            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}} ,
                            temperature=temperature,
                            top_p=top_p
                        )
                        
                        st.session_state.assistant_id = assistant.id
                        st.session_state.assistant_name = assistant_name
                        
                        # Thread 생성
                        thread = client.beta.threads.create()
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

elif st.session_state.current_page == "info":
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

elif st.session_state.current_page == "chat":
    st.title(f"✅ {st.session_state.assistant_name or 'Assistant'}와의 채팅")
    
    if not st.session_state.api_key:
            st.error("API Key 설정 창에서 API Key를 먼저 생성해주세요!")

    elif not st.session_state.assistant_id:
                st.error('Assistant 생성 창에서 Assistant를 먼저 생성해주세요!')

    else:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=st.session_state.api_key)
        
        # Streamlit용 커스텀 이벤트 핸들러
        class StreamlitEventHandler(AssistantEventHandler):
            def __init__(self, message_placeholder):
                super().__init__()
                self.message_placeholder = message_placeholder
                self.full_response = ""
                
            @override
            def on_text_created(self, text) -> None:
                pass
                
            @override
            def on_text_delta(self, delta, snapshot):
                self.full_response += delta.value
                self.message_placeholder.markdown(self.full_response)
                
            def on_tool_call_created(self, tool_call):
                pass
            
            def on_tool_call_delta(self, delta, snapshot):
                if delta.type == 'code_interpreter':
                    if delta.code_interpreter.input:
                        self.full_response += f"\n```python\n{delta.code_interpreter.input}\n```\n"
                        self.message_placeholder.markdown(self.full_response)
                    if delta.code_interpreter.outputs:
                        for output in delta.code_interpreter.outputs:
                            if output.type == "logs":
                                self.full_response += f"\n```\n{output.logs}\n```\n"
                                self.message_placeholder.markdown(self.full_response)

            def on_end(self):
                pass

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
            message = client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
            
            # Assistant 응답을 위한 플레이스홀더 생성
            with chat_container:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    
                    # 스트리밍 응답 처리
                    event_handler = StreamlitEventHandler(message_placeholder)
                    
                    # 스트리밍 실행
                    with client.beta.threads.runs.stream(
                        thread_id=st.session_state.thread_id,
                        assistant_id=st.session_state.assistant_id,
                        event_handler=event_handler
                    ) as stream:
                        stream.until_done()
                    
                    # 완성된 응답을 세션 상태에 저장
                    final_response = event_handler.full_response
                    if final_response:
                        st.session_state.messages.append({"role": "assistant", "content": final_response})
            
            # Increment the input key to clear the input field
            st.session_state.chat_input_key += 1
            st.rerun()