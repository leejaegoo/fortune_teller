"""
Google Gemini API 테스트 - 사용 가능한 모델 확인
"""
import os
import google.generativeai as genai

# API 키 설정
api_key = os.getenv("GOOGLE_API_KEY") or "AIzaSyC1izQsu7a9aw06-bW1sDI-JIckAoUjP1c"
genai.configure(api_key=api_key)

print("=" * 60)
print("🔍 Google Gemini API - 사용 가능한 모델 확인")
print("=" * 60)
print()

try:
    print("사용 가능한 모델 목록:")
    print("-" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   설명: {model.description}")
            print(f"   지원 메서드: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("=" * 60)
    print("\n가장 최신 모델로 테스트 시도:")
    print("-" * 60)
    
    # 여러 모델 이름 시도
    model_names = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'models/gemini-pro'
    ]
    
    for model_name in model_names:
        try:
            print(f"\n시도 중: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("안녕하세요!")
            print(f"✅ 성공! {model_name} 작동함!")
            print(f"응답: {response.text[:100]}...")
            break
        except Exception as e:
            print(f"❌ 실패: {str(e)[:80]}")
            
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    print("\nAPI 키가 올바른지 확인해주세요.")

