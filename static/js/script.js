// DOM 요소
const fortuneForm = document.getElementById('fortuneForm');
const formContainer = document.getElementById('formContainer');
const loading = document.getElementById('loading');
const resultContainer = document.getElementById('resultContainer');

console.log('Script loaded v4.0 (Fix display logic)');

// 폼 제출 이벤트
fortuneForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // 입력값 가져오기
    const name = document.getElementById('name').value;
    const birthDate = document.getElementById('birthDate').value;
    const gender = document.querySelector('input[name="gender"]:checked')?.value;
    
    if (!name || !birthDate || !gender) {
        alert('모든 정보를 입력해주세요!');
        return;
    }

    // UI 상태 변경: 폼 숨기고 로딩 표시
    formContainer.classList.add('hidden');
    formContainer.style.display = 'none'; // 폼 즉시 숨김
    
    loading.classList.add('show');
    loading.setAttribute('style', 'display: block !important;'); // 로딩 강제 표시
    resultContainer.classList.add('hidden');
    
    try {
        const response = await fetch('/get_fortune', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, birth_date: birthDate, gender })
        });
        
        const data = await response.json();
        console.log("API Response:", data);
        
        // 로딩 숨기기
        loading.classList.remove('show');
        loading.style.display = 'none'; // 강제 숨김
        console.log("Loading hidden");

        if (data.error) {
            throw new Error(data.error);
        }

        // 데이터 채우기
        console.log("Populating data...");
        document.getElementById('userName').textContent = `${data.name}님의 운세`;
        if (data.zodiac) {
            document.getElementById('zodiacEmoji').textContent = data.zodiac.emoji;
            document.getElementById('zodiacName').textContent = data.zodiac.name;
        }
        document.getElementById('resultDate').textContent = data.date;
        
        // 텍스트 변환 (마크다운 -> HTML)
        let htmlContent = data.full_text;
        if (htmlContent) {
            htmlContent = htmlContent.replace(/\*\*([^*]+)\*\*/g, '<h3>$1</h3>');
            htmlContent = htmlContent.replace(/\n/g, '<br>');
            document.getElementById('fortuneContent').innerHTML = htmlContent;
        }
        
        if (data.quote) {
            document.getElementById('quoteText').textContent = data.quote.text;
            document.getElementById('quoteAuthor').textContent = data.quote.author;
        }

        // 상품 정보 표시
        console.log("Products data:", data.products); // 디버깅용
        if (data.products && data.products.length > 0) {
            console.log("Displaying products:", data.products.length); // 디버깅용
            const productsGrid = document.getElementById('productsGrid');
            const productsSection = document.getElementById('productsSection');
            
            if (!productsGrid || !productsSection) {
                console.error("Products section elements not found!");
                return;
            }
            
            productsGrid.innerHTML = ''; // 기존 내용 초기화
            
            data.products.forEach(product => {
                const productCard = document.createElement('div');
                productCard.className = 'product-card';
                productCard.innerHTML = `
                    <a href="${product.link}" target="_blank" rel="noopener noreferrer">
                        <img src="${product.image}" alt="${product.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'200\\' height=\\'200\\'%3E%3Crect fill=\\'%23ddd\\' width=\\'200\\' height=\\'200\\'/%3E%3Ctext fill=\\'%23999\\' font-family=\\'sans-serif\\' font-size=\\'14\\' x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dy=\\'.3em\\'%3E이미지 없음%3C/text%3E%3C/svg%3E'">
                        <div class="product-info">
                            <h4>${product.name}</h4>
                            <p class="product-price">${product.price.toLocaleString()}원</p>
                            ${product.rating > 0 ? `<p class="product-rating">⭐ ${product.rating} (리뷰 ${product.reviews}개)</p>` : ''}
                        </div>
                    </a>
                `;
                productsGrid.appendChild(productCard);
            });
            
            productsSection.style.display = 'block';
            console.log("Products section displayed");
        } else {
            console.log("No products data found");
            const productsSection = document.getElementById('productsSection');
            if (productsSection) {
                productsSection.style.display = 'none';
            }
        }

        // 결과 화면 표시 (가장 중요!)
        resultContainer.classList.remove('hidden');
        resultContainer.setAttribute('style', 'display: block !important; visibility: visible !important; opacity: 1 !important;');
        
        // 폼 강제 숨김
        formContainer.classList.add('hidden');
        formContainer.style.display = 'none';

        console.log("Result forced visible");
        
        // 스크롤 이동
        setTimeout(() => {
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        console.error(error);
        alert("오류가 발생했습니다: " + error.message);
        
        // 복구
        loading.classList.remove('show');
        loading.style.display = 'none';
        formContainer.classList.remove('hidden');
        formContainer.style.display = 'block';
    }
});

// 초기화
const birthDateInput = document.getElementById('birthDate');
if(birthDateInput) {
    const today = new Date().toISOString().split('T')[0];
    birthDateInput.setAttribute('max', today);
    birthDateInput.setAttribute('value', '1995-01-01');
}
