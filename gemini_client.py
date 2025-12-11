"""
Google Gemini API 클라이언트
"""
import os
import google.generativeai as genai

class GeminiClient:
    """Google Gemini API를 사용하기 위한 클라이언트 클래스"""
    
    def __init__(self, api_key=None):
        """
        Gemini 클라이언트 초기화
        
        Args:
            api_key: Google API 키. None이면 환경변수에서 가져옵니다.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API 키가 제공되지 않았습니다. "
                "환경변수 GOOGLE_API_KEY를 설정하거나 api_key 파라미터를 제공하세요."
            )
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def chat(self, message, max_tokens=2048):
        """
        Gemini와 대화하기
        
        Args:
            message: 사용자 메시지
            max_tokens: 최대 토큰 수 (Gemini는 자동으로 관리)
            
        Returns:
            Gemini의 응답 메시지
        """
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"오류 발생: {str(e)}"
