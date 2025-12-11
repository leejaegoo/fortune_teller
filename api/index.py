"""
오늘의 운세 웹 애플리케이션 - Vercel Serverless Function
"""
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import random

# 부모 디렉토리를 path에 추가하여 모듈 import 가능하게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from gemini_client import GeminiClient
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: gemini_client를 직접 구현
    import google.generativeai as genai

    class GeminiClient:
        def __init__(self, api_key=None):
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')

        def chat(self, message, max_tokens=2048):
            try:
                response = self.model.generate_content(message)
                return response.text
            except Exception as e:
                return f"오류 발생: {str(e)}"

# Flask 앱 초기화 - 템플릿과 static 폴더 경로 설정
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# 12띠 정보
ZODIAC_ANIMALS = {
    0: {"name": "원숭이", "emoji": "🐵"},
    1: {"name": "닭", "emoji": "🐔"},
    2: {"name": "개", "emoji": "🐶"},
    3: {"name": "돼지", "emoji": "🐷"},
    4: {"name": "쥐", "emoji": "🐭"},
    5: {"name": "소", "emoji": "🐮"},
    6: {"name": "호랑이", "emoji": "🐯"},
    7: {"name": "토끼", "emoji": "🐰"},
    8: {"name": "용", "emoji": "🐲"},
    9: {"name": "뱀", "emoji": "🐍"},
    10: {"name": "말", "emoji": "🐴"},
    11: {"name": "양", "emoji": "🐑"}
}

# 영감을 주는 명언 모음
QUOTES = [
    {"text": "행복은 습관이다. 그것을 몸에 지니라.", "author": "허버드"},
    {"text": "미래는 현재 우리가 무엇을 하는가에 달려 있다.", "author": "마hatma 간디"},
    {"text": "성공의 비결은 시작하는 것이다.", "author": "마크 트웨인"},
    {"text": "믿음만 있다면 무엇이든 가능하다.", "author": "괴테"},
    {"text": "당신이 할 수 있다고 믿든, 할 수 없다고 믿든, 믿는 대로 될 것이다.", "author": "헨리 포드"},
    {"text": "좋은 일을 하는 데 가장 좋은 때는 바로 지금이다.", "author": "중국 속담"},
    {"text": "인생은 자전거를 타는 것과 같다. 균형을 유지하려면 계속 움직여야 한다.", "author": "아인슈타인"},
    {"text": "어제로부터 배우고, 오늘을 위해 살고, 내일을 위해 희망하라.", "author": "아인슈타인"},
    {"text": "기회는 일어나는 것이 아니라 만들어가는 것이다.", "author": "크리스 그로서"},
    {"text": "성공은 최종적인 것이 아니며, 실패는 치명적인 것이 아니다. 중요한 것은 계속하는 용기다.", "author": "윈스턴 처칠"},
    {"text": "당신의 시간은 한정되어 있으니, 다른 사람의 인생을 사는 데 낭비하지 마라.", "author": "스티브 잡스"},
    {"text": "행복의 문이 하나 닫히면 다른 문이 열린다.", "author": "헬렌 켈러"},
    {"text": "변화를 원한다면 스스로 그 변화가 되어라.", "author": "마hatma 간디"},
    {"text": "꿈을 이루는 비결은 꿈을 꾸는 것이다.", "author": "월트 디즈니"},
    {"text": "실패는 성공의 어머니다.", "author": "토마스 에디슨"}
]


def calculate_zodiac(birth_year):
    """
    생년으로 띠 계산

    Args:
        birth_year: 생년 (int)

    Returns:
        dict: 띠 정보 (이름, 이모지)
    """
    zodiac_index = birth_year % 12
    return ZODIAC_ANIMALS[zodiac_index]


def get_random_quote():
    """랜덤 명언 가져오기"""
    return random.choice(QUOTES)


def generate_fortune(name, birth_date, gender, zodiac):
    """
    Gemini AI를 사용하여 개인화된 운세 생성

    Args:
        name: 이름
        birth_date: 생년월일 (datetime)
        gender: 성별
        zodiac: 띠 정보

    Returns:
        dict: 운세 정보 (전체운, 사랑운, 재물운, 건강운, 직장/학업운)
    """
    try:
        # 환경 변수 확인
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다. Vercel 프로젝트 설정에서 환경 변수를 추가해주세요.")

        gemini_client = GeminiClient(api_key=api_key)

        today = datetime.now().strftime("%Y년 %m월 %d일")
        birth_str = birth_date.strftime("%Y년 %m월 %d일")
        age = datetime.now().year - birth_date.year

        prompt = f"""
당신은 전문 운세 상담가입니다. 다음 정보를 바탕으로 오늘의 운세를 작성해주세요:

- 이름: {name}님
- 생년월일: {birth_str} (만 {age}세)
- 성별: {gender}
- 띠: {zodiac['emoji']} {zodiac['name']}띠
- 오늘 날짜: {today}

다음 형식으로 운세를 작성해주세요. 각 항목은 2-3문장으로 구체적이고 긍정적으로 작성해주세요:

**전체운**
[전체적인 오늘의 운세]

**사랑운**
[사랑과 인간관계 운세]

**재물운**
[금전과 재물 운세]

**건강운**
[건강과 컨디션 운세]

**직장/학업운**
[일과 학업 운세]

**행운의 색상**
[하나의 색상]

**행운의 숫자**
[하나의 숫자]

각 카테고리마다 구체적이고 희망적인 조언을 담아주세요.
"""

        response = gemini_client.chat(prompt, max_tokens=2048)

        # 응답 검증
        if not response or "오류 발생:" in response:
            raise ValueError(f"AI 응답 오류: {response}")

        # 응답 파싱
        fortune_data = {
            "full_text": response,
            "name": name,
            "zodiac": zodiac,
            "date": today
        }

        return fortune_data

    except ValueError as e:
        # 환경 변수나 API 키 관련 에러
        print(f"ValueError in generate_fortune: {str(e)}")
        return {
            "error": str(e),
            "name": name,
            "zodiac": zodiac
        }
    except Exception as e:
        # 기타 예상치 못한 에러
        print(f"Exception in generate_fortune: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": f"운세 생성 중 오류가 발생했습니다: {str(e)}",
            "name": name,
            "zodiac": zodiac
        }


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/get_fortune', methods=['POST'])
def get_fortune():
    """운세 생성 API"""
    try:
        data = request.json

        # 입력 데이터 검증
        name = data.get('name', '').strip()
        birth_date_str = data.get('birth_date', '')
        gender = data.get('gender', '')

        if not all([name, birth_date_str, gender]):
            return jsonify({"error": "모든 정보를 입력해주세요."}), 400

        # 생년월일 파싱
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "올바른 날짜 형식이 아닙니다."}), 400

        # 띠 계산
        zodiac = calculate_zodiac(birth_date.year)

        # 운세 생성
        fortune = generate_fortune(name, birth_date, gender, zodiac)

        # 명언 추가
        quote = get_random_quote()
        fortune['quote'] = quote

        return jsonify(fortune)

    except Exception as e:
        return jsonify({"error": f"오류가 발생했습니다: {str(e)}"}), 500


# Vercel에서 이 앱을 실행하기 위한 엔트리포인트
# 로컬에서는 fortune_app.py를 직접 실행하세요
