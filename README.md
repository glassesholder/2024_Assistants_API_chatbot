# rag_chatbot
rag 챗봇입니다.

# 🤖 Assistants API 챗봇

OpenAI Assistants API를 활용한 PDF/DOCS 기반 챗봇입니다.

## 프로젝트 개요

이 프로젝트는 문서(PDF/DOCS)를 기반으로 AI 어시스턴트와 대화할 수 있는 웹 애플리케이션입니다. OpenAI의 Assistants API와 Vector Store를 사용하여 문서 기반 질의응답 시스템을 구현했습니다.

## 주요 기능

- 다중 PDF/DOCS 업로드: 여러 문서를 한 번에 업로드
- AI Assistant 생성: 업로드된 문서를 학습한 맞춤형 어시스턴트
- 실시간 채팅: 스트리밍 방식의 실시간 대화
- 리소스 관리: Assistant, Vector Store, 파일 상태 모니터링
- 완전 정리: OpenAI 플랫폼의 모든 리소스 자동 삭제
- 정보 대시보드: 생성된 리소스 현황 확인

## 기술 스택

- Frontend: Streamlit
- Backend: Python
- AI API: OpenAI Assistants API
- Document Processing: OpenAI Vector Store
- UI Components: streamlit-option-menu

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/glassesholder/2024_Assistants_API_chatbot.git
cd rag_chatbot
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
streamlit run chatbot.py
```

## 사용 방법

### 1. API Key 설정
- OpenAI API 키를 발급받아 입력합니다.
- [OpenAI Platform](https://platform.openai.com/api-keys)에서 API 키를 생성할 수 있습니다.

### 2. Assistant 생성
- PDF/DOCS 파일을 업로드합니다.
- Vector Store 이름을 지정합니다.
- Assistant 이름과 설명을 입력합니다.
- "Assistant 생성" 버튼을 클릭합니다.

### 3. 채팅 시작
- Assistant 생성 완료 후 채팅 메뉴로 이동합니다.
- 문서 기반의 질문을 입력하여 대화를 시작합니다.

### 4. 리소스 정리
- 사용 완료 후 "대화 종료" 메뉴에서 모든 리소스를 정리할 수 있습니다.

## 프로젝트 구조

```
2024_Assistants_API_chatbot/
├── chatbot.py              # 메인 애플리케이션
├── config.py               # 설정 관리
├── openai_client.py        # OpenAI API 클라이언트
├── file_manager.py         # 파일 업로드 관리
├── cleanup_manager.py      # 리소스 정리 관리
├── components/             # UI 컴포넌트
│   ├── guide_page.py       # 가이드 페이지
│   ├── api_key_page.py     # API 키 설정
│   ├── assistant_creation_page.py  # Assistant 생성
│   ├── chat_page.py        # 채팅 인터페이스
│   ├── info_page.py        # 정보 대시보드
│   └── cleanup_page.py     # 리소스 정리
├── uploads/                # 업로드된 파일 저장소
├── requirements.txt        # Python 의존성
└── README.md              # 프로젝트 문서
```

## 주요 모듈 설명

### OpenAI Assistants API 활용
- Assistant: 업로드된 문서를 학습한 AI 어시스턴트
- Vector Store: 문서 검색을 위한 벡터 데이터베이스
- Thread: 대화 세션 관리
- Streaming: 실시간 응답 스트리밍

### 핵심 기능
- 파일 업로드: 다중 PDF 파일 처리 및 Vector Store 연동
- 스트리밍 채팅: 실시간 응답 표시
- 리소스 관리: 생성된 모든 OpenAI 리소스 추적 및 정리
- 세션 관리: Streamlit 세션 상태를 통한 데이터 유지

## 주의사항

- OpenAI API 사용량에 따라 요금이 발생할 수 있습니다.
- 페이지 새로고침 시 세션 데이터가 초기화됩니다.
- 리소스 정리는 되돌릴 수 없으니 신중하게 사용하세요.
- PDF 파일은 텍스트 추출이 가능한 형태여야 합니다.

## 🙏 감사의 말

OpenAI 커뮤니티에 감사드립니다.
