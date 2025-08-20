# 주식 거래량 밀집도 분석기 📈

FinanceDataReader를 이용한 주식 거래량 밀집도 분석 프로그램입니다.
특정 종목과 분석 기간을 설정하면 많은 거래가 밀집해 있는 금액대를 분석하여 지지선/저항선을 예측할 수 있습니다.

## ✨ 주요 기능

- 📊 **거래량 밀집도 분석**: 특정 가격대에서 거래가 집중된 구간 식별
- 🎯 **지지선/저항선 분석**: 과거 데이터를 기반으로 주요 지지/저항선 자동 식별  
- 📈 **시각화**: 인터랙티브 차트와 상세한 분석 보고서 자동 생성
- 🔍 **스마트 종목 검색**: 종목명이나 코드로 쉬운 검색
- 📅 **다양한 기간 설정**: 1개월~5년까지 장기 분석 지원
- 🌙 **다크모드 지원**: 라이트/다크 모드 자동 적응

## 🚀 빠른 시작

### 방법 1: 자동 실행 스크립트 (추천)

```bash
# Linux/Mac
./run.sh

# Windows Git Bash
bash run.sh
```

### 방법 2: Python 스크립트

```bash
python run.py
```

### 방법 3: 수동 실행

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 웹 앱 실행
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

## 📱 사용법

1. 위의 실행 방법 중 하나를 선택하여 프로그램을 시작
2. 브라우저에서 `http://localhost:8501` 접속
3. 왼쪽 사이드바에서 설정:
   - **종목 선택**: 인기 종목 선택 또는 직접 검색
   - **분석 기간**: 1개월~5년 또는 사용자 정의
   - **분석 옵션**: 가격 구간 수, 상위 밀집 구간 수 조정
4. '🔍 분석 시작' 버튼 클릭
5. 결과 확인 및 보고서 다운로드

## 📦 필요한 패키지

- `finance-datareader>=0.9.96`: 한국 주식 데이터 수집
- `pandas>=1.5.0`: 데이터 처리
- `numpy>=1.21.0`: 수치 계산
- `matplotlib>=3.5.0`: 정적 차트
- `seaborn>=0.11.0`: 통계 시각화
- `plotly>=5.0.0`: 인터랙티브 차트
- `streamlit>=1.28.0`: 웹 UI
- `streamlit-plotly-events>=0.0.6`: 차트 이벤트 처리

## 📁 프로젝트 구조

```
Stock-density-analysis/
├── streamlit_app.py          # 웹 UI 메인 애플리케이션
├── stock_density_analyzer.py # 핵심 분석 엔진
├── interactive_analyzer.py   # 명령행 인터페이스
├── demo.py                   # 데모 프로그램
├── examples.py               # 사용 예제
├── requirements.txt          # 패키지 의존성
├── run.sh                   # Linux/Mac 실행 스크립트
├── run.py                   # Python 실행 스크립트
└── README.md                # 프로젝트 설명
```

## 🎯 분석 결과 활용법

### 거래량 밀집 구간
- 향후 지지/저항 역할 가능성 높음
- 구간 돌파 시 추세 전환 신호
- 박스권 매매 전략 수립 가능

### 지지선/저항선
- **지지선 근처**: 매수 타이밍 고려
- **저항선 근처**: 매도 타이밍 고려
- **돌파 시**: 추가 움직임 기대

## ⚠️ 주의사항

- 이 분석은 과거 데이터 기반이며 미래를 보장하지 않습니다
- 다른 기술적/기본적 분석과 함께 활용하시기 바랍니다
- 모든 투자 결정은 개인의 판단과 책임 하에 이루어져야 합니다

## 🛠️ 문제 해결

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Streamlit 실행 오류
```bash
pip install streamlit --upgrade
streamlit --version
```

### 데이터 수집 오류
- 네트워크 연결 확인
- 종목 코드 정확성 확인
- 분석 기간이 너무 오래되지 않았는지 확인

## 주요 기능

### 1. 거래량 밀집도 분석
- 설정한 기간 동안의 주식 데이터를 가격 구간별로 나누어 거래량 분석
- 가장 많은 거래가 이루어진 가격대 식별
- 거래량 밀도 계산 및 순위 제공

### 2. 지지선/저항선 분석
- 과거 데이터를 기반으로 주요 지지선과 저항선 식별
- 가격대별 터치 횟수 계산
- 현재가 기준 지지/저항 구간 제공

### 3. 시각화
- 주가 차트, 거래량 차트
- 가격 구간별 거래량 분포 차트
- 거래량 밀도 히트맵
- 인터랙티브 차트 (Plotly)

### 4. 분석 보고서
- 상세한 분석 결과를 텍스트 파일로 저장
- 투자 참고사항 및 해석 제공

## 설치 및 사용법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 기본 사용법
```bash
python stock_density_analyzer.py
```

프로그램 실행 후 다음 정보를 입력:
- 종목 코드 (예: 005930 - 삼성전자)
- 시작 날짜 (YYYY-MM-DD)
- 종료 날짜 (YYYY-MM-DD)

### 3. 예제 실행
```bash
python examples.py
```

## 주요 클래스 및 메서드

### StockDensityAnalyzer 클래스

#### `fetch_data(symbol, start_date, end_date)`
- 지정된 종목의 주식 데이터를 가져옵니다
- **매개변수:**
  - `symbol`: 종목 코드 (문자열)
  - `start_date`: 시작 날짜 ('YYYY-MM-DD')
  - `end_date`: 종료 날짜 ('YYYY-MM-DD')

#### `calculate_price_ranges(num_ranges=20)`
- 가격을 구간별로 나누어 거래량을 분석합니다
- **매개변수:**
  - `num_ranges`: 분석할 가격 구간 수 (기본값: 20)

#### `find_high_density_zones(price_ranges_df, top_n=5)`
- 거래량이 가장 밀집된 상위 구간을 찾습니다
- **매개변수:**
  - `price_ranges_df`: 가격 구간 데이터프레임
  - `top_n`: 반환할 상위 구간 수 (기본값: 5)

#### `calculate_support_resistance()`
- 지지선과 저항선을 계산합니다
- 최근 60일 데이터를 기반으로 분석

#### `plot_price_volume_analysis(price_ranges_df, save_path=None)`
- 분석 결과를 차트로 시각화합니다
- **매개변수:**
  - `price_ranges_df`: 가격 구간 데이터프레임
  - `save_path`: 차트 저장 경로 (선택사항)

#### `create_interactive_chart(price_ranges_df, save_path=None)`
- Plotly를 이용한 인터랙티브 차트를 생성합니다

#### `generate_report(price_ranges_df, high_density_zones)`
- 상세한 분석 보고서를 생성합니다

## 사용 예제

### 1. 기본 분석
```python
from stock_density_analyzer import StockDensityAnalyzer

# 분석기 초기화
analyzer = StockDensityAnalyzer()

# 삼성전자 데이터 가져오기
data = analyzer.fetch_data('005930', '2024-01-01', '2024-03-31')

# 가격 구간별 분석
price_ranges = analyzer.calculate_price_ranges(num_ranges=15)

# 거래량 밀집 구간 찾기
high_density = analyzer.find_high_density_zones(price_ranges, top_n=5)

# 차트 생성
analyzer.plot_price_volume_analysis(price_ranges)
```

### 2. 지지/저항선 분석
```python
# 지지/저항선 정보 가져오기
support_resistance = analyzer.calculate_support_resistance()

print(f"현재가: {support_resistance['current_price']:,.0f}원")
print("주요 지지선:")
for level in support_resistance['support_levels']:
    print(f"  - {level['price']:,.0f}원")
```

## 출력 파일

1. **분석 보고서**: `{종목코드}_density_analysis_{시작날짜}_{종료날짜}.txt`
2. **차트 이미지**: `{종목코드}_analysis_{시작날짜}_{종료날짜}.png`
3. **인터랙티브 차트**: `{종목코드}_interactive_{시작날짜}_{종료날짜}.html`

## 주요 종목 코드

- 삼성전자: 005930
- SK하이닉스: 000660
- NAVER: 035420
- 현대차: 005380
- 현대모비스: 012330
- LG화학: 051910
- 카카오: 035720

## 분석 결과 해석

### 거래량 밀집도
- **높은 밀집도**: 해당 가격대에서 치열한 매매가 이루어짐
- **지지/저항 역할**: 밀집 구간은 향후 지지선 또는 저항선 역할 가능성
- **거래 전략**: 밀집 구간 돌파 시 추세 전환 신호로 활용 가능

### 거래량 집중도
- **30% 이상**: 높은 집중도 (특정 가격대 선호도 높음)
- **20-30%**: 보통 집중도
- **20% 미만**: 낮은 집중도 (고른 분포)

## 주의사항

1. 과거 데이터 기반 분석이므로 미래 보장 없음
2. 다른 기술적/기본적 분석과 함께 활용 권장
3. 시장 상황 변화에 따른 패턴 변화 가능성 고려
4. 투자 판단은 개인 책임으로 진행

---

📊 **주식 거래량 밀집도 분석기 v1.0**  
⚠️ 투자 판단은 본인 책임입니다 | 📈 과거 데이터 기반 분석
