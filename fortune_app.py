"""
오늘의 운세 웹 애플리케이션
"""
import os
import random  # random 모듈 추가
from datetime import datetime
from flask import Flask, render_template, request, jsonify

try:
    from dotenv import load_dotenv
    # .env 파일 로드 (로컬 개발용)
    load_dotenv()
except ImportError:
    # 배포 환경에서는 dotenv가 없을 수 있음 (무시)
    pass

from gemini_client import GeminiClient
from fortune_generator import FortuneGenerator  # 백업용 생성기 추가

app = Flask(__name__)

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
    Claude AI를 사용하여 개인화된 운세 생성 (실패 시 백업 생성기 사용)
    """
    # 기본값: 백업 모드 실행
    def run_backup_mode(error_msg="Unknown Error"):
        print(f"⚠️ AI 호출 실패 (백업 모드 전환): {error_msg}")
        try:
            fortune_gen = FortuneGenerator()
            age = datetime.now().year - birth_date.year
            backup_response, products = fortune_gen.generate_fortune(name, age, gender, zodiac)
            result = {
                "full_text": backup_response,
                "name": name,
                "zodiac": zodiac,
                "date": datetime.now().strftime("%Y년 %m월 %d일"),
                "is_backup": True
            }
            # 상품 정보가 있으면 추가
            if products:
                result["products"] = products
            return result
        except Exception as e:
            # 백업마저 실패하면 정말 최소한의 응답 반환
            return {
                "full_text": f"운세 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.\n(Error: {str(e)})",
                "name": name,
                "zodiac": zodiac,
                "date": datetime.now().strftime("%Y년 %m월 %d일"),
                "error": str(e) # 프론트엔드가 에러로 인식하도록
            }

    try:
        # 1차 시도: Google Gemini AI 사용
        # 타임아웃 처리를 위한 설정
        import signal
        
        def handler(signum, frame):
            raise TimeoutError("AI Response Timeout")
            
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(5) # 5초 제한
        except AttributeError:
            pass

        gemini_client = GeminiClient()
        
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

다음 형식으로 운세를 작성해주세요. 순서를 정확히 지켜주세요:

**오늘의 운세**
[전체적인 오늘의 운세를 2-3문장으로 구체적이고 긍정적으로 작성]

**행운의 로또 번호**
[1부터 45까지의 숫자 중 6개를 쉼표로 구분하여 작성. 예: 7, 12, 23, 31, 38, 42]

**행운의 색상**
[하나의 색상만 작성. 예: 빨간색, 파란색, 노란색 등]

**추천 상품**
[행운의 색상과 어울리는 구체적인 상품 2-3개를 추천. 예: 빨간색 티셔츠, 빨간색 가방, 빨간색 액세서리]

각 항목을 명확하게 구분하여 작성해주세요.
"""
        
        response = gemini_client.chat(prompt, max_tokens=2048)
        
        # 타임아웃 해제
        try:
            signal.alarm(0)
        except AttributeError:
            pass
        
        # AI 응답이 에러 메시지를 포함하는지 확인
        if "오류 발생" in response:
            return run_backup_mode(response)
            
        return {
            "full_text": response,
            "name": name,
            "zodiac": zodiac,
            "date": today
        }
        
    except Exception as e:
        return run_backup_mode(str(e))


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


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔮 오늘의 운세 웹 애플리케이션 (Google Gemini 2.5 Flash)")
    print("="*50)
    print("\n✨ AI 기반 개인화 운세가 작동합니다!")
    print("브라우저에서 http://localhost:5001 을 열어주세요!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
