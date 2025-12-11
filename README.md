# Claude API 연결 설정

이 프로젝트는 Anthropic Claude API와 연결하는 예제입니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. API 키 설정:
   - `.env.example` 파일을 `.env`로 복사
   - `.env` 파일에 실제 Anthropic API 키 입력
   - 또는 환경변수로 설정: `export ANTHROPIC_API_KEY='your-api-key'`

## 사용 방법

### 기본 사용법

```python
from claude_client import ClaudeClient

# 클라이언트 생성 (환경변수에서 API 키 자동 로드)
claude = ClaudeClient()

# 대화하기
response = claude.chat("안녕하세요!")
print(response)
```

### API 키 직접 제공

```python
from claude_client import ClaudeClient

claude = ClaudeClient(api_key="your-api-key")
response = claude.chat("안녕하세요!")
print(response)
```

### 스트리밍 응답

```python
from claude_client import ClaudeClient

claude = ClaudeClient()
for chunk in claude.stream_chat("긴 답변을 생성해주세요"):
    print(chunk, end="", flush=True)
```

### 실행

```bash
python claude_client.py
```

## API 키 얻기

Anthropic API 키는 [Anthropic Console](https://console.anthropic.com/)에서 얻을 수 있습니다.





