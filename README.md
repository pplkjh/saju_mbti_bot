# 🔮 사주 & MBTI 종합 분석 서비스

생년월일과 MBTI를 기반으로 사주명리학과 성격 유형을 복합적으로 분석하는 AI 서비스입니다.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 주요 기능

- 📅 **사주 분석**: 생년월일 기반 사주팔자 해석
- 🧠 **MBTI 분석**: 16가지 성격 유형 분석
- 🔄 **복합 분석**: 사주와 MBTI의 상관관계 해석
- 📚 **학술 기반**: 7편의 학술 논문 데이터 활용
- 🤖 **AI 기반**: OpenAI GPT-3.5 활용
- 💾 **벡터 검색**: FAISS 기반 문서 검색

## 🏗️ 아키텍처

```
┌─────────────────┐
│   Streamlit     │  ← 프론트엔드 (포트 8501)
│   Frontend      │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │  ← 백엔드 API (포트 8000)
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌─────┐  ┌────────┐
│OpenAI  │ │FAISS│  │  PDF   │
│GPT-3.5 │ │ DB  │  │ Docs   │
└────────┘ └─────┘  └────────┘
```

## 📁 프로젝트 구조

```
saju_mbti_bot/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                # API 엔트리포인트
│   ├── models/
│   │   └── schemas.py         # Pydantic 모델
│   └── services/
│       ├── saju_analyzer.py   # 분석 로직
│       ├── llm_service.py     # OpenAI 서비스
│       └── vector_store.py    # FAISS 벡터 스토어
├── frontend/                   # Streamlit 프론트엔드
│   └── app.py                 # UI 애플리케이션
├── scripts/
│   └── build_vector_store.py  # PDF 벡터화 스크립트
├── data/
│   ├── *.pdf                  # 학술 논문 (7편)
│   └── vector_store/          # FAISS 인덱스 (생성됨)
├── .env.example               # 환경 변수 템플릿
├── railway.json               # Railway 배포 설정
└── README.md
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/pplkjh/saju_mbti_bot.git
cd saju_mbti_bot

# 환경 변수 설정
cp .env.example .env
# .env 파일에 OPENAI_API_KEY 입력
```

### 2. 백엔드 설치 & 실행

```bash
cd backend
pip install -r requirements.txt

# PDF 벡터 스토어 생성 (최초 1회)
python ../scripts/build_vector_store.py

# 백엔드 서버 실행
python main.py
```

백엔드가 http://localhost:8000 에서 실행됩니다.

### 3. 프론트엔드 실행

```bash
# 새 터미널에서
cd frontend
pip install -r requirements.txt

# Streamlit 앱 실행
streamlit run app.py
```

프론트엔드가 http://localhost:8501 에서 실행됩니다.

## 📚 참고 논문

본 서비스는 다음 학술 논문을 기반으로 합니다:

1. 사주 명리 일주론과 MBTI성격유형의 상호보완성에 관한 연구
2. 사주 명리학의 8가지 성격유형과 MBTI기능별 8가지 성격유형의 상관연구
3. 사주명리학을 통한 성격
4. 사주와 MBTI 성격이론과의 상관관계 연구
5. 사주의 오행분포가 성격형성에 미치는 영향
6. 역과 명리학

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: 고성능 비동기 API 프레임워크
- **LangChain**: LLM 오케스트레이션
- **FAISS**: 벡터 유사도 검색
- **OpenAI API**: GPT-3.5 Turbo
- **PyMuPDF**: PDF 텍스트 추출

### 프론트엔드
- **Streamlit**: 빠른 웹 UI 개발
- **Requests**: HTTP 클라이언트

## 🌐 배포

### Railway 배포 (무료/유료)

1. Railway 계정 생성: https://railway.app
2. GitHub 저장소 연결
3. 환경 변수 설정:
   - `OPENAI_API_KEY`
4. 자동 배포 완료!

### 로컬 Docker 배포

```bash
# 백엔드 Docker 이미지 빌드
docker build -t saju-mbti-backend ./backend

# 컨테이너 실행
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  saju-mbti-backend
```

## 📊 API 문서

백엔드 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

```
POST /api/v1/analyze
  - 사주 & MBTI 분석 수행

GET /api/v1/health
  - 서버 상태 확인

GET /
  - 헬스체크
```

## 💡 사용 예시

### API 직접 호출

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-21",
    "birth_time": "14:30",
    "gender": "여성",
    "name": "홍길동",
    "mbti": "INFJ"
  }'
```

### Python 클라이언트

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "birth_date": "1990-05-21",
        "birth_time": "14:30",
        "gender": "여성",
        "name": "홍길동",
        "mbti": "INFJ"
    }
)

result = response.json()
print(result["result"])
```

## 🔧 개발 & 커스터마이징

### 벡터 스토어 재생성

PDF 문서를 추가/변경한 경우:

```bash
python scripts/build_vector_store.py
```

### LLM 모델 변경

`.env` 파일에서:

```env
OPENAI_MODEL=gpt-4  # 또는 gpt-3.5-turbo, gpt-4-turbo 등
```

### UI 커스터마이징

`frontend/app.py` 파일을 수정하여 Streamlit UI를 자유롭게 커스터마이징할 수 있습니다.

## 📈 향후 계획

- [ ] 사용자 인증 & 프로필 관리
- [ ] 분석 결과 저장 & 히스토리
- [ ] 궁합 분석 기능 추가
- [ ] Flutter 모바일 앱 개발
- [ ] 일일 운세 푸시 알림
- [ ] 다국어 지원 (영어, 일본어)
- [ ] 결제 시스템 통합

## 🤝 기여

프로젝트 개선을 위한 기여를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📧 문의

문의사항이 있으시면 이슈를 생성해주세요.

---

**Made with ❤️ by pplkjh**
