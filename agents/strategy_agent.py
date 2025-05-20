import json

class StrategyAgent:
    def __init__(self):
        # 실제 구현에서는 전략 수립에 필요한 설정이나 모델 등을 초기화합니다.
        pass

    def run(self, market_data):
        """
        시장 조사 데이터를 기반으로 전략적 옵션과 권장 사항을 생성합니다.
        실제 애플리케이션에서는 이 부분에 복잡한 전략 수립 로직이 들어갑니다.
        """
        print("StrategyAgent: 전략 수립 중...")
        if not market_data:
            print("Warning: market_data가 비어있어 기본 전략을 사용합니다.")
            return {
                "strategic_options": [
                    {"option_name": "일반 시장 확대 전략", "description": "기존 제품으로 새로운 고객층 확보", "pros": ["낮은 초기 투자 비용"], "cons": ["경쟁 심화 가능성"]}
                ],
                "recommendations": ["시장 조사를 통해 구체적인 타겟 고객층 설정 필요"],
                "action_plan": {
                    "1단계": "경쟁사 분석 및 시장 동향 파악 (재실행 권장)",
                    "2단계": "타겟 고객층 정의 및 마케팅 전략 수립"
                }
            }

        # market_data를 활용한 전략 생성 (예시 로직)
        options = []
        if market_data.get("market_trends") and "시장 성장 중" in market_data["market_trends"]:
            options.append({
                "option_name": "적극적 시장 확장 전략",
                "description": "성장하는 시장의 기회를 활용하여 시장 점유율 확대",
                "pros": ["높은 성장 잠재력", "선점 효과 기대"],
                "cons": ["높은 경쟁 강도", "초기 투자 비용 발생"]
            })
        else:
            options.append({
                "option_name": "보수적 시장 유지 전략",
                "description": "현재 시장 지위를 유지하며 안정적인 수익 확보",
                "pros": ["낮은 위험", "안정적 운영 가능"],
                "cons": ["성장 기회 제한적", "경쟁 환경 변화에 취약"]
            })

        if market_data.get("customer_segments") and "가격 민감형" in market_data["customer_segments"]:
            options.append({
                "option_name": "가격 경쟁력 강화 전략",
                "description": "가격 민감형 고객을 타겟으로 한 가격 정책 수립",
                "pros": ["넓은 고객층 확보 가능", "단기적 매출 증대 효과"],
                "cons": ["수익성 악화 우려", "브랜드 이미지 저하 가능성"]
            })

        recommendations = ["상기 전략 옵션들을 종합적으로 검토하여 최적의 방향 결정 필요"]
        if not options:
             recommendations.append("시장 데이터 분석을 통한 추가 전략 도출 필요")

        action_plan = {
            "1단계": "선택된 전략에 대한 세부 실행 계획 수립",
            "2단계": "필요 자원 확보 및 팀 구성",
            "3단계": "실행 및 성과 모니터링"
        }

        strategy_output = {
            "strategic_options": options,
            "recommendations": recommendations,
            "action_plan": action_plan
        }
        print("StrategyAgent: 전략 수립 완료.")
        return strategy_output

if __name__ == '__main__':
    # 테스트를 위해 StrategyAgent 실행 예시
    # 실제 실행은 main.py에서 이루어집니다.
    dummy_market_data = {
        "market_trends": ["시장 성장 중", "AI 기술 도입 확산"],
        "competitor_analysis": {"CompetitorA": "점유율 50%", "CompetitorB": "신기술 도입에 적극적"},
        "customer_segments": ["가격 민감형", "혁신 추구형"]
    }
    agent = StrategyAgent()
    strategy = agent.run(dummy_market_data)
    print("\nStrategyAgent 결과:")
    print(json.dumps(strategy, indent=4, ensure_ascii=False))

    print("\n--- 빈 시장 데이터로 실행 시 --- ")
    empty_data_strategy = agent.run({})
    print(json.dumps(empty_data_strategy, indent=4, ensure_ascii=False))
