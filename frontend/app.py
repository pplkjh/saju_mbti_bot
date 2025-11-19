"""
Streamlit frontend for Saju & MBTI Analysis
"""
import streamlit as st
import requests
from datetime import datetime
import os

# 페이지 설정
st.set_page_config(
    page_title="사주 & MBTI 분석",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


def main():
    """메인 애플리케이션"""

    # 헤더
    st.title("🔮 사주 & MBTI 종합 분석")
    st.markdown("---")

    # 사이드바
    with st.sidebar:
        st.header("ℹ️ 서비스 안내")
        st.markdown("""
        **사주와 MBTI를 함께 분석합니다**

        - 📅 생년월일 기반 사주 분석
        - 🧠 MBTI 성격 유형 분석
        - 🔄 두 이론의 복합 해석
        - 💡 맞춤 조언 제공

        ### 📚 분석 기반
        - 사주명리학 학술 논문
        - MBTI 상관관계 연구
        - AI 기반 종합 해석
        """)

        # API 상태 표시
        st.markdown("---")
        st.subheader("🔌 서버 상태")
        if check_api_health():
            st.success("✅ 정상 작동 중")
        else:
            st.error("❌ 서버 연결 실패")
            st.info(f"API URL: {API_URL}")

    # 메인 입력 폼
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 기본 정보")
        name = st.text_input("이름", placeholder="홍길동")
        gender = st.radio("성별", ["남성", "여성"], horizontal=True)

    with col2:
        st.subheader("🎂 생년월일 & 시간")
        birth_date = st.date_input(
            "생년월일",
            value=datetime(1990, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now()
        )
        birth_time = st.time_input("출생 시간", value=datetime.strptime("12:00", "%H:%M").time())

    # MBTI 선택
    st.subheader("🧠 MBTI 유형")

    mbti_col1, mbti_col2, mbti_col3, mbti_col4 = st.columns(4)

    with mbti_col1:
        ei = st.selectbox("에너지 방향", ["E (외향)", "I (내향)"])
    with mbti_col2:
        sn = st.selectbox("인식 기능", ["S (감각)", "N (직관)"])
    with mbti_col3:
        tf = st.selectbox("판단 기능", ["T (사고)", "F (감정)"])
    with mbti_col4:
        jp = st.selectbox("생활 양식", ["J (판단)", "P (인식)"])

    mbti = ei[0] + sn[0] + tf[0] + jp[0]

    st.info(f"선택된 MBTI: **{mbti}**")

    # 분석 버튼
    st.markdown("---")

    if st.button("🔮 분석 시작", type="primary", use_container_width=True):
        if not name:
            st.warning("⚠️ 이름을 입력해주세요.")
            return

        # 로딩 표시
        with st.spinner("🔄 분석 중... 잠시만 기다려주세요."):

            # API 호출
            result = call_analysis_api(
                birth_date=birth_date.strftime("%Y-%m-%d"),
                birth_time=birth_time.strftime("%H:%M"),
                gender=gender,
                name=name,
                mbti=mbti
            )

            # 결과 표시
            st.markdown("---")

            if result.get("success"):
                st.success(f"✅ {name}님의 분석이 완료되었습니다!")

                # 결과를 확장 가능한 영역에 표시
                with st.container():
                    st.markdown("### 📊 분석 결과")
                    st.markdown(result["result"])

                # 저장 버튼
                st.download_button(
                    label="💾 결과 다운로드",
                    data=result["result"],
                    file_name=f"saju_mbti_analysis_{name}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"❌ 분석 실패: {result.get('result', '알 수 없는 오류')}")

    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <small>사주 & MBTI 분석 서비스 v1.0.0 | Powered by AI</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
