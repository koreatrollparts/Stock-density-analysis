"""
간단한 테스트 스크립트
FinanceDataReader 라이브러리가 제대로 작동하는지 확인
"""

import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime, timedelta

print("=== FinanceDataReader 테스트 ===")

# 삼성전자 최근 10일 데이터 테스트
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

print(f"삼성전자(005930) 최근 10일 데이터 테스트")
print(f"기간: {start_date} ~ {end_date}")

try:
    # 데이터 가져오기
    data = fdr.DataReader('005930', start_date, end_date)
    
    if not data.empty:
        print(f"✅ 데이터 가져오기 성공!")
        print(f"데이터 개수: {len(data)}개")
        print(f"컬럼: {list(data.columns)}")
        print(f"최신 종가: {data['Close'].iloc[-1]:,.0f}원")
        print("\n최근 3일 데이터:")
        print(data.tail(3))
    else:
        print("❌ 데이터 가져오기 실패")
    
except ImportError as e:
    print(f"❌ 라이브러리 import 실패: {e}")
except Exception as e:
    print(f"❌ 테스트 실패: {e}")

print("\n=== 분석기 클래스 테스트 ===")
try:
    from stock_density_analyzer import StockDensityAnalyzer
    
    analyzer = StockDensityAnalyzer()
    print("✅ StockDensityAnalyzer 클래스 로드 성공!")
    
    # 간단한 데이터 fetch 테스트
    test_data = analyzer.fetch_data('005930', start_date, end_date)
    if test_data is not None:
        print("✅ 데이터 fetch 메서드 테스트 성공!")
    else:
        print("❌ 데이터 fetch 메서드 테스트 실패")
        
except Exception as e:
    print(f"❌ 분석기 클래스 테스트 실패: {e}")

print("\n모든 테스트가 완료되었습니다!")
