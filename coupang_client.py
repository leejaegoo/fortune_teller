"""
쿠팡 파트너스 API 클라이언트
"""
import os
import requests
import hmac
import hashlib
import base64
from datetime import datetime
from urllib.parse import quote

class CoupangClient:
    """쿠팡 파트너스 API를 사용하기 위한 클라이언트 클래스"""
    
    def __init__(self, access_key=None, secret_key=None):
        """
        쿠팡 클라이언트 초기화
        
        Args:
            access_key: 쿠팡 파트너스 Access Key
            secret_key: 쿠팡 파트너스 Secret Key
        """
        self.access_key = access_key or os.getenv("COUPANG_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("COUPANG_SECRET_KEY")
        
        if not self.access_key or not self.secret_key:
            # API 키가 없어도 에러를 던지지 않고, 상품 검색 실패 시 빈 리스트 반환
            self.access_key = None
            self.secret_key = None
        
        self.base_url = "https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/search"
    
    def _generate_signature(self, method, path, secret_key, access_key):
        """쿠팡 API 서명 생성"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        message = f"{timestamp}{method}{path}"
        signature = base64.b64encode(
            hmac.new(
                secret_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        return timestamp, signature
    
    def search_products(self, keyword, limit=3):
        """
        상품 검색
        
        Args:
            keyword: 검색어
            limit: 반환할 상품 개수 (기본값: 3)
            
        Returns:
            list: 상품 정보 리스트 (이름, 가격, 이미지, 링크)
        """
        if not self.access_key or not self.secret_key:
            return []
        
        try:
            # 검색어 URL 인코딩
            keyword_encoded = quote(keyword)
            path = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword={keyword_encoded}"
            
            # 서명 생성
            timestamp, signature = self._generate_signature("GET", path, self.secret_key, self.access_key)
            
            # 헤더 설정
            headers = {
                "Authorization": f"CEA algorithm=HmacSHA256, access-key={self.access_key}, signed-date={timestamp}, signature={signature}",
                "Content-Type": "application/json;charset=UTF-8"
            }
            
            # API 호출
            response = requests.get(
                f"https://api-gateway.coupang.com{path}",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                products = []
                
                # 상품 정보 추출
                if "data" in data and "productData" in data["data"]:
                    for item in data["data"]["productData"][:limit]:
                        product = {
                            "name": item.get("productName", ""),
                            "price": item.get("productPrice", 0),
                            "image": item.get("productImage", ""),
                            "link": item.get("productUrl", ""),
                            "rating": item.get("rating", 0),
                            "reviews": item.get("reviewCount", 0)
                        }
                        products.append(product)
                
                return products
            else:
                return []
                
        except Exception as e:
            print(f"쿠팡 API 오류: {e}")
            return []
    
    def search_by_color(self, color, product_type="의류", limit=3):
        """
        색상별 상품 검색
        
        Args:
            color: 색상 (예: "빨간색", "파란색")
            product_type: 상품 유형 (기본값: "의류")
            limit: 반환할 상품 개수
            
        Returns:
            list: 상품 정보 리스트
        """
        # 색상별 검색어 매핑
        color_keywords = {
            "빨간색": f"{color} {product_type}",
            "파란색": f"{color} {product_type}",
            "노란색": f"{color} {product_type}",
            "초록색": f"{color} {product_type}",
            "보라색": f"{color} {product_type}",
            "주황색": f"{color} {product_type}",
            "분홍색": f"{color} {product_type}",
            "하늘색": f"{color} {product_type}",
            "민트색": f"{color} {product_type}",
            "베이지색": f"{color} {product_type}",
            "흰색": f"{color} {product_type}",
            "검은색": f"{color} {product_type}",
            "금색": f"{color} 액세서리",
            "은색": f"{color} 액세서리",
            "청록색": f"{color} {product_type}"
        }
        
        keyword = color_keywords.get(color, f"{color} {product_type}")
        return self.search_products(keyword, limit)

