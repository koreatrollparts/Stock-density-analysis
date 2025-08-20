"""
대화형 주식 거래량 밀집도 분석기
사용자 친화적인 인터페이스 제공
"""

from stock_density_analyzer import StockDensityAnalyzer
from datetime import datetime, timedelta
import os

# 주요 종목 코드 사전
POPULAR_STOCKS = {
    '1': ('005930', '삼성전자'),
    '2': ('000660', 'SK하이닉스'),
    '3': ('035420', 'NAVER'),
    '4': ('005380', '현대차'),
    '5': ('012330', '현대모비스'),
    '6': ('051910', 'LG화학'),
    '7': ('035720', '카카오'),
    '8': ('207940', '삼성바이오로직스'),
    '9': ('006400', '삼성SDI'),
    '10': ('068270', '셀트리온')
}

def clear_screen():
    """화면 지우기 (운영체제별 호환)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """프로그램 헤더 출력"""
    print("=" * 70)
    print("🔍 주식 거래량 밀집도 분석기")
    print("💰 FinanceDataReader를 이용한 거래량 분석")
    print("=" * 70)

def show_popular_stocks():
    """인기 종목 목록 출력"""
    print("\n📈 인기 종목 목록:")
    print("-" * 40)
    for key, (code, name) in POPULAR_STOCKS.items():
        print(f"{key:2s}. {name} ({code})")
    print("-" * 40)

def get_stock_selection():
    """종목 선택"""
    print("\n🎯 분석할 종목을 선택하세요:")
    show_popular_stocks()
    print("11. 직접 입력")
    
    while True:
        choice = input("\n선택 (1-11): ").strip()
        
        if choice in POPULAR_STOCKS:
            code, name = POPULAR_STOCKS[choice]
            print(f"✅ 선택된 종목: {name} ({code})")
            return code, name
        elif choice == '11':
            while True:
                code = input("종목 코드를 입력하세요 (예: 005930): ").strip()
                if code:
                    name = input(f"종목명을 입력하세요 (선택사항): ").strip()
                    if not name:
                        name = f"종목-{code}"
                    return code, name
                else:
                    print("❌ 종목 코드를 입력해주세요.")
        else:
            print("❌ 잘못된 선택입니다. 1-11 중에서 선택해주세요.")

def get_date_range():
    """분석 기간 선택"""
    print("\n📅 분석 기간을 선택하세요:")
    print("1. 최근 1개월")
    print("2. 최근 3개월")
    print("3. 최근 6개월")
    print("4. 최근 1년")
    print("5. 직접 입력")
    
    while True:
        choice = input("\n선택 (1-5): ").strip()
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        if choice == '1':
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            period_name = "최근 1개월"
        elif choice == '2':
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            period_name = "최근 3개월"
        elif choice == '3':
            start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            period_name = "최근 6개월"
        elif choice == '4':
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            period_name = "최근 1년"
        elif choice == '5':
            while True:
                try:
                    start_input = input("시작 날짜 (YYYY-MM-DD): ").strip()
                    end_input = input("종료 날짜 (YYYY-MM-DD): ").strip()
                    
                    # 날짜 형식 검증
                    datetime.strptime(start_input, '%Y-%m-%d')
                    datetime.strptime(end_input, '%Y-%m-%d')
                    
                    start_date = start_input
                    end_date = end_input
                    period_name = f"{start_date} ~ {end_date}"
                    break
                except ValueError:
                    print("❌ 올바른 날짜 형식(YYYY-MM-DD)으로 입력해주세요.")
        else:
            print("❌ 잘못된 선택입니다. 1-5 중에서 선택해주세요.")
            continue
        
        print(f"✅ 선택된 기간: {period_name}")
        return start_date, end_date, period_name

def get_analysis_options():
    """분석 옵션 선택"""
    print("\n⚙️ 분석 옵션을 설정하세요:")
    
    # 가격 구간 수
    while True:
        try:
            num_ranges = input("가격 구간 수 (기본 20, 10-50 권장): ").strip()
            if not num_ranges:
                num_ranges = 20
            else:
                num_ranges = int(num_ranges)
                if num_ranges < 5 or num_ranges > 100:
                    print("❌ 5-100 사이의 값을 입력해주세요.")
                    continue
            break
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
    
    # 상위 밀집 구간 수
    while True:
        try:
            top_zones = input("상위 밀집 구간 수 (기본 5): ").strip()
            if not top_zones:
                top_zones = 5
            else:
                top_zones = int(top_zones)
                if top_zones < 1 or top_zones > 20:
                    print("❌ 1-20 사이의 값을 입력해주세요.")
                    continue
            break
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
    
    # 차트 생성 여부
    create_charts = input("차트를 생성하시겠습니까? (y/n, 기본 y): ").lower().strip()
    if not create_charts:
        create_charts = 'y'
    create_charts = create_charts == 'y'
    
    print(f"✅ 설정 완료:")
    print(f"   - 가격 구간 수: {num_ranges}")
    print(f"   - 상위 밀집 구간: {top_zones}")
    print(f"   - 차트 생성: {'예' if create_charts else '아니오'}")
    
    return num_ranges, top_zones, create_charts

def run_analysis(symbol, name, start_date, end_date, period_name, num_ranges, top_zones, create_charts):
    """분석 실행"""
    print(f"\n🔄 분석을 시작합니다...")
    print(f"📊 종목: {name} ({symbol})")
    print(f"📅 기간: {period_name}")
    print("-" * 50)
    
    analyzer = StockDensityAnalyzer()
    
    try:
        # 1. 데이터 수집
        print("1️⃣ 데이터 수집 중...")
        data = analyzer.fetch_data(symbol, start_date, end_date)
        
        if data is None:
            print("❌ 데이터 수집에 실패했습니다.")
            return False
        
        # 2. 가격 구간별 분석
        print("2️⃣ 가격 구간별 거래량 분석 중...")
        price_ranges = analyzer.calculate_price_ranges(num_ranges=num_ranges)
        
        # 3. 밀집 구간 분석
        print("3️⃣ 거래량 밀집 구간 분석 중...")
        high_density_zones = analyzer.find_high_density_zones(price_ranges, top_n=top_zones)
        
        # 4. 지지/저항선 분석
        print("4️⃣ 지지/저항선 분석 중...")
        support_resistance = analyzer.calculate_support_resistance()
        
        # 5. 보고서 생성
        print("5️⃣ 분석 보고서 생성 중...")
        report = analyzer.generate_report(price_ranges, high_density_zones)
        
        # 결과 출력
        print("\n" + "="*70)
        print("📊 분석 결과")
        print("="*70)
        print(report)
        
        # 파일 저장
        filename = f"{symbol}_{name}_analysis_{start_date}_{end_date}.txt"
        filename = filename.replace(" ", "_").replace("/", "_")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"분석 대상: {name} ({symbol})\n")
            f.write(f"분석 기간: {period_name}\n")
            f.write("="*70 + "\n")
            f.write(report)
        
        print(f"\n💾 상세 보고서가 '{filename}' 파일로 저장되었습니다.")
        
        # 차트 생성
        if create_charts:
            print("\n6️⃣ 차트 생성 중...")
            try:
                chart_filename = f"{symbol}_{name}_chart_{start_date}_{end_date}.png"
                chart_filename = chart_filename.replace(" ", "_").replace("/", "_")
                
                analyzer.plot_price_volume_analysis(price_ranges, save_path=chart_filename)
                print(f"📈 차트가 '{chart_filename}' 파일로 저장되었습니다.")
                
                # 인터랙티브 차트
                interactive_filename = f"{symbol}_{name}_interactive_{start_date}_{end_date}.html"
                interactive_filename = interactive_filename.replace(" ", "_").replace("/", "_")
                
                analyzer.create_interactive_chart(price_ranges, save_path=interactive_filename)
                print(f"🌐 인터랙티브 차트가 '{interactive_filename}' 파일로 저장되었습니다.")
                
            except Exception as e:
                print(f"⚠️ 차트 생성 중 오류: {e}")
        
        print("\n✅ 분석이 완료되었습니다!")
        return True
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    while True:
        clear_screen()
        print_header()
        
        try:
            # 1. 종목 선택
            symbol, name = get_stock_selection()
            
            # 2. 기간 선택
            start_date, end_date, period_name = get_date_range()
            
            # 3. 옵션 설정
            num_ranges, top_zones, create_charts = get_analysis_options()
            
            # 4. 분석 실행
            success = run_analysis(symbol, name, start_date, end_date, period_name, 
                                 num_ranges, top_zones, create_charts)
            
            if success:
                print("\n💡 투자 참고사항:")
                print("   - 이 분석은 과거 데이터를 기반으로 하며, 미래를 보장하지 않습니다")
                print("   - 다른 기술적/기본적 분석과 함께 활용하시기 바랍니다")
                print("   - 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다")
            
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 예기치 못한 오류: {e}")
        
        # 재실행 여부 확인
        print("\n" + "="*50)
        restart = input("다른 종목을 분석하시겠습니까? (y/n): ").lower().strip()
        if restart != 'y':
            print("\n👋 분석을 종료합니다. 감사합니다!")
            break

if __name__ == "__main__":
    main()
