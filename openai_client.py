"""
OpenAI API 클라이언트 모듈
OpenAI API와의 상호작용을 담당합니다.
"""
import streamlit as st
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import time

def validate_api_key(api_key):
    """API 키 유효성 검증"""
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        return True
    except Exception as e:
        st.error(f"잘못된 API_KEY 입니다. API_KEY를 다시 입력해주세요!")
        return False

def create_vector_store(client, name):
    """Vector Store 생성"""
    return client.beta.vector_stores.create(name=name)

def upload_files_to_vector_store(client, vector_store_id, file_handles):
    """Vector Store에 파일 업로드"""
    return client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id,
        files=file_handles
    )

def create_assistant(client, name, instructions, model, vector_store_id, temperature=0.5, top_p=0.5):
    """Assistant 생성"""
    return client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        temperature=temperature,
        top_p=top_p
    )

def create_thread(client):
    """Thread 생성"""
    return client.beta.threads.create()

def create_message(client, thread_id, content):
    """메시지 생성"""
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

class StreamlitEventHandler(AssistantEventHandler):
    """Streamlit용 커스텀 이벤트 핸들러"""
    
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

def stream_assistant_response(client, thread_id, assistant_id, event_handler):
    """Assistant 응답 스트리밍"""
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler
    ) as stream:
        stream.until_done()
    
    return event_handler.full_response
