# utils/generator.py
import random

def generate_dynamic_startup_info():
    startups = [
        {
            "name": "퓨처테크 솔루션즈",
            "industry": "AI 및 머신러닝",
            "founded_year": 2022,
            "description": "기업용 AI 기반 자동화 플랫폼 개발",
            "core_products": [
                {"name": "자동화 엔진 Alpha", "description": "반복 업무 자동화를 위한 AI 솔루션"}
            ],
            "unique_selling_points": [
                "최신 AI 알고리즘 적용",
                "높은 정확도와 빠른 처리 속도",
                "사용자 친화적 인터페이스"
            ],
            "target_customers": ["대기업", "중견기업의 IT 부서 및 운영팀"],
            "current_markets": ["대한민국"],
            "business_model": "SaaS 구독 (월별/연간)",
            "funding": {"total_raised": "$1.2M", "latest_round": "Seed"}
        },
        {
            "name": "그린에너지 이노베이션",
            "industry": "신재생에너지",
            "founded_year": 2021,
            "description": "차세대 태양광 패널 및 에너지 저장 시스템 개발",
            "core_products": [
                {"name": "썬빔 X", "description": "고효율 경량 태양광 패널"},
                {"name": "에너지스토어 Q", "description": "가정용 및 산업용 ESS"}
            ],
            "unique_selling_points": [
                "기존 대비 20% 높은 발전 효율",
                "친환경 소재 사용 및 긴 수명",
                "AI 기반 에너지 관리 시스템 연동"
            ],
            "target_customers": ["건물주", "에너지 기업", "지방 자치 단체"],
            "current_markets": ["대한민국", "호주"],
            "business_model": "제품 판매 및 설치, 유지보수 서비스",
            "funding": {"total_raised": "$3M", "latest_round": "Series A"}
        },
        {
            "name": "헬스테크",
            "industry": "디지털 헬스케어",
            "founded_year": 2021,
            "description": "AI 기반 개인 맞춤형 건강 관리 플랫폼 개발",
            "core_products": [
                {"name": "헬스메이트 프로", "description": "AI 기반 건강 관리 애플리케이션"}
            ],
            "unique_selling_points": [
                "개인화된 건강 조언 제공",
                "다양한 웨어러블 기기와의 호환성",
                "의료 전문가 감수 콘텐츠"
            ],
            "target_customers": ["건강에 관심 있는 20-45세 성인", "만성질환 관리가 필요한 40-65세"],
            "current_markets": ["대한민국"],
            "business_model": "프리미엄 구독 모델",
            "funding": {"total_raised": "$2.5M", "latest_round": "Seed"}
        }
    ]
    # 건강 관리 스타트업을 반환하도록 고정
    return startups[2]  # 헬스테크 반환

def generate_dynamic_target_countries():
    country_pool = [
        {"name": "인도네시아", "reason": "빠르게 성장하는 디지털 시장 및 높은 모바일 보급률"},
        {"name": "필리핀", "reason": "젊은 인구층과 증가하는 중산층, 영어 사용 인구 다수"},
        {"name": "태국", "reason": "성장하는 디지털 헬스케어 시장 및 정부의 디지털 전환 정책"},
        {"name": "베트남", "reason": "빠른 경제 성장과 기술 혁신에 개방적인 환경"},
        {"name": "말레이시아", "reason": "안정적인 비즈니스 환경과 정부의 디지털 이니셔티브"}
    ]
    # 인도네시아, 필리핀, 태국 3개 국가 고정 반환
    return [country_pool[0], country_pool[1], country_pool[2]]

def generate_dynamic_market_data(target_countries_info_list): # 입력 인자 이름 주의
    market_data_samples = {
        "미국": {
            "market_size": "약 1500억 달러 (AI 시장)",
            "growth_rate": "연 30% 이상",
            "regulations": [
                {"name": "데이터 프라이버시 규정 (CCPA 등)", "description": "엄격한 개인정보보호 규정 준수 필요"},
                {"name": "AI 윤리 가이드라인", "description": "연방 및 주 정부 차원의 AI 윤리 및 책임 관련 논의 활발"}
            ],
            "competitors": [
                {"name": "글로벌 AI 선도기업 (예: Google, Microsoft, AWS)", "market_share": "높음", "strengths": ["자본력", "기술력", "브랜드 인지도"]},
                {"name": "다수의 AI 스타트업", "market_share": "다양함", "strengths": ["특정 분야 전문성", "빠른 실행력"]}
            ],
            "consumer_trends": ["클라우드 기반 AI 서비스 도입 가속화", "산업별 특화 AI 솔루션 수요 증가", "AI 도입을 통한 생산성 향상 기대"]
        },
        "독일": {
            "market_size": "약 100억 유로 (제조업 AI)",
            "growth_rate": "연 25%",
            "regulations": [
                {"name": "GDPR (일반 개인정보 보호법)", "description": "유럽 연합의 강력한 개인정보보호 규정"},
                {"name": "산업 표준 및 인증 (Industrie 4.0)", "description": "스마트 팩토리 관련 표준 준수 중요"}
            ],
            "competitors": [
                {"name": "지멘스 (Siemens)", "market_share": "높음 (산업 자동화)", "strengths": ["기존 시장 지배력", "광범위한 산업 네트워크"]},
                {"name": "SAP", "market_share": "높음 (ERP 및 SCM)", "strengths": ["기업용 소프트웨어 전문성", "데이터 분석 능력"]}
            ],
            "consumer_trends": ["예측 유지보수, 품질 관리 등 AI 활용 증가", "에너지 효율성 및 지속가능성에 대한 관심 고조", "데이터 보안 및 신뢰성 중시"]
        },
        "싱가포르": {
            "market_size": "약 10억 달러 (AI 시장)",
            "growth_rate": "연 40%",
            "regulations": [
                {"name": "AI 윤리 거버넌스 프레임워크", "description": "정부 주도의 AI 개발 및 도입 가이드라인"},
                {"name": "PDPA (개인정보보호법)", "description": "자국 내 개인정보보호 규정"}
            ],
            "competitors": [
                {"name": "현지 및 다국적 AI 솔루션 기업", "market_share": "경쟁적", "strengths": ["정부 지원 활용", "아시아 시장 이해도"]},
                {"name": "대학 및 연구기관 기반 스타트업", "market_share": "신규 진입", "strengths": ["혁신 기술"]}
            ],
            "consumer_trends": ["스마트시티 프로젝트와 연계된 AI 솔루션 수요", "금융, 헬스케어, 물류 분야 AI 도입 활발", "디지털 전환 가속화"]
        },
        "캐나다": {
            "market_size": "약 50억 달러 (AI 시장)",
            "growth_rate": "연 28%",
            "regulations": [
                {"name": "PIPEDA (개인정보보호 및 전자기록법)", "description": "연방 개인정보보호법"},
                {"name": "AI 규제 관련 논의 진행 중", "description": "정부 차원에서 AI 전략 및 규제 프레임워크 개발 중"}
            ],
            "competitors": [
                {"name": "Element AI (ServiceNow에 인수)", "market_share": "과거 주요 플레이어", "strengths": ["AI 연구 역량"]},
                {"name": "다수의 중소규모 AI 기업", "market_share": "다양함", "strengths": ["특정 기술 전문성", "연구기관과의 협력"]}
            ],
            "consumer_trends": ["AI 연구 및 인재 개발에 대한 정부 투자 확대", "자연어 처리, 컴퓨터 비전 등 핵심 AI 기술 발달", "청정 기술 및 헬스케어 분야 AI 응용 관심"]
        },
        "인도네시아": {
            "market_size": "약 30억 달러 (디지털 헬스케어 시장)",
            "growth_rate": "연간 25%",
            "regulations": [
                {"name": "전자정보 거래법", "description": "데이터 보안 및 개인정보 보호 관련 규정"},
                {"name": "의료기기 규제", "description": "헬스케어 앱 등록 및 인증 필요"}
            ],
            "competitors": [
                {"name": "현지 헬스케어 앱", "market_share": "중간", "strengths": ["현지 시장 이해", "사용자 기반 보유"]},
                {"name": "글로벌 디지털 헬스 기업", "market_share": "낮음", "strengths": ["기술력", "자본력"]}
            ],
            "consumer_trends": ["건강 관리에 대한 관심 증가", "모바일 앱 사용률 높음", "현지화된 콘텐츠 선호"]
        },
        "필리핀": {
            "market_size": "약 15억 달러 (디지털 헬스케어 시장)",
            "growth_rate": "연간 20%",
            "regulations": [
                {"name": "데이터 프라이버시 법", "description": "개인 의료 데이터 취급 관련 규정"},
                {"name": "전자상거래법", "description": "디지털 서비스 제공 관련 법률"}
            ],
            "competitors": [
                {"name": "주요 통신사 제공 헬스 서비스", "market_share": "높음", "strengths": ["대규모 사용자 기반", "마케팅 역량"]},
                {"name": "스타트업 헬스케어 앱", "market_share": "낮음", "strengths": ["혁신적 기능", "젊은 층 타겟팅"]}
            ],
            "consumer_trends": ["모바일 결제 시스템 이용 증가", "소셜 미디어 영향력 높음", "건강 정보 접근성 개선 요구"]
        },
        "태국": {
            "market_size": "약 25억 달러 (디지털 헬스케어 시장)",
            "growth_rate": "연간 18%",
            "regulations": [
                {"name": "개인정보보호법", "description": "의료 데이터 취급에 대한 엄격한 규제"},
                {"name": "의료기기법", "description": "디지털 헬스케어 앱 등록 및 인증 절차"}
            ],
            "competitors": [
                {"name": "병원 그룹 연계 앱", "market_share": "높음", "strengths": ["의료 전문성", "기존 환자 네트워크"]},
                {"name": "웰니스 중심 앱", "market_share": "중간", "strengths": ["사용자 경험", "라이프스타일 통합"]}
            ],
            "consumer_trends": ["프리미엄 헬스케어 서비스 수요", "예방적 건강관리 관심 증가", "디지털 기기 활용 건강 모니터링 선호"]
        }
    }
    # target_countries_info_list는 [{ "name": "미국", "reason": "..." }, ...] 형태의 리스트여야 함
    generated_data = {}
    for country_info in target_countries_info_list:
        country_name = country_info.get("name")
        if country_name in market_data_samples:
            generated_data[country_name] = market_data_samples[country_name]
        else:
            # 샘플에 없는 국가 요청 시 기본값 또는 빈 값 처리
            generated_data[country_name] = {"market_size": "정보 없음", "growth_rate": "정보 없음", "regulations": [], "competitors": [], "consumer_trends": ["정보 없음"]}
    return generated_data 