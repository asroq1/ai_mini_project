# main.py
import json
import os
import argparse

# --- utils.generator 임포트 시도 및 로깅 강화 ---
GENERATOR_MODULE_PATH_FOR_LOGGING = os.path.abspath(os.path.join("utils", "generator.py"))
GENERATOR_AVAILABLE = False
generate_dynamic_startup_info = None
generate_dynamic_target_countries = None
generate_dynamic_market_data = None

print(f"정보: utils.generator 모듈 임포트 시도 중... (예상 경로: {GENERATOR_MODULE_PATH_FOR_LOGGING})")
if os.path.exists(os.path.join("utils", "generator.py")):
    try:
        # Python의 모듈 검색 경로에 utils가 포함되도록 임시 조치 (더 근본적인 해결책은 PYTHONPATH 설정 또는 패키지 구조화)
        # import sys
        # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))) # 현재 파일 기준
        
        from utils.generator import generate_dynamic_startup_info as gd_startup
        from utils.generator import generate_dynamic_target_countries as gd_countries
        from utils.generator import generate_dynamic_market_data as gd_market_data
        
        generate_dynamic_startup_info = gd_startup
        generate_dynamic_target_countries = gd_countries
        generate_dynamic_market_data = gd_market_data
        
        GENERATOR_AVAILABLE = True
        print(f"성공: {GENERATOR_MODULE_PATH_FOR_LOGGING} 에서 실제 데이터 생성 함수들을 성공적으로 가져왔습니다.")
    except ImportError as e:
        print(f"오류!: {GENERATOR_MODULE_PATH_FOR_LOGGING} 파일은 찾았으나, 내부 함수 임포트 중 오류 발생: {e}")
        print(f"       (상세: {type(e).__name__} - {e})")
        print(f"       utils/generator.py 파일 내에 generate_dynamic_startup_info, generate_dynamic_target_countries, generate_dynamic_market_data 함수가 정확히 정의되어 있는지,")
        print(f"       그리고 해당 파일에 문법 오류가 없는지, `import random`이 포함되어 있는지 확인하세요.")
    except Exception as e:
        print(f"오류!: {GENERATOR_MODULE_PATH_FOR_LOGGING} 처리 중 예기치 않은 오류 발생: {e}")
        print(f"       (상세: {type(e).__name__} - {e})")
else:
    print(f"경고!: {GENERATOR_MODULE_PATH_FOR_LOGGING} 파일을 찾을 수 없습니다. 동적 데이터 생성 기능이 비활성화됩니다.")

# GENERATOR_AVAILABLE이 False일 경우를 대비한 비상용 함수 정의
if not GENERATOR_AVAILABLE:
    print("경고: 실제 데이터 생성 함수를 사용할 수 없으므로, 비상용(fallback) 함수를 정의합니다.")
    def generate_dynamic_startup_info_fallback(): 
        print("DEBUG: 호출됨 - generate_dynamic_startup_info_fallback (비상용)")
        return {"name": "[자동생성실패] 스타트업", "industry": "미정", "core_products": [{"name": "[자동생성실패] 제품"}], "target_customers": ["일반 고객 (비상용)"]}
    def generate_dynamic_target_countries_fallback(): 
        print("DEBUG: 호출됨 - generate_dynamic_target_countries_fallback (비상용)")
        return [{"name": "글로벌 (비상용 생성실패)"}]
    def generate_dynamic_market_data_fallback(countries):
        print("DEBUG: 호출됨 - generate_dynamic_market_data_fallback (비상용)")
        return {}
    
    # 실제 사용할 함수를 비상용 함수로 지정
    generate_dynamic_startup_info = generate_dynamic_startup_info_fallback
    generate_dynamic_target_countries = generate_dynamic_target_countries_fallback
    generate_dynamic_market_data = generate_dynamic_market_data_fallback

# --- 나머지 코드 ---
from agents.research_agent import ResearchAgent
from agents.strategy_agent import StrategyAgent
from agents.report_agent import ReportAgent
from utils.md_to_pdf import convert_md_to_pdf # PDF 변환 함수 임포트

DATA_DIR = "data"
STATE_FILENAME = "state.json"
STATE_FILE_PATH = os.path.join(DATA_DIR, STATE_FILENAME)

def ensure_data_directory_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"정보: {DATA_DIR} 디렉토리를 생성했습니다.")

def save_generated_state(data, file_path):
    ensure_data_directory_exists()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"정보: State 데이터를 {file_path}에 성공적으로 저장했습니다.")
    except Exception as e:
        print(f"오류!: State 데이터를 {file_path}에 저장 중 오류 발생: {e}")

def create_state_from_generator(state_file_to_save):
    print(f"\n정보: {state_file_to_save}에 저장할 동적 데이터 생성을 시작합니다...")
    if not GENERATOR_AVAILABLE:
        print("경고: (create_state_from_generator 내 확인) 실제 데이터 생성 함수를 사용할 수 없어 비상용 데이터를 사용합니다.")
    
    print("DEBUG: generate_dynamic_startup_info 함수 호출 시도...")
    startup_info = generate_dynamic_startup_info()
    print(f"  DEBUG: 생성된 startup_info: {json.dumps(startup_info, ensure_ascii=False, indent=2)}")
    
    print("DEBUG: generate_dynamic_target_countries 함수 호출 시도...")
    target_countries_info = generate_dynamic_target_countries()
    print(f"  DEBUG: 생성된 target_countries_info: {json.dumps(target_countries_info, ensure_ascii=False, indent=2)}")
     
    print("DEBUG: generate_dynamic_market_data 함수 호출 시도...")
    market_data_by_country = generate_dynamic_market_data(target_countries_info) # 인자로 target_countries_info 전달
    print(f"  DEBUG: 생성된 market_data_by_country: {json.dumps(market_data_by_country, ensure_ascii=False, indent=2)}")

    # 데이터 통합 로직 시작
    print("DEBUG: market_analysis 데이터 통합 시작...")
    all_trends = []
    all_competitors = {}
    all_customer_segments = startup_info.get("target_customers", []) # 기본값 사용
    if not isinstance(all_customer_segments, list): # 항상 리스트 형태가 되도록 보장
        all_customer_segments = [str(all_customer_segments)] if all_customer_segments else []

    if isinstance(market_data_by_country, dict):
        for country_name, country_data in market_data_by_country.items():
            print(f"  DEBUG: '{country_name}' 국가 데이터 처리 중...")
            if isinstance(country_data, dict):
                # 트렌드 통합
                country_trends = country_data.get("consumer_trends", [])
                if isinstance(country_trends, list):
                    all_trends.extend(country_trends)
                    print(f"    DEBUG: '{country_name}' 트렌드 추가: {country_trends}")
                else:
                    print(f"    경고: '{country_name}'의 consumer_trends가 리스트가 아닙니다: {country_trends}")

                # 경쟁사 통합
                country_competitors = country_data.get("competitors", [])
                if isinstance(country_competitors, list):
                    for comp in country_competitors:
                        if isinstance(comp, dict):
                            comp_name = comp.get("name", f"UnknownCompetitor_{country_name}")
                            strengths = ", ".join(comp.get("strengths", ["강점 정보 없음"]))
                            all_competitors[comp_name] = strengths
                            print(f"    DEBUG: '{country_name}' 경쟁사 추가: {comp_name} - {strengths}")
                        else:
                            print(f"    경고: '{country_name}'의 경쟁사 항목이 딕셔너리가 아닙니다: {comp}")
                else:
                    print(f"    경고: '{country_name}'의 competitors가 리스트가 아닙니다: {country_competitors}")
            else:
                print(f"  경고!: market_data_by_country의 '{country_name}' 항목이 딕셔너리가 아닙니다: {country_data}")
    else:
        print(f"경고!: market_data_by_country가 딕셔너리가 아닙니다 (그래서 통합 불가): {market_data_by_country}")
            
    all_trends = list(set(all_trends)) # 중복 제거
    if not all_trends: all_trends = ["(시장 트렌드 정보가 생성되지 않았거나 비어있습니다)"]
    if not all_competitors: all_competitors = {"(경쟁사 정보 없음)": "(데이터가 생성되지 않았거나 비어있습니다)"}
    if not all_customer_segments: all_customer_segments = ["(고객 세그먼트 정보가 생성되지 않았거나 비어있습니다)"]

    market_analysis_for_state = {
        "trends": all_trends,
        "competitors": all_competitors,
        "customer_segments": all_customer_segments
    }
    print(f"  DEBUG: 최종 통합된 market_analysis: {json.dumps(market_analysis_for_state, ensure_ascii=False, indent=2)}")

    # 최종 state.json 구조
    state_data = {
        "company_info": startup_info,
        "target_countries_info": target_countries_info, 
        "market_analysis": market_analysis_for_state,
        "strategic_goals": { 
            "primary_goal": f"{startup_info.get('name', '[회사명 누락]')}의 글로벌 시장 점유율 확대 (동적 생성)",
            "secondary_goals": ["신규 고객 1000명 유치 (동적 생성)", "브랜드 인지도 20% 향상 (동적 생성)"]
        }
    }
    save_generated_state(state_data, state_file_to_save)
    print(f"정보: 동적 데이터 생성을 완료하고 {state_file_to_save}에 저장했습니다.")
    return state_data

def main():
    parser = argparse.ArgumentParser(description="Generate a multinational market entry strategy report.")
    parser.add_argument("--company_name", type=str, default=None, help="Name of the company. Overrides generated or state file data.")
    parser.add_argument("--product_name", type=str, default=None, help="Name of the product/service. Overrides generated or state file data.")
    parser.add_argument("--state_file", type=str, default=STATE_FILE_PATH, help=f"Path to the state JSON file. Defaults to {STATE_FILE_PATH}")
    parser.add_argument("--output_dir", type=str, default="output", help="Directory to save the report.")
    parser.add_argument("--report_filename", type=str, default="final_report", help="Base name for the output report files (without extension).")
    parser.add_argument("--force_generate_data", action="store_true", help="Force generation of new dynamic data, overwriting existing state file specified by --state_file.")

    args = parser.parse_args()
    
    ensure_data_directory_exists() # data 디렉토리 생성 확인

    current_company_name = "[회사명 기본값]"
    current_product_name = "[제품명 기본값]"
    loaded_state_company_info = {} # state 파일에서 로드된 company_info 저장용
    
    effective_state_file_path = args.state_file

    if args.force_generate_data or not os.path.exists(effective_state_file_path):
        if args.force_generate_data:
            print(f"정보: --force_generate_data 설정으로 {effective_state_file_path}에 새로운 state 데이터를 생성합니다...")
        else:
            print(f"정보: State 파일 {effective_state_file_path}을(를) 찾을 수 없어 새로 생성합니다...")
        
        generated_state = create_state_from_generator(effective_state_file_path)
        loaded_state_company_info = generated_state.get("company_info", {})
    else:
        print(f"정보: 기존 State 파일 {effective_state_file_path}을(를) 사용합니다.")
        try:
            with open(effective_state_file_path, 'r', encoding='utf-8') as f:
                loaded_state = json.load(f)
            loaded_state_company_info = loaded_state.get("company_info", {})
        except Exception as e:
            print(f"오류!: {effective_state_file_path} 로드 중 오류 발생: {e}. 파일 내용을 확인하거나 --force_generate_data 옵션을 사용하세요.")
            print("오류로 인해 비상용 최소 데이터로 보고서 생성을 시도합니다.")
            # 비상용 데이터로 ReportAgent에 전달할 값 설정
            loaded_state_company_info = {"name": "[State 로드 실패 회사]", "core_products": [{"name": "[State 로드 실패 제품]"}]}


    # 회사명 및 제품명 결정 (명령줄 인자 > state 파일 > 비상용 함수 기본값 > 최종 기본값)
    current_company_name = loaded_state_company_info.get("name")
    products = loaded_state_company_info.get("core_products", [])
    if products and isinstance(products, list) and len(products) > 0 and isinstance(products[0], dict):
        current_product_name = products[0].get("name")
    else:
        current_product_name = "[제품명 정보 없음]"

    final_company_name = args.company_name if args.company_name is not None else current_company_name
    final_product_name = args.product_name if args.product_name is not None else current_product_name
    
    # 회사명이나 제품명이 없는 경우 기본값 사용
    if not final_company_name or "[자동생성실패]" in str(final_company_name) or "[State 로드 실패 회사]" in str(final_company_name):
        final_company_name = "헬스테크"
    if not final_product_name or "[자동생성실패]" in str(final_product_name) or "[State 로드 실패 제품]" in str(final_product_name):
        final_product_name = "헬스메이트 프로"

    print(f"\n--- 에이전트 파이프라인 시작 (대상: '{final_company_name}' - '{final_product_name}') ---")

    print(f"\n[1/3] ResearchAgent 실행 (입력 state 파일: {effective_state_file_path})")
    research_agent = ResearchAgent(data_path=effective_state_file_path)
    market_data_from_research = research_agent.run()
    print(f"  DEBUG: ResearchAgent로부터 받은 market_data: {json.dumps(market_data_from_research, ensure_ascii=False, indent=2)}")

    print(f"\n[2/3] StrategyAgent 실행 (입력: ResearchAgent 결과)")
    strategy_agent = StrategyAgent()
    strategy_options = strategy_agent.run(market_data_from_research)
    print(f"  DEBUG: StrategyAgent로부터 받은 strategy_options: {json.dumps(strategy_options, ensure_ascii=False, indent=2)}")

    print(f"\n[3/3] ReportAgent 실행 (입력: ResearchAgent 및 StrategyAgent 결과)")
    report_agent = ReportAgent(output_dir=args.output_dir)
    md_file, md_success = report_agent.generate_markdown_report(
        market_data=market_data_from_research, 
        strategy_options=strategy_options,
        company_name=final_company_name,
        product_name=final_product_name,
        report_filename=args.report_filename
    )

    print("\n--- 에이전트 파이프라인 종료 ---\
")

    if md_success and md_file:
        print(f"성공: 최종 보고서 (Markdown)가 {os.path.abspath(md_file)}에 생성되었습니다.")
        # PDF 변환 시도
        print(f"정보: Markdown 보고서를 PDF로 변환 시도 중...")
        # convert_md_to_pdf 함수는 절대 경로를 기대하므로, md_file과 args.output_dir이 절대 경로인지 확인하거나 변환합니다.
        abs_md_file = os.path.abspath(md_file)
        abs_output_dir = os.path.abspath(args.output_dir)
        
        pdf_file, pdf_success = convert_md_to_pdf(abs_md_file, abs_output_dir)
        if pdf_success and pdf_file:
            print(f"성공: PDF 보고서가 {pdf_file}에 생성되었습니다.")
        else:
            print("실패: PDF 보고서 생성에 실패했습니다. Markdown 파일은 생성되었을 수 있습니다.")
            print("       'markdown-pdf'가 설치되어 있고 PATH에 잡혀있는지 확인하세요. (npm install -g markdown-pdf)")

        # print("보고서 내용 일부 미리보기 (처음 1000자):")
        # try:
        #     with open(md_file, 'r', encoding='utf-8') as f_report:
        #         print(f_report.read(1000) + "...") 
        # except Exception as e:
        #     print(f"오류: 보고서 미리보기 중 오류 발생: {e}")
    else:
        print("실패: 최종 보고서 (Markdown) 생성에 실패했습니다.")

if __name__ == "__main__":
    main()