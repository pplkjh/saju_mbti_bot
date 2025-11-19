"""
LLM service for generating analysis using OpenAI
"""
import os
from typing import List
import openai
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """OpenAI LLM 서비스"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    def generate_analysis(
        self,
        birth_date: str,
        birth_time: str,
        gender: str,
        name: str,
        mbti: str,
        context_documents: List[str] = None
    ) -> str:
        """사주와 MBTI 복합 분석 생성"""

        system_role = """
당신은 사주와 MBTI를 전문적으로 분석하는 AI 전문가입니다.
사용자의 생년월일, 출생 시간, 성별, 이름, MBTI를 바탕으로 다음을 분석합니다:

1. **사주 분석**: 오행, 천간지지, 사주팔자 기본 해석
2. **MBTI 성향 분석**: 해당 MBTI 유형의 특성
3. **복합 분석**: 사주와 MBTI의 상관관계 및 시너지
4. **운세 및 성격**: 종합적인 성격, 능력, 적성 분석
5. **조언**: 발전 방향 및 주의점

답변은 친근하면서도 전문적인 톤으로 작성하며, 근거 있는 분석을 제공합니다.
제공된 참고 문서가 있다면 이를 적극 활용합니다.
"""

        # 컨텍스트 문서 포함
        context_text = ""
        if context_documents:
            context_text = "\n\n### 📚 참고 문서:\n" + "\n---\n".join(context_documents)

        user_content = f"""
다음 사용자 정보를 바탕으로 사주와 MBTI를 종합적으로 분석해주세요:

**📋 기본 정보:**
- 이름: {name}
- 생년월일: {birth_date}
- 출생 시간: {birth_time}
- 성별: {gender}
- MBTI: {mbti}

**🎯 분석 요청:**
1. 사주 기본 분석 (오행, 사주팔자)
2. MBTI {mbti} 유형의 특성
3. 사주와 MBTI의 상관관계 분석
4. 종합 성격 및 능력 분석
5. 운세 및 조언

{context_text}

상세하고 구체적으로 분석해주세요. 한국어로 답변하며, 이모지를 적절히 사용하여 가독성을 높여주세요.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            result = response.choices[0].message.content
            logger.info(f"✅ Analysis generated successfully (tokens: {response.usage.total_tokens})")
            return result

        except Exception as e:
            logger.error(f"❌ LLM generation error: {e}")
            raise


# 싱글톤 인스턴스
llm_service = LLMService()
