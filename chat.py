"""
Claude와의 대화형 채팅 인터페이스
"""
import os
import sys
from anthropic import Anthropic


class ChatInterface:
    """대화형 채팅 인터페이스"""
    
    def __init__(self, api_key=None):
        """
        채팅 인터페이스 초기화
        
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
        self.conversation_history = []
        self.model = "claude-3-5-sonnet-20241022"
    
    def add_message(self, role, content):
        """대화 히스토리에 메시지 추가"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def chat(self, user_message):
        """
        사용자 메시지를 보내고 Claude의 응답을 받습니다.
        
        Args:
            user_message: 사용자 메시지
            
        Returns:
            Claude의 응답
        """
        # 사용자 메시지를 히스토리에 추가
        self.add_message("user", user_message)
        
        try:
            # Claude에게 메시지 전송
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=self.conversation_history
            )
            
            # 어시스턴트 응답을 히스토리에 추가
            assistant_message = response.content[0].text
            self.add_message("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"오류 발생: {str(e)}"
    
    def stream_chat(self, user_message):
        """
        스트리밍 방식으로 응답을 받습니다.
        
        Args:
            user_message: 사용자 메시지
            
        Yields:
            응답 청크
        """
        # 사용자 메시지를 히스토리에 추가
        self.add_message("user", user_message)
        
        try:
            # 스트리밍으로 응답 받기
            full_response = ""
            
            with self.client.messages.stream(
                model=self.model,
                max_tokens=4096,
                messages=self.conversation_history
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    yield text
            
            # 전체 응답을 히스토리에 추가
            self.add_message("assistant", full_response)
            
        except Exception as e:
            error_msg = f"오류 발생: {str(e)}"
            yield error_msg
    
    def clear_history(self):
        """대화 히스토리 초기화"""
        self.conversation_history = []
        print("\n✨ 대화 히스토리가 초기화되었습니다.\n")
    
    def show_history(self):
        """대화 히스토리 출력"""
        if not self.conversation_history:
            print("\n대화 히스토리가 없습니다.\n")
            return
        
        print("\n" + "="*50)
        print("대화 히스토리")
        print("="*50)
        for i, msg in enumerate(self.conversation_history, 1):
            role = "사용자" if msg["role"] == "user" else "Claude"
            print(f"\n[{i}] {role}:")
            print(msg["content"])
        print("\n" + "="*50 + "\n")
    
    def run(self):
        """채팅 인터페이스 실행"""
        print("\n" + "="*50)
        print("🤖 Claude 채팅창")
        print("="*50)
        print("\n명령어:")
        print("  - 메시지 입력: Claude와 대화")
        print("  - /clear: 대화 히스토리 초기화")
        print("  - /history: 대화 히스토리 보기")
        print("  - /exit, /quit: 종료")
        print("\n" + "="*50 + "\n")
        
        while True:
            try:
                # 사용자 입력 받기
                user_input = input("나: ").strip()
                
                if not user_input:
                    continue
                
                # 명령어 처리
                if user_input.lower() in ["/exit", "/quit"]:
                    print("\n👋 채팅을 종료합니다.\n")
                    break
                
                elif user_input.lower() == "/clear":
                    self.clear_history()
                    continue
                
                elif user_input.lower() == "/history":
                    self.show_history()
                    continue
                
                # Claude 응답 받기 (스트리밍)
                print("\nClaude: ", end="", flush=True)
                for chunk in self.stream_chat(user_input):
                    print(chunk, end="", flush=True)
                print("\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 채팅을 종료합니다.\n")
                break
            except EOFError:
                print("\n\n👋 채팅을 종료합니다.\n")
                break
            except Exception as e:
                print(f"\n오류 발생: {e}\n")


def main():
    """메인 함수"""
    try:
        # API 키 확인
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("\n❌ 오류: API 키가 설정되지 않았습니다.\n")
            print("사용 방법:")
            print("1. 환경변수 설정:")
            print("   export ANTHROPIC_API_KEY='your-api-key'")
            print("\n2. 또는 .env 파일 생성:")
            print("   ANTHROPIC_API_KEY=your-api-key")
            print("\n3. API 키는 https://console.anthropic.com/ 에서 얻을 수 있습니다.\n")
            sys.exit(1)
        
        # 채팅 인터페이스 시작
        chat = ChatInterface()
        chat.run()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

