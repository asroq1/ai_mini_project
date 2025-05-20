#!/usr/bin/env python3
# report_agent.py - 최종 보고서를 생성하는 스크립트

import json
import os
from utils.generator import generate_dynamic_startup_info, generate_dynamic_target_countries, generate_dynamic_market_data

def load_data():
    """데이터 파일을 로드하거나 동적으로 생성합니다."""
    try:
        # 먼저 data 폴더의 파일을 로드 시도
        with open('data/sample_data.json', 'r', encoding='utf-8') as f:
            print("data/sample_data.json에서 데이터를 로드합니다.")
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        try:
            # 루트의 파일을 로드 시도
            with open('sample_data.json', 'r', encoding='utf-8') as f:
                print("sample_data.json에서 데이터를 로드합니다.")
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 둘 다 실패하면 동적 데이터 생성
            print("데이터 파일을 찾을 수 없어 동적으로 데이터를 생성합니다.")
            startup_info = generate_dynamic_startup_info()
            target_countries = generate_dynamic_target_countries()
            market_data = generate_dynamic_market_data(target_countries)
            
            return {
                "startup_info": startup_info,
                "target_countries": target_countries,
                "market_data": market_data
            }

def generate_report(data):
    """데이터를 기반으로 Markdown 형식의 보고서를 생성합니다."""
    startup = data.get("startup_info", {})
    countries = data.get("target_countries", [])
    market_data = data.get("market_data", {})
    
    # 시작 부분
    report = f"""# {startup.get('name', '회사명')} 해외 진출 전략 보고서

## 1. 회사 개요

- **회사명**: {startup.get('name', '회사명')}
- **산업**: {startup.get('industry', '산업 정보 없음')}
- **설립년도**: {startup.get('founded_year', '정보 없음')}
- **사업 설명**: {startup.get('description', '사업 설명 없음')}

### 1.1 핵심 제품/서비스
"""

    # 핵심 제품
    core_products = startup.get('core_products', [])
    if core_products:
        for product in core_products:
            report += f"- **{product.get('name', '제품명')}**: {product.get('description', '설명 없음')}\n"
    else:
        report += "- 핵심 제품 정보 없음\n"
    
    # USP
    report += "\n### 1.2 핵심 경쟁력(USP)\n"
    usps = startup.get('unique_selling_points', [])
    if usps:
        for usp in usps:
            report += f"- {usp}\n"
    else:
        report += "- 핵심 경쟁력 정보 없음\n"
    
    # 타겟 고객
    report += "\n### 1.3 타겟 고객\n"
    customers = startup.get('target_customers', [])
    if customers:
        for customer in customers:
            report += f"- {customer}\n"
    else:
        report += "- 타겟 고객 정보 없음\n"
    
    # 현재 시장
    report += "\n### 1.4 현재 진출 시장\n"
    markets = startup.get('current_markets', [])
    if markets:
        for market in markets:
            report += f"- {market}\n"
    else:
        report += "- 현재 진출 시장 정보 없음\n"
    
    # 비즈니스 모델
    report += f"\n### 1.5 비즈니스 모델\n- {startup.get('business_model', '비즈니스 모델 정보 없음')}\n"
    
    # 펀딩 정보
    funding = startup.get('funding', {})
    report += f"\n### 1.6 펀딩 정보\n- **총 조달액**: {funding.get('total_raised', '정보 없음')}\n- **최근 라운드**: {funding.get('latest_round', '정보 없음')}\n"
    
    # 2. 타겟 국가
    report += "\n## 2. 해외 진출 타겟 국가\n"
    
    if countries:
        for i, country in enumerate(countries, 1):
            report += f"\n### 2.{i} {country.get('name', '국가명')}\n"
            report += f"- **선정 이유**: {country.get('reason', '정보 없음')}\n"
            
            # 해당 국가의 시장 데이터
            country_data = market_data.get(country.get('name', ''), {})
            if country_data:
                report += f"\n#### 시장 규모 및 성장률\n"
                report += f"- **시장 규모**: {country_data.get('market_size', '정보 없음')}\n"
                report += f"- **성장률**: {country_data.get('growth_rate', '정보 없음')}\n"
                
                # 규제
                regulations = country_data.get('regulations', [])
                if regulations:
                    report += "\n#### 주요 규제 및 정책\n"
                    for reg in regulations:
                        report += f"- **{reg.get('name', '규제명')}**: {reg.get('description', '설명 없음')}\n"
                
                # 경쟁사
                competitors = country_data.get('competitors', [])
                if competitors:
                    report += "\n#### 주요 경쟁사 분석\n"
                    for comp in competitors:
                        report += f"- **{comp.get('name', '경쟁사')}**\n"
                        report += f"  - 시장 점유율: {comp.get('market_share', '정보 없음')}\n"
                        report += "  - 강점: " + ", ".join(comp.get('strengths', ['정보 없음'])) + "\n"
                
                # 소비자 트렌드
                trends = country_data.get('consumer_trends', [])
                if trends:
                    report += "\n#### 소비자 트렌드\n"
                    for trend in trends:
                        report += f"- {trend}\n"
    else:
        report += "- 타겟 국가 정보 없음\n"
    
    # 3. 진출 전략 (예시)
    report += "\n## 3. 해외 진출 전략\n"
    report += "\n### 3.1 시장 진입 전략\n"
    report += "- 현지 파트너십 구축을 통한 네트워크 확보\n"
    report += "- 타겟 고객군 대상 파일럿 프로젝트 진행\n"
    report += "- 단계별 확장 전략 수립 (1차년도: 시장 테스트, 2차년도: 영업 확대, 3차년도: 현지 법인 설립)\n"
    
    report += "\n### 3.2 마케팅 전략\n"
    report += "- 현지 산업 전시회 및 컨퍼런스 참가\n"
    report += "- 특화된 고객 세그먼트 대상 디지털 마케팅 캠페인\n"
    report += "- 성공 사례 구축 및 레퍼런스 마케팅\n"
    
    report += "\n### 3.3 현지화 전략\n"
    report += "- 현지 규제 및 표준 준수를 위한 제품/서비스 조정\n"
    report += "- 현지 언어 및 문화를 고려한 UI/UX 개선\n"
    report += "- 현지 비즈니스 관행에 맞춘 영업 프로세스 구축\n"
    
    # 4. 리스크 및 대응 방안 (예시)
    report += "\n## 4. 리스크 및 대응 방안\n"
    
    report += "\n### 4.1 시장 리스크\n"
    report += "- **리스크**: 경쟁 심화로 인한 시장 진입 장벽\n"
    report += "- **대응 방안**: 틈새 시장 타겟팅 및 차별화 전략 강화\n"
    
    report += "\n### 4.2 규제 리스크\n"
    report += "- **리스크**: 데이터 보호 및 개인정보 관련 규제 강화\n"
    report += "- **대응 방안**: 현지 법률 전문가 자문 및 관련 인증 획득\n"
    
    report += "\n### 4.3 운영 리스크\n"
    report += "- **리스크**: 원격 운영으로 인한 관리 효율성 저하\n"
    report += "- **대응 방안**: 현지 핵심 인력 확보 및 효과적인 커뮤니케이션 체계 구축\n"
    
    # 5. 결론
    report += "\n## 5. 결론 및 향후 계획\n"
    report += "\n본 보고서는 데이터 기반 분석을 통해 도출된 타겟 국가 진출 전략을 제시하였습니다. "
    report += f"{startup.get('name', '회사')}의 핵심 경쟁력을 활용하여 효과적으로 해외 시장에 진입하기 위해서는 "
    report += "현지화 전략과 시장별 특성에 맞는 접근이 필요합니다.\n\n"
    report += "향후 분기별 진행 상황을 모니터링하며 전략을 적절히 조정해나갈 예정입니다.\n"
    
    # 보고서 끝
    report += "\n---\n"
    report += "© 2024 글로벌 진출 전략 보고서. 모든 권리 보유."
    
    return report

def save_report(report_content):
    """생성된 보고서를 파일로 저장합니다."""
    try:
        with open('final_report.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
            print("final_report.md 파일이 성공적으로 생성되었습니다.")
        return True
    except Exception as e:
        print(f"보고서 저장 중 오류 발생: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("해외 진출 전략 보고서 생성을 시작합니다...")
    data = load_data()
    report_content = generate_report(data)
    save_result = save_report(report_content)
    
    if save_result:
        print("보고서 생성이 완료되었습니다. final_report.md 파일을 확인하세요.")
    else:
        print("보고서 생성에 실패했습니다.")

if __name__ == "__main__":
    main() 