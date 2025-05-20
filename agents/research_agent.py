import json
from utils.generator import generate_dynamic_market_data # Import the generator function

class ResearchAgent:
    def __init__(self, data_path="data/state.json"):
        self.data_path = data_path
        # 실제 구현에서는 state.json의 특정 부분을 사용하거나 외부 API 호출 등을 통해 데이터를 수집합니다.
        # 여기서는 state.json의 일부를 모방한 더미 데이터를 사용합니다.

    def run(self, target_countries=None): # Add target_countries parameter
        """
        시장 조사 데이터를 분석하고 결과를 반환합니다.
        실제 애플리케이션에서는 이 부분에 복잡한 데이터 수집 및 분석 로직이 들어갑니다.
        """
        print("ResearchAgent: 시장 조사 데이터 분석 중...")
        market_data_from_state = None
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                # Try to get market_data directly if it exists and is structured as expected
                if "market_data" in state_data and isinstance(state_data["market_data"], dict):
                    market_data_from_state = state_data["market_data"]
                # Fallback to older structure if market_data is not directly available
                elif "market_analysis" in state_data:
                     market_data_from_state = {
                        "market_trends": state_data.get("market_analysis", {}).get("trends", []),
                        "competitor_analysis": state_data.get("market_analysis", {}).get("competitors", {}),
                        "customer_segments": state_data.get("market_analysis", {}).get("customer_segments", [])
                    }
        except FileNotFoundError:
            print(f"Warning: {self.data_path} not found. Will attempt to generate market data.")
        except json.JSONDecodeError:
            print(f"Warning: Error decoding JSON from {self.data_path}. Will attempt to generate market data.")

        # Check if data from state is sufficient or if we need to generate it
        # A simple check: if trends are empty or contain "데이터 생성 실패"
        should_generate_data = True
        if market_data_from_state and market_data_from_state.get("market_trends") and "데이터 생성 실패" not in market_data_from_state.get("market_trends", []):
            should_generate_data = False
            market_data = market_data_from_state
            print("ResearchAgent: Using market data from state.json")
        
        if should_generate_data:
            print("ResearchAgent: Generating dynamic market data.")
            if target_countries:
                # Generate data for specific countries
                generated_data = {}
                for country in target_countries:
                    country_data = generate_dynamic_market_data(country)
                    # Structure it similarly to how ReportAgent expects for multiple countries
                    generated_data[country] = {
                        "market_size_growth": country_data.get("market_size_growth"),
                        "regulations_barriers": country_data.get("regulations_barriers"),
                        "competition_status": country_data.get("competition_status")
                    }
                # For the overall market_data structure expected by StrategyAgent,
                # we might need to aggregate or select representative data.
                # For now, let's try to create a compatible structure.
                # This part might need refinement based on how StrategyAgent consumes this.
                if generated_data:
                    # Example: take trends from the first country, aggregate competitors etc.
                    # This is a placeholder for a more sophisticated aggregation.
                    first_country_name = target_countries[0]
                    first_country_data = generated_data[first_country_name]
                    
                    market_data = {
                        "market_trends": [f"{first_country_name} 시장: {first_country_data.get('market_size_growth', 'N/A')}"],
                        "competitor_analysis": {
                            f"{country} 경쟁사": first_country_data.get('competition_status', 'N/A') for country, first_country_data in generated_data.items()
                        },
                        "customer_segments": [f"{first_country_name} 고객 특성: (상세 분석 필요)"], # Placeholder
                        "country_specific_data": generated_data # Keep detailed per-country data
                    }
                else: # Fallback if no target countries or data generation failed
                    market_data = {
                        "market_trends": ["동적 데이터 생성 실패 - 트렌드"],
                        "competitor_analysis": {"경쟁사정보없음": "동적 생성 실패"},
                        "customer_segments": ["동적 데이터 생성 실패 - 고객군"]
                    }
            else: # Fallback if no target_countries provided
                print("ResearchAgent: No target countries provided for dynamic data generation. Using default fallback.")
                market_data = {
                    "market_trends": ["타겟 국가 정보 없음 - 트렌드"],
                    "competitor_analysis": {"경쟁사정보없음": "타겟 국가 정보 없음"},
                    "customer_segments": ["타겟 국가 정보 없음 - 고객군"]
                }
            print("ResearchAgent: Dynamic market data generated.")
        
        print("ResearchAgent: 시장 조사 완료.")
        return market_data

if __name__ == '__main__':
    # 테스트를 위해 ResearchAgent 실행 예시
    # 실제 실행은 main.py에서 이루어집니다.
    # 테스트를 위해서는 data/state.json 파일이 필요합니다.
    # state.json 파일이 없다면 빈 파일을 생성하거나, 아래 코드를 주석처리하고 테스트하세요.
    # if not os.path.exists("data"):
    #     os.makedirs("data")
    # if not os.path.exists("data/state.json"):
    #     with open("data/state.json", "w", encoding='utf-8') as f:
    #         json.dump({
    #             "market_analysis": {
    #                 "trends": ["AI 기반 솔루션 수요 증가", "클라우드 기술 보편화"],
    #                 "competitors": {"CompetitorA": "시장 선두 주자", "CompetitorB": "빠르게 성장 중"},
    #                 "customer_segments": ["대기업", "중소기업", "스타트업"]
    #             }
    #         }, f, ensure_ascii=False, indent=4)

    agent = ResearchAgent()
    # data = agent.run() # Old way
    # Simulate main.py behavior for testing
    try:
        with open(agent.data_path, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        current_state = {}
    
    target_countries_from_state = current_state.get("target_countries", ["인도네시아", "필리핀", "태국"]) # Default if not in state
    data = agent.run(target_countries=target_countries_from_state)

    print("\\nResearchAgent 결과:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
