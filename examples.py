"""
주식 거래량 밀집도 분석 - 사용 예제
"""

from stock_density_analyzer import StockDensityAnalyzer
from datetime import datetime, timedelta

def example_analysis():
    """삼성전자 분석 예제"""
    
    # 분석기 초기화
    analyzer = StockDensityAnalyzer()
    
    # 삼성전자 최근 3개월 데이터 분석
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print("=== 삼성전자 거래량 밀집도 분석 예제 ===")
    
    # 데이터 가져오기
    data = analyzer.fetch_data('005930', start_date, end_date)
    
    if data is not None:
        # 가격 구간별 분석
        price_ranges = analyzer.calculate_price_ranges(num_ranges=15)
        
        # 상위 거래량 밀집 구간
        high_density = analyzer.find_high_density_zones(price_ranges, top_n=5)
        
        # 지지/저항선 분석
        support_resistance = analyzer.calculate_support_resistance()
        
        print("\n=== 지지/저항선 정보 ===")
        print(f"현재가: {support_resistance['current_price']:,.0f}원")
        
        if support_resistance['support_levels']:
            print("주요 지지선:")
            for level in support_resistance['support_levels']:
                print(f"  - {level['price']:,.0f}원 (터치 {level['touches']}회)")
        
        if support_resistance['resistance_levels']:
            print("주요 저항선:")
            for level in support_resistance['resistance_levels']:
                print(f"  - {level['price']:,.0f}원 (터치 {level['touches']}회)")
        
        # 차트 생성
        analyzer.plot_price_volume_analysis(price_ranges)
        
        # 보고서 생성
        report = analyzer.generate_report(price_ranges, high_density)
        
        # 파일로 저장
        with open('samsung_analysis_example.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n예제 분석이 완료되었습니다!")
        print("samsung_analysis_example.txt 파일을 확인하세요.")

def batch_analysis_example():
    """여러 종목 일괄 분석 예제"""
    
    stocks = {
        '005930': '삼성전자',
        '000660': 'SK하이닉스', 
        '035420': 'NAVER',
        '005380': '현대차',
        '012330': '현대모비스'
    }
    
    analyzer = StockDensityAnalyzer()
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
    
    results = {}
    
    print("=== 여러 종목 일괄 분석 예제 ===")
    
    for code, name in stocks.items():
        print(f"\n{name}({code}) 분석 중...")
        
        try:
            data = analyzer.fetch_data(code, start_date, end_date)
            if data is not None:
                price_ranges = analyzer.calculate_price_ranges(num_ranges=10)
                high_density = analyzer.find_high_density_zones(price_ranges, top_n=3)
                
                # 상위 거래량 밀집 구간 정보 저장
                top_zone = high_density.iloc[0]
                results[name] = {
                    'code': code,
                    'current_price': data['Close'].iloc[-1],
                    'top_density_range': f"{top_zone['range_start']:,.0f}~{top_zone['range_end']:,.0f}원",
                    'top_density_volume': top_zone['total_volume']
                }
                
        except Exception as e:
            print(f"{name} 분석 실패: {e}")
    
    # 결과 요약
    print("\n=== 분석 결과 요약 ===")
    for name, info in results.items():
        print(f"{name}({info['code']})")
        print(f"  현재가: {info['current_price']:,.0f}원")
        print(f"  최대 거래량 구간: {info['top_density_range']}")
        print(f"  해당 구간 거래량: {info['top_density_volume']:,.0f}주")
        print()

if __name__ == "__main__":
    # 예제 실행
    print("1. 삼성전자 단일 분석")
    print("2. 여러 종목 일괄 분석")
    
    choice = input("실행할 예제를 선택하세요 (1 또는 2): ").strip()
    
    if choice == "1":
        example_analysis()
    elif choice == "2":
        batch_analysis_example()
    else:
        print("잘못된 선택입니다.")
