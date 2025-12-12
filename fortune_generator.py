"""
API 없이 작동하는 운세 생성기
"""
import random
from coupang_client import CoupangClient

class FortuneGenerator:
    """운세 템플릿 기반 생성기"""
    
    # 전체운 템플릿
    OVERALL_FORTUNES = [
        "오늘은 새로운 시작을 알리는 긍정적인 에너지가 가득한 날입니다. 작은 변화들이 큰 행운으로 이어질 수 있으니, 직관을 믿고 행동하세요. 주변 사람들과의 소통이 특히 중요한 시기입니다.",
        "행운의 기운이 당신을 감싸고 있습니다. 오늘 하루는 평소보다 더 적극적으로 행동하면 좋은 결과를 얻을 수 있습니다. 오후 시간대에 특히 좋은 일이 생길 가능성이 높습니다.",
        "차분하게 하루를 시작하세요. 급하게 서두르기보다는 신중한 판단이 필요한 시기입니다. 작은 일에서도 배움을 얻을 수 있으니, 모든 순간에 집중하세요.",
        "오늘은 당신의 매력이 빛나는 날입니다. 자신감을 가지고 하루를 보내면 예상치 못한 좋은 소식을 들을 수 있습니다. 긍정적인 마음가짐이 행운을 불러옵니다.",
        "변화의 바람이 불고 있습니다. 새로운 기회가 찾아올 수 있으니 마음을 열고 받아들이세요. 과거에 집착하기보다는 미래를 향해 나아가는 것이 좋습니다."
    ]
    
    # 사랑운 템플릿
    LOVE_FORTUNES = [
        "연인과의 관계에서 깊은 대화가 필요한 시기입니다. 마음을 솔직하게 표현하면 관계가 더욱 돈독해질 것입니다. 솔로라면 새로운 만남의 기회가 있을 수 있습니다.",
        "사랑의 에너지가 강하게 흐르는 날입니다. 상대방에게 작은 선물이나 따뜻한 말 한마디가 큰 감동을 줄 수 있습니다. 주변을 둘러보세요, 당신을 바라보는 누군가가 있을지도 모릅니다.",
        "인내심이 필요한 시기입니다. 급하게 결론을 내리기보다는 상대방의 입장을 이해하려고 노력하세요. 이해와 배려가 관계를 더욱 견고하게 만들어줄 것입니다.",
        "로맨틱한 분위기가 감도는 날입니다. 특별한 데이트를 계획해보는 것은 어떨까요? 작은 이벤트라도 상대방에게 큰 감동을 줄 수 있습니다.",
        "자기 자신을 사랑하는 것이 먼저입니다. 자신감 있는 모습이 타인에게도 매력적으로 보입니다. 새로운 인연이 찾아올 가능성이 높은 날입니다."
    ]
    
    # 재물운 템플릿
    WEALTH_FORTUNES = [
        "금전적으로 안정적인 시기입니다. 충동구매는 피하고 계획적인 소비를 하세요. 작은 투자 기회가 찾아올 수 있으니 신중하게 검토해보세요.",
        "예상치 못한 수입이 생길 수 있는 날입니다. 하지만 쉽게 얻은 돈은 쉽게 나갈 수 있으니 저축을 생각해보세요. 장기적인 재정 계획을 세우기 좋은 시기입니다.",
        "지출이 많아질 수 있는 시기이니 주의가 필요합니다. 필요한 것과 원하는 것을 구분하여 현명한 소비를 하세요. 작은 절약이 큰 부를 만듭니다.",
        "재물운이 상승하는 시기입니다. 새로운 수입원을 찾거나 부업을 시작하기 좋은 때입니다. 적극적인 태도가 금전적 기회를 가져다줄 것입니다.",
        "현재 가진 것에 감사하는 마음이 더 큰 풍요를 불러옵니다. 나눔과 베풂의 정신이 결국 당신에게 돌아올 것입니다. 필요한 곳에 투자하세요."
    ]
    
    # 건강운 템플릿
    HEALTH_FORTUNES = [
        "전반적으로 좋은 컨디션을 유지하고 있습니다. 꾸준한 운동과 충분한 휴식이 중요합니다. 물을 자주 마시고 스트레칭으로 몸을 풀어주세요.",
        "피로가 누적되어 있을 수 있습니다. 오늘은 충분한 휴식을 취하는 것이 좋습니다. 과로는 피하고 여유 있게 하루를 보내세요.",
        "활력이 넘치는 날입니다. 새로운 운동이나 건강한 습관을 시작하기 좋은 시기입니다. 규칙적인 생활 리듬을 유지하면 더욱 좋은 컨디션을 유지할 수 있습니다.",
        "소화기 계통에 신경을 쓰세요. 규칙적인 식사와 건강한 음식 섭취가 중요합니다. 과식이나 야식은 피하는 것이 좋습니다.",
        "정신 건강도 중요합니다. 명상이나 요가 등으로 마음의 평화를 찾아보세요. 긍정적인 생각이 신체 건강에도 좋은 영향을 미칩니다."
    ]
    
    # 직장/학업운 템플릿
    WORK_FORTUNES = [
        "업무나 학업에서 좋은 성과를 낼 수 있는 날입니다. 집중력이 높아져 있으니 중요한 일을 처리하기 좋은 시기입니다. 동료나 선생님과의 협력이 큰 도움이 될 것입니다.",
        "새로운 프로젝트나 학습 과제를 시작하기 좋은 때입니다. 창의적인 아이디어가 떠오를 수 있으니 메모해두세요. 적극적인 자세가 인정받을 것입니다.",
        "인내심이 필요한 시기입니다. 결과가 바로 나오지 않더라도 꾸준히 노력하세요. 작은 성취들이 모여 큰 성공으로 이어질 것입니다.",
        "상사나 선배로부터 좋은 조언을 들을 수 있는 날입니다. 겸손한 자세로 배움의 기회를 놓치지 마세요. 네트워킹이 중요한 시기입니다.",
        "업무나 학업에서 전환점이 찾아올 수 있습니다. 변화를 두려워하지 말고 새로운 도전을 받아들이세요. 당신의 능력을 보여줄 좋은 기회입니다."
    ]
    
    # 행운의 색상
    LUCKY_COLORS = [
        "빨간색", "파란색", "노란색", "초록색", "보라색",
        "주황색", "분홍색", "하늘색", "민트색", "베이지색",
        "흰색", "검은색", "금색", "은색", "청록색"
    ]
    
    # 색상별 상품 추천
    COLOR_PRODUCTS = {
        "빨간색": "빨간색 티셔츠, 빨간색 가방, 빨간색 액세서리",
        "파란색": "파란색 후드티, 파란색 운동화, 파란색 시계",
        "노란색": "노란색 스카프, 노란색 지갑, 노란색 케이스",
        "초록색": "초록색 후드티, 초록색 가방, 초록색 모자",
        "보라색": "보라색 스웨터, 보라색 액세서리, 보라색 양말",
        "주황색": "주황색 후드티, 주황색 운동화, 주황색 모자",
        "분홍색": "분홍색 티셔츠, 분홍색 가방, 분홍색 액세서리",
        "하늘색": "하늘색 셔츠, 하늘색 가방, 하늘색 시계",
        "민트색": "민트색 후드티, 민트색 운동화, 민트색 모자",
        "베이지색": "베이지색 코트, 베이지색 가방, 베이지색 신발",
        "흰색": "흰색 티셔츠, 흰색 운동화, 흰색 모자",
        "검은색": "검은색 후드티, 검은색 가방, 검은색 시계",
        "금색": "금색 액세서리, 금색 시계, 금색 지갑",
        "은색": "은색 액세서리, 은색 시계, 은색 케이스",
        "청록색": "청록색 후드티, 청록색 가방, 청록색 운동화"
    }
    
    def generate_fortune(self, name, age, gender, zodiac):
        """
        개인화된 운세 생성
        
        Args:
            name: 이름
            age: 나이
            gender: 성별
            zodiac: 띠 정보
            
        Returns:
            dict: 운세 정보
        """
        # 이름과 나이를 기반으로 시드 설정 (같은 날 같은 결과)
        seed = sum(ord(c) for c in name) + age
        random.seed(seed)
        
        # 행운의 색상 선택
        lucky_color = random.choice(self.LUCKY_COLORS)
        
        # 행운의 로또 번호 6개 생성 (1~45 중복 없이)
        lotto_numbers = sorted(random.sample(range(1, 46), 6))
        lotto_str = ", ".join(map(str, lotto_numbers))
        
        # 쿠팡 API로 실제 상품 검색 시도
        products = []
        try:
            coupang = CoupangClient()
            products = coupang.search_by_color(lucky_color, limit=3)
        except Exception as e:
            print(f"쿠팡 상품 검색 실패: {e}")
        
        # API 실패 시 더미 상품 데이터 생성 (테스트용)
        if not products:
            products = self._get_dummy_products(lucky_color)
        
        # 상품 정보 포맷팅 (텍스트용)
        if products:
            product_recommendation = "\n".join([
                f"- {p['name']} ({p['price']:,}원)" for p in products
            ])
        else:
            # 최후의 수단: 기본 텍스트
            product_recommendation = self.COLOR_PRODUCTS.get(lucky_color, "해당 색상의 액세서리나 의류")
        
        fortune_text = f"""**오늘의 운세**
{random.choice(self.OVERALL_FORTUNES)}

**행운의 로또 번호**
{lotto_str}

**행운의 색상**
{lucky_color}

**추천 상품**
{product_recommendation}
"""
        
        return fortune_text, products  # 상품 정보도 함께 반환
    
    def _get_zodiac_fortune(self, zodiac_name):
        """띠별 특별 운세"""
        zodiac_fortunes = {
            "쥐": "지혜롭고 민첩한 성격이 빛을 발할 것입니다. 오늘은 기회를 포착하는 능력이 뛰어난 날입니다.",
            "소": "성실함과 끈기가 인정받는 날입니다. 꾸준한 노력이 결실을 맺을 것입니다.",
            "호랑이": "용기와 자신감이 넘치는 하루입니다. 리더십을 발휘할 기회가 찾아올 것입니다.",
            "토끼": "온화하고 세심한 당신의 장점이 빛나는 날입니다. 주변 사람들과의 조화가 중요합니다.",
            "용": "카리스마와 추진력이 강해지는 날입니다. 큰 목표를 향해 나아가기 좋은 시기입니다.",
            "뱀": "지혜와 직관력이 뛰어난 날입니다. 중요한 결정을 내리기에 좋은 시기입니다.",
            "말": "활발하고 긍정적인 에너지가 넘치는 날입니다. 새로운 도전을 시작하기 좋습니다.",
            "양": "예술적 감각과 창의력이 돋보이는 날입니다. 평화로운 하루를 보내세요.",
            "원숭이": "재치와 유머 감각이 빛나는 날입니다. 사교적인 활동이 행운을 가져다줄 것입니다.",
            "닭": "계획성과 조직력이 뛰어난 날입니다. 체계적으로 일을 처리하면 좋은 결과를 얻을 것입니다.",
            "개": "충직하고 성실한 당신의 모습이 신뢰를 받는 날입니다. 진심이 통하는 하루가 될 것입니다.",
            "돼지": "관대하고 낙천적인 성격이 행운을 부릅니다. 여유로운 마음가짐이 좋은 기회를 가져다줄 것입니다."
        }
        
        return zodiac_fortunes.get(zodiac_name, "오늘은 특별히 행운이 따르는 날입니다. 긍정적인 마음으로 하루를 보내세요.")
    
    def _get_dummy_products(self, color):
        """테스트용 더미 상품 데이터 생성"""
        dummy_products = {
            "빨간색": [
                {"name": f"{color} 기본 티셔츠", "price": 19900, "image": "https://via.placeholder.com/200x200/FF0000/FFFFFF?text=Red+Tee", "link": "#", "rating": 4.5, "reviews": 123},
                {"name": f"{color} 캐주얼 가방", "price": 39000, "image": "https://via.placeholder.com/200x200/FF0000/FFFFFF?text=Red+Bag", "link": "#", "rating": 4.3, "reviews": 87},
                {"name": f"{color} 스니커즈", "price": 89000, "image": "https://via.placeholder.com/200x200/FF0000/FFFFFF?text=Red+Shoes", "link": "#", "rating": 4.7, "reviews": 256}
            ],
            "파란색": [
                {"name": f"{color} 후드티", "price": 45000, "image": "https://via.placeholder.com/200x200/0000FF/FFFFFF?text=Blue+Hoodie", "link": "#", "rating": 4.6, "reviews": 198},
                {"name": f"{color} 운동화", "price": 129000, "image": "https://via.placeholder.com/200x200/0000FF/FFFFFF?text=Blue+Shoes", "link": "#", "rating": 4.8, "reviews": 342},
                {"name": f"{color} 시계", "price": 159000, "image": "https://via.placeholder.com/200x200/0000FF/FFFFFF?text=Blue+Watch", "link": "#", "rating": 4.4, "reviews": 156}
            ],
            "노란색": [
                {"name": f"{color} 스카프", "price": 25000, "image": "https://via.placeholder.com/200x200/FFFF00/000000?text=Yellow+Scarf", "link": "#", "rating": 4.2, "reviews": 94},
                {"name": f"{color} 지갑", "price": 59000, "image": "https://via.placeholder.com/200x200/FFFF00/000000?text=Yellow+Wallet", "link": "#", "rating": 4.5, "reviews": 178},
                {"name": f"{color} 케이스", "price": 15000, "image": "https://via.placeholder.com/200x200/FFFF00/000000?text=Yellow+Case", "link": "#", "rating": 4.3, "reviews": 67}
            ],
            "초록색": [
                {"name": f"{color} 후드티", "price": 42000, "image": "https://via.placeholder.com/200x200/00FF00/000000?text=Green+Hoodie", "link": "#", "rating": 4.5, "reviews": 145},
                {"name": f"{color} 가방", "price": 68000, "image": "https://via.placeholder.com/200x200/00FF00/000000?text=Green+Bag", "link": "#", "rating": 4.4, "reviews": 112},
                {"name": f"{color} 모자", "price": 28000, "image": "https://via.placeholder.com/200x200/00FF00/000000?text=Green+Cap", "link": "#", "rating": 4.6, "reviews": 203}
            ],
            "보라색": [
                {"name": f"{color} 스웨터", "price": 89000, "image": "https://via.placeholder.com/200x200/800080/FFFFFF?text=Purple+Sweater", "link": "#", "rating": 4.7, "reviews": 234},
                {"name": f"{color} 액세서리", "price": 35000, "image": "https://via.placeholder.com/200x200/800080/FFFFFF?text=Purple+Accessory", "link": "#", "rating": 4.3, "reviews": 98},
                {"name": f"{color} 양말", "price": 12000, "image": "https://via.placeholder.com/200x200/800080/FFFFFF?text=Purple+Socks", "link": "#", "rating": 4.4, "reviews": 156}
            ]
        }
        
        # 기본 더미 상품 (색상별 매칭이 안 될 경우)
        default_products = [
            {"name": f"{color} 기본 상품 1", "price": 30000, "image": "https://via.placeholder.com/200x200/CCCCCC/666666?text=Product+1", "link": "#", "rating": 4.5, "reviews": 100},
            {"name": f"{color} 기본 상품 2", "price": 50000, "image": "https://via.placeholder.com/200x200/CCCCCC/666666?text=Product+2", "link": "#", "rating": 4.3, "reviews": 80},
            {"name": f"{color} 기본 상품 3", "price": 70000, "image": "https://via.placeholder.com/200x200/CCCCCC/666666?text=Product+3", "link": "#", "rating": 4.6, "reviews": 120}
        ]
        
        return dummy_products.get(color, default_products)

