"""
주식 거래량 밀집도 분석 데모
삼성전자를 예시로 한 자동 분석 실행
"""

from stock_density_analyzer import StockDensityAnalyzer
from datetime import datetime, timedelta

def demo_analysis():
    """삼성전자 거래량 밀집도 분석 데모"""
    
    print("=" * 60)
    print("주식 거래량 밀집도 분석기 - 데모")
    print("=" * 60)
    
    # 분석기 초기화
    analyzer = StockDensityAnalyzer()
    
    # 분석 기간 설정 (최근 3개월)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    symbol = '005930'  # 삼성전자
    
    print(f"📊 분석 대상: 삼성전자 ({symbol})")
    print(f"📅 분석 기간: {start_date} ~ {end_date}")
    print()
    
    try:
        # 1. 데이터 가져오기
        print("1️⃣ 주식 데이터 수집 중...")
        data = analyzer.fetch_data(symbol, start_date, end_date)
        
        if data is None:
            print("❌ 데이터 수집 실패")
            return
        
        # 2. 가격 구간별 거래량 분석
        print("\n2️⃣ 가격 구간별 거래량 분석 중...")
        price_ranges = analyzer.calculate_price_ranges(num_ranges=15)
        
        # 3. 거래량 밀집 구간 찾기
        print("\n3️⃣ 거래량 밀집 구간 분석 중...")
        high_density_zones = analyzer.find_high_density_zones(price_ranges, top_n=5)
        
        # 4. 지지/저항선 분석
        print("\n4️⃣ 지지/저항선 분석 중...")
        support_resistance = analyzer.calculate_support_resistance()
        
        print(f"\n현재가: {support_resistance['current_price']:,.0f}원")
        
        if support_resistance['support_levels']:
            print("\n🔻 주요 지지선:")
            for level in support_resistance['support_levels']:
                print(f"   {level['price']:,.0f}원 (터치 {level['touches']}회)")
        
        if support_resistance['resistance_levels']:
            print("\n🔺 주요 저항선:")
            for level in support_resistance['resistance_levels']:
                print(f"   {level['price']:,.0f}원 (터치 {level['touches']}회)")
        
        # 5. 분석 보고서 생성
        print("\n5️⃣ 분석 보고서 생성 중...")
        report = analyzer.generate_report(price_ranges, high_density_zones)
        
        # 보고서 출력
        print(report)
        
        # 6. 파일로 저장
        report_filename = f"demo_{symbol}_analysis.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📄 상세 보고서가 '{report_filename}' 파일로 저장되었습니다.")
        
        # 7. 차트 생성 여부 확인
        print(f"\n📈 차트를 생성하시겠습니까? (y/n): ", end="")
        create_charts = input().lower().strip() == 'y'
        
        if create_charts:
            print("\n6️⃣ 차트 생성 중...")
            
            try:
                # 정적 차트
                chart_filename = f"demo_{symbol}_charts.png"
                analyzer.plot_price_volume_analysis(price_ranges, save_path=chart_filename)
                print(f"📊 차트가 '{chart_filename}' 파일로 저장되었습니다.")
                
                # 인터랙티브 차트
                interactive_filename = f"demo_{symbol}_interactive.html"
                analyzer.create_interactive_chart(price_ranges, save_path=interactive_filename)
                print(f"🌐 인터랙티브 차트가 '{interactive_filename}' 파일로 저장되었습니다.")
                
            except Exception as e:
                print(f"⚠️ 차트 생성 중 오류 발생: {e}")
                print("차트 생성을 건너뛰고 분석을 완료합니다.")
        
        print("\n✅ 분석이 완료되었습니다!")
        print("\n📝 분석 결과 요약:")
        print(f"   - 분석 기간: {len(data)}일")
        print(f"   - 현재가: {data['Close'].iloc[-1]:,.0f}원")
        print(f"   - 기간 최고가: {data['High'].max():,.0f}원")
        print(f"   - 기간 최저가: {data['Low'].min():,.0f}원")
        print(f"   - 평균 거래량: {data['Volume'].mean():,.0f}주")
        
        # 투자 팁
        print("\n💡 분석 활용 팁:")
        print("   1. 거래량 밀집 구간은 향후 지지/저항 역할을 할 가능성이 높습니다")
        print("   2. 현재가가 밀집 구간을 돌파할 때 추세 전환 신호로 활용하세요")
        print("   3. 지지선 근처에서는 매수, 저항선 근처에서는 매도를 고려해보세요")
        print("   4. 거래량과 함께 가격 움직임을 관찰하여 신뢰도를 높이세요")
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        print("네트워크 상태를 확인하거나 잠시 후 다시 시도해주세요.")

if __name__ == "__main__":
    demo_analysis()
