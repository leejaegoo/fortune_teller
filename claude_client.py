"""
Claude API 클라이언트 연결 예제
"""
import os
from anthropic import Anthropic

class ClaudeClient:
    """Claude API를 사용하기 위한 클라이언트 클래스"""
    
    def __init__(self, api_key=None):
        """
        Claude 클라이언트 초기화
        
        Args:
            api_key: Anthropic API 키. None이면 환경변수에서 가져옵니다.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API 키가 제공되지 않았습니다. "
                "환경변수 ANTHROPIC_API_KEY를 설정하거나 api_key 파라미터를 제공하세요."
            )
        self.client = Anthropic(api_key=self.api_key)
    
    def chat(self, message, model="claude-3-5-sonnet-20241022", max_tokens=1024):
        """
        Claude와 대화하기
        
        Args:
            message: 사용자 메시지
            model: 사용할 Claude 모델 (기본값: claude-3-5-sonnet-20241022)
            max_tokens: 최대 토큰 수
            
        Returns:
            Claude의 응답 메시지
        """
        try:
            message_obj = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return message_obj.content[0].text
        except Exception as e:
            return f"오류 발생: {str(e)}"
    
    def stream_chat(self, message, model="claude-3-5-sonnet-20241022", max_tokens=1024):
        """
        Claude와 스트리밍 대화하기
        
        Args:
            message: 사용자 메시지
            model: 사용할 Claude 모델
            max_tokens: 최대 토큰 수
            
        Yields:
            스트리밍된 응답 청크
        """
        try:
            stream = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": message}
                ],
                stream=True
            )
            for event in stream:
                if event.type == "content_block_delta":
                    yield event.delta.text
        except Exception as e:
            yield f"오류 발생: {str(e)}"


def main():
    """사용 예제"""
    try:
        # 클라이언트 생성
        claude = ClaudeClient()
        
        # 간단한 대화
        print("Claude에게 질문하기...")
        response = claude.chat("안녕하세요! 간단히 자기소개 해주세요.")
        print(f"\nClaude 응답:\n{response}\n")
        
        # 스트리밍 대화 예제
        print("스트리밍 응답 받기...")
        print("Claude 응답: ", end="", flush=True)
        for chunk in claude.stream_chat("파이썬에 대해 한 문장으로 설명해주세요."):
            print(chunk, end="", flush=True)
        print("\n")
        
    except ValueError as e:
        print(f"설정 오류: {e}")
        print("\n사용 방법:")
        print("1. 환경변수 설정: export ANTHROPIC_API_KEY='your-api-key'")
        print("2. 또는 코드에서 직접 API 키 제공: ClaudeClient(api_key='your-api-key')")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()





