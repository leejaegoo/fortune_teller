"""
OpenAI API 클라이언트
"""
import os
from openai import OpenAI

class OpenAIClient:
    """OpenAI API를 사용하기 위한 클라이언트 클래스"""
    
    def __init__(self, api_key=None):
        """
        OpenAI 클라이언트 초기화
        
        Args:
            api_key: OpenAI API 키. None이면 환경변수에서 가져옵니다.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API 키가 제공되지 않았습니다. "
                "환경변수 OPENAI_API_KEY를 설정하거나 api_key 파라미터를 제공하세요."
            )
        self.client = OpenAI(api_key=self.api_key)
    
    def chat(self, message, model="gpt-3.5-turbo", max_tokens=2048):
        """
        OpenAI와 대화하기
        
        Args:
            message: 사용자 메시지
            model: 사용할 모델 (기본값: gpt-3.5-turbo)
            max_tokens: 최대 토큰 수
            
        Returns:
            OpenAI의 응답 메시지
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": message}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"오류 발생: {str(e)}"

