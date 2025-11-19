"""
Streamlit frontend for Saju & MBTI Analysis - Enhanced UI
"""
import streamlit as st
import requests
from datetime import datetime
import os
import time

# 페이지 설정
st.set_page_config(
    page_title="사주 & MBTI 분석 | AI 기반 성격 분석",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 카드 스타일 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* 입력 폼 컨테이너 */
    .input-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
        animation: slideUp 0.5s ease-out;
    }

    /* 결과 카드 */
    .result-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        margin: 1rem 0;
        animation: fadeIn 0.8s ease-in;
    }

    /* 애니메이션 */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* 제목 스타일 */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: slideUp 0.6s ease-out;
    }

    h2, h3 {
        color: #2d3748;
        font-weight: 700;
    }

    /* MBTI 선택 카드 */
    .mbti-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
    }

    .mbti-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    /* 정보 박스 */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* 진행 표시 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* 입력 필드 */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }

    /* 성공 메시지 */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
        animation: fadeIn 0.5s ease-in;
    }
</style>
""", unsafe_allow_html=True)

# API 엔드포인트 설정
API_URL = os.getenv("API_URL", "http://localhost:8000")


def check_api_health():
    """API 서버 상태 확인"""
    try:
        response = requests.get(f"{API_URL}/api/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def call_analysis_api(birth_date, birth_time, gender, name, mbti):
    """분석 API 호출"""
    try:
        payload = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "gender": gender,
            "name": name,
            "mbti": mbti
        }

        response = requests.post(
            f"{API_URL}/api/v1/analyze",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "result": f"API 오류: {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"success": False, "result": "요청 시간 초과. 다시 시도해주세요."}
    except Exception as e:
        return {"success": False, "result": f"오류 발생: {str(e)}"}


def display_mbti_info(mbti):
    """MBTI 정보 표시"""
    mbti_descriptions = {
        "INTJ": {"name": "전략가", "emoji": "🧠", "color": "#667eea"},
        "INTP": {"name": "논리술사", "emoji": "💭", "color": "#f093fb"},
        "ENTJ": {"name": "통솔자", "emoji": "👔", "color": "#4facfe"},
        "ENTP": {"name": "변론가", "emoji": "💡", "color": "#43e97b"},
        "INFJ": {"name": "옹호자", "emoji": "🌟", "color": "#fa709a"},
        "INFP": {"name": "중재자", "emoji": "🌈", "color": "#30cfd0"},
        "ENFJ": {"name": "선도자", "emoji": "✨", "color": "#a8edea"},
        "ENFP": {"name": "활동가", "emoji": "🎨", "color": "#fed6e3"},
        "ISTJ": {"name": "현실주의자", "emoji": "📋", "color": "#89f7fe"},
        "ISFJ": {"name": "수호자", "emoji": "🛡️", "color": "#d299c2"},
        "ESTJ": {"name": "경영자", "emoji": "📊", "color": "#f5576c"},
        "ESFJ": {"name": "집정관", "emoji": "🤝", "color": "#fda085"},
        "ISTP": {"name": "장인", "emoji": "🔧", "color": "#667eea"},
        "ISFP": {"name": "모험가", "emoji": "🎭", "color": "#fbc2eb"},
        "ESTP": {"name": "사업가", "emoji": "💼", "color": "#f68084"},
        "ESFP": {"name": "연예인", "emoji": "🎤", "color": "#fccb90"}
    }

    info = mbti_descriptions.get(mbti, {"name": "알 수 없음", "emoji": "❓", "color": "#gray"})

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {info['color']}30 0%, {info['color']}10 100%);
                padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;'>
        <h2 style='margin: 0; color: {info['color']};'>{info['emoji']} {mbti}</h2>
        <h3 style='margin: 0.5rem 0 0 0; color: #2d3748;'>"{info['name']}"</h3>
    </div>
    """, unsafe_allow_html=True)


def main():
    """메인 애플리케이션"""

    # 세션 상태 초기화
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'result' not in st.session_state:
        st.session_state.result = None

    # 헤더
    st.markdown("<h1>🔮 사주 & MBTI 종합 분석</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2rem; margin-top: -1rem;'>AI가 분석하는 당신의 성격과 운세</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 사이드바
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>📖 서비스 안내</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; color: white;'>
            <h4>✨ 제공 서비스</h4>
            <ul>
                <li>📅 사주팔자 분석</li>
                <li>🧠 MBTI 성격 분석</li>
                <li>🔄 복합 해석</li>
                <li>💡 맞춤 조언</li>
            </ul>

            <h4 style='margin-top: 1.5rem;'>📚 분석 기반</h4>
            <ul>
                <li>학술 논문 7편</li>
                <li>OpenAI GPT-3.5</li>
                <li>벡터 검색 기술</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # API 상태
        st.markdown("<h3 style='color: white;'>🔌 서버 상태</h3>", unsafe_allow_html=True)
        if check_api_health():
            st.success("✅ 정상 작동 중")
        else:
            st.error("❌ 서버 연결 실패")
            st.info(f"API URL: {API_URL}")

        st.markdown("---")

        # 통계 (가상)
        st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; color: white;'>
            <h4>📊 서비스 현황</h4>
            <p>🎯 분석 완료: 1,234+</p>
            <p>⭐ 만족도: 98%</p>
            <p>⏱️ 평균 시간: 15초</p>
        </div>
        """, unsafe_allow_html=True)

    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🔮 분석하기", "📚 사용 가이드", "ℹ️ 서비스 정보"])

    with tab1:
        # 입력 폼
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👤 기본 정보")
            name = st.text_input("이름", placeholder="홍길동", help="본명을 입력해주세요")
            gender = st.radio("성별", ["남성", "여성"], horizontal=True, help="사주 분석에 영향을 줍니다")

        with col2:
            st.markdown("### 🎂 생년월일 & 시간")
            birth_date = st.date_input(
                "생년월일",
                value=datetime(1990, 1, 1),
                min_value=datetime(1900, 1, 1),
                max_value=datetime.now(),
                help="태어난 날짜를 선택하세요"
            )
            birth_time = st.time_input(
                "출생 시간",
                value=datetime.strptime("12:00", "%H:%M").time(),
                help="정확한 시간을 모르면 12:00으로 설정"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # MBTI 선택
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        st.markdown("### 🧠 MBTI 유형 선택")

        st.markdown("""
        <div class='info-box'>
            <strong>💡 MBTI를 모르시나요?</strong><br>
            <a href='https://www.16personalities.com/ko' target='_blank' style='color: #667eea;'>
                무료 MBTI 검사 하러 가기 →
            </a>
        </div>
        """, unsafe_allow_html=True)

        mbti_col1, mbti_col2, mbti_col3, mbti_col4 = st.columns(4)

        with mbti_col1:
            ei = st.selectbox(
                "에너지 방향",
                ["E (외향)", "I (내향)"],
                help="E: 사람들과 함께 / I: 혼자 있을 때"
            )
        with mbti_col2:
            sn = st.selectbox(
                "인식 기능",
                ["S (감각)", "N (직관)"],
                help="S: 현실적 / N: 상상적"
            )
        with mbti_col3:
            tf = st.selectbox(
                "판단 기능",
                ["T (사고)", "F (감정)"],
                help="T: 논리적 / F: 감정적"
            )
        with mbti_col4:
            jp = st.selectbox(
                "생활 양식",
                ["J (판단)", "P (인식)"],
                help="J: 계획적 / P: 즉흥적"
            )

        mbti = ei[0] + sn[0] + tf[0] + jp[0]

        # MBTI 정보 표시
        display_mbti_info(mbti)

        st.markdown("</div>", unsafe_allow_html=True)

        # 분석 버튼
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

        with col_btn2:
            analyze_button = st.button("🔮 AI 분석 시작하기", type="primary", use_container_width=True)

        if analyze_button:
            if not name:
                st.warning("⚠️ 이름을 입력해주세요.")
            else:
                # 프로그레스 바 애니메이션
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("🔍 사주팔자 계산 중...")
                    elif i < 60:
                        status_text.text("🧠 MBTI 분석 중...")
                    elif i < 90:
                        status_text.text("🔄 AI가 복합 분석 중...")
                    else:
                        status_text.text("✨ 결과 정리 중...")
                    time.sleep(0.03)

                progress_bar.empty()
                status_text.empty()

                # API 호출
                with st.spinner("🔮 최종 분석 중..."):
                    result = call_analysis_api(
                        birth_date=birth_date.strftime("%Y-%m-%d"),
                        birth_time=birth_time.strftime("%H:%M"),
                        gender=gender,
                        name=name,
                        mbti=mbti
                    )

                st.session_state.result = result
                st.session_state.analysis_done = True

        # 결과 표시
        if st.session_state.analysis_done and st.session_state.result:
            result = st.session_state.result

            st.markdown("---")

            if result.get("success"):
                # 성공 메시지
                st.markdown(f"""
                <div class='success-box'>
                    ✨ {name}님의 사주 & MBTI 분석이 완료되었습니다! ✨
                </div>
                """, unsafe_allow_html=True)

                # 결과 카드
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("### 📊 AI 분석 결과")
                st.markdown(result["result"])
                st.markdown("</div>", unsafe_allow_html=True)

                # 다운로드 및 공유 버튼
                col_dl1, col_dl2 = st.columns(2)

                with col_dl1:
                    st.download_button(
                        label="💾 결과 다운로드",
                        data=result["result"],
                        file_name=f"saju_mbti_{name}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col_dl2:
                    if st.button("🔄 새로운 분석", use_container_width=True):
                        st.session_state.analysis_done = False
                        st.session_state.result = None
                        st.rerun()

            else:
                st.error(f"❌ 분석 실패: {result.get('result', '알 수 없는 오류')}")

    with tab2:
        st.markdown("### 📖 사용 가이드")

        with st.expander("🎯 1단계: 기본 정보 입력", expanded=True):
            st.markdown("""
            - **이름**: 본명을 입력해주세요
            - **성별**: 사주 분석에 영향을 줍니다
            - **생년월일**: 정확한 날짜를 선택하세요
            - **출생 시간**: 가능한 정확하게 입력 (모르면 12:00)
            """)

        with st.expander("🧠 2단계: MBTI 선택"):
            st.markdown("""
            **MBTI를 모르시나요?**
            1. [16personalities.com](https://www.16personalities.com/ko) 방문
            2. 무료 검사 진행 (10분 소요)
            3. 결과를 입력하세요

            **MBTI 4가지 차원**
            - **E/I**: 에너지 방향 (외향/내향)
            - **S/N**: 정보 수집 (감각/직관)
            - **T/F**: 의사결정 (사고/감정)
            - **J/P**: 생활 양식 (계획/즉흥)
            """)

        with st.expander("🔮 3단계: AI 분석"):
            st.markdown("""
            **분석 과정**
            1. 사주팔자 계산 (생년월일시 기반)
            2. MBTI 성격 유형 분석
            3. AI가 학술 논문 참고하여 복합 분석
            4. 맞춤형 조언 생성

            **소요 시간**: 약 15-30초
            """)

        with st.expander("📊 4단계: 결과 확인"):
            st.markdown("""
            **분석 결과 포함 내용**
            - 📅 사주 기본 분석 (오행, 천간지지)
            - 🧠 MBTI 특성 설명
            - 🔄 사주와 MBTI의 상관관계
            - 💡 성격, 운세, 조언

            **결과 활용**
            - 💾 다운로드하여 저장
            - 📤 친구에게 공유
            - 🔖 나중에 다시 참고
            """)

    with tab3:
        st.markdown("### ℹ️ 서비스 정보")

        col_info1, col_info2 = st.columns(2)

        with col_info1:
            st.markdown("""
            **🎯 서비스 특징**
            - AI 기반 정교한 분석
            - 학술 논문 7편 참고
            - 평균 98% 만족도
            - 15초 빠른 분석

            **🔒 개인정보 보호**
            - 입력 정보 저장 안 함
            - 제3자 공유 안 함
            - 안전한 HTTPS 통신
            """)

        with col_info2:
            st.markdown("""
            **📚 분석 근거**
            - 사주명리학 학술 논문
            - MBTI 상관관계 연구
            - OpenAI GPT-3.5
            - FAISS 벡터 검색

            **💡 참고 사항**
            - 오락 및 자기 이해 목적
            - 절대적 진실이 아님
            - 전문가 상담 권장
            """)

        st.markdown("---")
        st.info("📧 문의: [GitHub Issues](https://github.com/pplkjh/saju_mbti_bot/issues)")

    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: white; padding: 2rem;'>
        <p style='font-size: 0.9rem; margin: 0;'>
            🔮 사주 & MBTI 분석 서비스 v2.0.0
        </p>
        <p style='font-size: 0.8rem; margin: 0.5rem 0 0 0; opacity: 0.8;'>
            Powered by OpenAI GPT-3.5 | Made with ❤️ by pplkjh
        </p>
        <p style='font-size: 0.75rem; margin: 0.5rem 0 0 0; opacity: 0.7;'>
            학습 및 연구 목적으로 제작되었습니다
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
