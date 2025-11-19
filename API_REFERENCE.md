# 📡 API Reference

## 사주 & MBTI 분석 API 레퍼런스

**Base URL**: `https://your-domain.com`
**Version**: v1
**Protocol**: HTTPS
**Format**: JSON

---

## 목차

1. [인증](#인증)
2. [엔드포인트](#엔드포인트)
3. [데이터 모델](#데이터-모델)
4. [에러 코드](#에러-코드)
5. [Rate Limiting](#rate-limiting)
6. [예제 코드](#예제-코드)

---

## 인증

현재 버전은 **인증이 필요하지 않습니다**.

향후 버전에서 API 키 인증이 추가될 예정입니다:
```http
Authorization: Bearer YOUR_API_KEY
```

---

## 엔드포인트

### 1. 헬스체크

서버 상태를 확인합니다.

```http
GET /
```

#### 응답

```json
{
  "status": "healthy",
  "message": "사주 & MBTI 분석 API가 정상 작동 중입니다.",
  "vector_store_loaded": true
}
```

#### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | string | 서버 상태 ("healthy" or "unhealthy") |
| `message` | string | 상태 메시지 |
| `vector_store_loaded` | boolean | 벡터 스토어 로드 여부 |

#### cURL 예제

```bash
curl http://localhost:8000/
```

---

### 2. API 헬스체크 (간단)

API 서버 상태를 간단히 확인합니다.

```http
GET /api/v1/health
```

#### 응답

```json
{
  "status": "ok",
  "timestamp": "2025-01-19T10:30:00",
  "vector_store": "loaded"
}
```

#### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | string | 상태 ("ok" or "error") |
| `timestamp` | string | ISO 8601 형식 타임스탬프 |
| `vector_store` | string | 벡터 스토어 상태 ("loaded" or "not loaded") |

#### cURL 예제

```bash
curl http://localhost:8000/api/v1/health
```

---

### 3. 사주 & MBTI 분석

생년월일, 출생 시간, 성별, 이름, MBTI를 기반으로 종합 분석을 수행합니다.

```http
POST /api/v1/analyze
```

#### 요청 헤더

```http
Content-Type: application/json
```

#### 요청 본문

```json
{
  "birth_date": "1990-05-21",
  "birth_time": "14:30",
  "gender": "여성",
  "name": "홍길동",
  "mbti": "INFJ"
}
```

#### 요청 필드

| 필드 | 타입 | 필수 | 설명 | 예시 |
|------|------|------|------|------|
| `birth_date` | string | ✅ | 생년월일 (YYYY-MM-DD) | "1990-05-21" |
| `birth_time` | string | ✅ | 출생 시간 (HH:MM, 24시간 형식) | "14:30" |
| `gender` | string | ✅ | 성별 ("남성" or "여성") | "여성" |
| `name` | string | ✅ | 이름 | "홍길동" |
| `mbti` | string | ✅ | MBTI 유형 (4자리 대문자) | "INFJ" |

#### 성공 응답 (200 OK)

```json
{
  "success": true,
  "result": "홍길동님의 사주와 MBTI 분석 결과입니다.\n\n### 사주 분석\n1990년 5월 21일에 태어난 홍길동님은...\n\n### MBTI 분석\nINFJ 유형은 옹호자로 알려져 있으며...\n\n### 복합 분석\n사주와 MBTI를 종합해보면...",
  "timestamp": "2025-01-19T10:30:00.123456"
}
```

#### 응답 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | boolean | 분석 성공 여부 |
| `result` | string | 분석 결과 텍스트 (마크다운 형식) |
| `timestamp` | string | ISO 8601 형식 타임스탬프 |

#### 에러 응답 (400 Bad Request)

```json
{
  "detail": [
    {
      "loc": ["body", "birth_date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 에러 응답 (500 Internal Server Error)

```json
{
  "detail": "분석 중 오류가 발생했습니다: OpenAI API timeout"
}
```

#### cURL 예제

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

#### Python 예제

```python
import requests

url = "http://localhost:8000/api/v1/analyze"
data = {
    "birth_date": "1990-05-21",
    "birth_time": "14:30",
    "gender": "여성",
    "name": "홍길동",
    "mbti": "INFJ"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["result"])
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

#### JavaScript 예제

```javascript
const analyzeUser = async () => {
  const response = await fetch('http://localhost:8000/api/v1/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      birth_date: "1990-05-21",
      birth_time: "14:30",
      gender: "여성",
      name: "홍길동",
      mbti: "INFJ"
    })
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data.result);
  } else {
    console.error('Error:', response.status);
  }
};

analyzeUser();
```

---

## 데이터 모델

### AnalysisRequest

사주 MBTI 분석 요청 모델

```python
{
  "birth_date": str,  # YYYY-MM-DD 형식
  "birth_time": str,  # HH:MM 형식 (24시간)
  "gender": str,      # "남성" or "여성"
  "name": str,        # 이름
  "mbti": str         # 4자리 MBTI (예: "INFJ")
}
```

**유효성 검증**:
- `birth_date`: 1900-01-01 ~ 현재
- `birth_time`: 00:00 ~ 23:59
- `gender`: "남성" 또는 "여성"만 허용
- `mbti`: 16가지 유형 중 하나 (대문자)

**유효한 MBTI 유형**:
```
INTJ, INTP, ENTJ, ENTP,
INFJ, INFP, ENFJ, ENFP,
ISTJ, ISFJ, ESTJ, ESFJ,
ISTP, ISFP, ESTP, ESFP
```

---

### AnalysisResponse

사주 MBTI 분석 응답 모델

```python
{
  "success": bool,       # 성공 여부
  "result": str,         # 분석 결과 (마크다운)
  "timestamp": datetime  # 분석 시각
}
```

---

### HealthResponse

서버 상태 응답 모델

```python
{
  "status": str,                 # "healthy" or "unhealthy"
  "message": str,                # 상태 메시지
  "vector_store_loaded": bool    # 벡터 스토어 로드 여부
}
```

---

## 에러 코드

### HTTP 상태 코드

| 코드 | 설명 | 원인 |
|------|------|------|
| 200 | OK | 요청 성공 |
| 400 | Bad Request | 잘못된 요청 형식 |
| 422 | Unprocessable Entity | 유효성 검증 실패 |
| 500 | Internal Server Error | 서버 내부 오류 |
| 503 | Service Unavailable | 서비스 일시 중단 |

### 에러 응답 형식

#### 유효성 검증 오류 (422)

```json
{
  "detail": [
    {
      "loc": ["body", "birth_date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 서버 오류 (500)

```json
{
  "detail": "분석 중 오류가 발생했습니다: [에러 메시지]"
}
```

### 일반적인 에러 메시지

| 에러 메시지 | 원인 | 해결 방법 |
|------------|------|-----------|
| `field required` | 필수 필드 누락 | 모든 필드 포함 |
| `Invalid MBTI type` | 잘못된 MBTI 형식 | 16가지 유형 중 선택 |
| `Invalid date format` | 날짜 형식 오류 | YYYY-MM-DD 형식 사용 |
| `OpenAI API timeout` | API 타임아웃 | 잠시 후 재시도 |
| `Rate limit exceeded` | 요청 제한 초과 | 1분 후 재시도 |

---

## Rate Limiting

### 현재 정책

현재는 Rate Limiting이 적용되지 않습니다.

### 향후 계획

```
무료 티어: 10 requests/minute
프리미엄: 100 requests/minute
엔터프라이즈: Unlimited
```

### Rate Limit 초과 시

```json
{
  "detail": "Rate limit exceeded. Please try again in 60 seconds."
}
```

응답 헤더:
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642598400
```

---

## 예제 코드

### Python (requests)

```python
import requests
from datetime import datetime

class SajuMBTIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def analyze(self, birth_date, birth_time, gender, name, mbti):
        """사주 MBTI 분석 요청"""
        url = f"{self.base_url}/api/v1/analyze"
        data = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "gender": gender,
            "name": name,
            "mbti": mbti
        }

        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def health_check(self):
        """서버 상태 확인"""
        url = f"{self.base_url}/api/v1/health"
        response = requests.get(url)
        return response.json()

# 사용 예시
client = SajuMBTIClient()

# 헬스체크
health = client.health_check()
print(f"Server status: {health['status']}")

# 분석 요청
result = client.analyze(
    birth_date="1990-05-21",
    birth_time="14:30",
    gender="여성",
    name="홍길동",
    mbti="INFJ"
)

if result and result["success"]:
    print(result["result"])
```

---

### JavaScript (Fetch API)

```javascript
class SajuMBTIClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async analyze(birthDate, birthTime, gender, name, mbti) {
    const url = `${this.baseUrl}/api/v1/analyze`;
    const data = {
      birth_date: birthDate,
      birth_time: birthTime,
      gender: gender,
      name: name,
      mbti: mbti
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error:', error);
      return null;
    }
  }

  async healthCheck() {
    const url = `${this.baseUrl}/api/v1/health`;
    const response = await fetch(url);
    return await response.json();
  }
}

// 사용 예시
const client = new SajuMBTIClient();

// 헬스체크
client.healthCheck().then(health => {
  console.log('Server status:', health.status);
});

// 분석 요청
client.analyze('1990-05-21', '14:30', '여성', '홍길동', 'INFJ')
  .then(result => {
    if (result && result.success) {
      console.log(result.result);
    }
  });
```

---

### cURL

#### 기본 요청

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

#### Pretty Print (jq 사용)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-21",
    "birth_time": "14:30",
    "gender": "여성",
    "name": "홍길동",
    "mbti": "INFJ"
  }' | jq .
```

#### 결과를 파일로 저장

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-21",
    "birth_time": "14:30",
    "gender": "여성",
    "name": "홍길동",
    "mbti": "INFJ"
  }' -o result.json
```

---

### PHP

```php
<?php

class SajuMBTIClient {
    private $baseUrl;

    public function __construct($baseUrl = 'http://localhost:8000') {
        $this->baseUrl = $baseUrl;
    }

    public function analyze($birthDate, $birthTime, $gender, $name, $mbti) {
        $url = $this->baseUrl . '/api/v1/analyze';
        $data = [
            'birth_date' => $birthDate,
            'birth_time' => $birthTime,
            'gender' => $gender,
            'name' => $name,
            'mbti' => $mbti
        ];

        $options = [
            'http' => [
                'method' => 'POST',
                'header' => 'Content-Type: application/json',
                'content' => json_encode($data)
            ]
        ];

        $context = stream_context_create($options);
        $result = file_get_contents($url, false, $context);

        return json_decode($result, true);
    }
}

// 사용 예시
$client = new SajuMBTIClient();
$result = $client->analyze('1990-05-21', '14:30', '여성', '홍길동', 'INFJ');

if ($result && $result['success']) {
    echo $result['result'];
}
?>
```

---

## 대화형 API 문서

FastAPI는 자동으로 대화형 API 문서를 생성합니다.

### Swagger UI

```
http://localhost:8000/docs
```

- 모든 엔드포인트 탐색
- 직접 API 테스트 가능
- 요청/응답 예제 제공

### ReDoc

```
http://localhost:8000/redoc
```

- 깔끔한 읽기 전용 문서
- 검색 기능
- 코드 예제

---

## 버전 관리

### 현재 버전

```
v1 (안정 버전)
```

### API 버전 표기

URL 경로에 버전 포함:
```
/api/v1/analyze
```

### 향후 계획

```
v2 (예정)
- 사용자 인증 추가
- 궁합 분석 API
- 일일 운세 API
- 웹훅 지원
```

---

## 지원 및 문의

- **GitHub Issues**: https://github.com/pplkjh/saju_mbti_bot/issues
- **이메일**: (추가 예정)
- **문서**: https://github.com/pplkjh/saju_mbti_bot/blob/main/README.md

---

**Happy Coding!** 🚀
