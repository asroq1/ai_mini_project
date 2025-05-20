import os
from pathlib import Path
import json

class ReportAgent:
    def __init__(self, model="gpt-4-turbo", temperature=0.2, output_dir=None):
        self.model = model
        self.temperature = temperature
        
        # output_dir 인자를 처리하는 코드 추가
        self.output_dir = Path(output_dir) if output_dir else Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # 보고서 생성 프롬프트 로드
        try:
            with open("보고서_생성_프롬프트.txt", "r", encoding="utf-8") as file:
                self.report_prompt_template = file.read()
        except FileNotFoundError:
            self.report_prompt_template = "다국적 시장 진출 전략 보고서를 작성하세요."
            print("경고: '보고서_생성_프롬프트.txt' 파일을 찾을 수 없습니다. 기본 프롬프트를 사용합니다.")
    
    def generate_markdown_report(self, market_data, strategy_options, company_name, product_name, report_filename="final_report"):
        """
        마크다운 보고서를 생성하는 메서드
        """
        # 상태 데이터 구성
        state = {
            "startup_info": {
                "name": company_name,
                "business_model": "글로벌 시장 진출을 준비하는 기업",
                "products": product_name
            },
            "target_countries": self._extract_target_countries(market_data),
            "market_data": self._process_market_data(market_data),
            "strategy_options": self._process_strategy_options(strategy_options)
        }
        
        # 보고서 생성
        final_report = self._create_sample_report(
            state["startup_info"], 
            state["target_countries"], 
            state["market_data"], 
            state["strategy_options"]
        )
        
        # 두 위치에 모두 보고서 저장
        md_path = self.output_dir / f"{report_filename}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(final_report)
            
        # reports 디렉토리에도 저장
        report_path = self.reports_dir / f"{report_filename}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(final_report)
            
        return str(md_path), True
        
    def _extract_target_countries(self, market_data):
        """시장 데이터에서 목표 국가 추출"""
        # 여기서는 기본값으로 몇 개의 국가를 설정
        # 실제로는 market_data에서 추출해야 함
        return ["인도네시아", "필리핀", "태국"]
        
    def _process_market_data(self, market_data):
        """시장 데이터 처리"""
        processed_data = {}
        
        # 기본 구조 설정
        for country in self._extract_target_countries(market_data):
            processed_data[country] = {
                "market_size": f"{country}의 디지털 시장은 연간 15-20% 성장 중",
                "regulations": f"{country}의 규제 환경은 비교적 우호적",
                "competition": f"{country}의 시장은 몇몇 주요 경쟁사가 있으나 혁신적 서비스 부족"
            }
        
        # market_data에 있는 정보로 보완
        if market_data and isinstance(market_data, dict):
            # 시장 트렌드 처리
            trends = market_data.get("market_trends", [])
            if trends and trends[0] != "데이터 생성 실패":
                for country in processed_data:
                    processed_data[country]["trends"] = trends
                    
            # 경쟁사 분석 처리
            competitors = market_data.get("competitor_analysis", {})
            if competitors and not ("경쟁사정보없음" in competitors and competitors["경쟁사정보없음"] == "생성실패"):
                for country in processed_data:
                    processed_data[country]["competitors"] = competitors
                    
            # 고객 세그먼트 처리
            segments = market_data.get("customer_segments", [])
            if segments and segments[0] != "데이터 생성 실패":
                for country in processed_data:
                    processed_data[country]["segments"] = segments
        
        return processed_data
        
    def _process_strategy_options(self, strategy_options):
        """전략 옵션 처리"""
        processed_options = {}
        
        # 국가별 기본 전략 설정
        for country in ["인도네시아", "필리핀", "태국"]:
            processed_options[country] = {
                "entry_strategy": f"{country} 맞춤형 진입 전략",
                "pros_cons": {
                    "pros": ["현지 시장 빠른 적응", "리스크 분산"],
                    "cons": ["초기 투자 필요", "현지 파트너 의존"]
                },
                "conditions": "현지 규제 환경에 따른 맞춤형 접근 필요",
                "partnership": "현지 주요 기업과의 전략적 제휴",
                "risks": ["규제 변화", "문화적 차이", "경쟁 심화"]
            }
            
        # 제공된 전략 옵션 정보로 보완
        if strategy_options and isinstance(strategy_options, dict):
            strategic_options = strategy_options.get("strategic_options", [])
            if strategic_options:
                # 여기서 전략 옵션을 처리하여 국가별 전략에 반영할 수 있음
                for option in strategic_options:
                    # 예시: 모든 국가에 동일한 전략 옵션 정보 추가
                    for country in processed_options:
                        name = option.get("option_name", "")
                        if "보수적" in name:
                            processed_options[country]["strategic_approach"] = "보수적"
                        elif "적극적" in name:
                            processed_options[country]["strategic_approach"] = "적극적"
                        elif "단계적" in name:
                            processed_options[country]["strategic_approach"] = "단계적"
        
        return processed_options
    
    def generate_final_report(self, state):
        """
        최종 보고서 생성 함수 (기존 코드 유지)
        """
        # 상태 데이터 가져오기
        startup_info = state.get("startup_info", {})
        target_countries = state.get("target_countries", [])
        market_data = state.get("market_data", {})
        strategy_options = state.get("strategy_options", {})
        
        # 프롬프트에 실제 데이터 삽입 준비
        report_prompt = self._prepare_prompt(
            startup_info, target_countries, market_data, strategy_options
        )
        
        # 여기서는 실제 데이터를 바탕으로 보고서 내용을 구성합니다
        # 실제 LLM 호출 대신 보고서 예시를 직접 생성
        final_report = self._create_sample_report(
            startup_info, target_countries, market_data, strategy_options
        )
        
        # 보고서를 파일로 저장 (output 디렉토리에도 저장)
        report_path = self.reports_dir / "final_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(final_report)
            
        # output 디렉토리에도 저장
        output_path = self.output_dir / "final_report.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_report)
        
        # 상태 업데이트
        state["final_report"] = final_report
        
        return state
    
    def _prepare_prompt(self, startup_info, target_countries, market_data, strategy_options):
        """프롬프트 준비 함수"""
        # 실제 데이터로 프롬프트 구성
        prompt = self.report_prompt_template
        # 필요한 경우 프롬프트에 변수 삽입
        return prompt
    
    def _create_sample_report(self, startup_info, target_countries, market_data, strategy_options):
        """샘플 보고서 생성 함수"""
        
        # 기업명 설정 (기본값 또는 상태에서 가져옴)
        company_name = startup_info.get("name", "헬스테크")
        business_model = startup_info.get("business_model", "프리미엄 구독 모델")
        
        # 제품명은 core_products에서 가져옴
        core_products = startup_info.get("core_products", [{"name": "헬스메이트 프로", "description": "AI 기반 건강 관리 애플리케이션"}])
        products = core_products[0].get("name", "헬스메이트 프로") if core_products else "헬스메이트 프로"
        
        # 국가 목록 (기본값 또는 상태에서 가져옴)
        countries = target_countries or ["인도네시아", "필리핀", "태국"]
        
        # 보고서 시작 부분
        report = f"""# 다국적 시장 진출 전략 보고서: {company_name}

## SUMMARY

1. {company_name}의 해외 진출에 있어 가장 유망한 국가는 {', '.join(countries)}입니다.
2. 진출 시 핵심적인 기회 요소는 시장 성장 잠재력과 혁신적인 제품/서비스에 대한 수요 증가입니다.
3. 권장되는 진입 전략 개요는 각 국가별 특성에 맞는 파트너십 기반 접근법과 단계적 시장 침투 전략입니다.
4. 성공을 위한 가장 중요한 조건은 철저한 현지 시장 조사, 강력한 현지 파트너십 구축, 지속적인 제품/서비스 현지화 노력입니다.
5. 예상되는 타임라인 개요는 시장 조사 및 준비(3-6개월), 초기 시장 진입 및 검증(6-12개월), 본격 확장(12개월 이후)의 단계적 접근입니다.

## 스타트업 개요

- **핵심 제품/서비스 및 차별점**: {products}
  - AI 기술을 활용한 개인 맞춤형 건강 관리 솔루션 제공
  - 사용자 데이터 기반 맞춤형 건강 조언 및 모니터링 기능
  - 웨어러블 기기와의 통합 및 실시간 건강 데이터 분석
  - 다양한 언어 지원 및 문화적 요소를 고려한 인터페이스

- **해외 진출 목표**: {business_model}
  - 동남아시아 주요 시장에서의 사용자 기반 확보
  - 2년 내 목표 국가에서 월간 활성 사용자 100만 명 달성
  - 현지 의료 서비스 제공자 및 보험사와의 파트너십 구축
  - 장기적으로 아시아 태평양 지역 건강관리 플랫폼 시장의 선도적 위치 확보

## 국가별 시장 분석
"""

        # 각 국가별 섹션 추가
        for country in countries:
            # 각 국가별 분석 데이터 (실제로는 market_data에서 가져옴)
            country_data = market_data.get(country, {})
            market_size = country_data.get("market_size", "연간 20% 성장하는 10억 달러 규모")
            regulations = country_data.get("regulations", "의료 데이터 관련 규제가 있으나 점차 완화되는 추세")
            competition = country_data.get("competition", "현지 기업과 일부 글로벌 기업의 경쟁이 존재하나 혁신적 서비스는 부족")
            
            report += f"""
### {country}

- **시장 규모 및 성장 가능성**: {market_size}
  - 디지털 헬스케어 시장이 빠르게 성장하는 추세
  - 중산층 증가에 따른 건강 관리 서비스 수요 상승
  - 스마트폰 보급률이 높아 디지털 서비스 접근성 우수

- **주요 규제 및 진입 장벽**: {regulations}
  - 의료 데이터 처리에 관한 현지 규제 준수 필요
  - 외국 기업 진출에 대한 일부 제한적 규제 존재
  - 현지 파트너십을 통한 규제 대응이 권장됨

- **경쟁 현황**: {competition}
  - 주요 경쟁사: 현지 헬스케어 앱 2-3개, 글로벌 기업 1-2개
  - 경쟁사들은 기본적인 건강 모니터링에 집중, AI 기반 맞춤형 서비스는 부족
  - 사용자 리뷰 분석 결과, 현지화된 콘텐츠와 정확한 건강 조언에 대한 니즈가 높음
"""

        # 진출 전략 섹션 추가
        report += "\n## 진출 전략\n"
        
        for country in countries:
            # 각 국가별 전략 데이터 (실제로는 strategy_options에서 가져옴)
            country_strategy = strategy_options.get(country, {})
            entry_strategy = country_strategy.get("entry_strategy", "현지 파트너십 모델")
            pros_cons = country_strategy.get("pros_cons", {"pros": ["빠른 시장 진입", "현지 전문성 활용"], "cons": ["이익 분배", "운영 통제력 제한"]})
            conditions = country_strategy.get("conditions", "엄격한 의료 데이터 규제 환경에서는 현지 의료기관과의 제휴가 효과적")
            partnership = country_strategy.get("partnership", "현지 주요 병원 체인 또는 통신사와의 전략적 제휴")
            risks = country_strategy.get("risks", ["규제 변화", "파트너십 갈등", "데이터 보안 이슈"])
            
            # pros_cons 딕셔너리에서 장점과 단점 추출
            pros = pros_cons.get("pros", []) if isinstance(pros_cons, dict) else []
            cons = pros_cons.get("cons", []) if isinstance(pros_cons, dict) else []
            
            report += f"""
### {country}

- **권장 진입 방식**: {entry_strategy}
  - **장점**: {', '.join(pros)}
  - **단점**: {', '.join(cons)}
  - **적합 조건**: {conditions}

- **파트너십 접근법**: 
  - {partnership}
  - 현지 의료 전문가 네트워크 구축으로 콘텐츠 신뢰성 향상
  - 주요 보험사와의 협력을 통한 사용자 혜택 제공

- **리스크 요소 및 대응 방안**:
  - **{risks[0] if len(risks) > 0 else '규제 변화'}**: 법률 전문가 고용 및 정기적인 규제 모니터링
  - **{risks[1] if len(risks) > 1 else '파트너십 갈등'}**: 명확한 계약 조건 및 정기적인 커뮤니케이션 체계 구축
  - **{risks[2] if len(risks) > 2 else '데이터 보안 이슈'}**: 현지 규정을 준수하는 강력한 데이터 보안 시스템 구축
"""

        # 실행 계획 섹션 추가
        report += """
## 실행 계획

- **단계별 접근법**
  1. **1단계: 3-6개월 - 시장 조사 및 준비**
     * 목표: 현지 시장에 대한 심층 이해 및 파트너십 구축 준비
     * 주요 활동: 현지 사용자 조사, 규제 분석, 파트너 후보 접촉, 제품 현지화 준비
     * **의사결정 포인트**: 규제 환경 및 시장 상황에 따른 우선순위 국가 선정
       - 규제 환경이 우호적인 국가 → 직접 진출 모델 고려
       - 규제 장벽이 높은 국가 → 현지 파트너십 모델 우선 적용

  2. **2단계: 6-12개월 - 초기 시장 진입 및 검증**
     * 목표: 1-2개 우선순위 국가에서 MVP 출시 및 사용자 피드백 수집
     * 주요 활동: 현지화된 앱 출시, 소규모 마케팅 캠페인, 베타 테스터 그룹 운영
     * **의사결정 포인트**: 초기 성과에 따른 전략 조정
       - 사용자 획득 비용 낮고 리텐션 높음 → 마케팅 투자 확대
       - 예상보다 낮은 성과 → 제품 기능 및 현지화 전략 재검토

  3. **3단계: 12개월 이후 - 본격 확장**
     * 목표: 검증된 시장에서의 사용자 기반 확대 및 추가 국가로의 확장
     * 주요 활동: 마케팅 투자 확대, 추가 기능 개발, 현지 팀 구축, 수익화 모델 강화
     * **의사결정 포인트**: 장기적인 확장 방향
       - 특정 국가에서 강한 성장세 → 해당 국가 집중 투자
       - 전반적으로 고른 성장 → 균형적인 리소스 배분

- **주요 고려사항**:
  - 각 국가별 문화적 특성을 반영한 제품 현지화 전략
  - 데이터 보안 및 개인정보 보호 관련 현지 규제 준수
  - 현지 의료 시스템 및 관행에 맞는 서비스 조정
  - 지속 가능한 수익 모델 구축 및 검증

## KPI 및 성과 측정
- 국가별 사용자 획득 비용(CAC)
- 월간 활성 사용자 수(MAU)
- 사용자 유지율(Retention Rate)
- 앱 평점 및 사용자 피드백 점수
- 매출 및 수익성 지표
- 시장 점유율 변화
"""

        return report