// DOM 요소
const fortuneForm = document.getElementById('fortuneForm');
const formContainer = document.getElementById('formContainer');
const loading = document.getElementById('loading');
const resultContainer = document.getElementById('resultContainer');

// 폼 제출 이벤트
fortuneForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // 입력값 가져오기
    const name = document.getElementById('name').value.trim();
    const birthDate = document.getElementById('birthDate').value;
    const gender = document.querySelector('input[name="gender"]:checked')?.value;
    
    // 유효성 검사
    if (!name || !birthDate || !gender) {
        alert('모든 정보를 입력해주세요!');
        return;
    }
    
    // UI 상태 변경
    formContainer.classList.add('hidden');
    loading.classList.add('show');
    resultContainer.classList.remove('show');
    
    try {
        // API 호출
        const response = await fetch('/get_fortune', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                birth_date: birthDate,
                gender: gender
            })
        });
        
        const data = await response.json();

        // 디버깅: 응답 데이터 확인
        console.log('API Response:', data);

        if (response.ok) {
            // 에러 필드가 있는지 확인
            if (data.error) {
                throw new Error(data.error);
            }
            // 성공: 결과 표시
            displayFortune(data);
        } else {
            // 오류 처리
            throw new Error(data.error || '운세를 가져오는데 실패했습니다.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert(`오류가 발생했습니다: ${error.message}`);
        
        // UI 복원
        loading.classList.remove('show');
        formContainer.classList.remove('hidden');
    }
});

/**
 * 운세 결과를 화면에 표시
 */
function displayFortune(data) {
    // 로딩 숨기기
    loading.classList.remove('show');
    
    // 기본 정보 표시
    document.getElementById('userName').textContent = `${data.name}님의 오늘의 운세`;
    document.getElementById('zodiacEmoji').textContent = data.zodiac.emoji;
    document.getElementById('zodiacName').textContent = `${data.zodiac.name}띠`;
    document.getElementById('resultDate').textContent = data.date;
    
    // 운세 내용 파싱 및 표시
    const fortuneContent = document.getElementById('fortuneContent');
    fortuneContent.innerHTML = parseFortuneText(data.full_text);
    
    // 명언 표시
    if (data.quote) {
        document.getElementById('quoteText').textContent = `"${data.quote.text}"`;
        document.getElementById('quoteAuthor').textContent = `- ${data.quote.author}`;
    }
    
    // 결과 컨테이너 표시
    resultContainer.classList.add('show');
    
    // 스크롤을 결과로 이동
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Claude의 운세 텍스트를 HTML로 변환
 */
function parseFortuneText(text) {
    // text가 없으면 에러 메시지 반환
    if (!text) {
        console.error('Fortune text is undefined or empty');
        return '<p class="error">운세를 불러올 수 없습니다. 다시 시도해주세요.</p>';
    }

    // **제목** 형식을 h3 태그로 변환
    let html = text.replace(/\*\*([^*]+)\*\*/g, '<h3>$1</h3>');
    
    // 줄바꿈을 <p> 태그로 변환
    const lines = html.split('\n').filter(line => line.trim());
    let result = '';
    let currentParagraph = '';
    
    lines.forEach(line => {
        if (line.startsWith('<h3>')) {
            // 제목이면 이전 단락을 마무리하고 제목 추가
            if (currentParagraph) {
                result += `<p>${currentParagraph}</p>`;
                currentParagraph = '';
            }
            result += line;
        } else {
            // 일반 텍스트면 단락에 추가
            if (currentParagraph) {
                currentParagraph += ' ';
            }
            currentParagraph += line.trim();
        }
    });
    
    // 마지막 단락 추가
    if (currentParagraph) {
        result += `<p>${currentParagraph}</p>`;
    }
    
    return result;
}

/**
 * 생년월일 입력 제한 (오늘 날짜까지만)
 */
const birthDateInput = document.getElementById('birthDate');
const today = new Date().toISOString().split('T')[0];
birthDateInput.setAttribute('max', today);

// 기본값을 1990년으로 설정
birthDateInput.setAttribute('value', '1990-01-01');

/**
 * 입력 필드 포커스 효과
 */
const inputs = document.querySelectorAll('input[type="text"], input[type="date"]');
inputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
        this.parentElement.style.transition = 'transform 0.2s ease';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

/**
 * 이름 입력 시 자동으로 다음 필드로 포커스 이동
 */
document.getElementById('name').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('birthDate').focus();
    }
});

// 페이지 로드 시 애니메이션
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

