"""
주식 거래량 밀집도 분석기 - Streamlit Web UI
사용자 친화적인 웹 인터페이스
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
from stock_density_analyzer import StockDensityAnalyzer
import io
import base64

# 페이지 설정
st.set_page_config(
    page_title="주식 거래량 밀집도 분석기",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용 (다크모드 호환)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: var(--text-color-secondary, #666);
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-container {
        background-color: var(--background-color-secondary, #f0f2f6);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color, #e0e0e0);
    }
    .analysis-result {
        background-color: var(--background-color-accent, rgba(31, 119, 180, 0.1));
        color: var(--text-color, inherit);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        border: 1px solid var(--border-color, rgba(31, 119, 180, 0.2));
    }
    .analysis-result h4 {
        color: var(--text-color, inherit);
        margin-bottom: 1rem;
    }
    .analysis-result ul, .analysis-result li {
        color: var(--text-color, inherit);
    }
    .warning-box {
        background-color: var(--warning-background, rgba(255, 193, 7, 0.1));
        color: var(--text-color, inherit);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        border: 1px solid var(--border-color, rgba(255, 193, 7, 0.3));
    }
    .warning-box h4 {
        color: var(--text-color, inherit);
        margin-bottom: 1rem;
    }
    .warning-box ul, .warning-box li {
        color: var(--text-color, inherit);
    }
    .success-box {
        background-color: var(--success-background, rgba(40, 167, 69, 0.1));
        color: var(--text-color, inherit);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        border: 1px solid var(--border-color, rgba(40, 167, 69, 0.3));
    }
    .success-box h4 {
        color: var(--text-color, inherit);
        margin-bottom: 1rem;
    }
    .success-box ul, .success-box li {
        color: var(--text-color, inherit);
    }
    
    /* 다크모드 전용 스타일 */
    @media (prefers-color-scheme: dark) {
        .subtitle {
            color: #bbb;
        }
        .metric-container {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .analysis-result {
            background-color: rgba(31, 119, 180, 0.15);
            border: 1px solid rgba(31, 119, 180, 0.3);
        }
        .warning-box {
            background-color: rgba(255, 193, 7, 0.15);
            border: 1px solid rgba(255, 193, 7, 0.4);
        }
        .success-box {
            background-color: rgba(40, 167, 69, 0.15);
            border: 1px solid rgba(40, 167, 69, 0.4);
        }
    }
    
    /* Streamlit 다크모드 감지 */
    [data-theme="dark"] .subtitle {
        color: #bbb;
    }
    [data-theme="dark"] .metric-container {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-theme="dark"] .analysis-result {
        background-color: rgba(31, 119, 180, 0.15);
        border: 1px solid rgba(31, 119, 180, 0.3);
    }
    [data-theme="dark"] .warning-box {
        background-color: rgba(255, 193, 7, 0.15);
        border: 1px solid rgba(255, 193, 7, 0.4);
    }
    [data-theme="dark"] .success-box {
        background-color: rgba(40, 167, 69, 0.15);
        border: 1px solid rgba(40, 167, 69, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown('<h1 class="main-header">📈 주식 거래량 밀집도 분석기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">FinanceDataReader를 이용한 스마트 거래량 분석</p>', unsafe_allow_html=True)

# 사이드바 설정
st.sidebar.header("📊 분석 설정")

# 인기 종목 데이터
POPULAR_STOCKS = {
    "삼성전자": "005930",
    "SK하이닉스": "000660", 
    "NAVER": "035420",
    "현대차": "005380",
    "현대모비스": "012330",
    "LG화학": "051910",
    "카카오": "035720",
    "삼성바이오로직스": "207940",
    "셀트리온": "068270",
    "펄어비스": "263750",
    "POSCO홀딩스": "005490",
    "기아": "000270",
    "LG에너지솔루션": "373220",
    "KB금융": "105560",
    "신한지주": "055550",
    "하나금융지주": "086790",
    "삼성SDI": "006400",
    "LG전자": "066570",
    "SK텔레콤": "017670",
    "KT&G": "033780",
    "삼성물산": "028260",
    "현대글로비스": "086280",
    "SK이노베이션": "096770",
    "포스코케미칼": "003670",
    "한국전력": "015760",
    "CJ대한통운": "000120",
    "두산에너빌리티": "034020",
    "크래프톤": "259960",
    "컴투스": "078340",
    "위메이드": "112040",
    "직접입력": "custom"
}

# 종목 선택
st.sidebar.subheader("🎯 종목 선택")

# 종목 검색 입력창
search_input = st.sidebar.text_input(
    "종목명 또는 종목코드 입력:",
    value="",
    placeholder="예: 삼성전자, 005930, SK하이닉스",
    help="종목명(일부분도 가능) 또는 6자리 종목코드를 입력하세요"
)

# 검색 결과 처리
if search_input:
    # 종목코드인지 확인 (6자리 숫자)
    if search_input.isdigit() and len(search_input) == 6:
        stock_code = search_input
        stock_name = f"종목코드_{search_input}"
        st.sidebar.success(f"✅ 종목코드: {stock_code}")
        
    else:
        # 종목명으로 검색
        matched_stocks = []
        search_lower = search_input.lower()
        
        # 인기 종목에서 검색
        for name, code in POPULAR_STOCKS.items():
            if name != "직접입력" and search_lower in name.lower():
                matched_stocks.append((name, code))
        
        # 추가 종목 데이터베이스
        additional_stocks = {
            "LG전자": "066570",
            "포스코홀딩스": "005490",
            "네이버": "035420",  # NAVER와 동일
            "카카오뱅크": "323410",
            "삼성SDI": "006400",
            "LG에너지솔루션": "373220",
            "SK이노베이션": "096770",
            "현대중공업": "009540",
            "기아": "000270",
            "두산에너빌리티": "034020",
            "POSCO": "005490",
            "삼성물산": "028260",
            "KB금융": "105560",
            "신한지주": "055550",
            "하나금융지주": "086790",
            "SK텔레콤": "017670",
            "KT": "030200",
            "LG유플러스": "032640"
        }
        
        # 추가 종목에서도 검색
        for name, code in additional_stocks.items():
            if search_lower in name.lower():
                matched_stocks.append((name, code))
        
        if matched_stocks:
            if len(matched_stocks) == 1:
                # 정확히 하나 매칭되면 자동 선택
                stock_name, stock_code = matched_stocks[0]
                st.sidebar.success(f"✅ {stock_name} ({stock_code})")
            else:
                # 여러 개 매칭되면 선택 옵션 제공
                st.sidebar.write(f"🔍 {len(matched_stocks)}개 종목 발견:")
                selected_match = st.sidebar.selectbox(
                    "원하는 종목을 선택하세요:",
                    options=[f"{name} ({code})" for name, code in matched_stocks],
                    key="stock_search_results"
                )
                if selected_match:
                    stock_name = selected_match.split(" (")[0]
                    stock_code = selected_match.split("(")[1].replace(")", "")
                    st.sidebar.success(f"✅ 선택됨: {stock_name} ({stock_code})")
                else:
                    stock_code = None
                    stock_name = None
        else:
            # 매칭되는 종목이 없으면 직접 입력으로 처리
            if len(search_input) >= 2:
                st.sidebar.warning("⚠️ 매칭되는 종목을 찾을 수 없습니다.")
                
                # 숫자가 포함되어 있으면 종목코드로 가정
                if any(char.isdigit() for char in search_input):
                    manual_code = st.sidebar.text_input(
                        "종목코드를 정확히 입력하세요 (6자리):",
                        value=search_input,
                        max_chars=6,
                        key="manual_code_input"
                    )
                    if manual_code and manual_code.isdigit() and len(manual_code) == 6:
                        stock_code = manual_code
                        stock_name = f"직접입력_{manual_code}"
                        st.sidebar.info(f"ℹ️ 종목코드 {stock_code}로 분석합니다")
                    else:
                        stock_code = None
                        stock_name = None
                else:
                    st.sidebar.info("💡 정확한 종목명이나 6자리 종목코드를 입력해주세요")
                    stock_code = None
                    stock_name = None
            else:
                stock_code = None
                stock_name = None
else:
    stock_code = None
    stock_name = None

# 분석 기간 설정
st.sidebar.subheader("📅 분석 기간")
period_options = {
    "최근 1개월": 30,
    "최근 3개월": 90,
    "최근 6개월": 180,
    "최근 1년": 365,
    "최근 2년": 730,
    "최근 3년": 1095,
    "최근 4년": 1460,
    "최근 5년": 1825,
    "사용자 정의": "custom"
}

selected_period = st.sidebar.selectbox(
    "분석 기간을 선택하세요:",
    options=list(period_options.keys()),
    index=1  # 기본값: 최근 3개월
)

if selected_period == "사용자 정의":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "시작일",
            value=datetime.now() - timedelta(days=90),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "종료일",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
else:
    days = period_options[selected_period]
    end_date_str = datetime.now().strftime('%Y-%m-%d')
    start_date_str = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

# 분석 옵션
st.sidebar.subheader("⚙️ 분석 옵션")
num_ranges = st.sidebar.slider(
    "가격 구간 수",
    min_value=10,
    max_value=30,
    value=15,
    help="가격을 나눌 구간의 수를 설정합니다"
)

top_zones = st.sidebar.slider(
    "상위 밀집 구간 수",
    min_value=3,
    max_value=10,
    value=5,
    help="표시할 상위 거래량 밀집 구간의 수입니다"
)

# 지지선/저항선 설정
st.sidebar.subheader("📊 지지선/저항선 설정")

# 분석 기간 연동 옵션
use_full_period = st.sidebar.checkbox(
    "📅 전체 분석 기간 사용",
    value=True,
    help="체크 시 주 분석 기간과 동일하게 지지선/저항선을 분석합니다"
)

if use_full_period:
    # 전체 기간 사용 시 계산된 일수 표시
    if selected_period != "사용자 정의":
        days = period_options[selected_period]
        st.sidebar.info(f"🔗 지지선/저항선 분석 기간: {days}일 (주 분석 기간과 동일)")
        support_resistance_days = days
    else:
        # 사용자 정의 기간의 일수 계산
        from datetime import datetime
        start_dt = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date_str, '%Y-%m-%d')
        days_diff = (end_dt - start_dt).days
        st.sidebar.info(f"🔗 지지선/저항선 분석 기간: {days_diff}일 (주 분석 기간과 동일)")
        support_resistance_days = days_diff
else:
    # 별도 설정 사용
    support_resistance_days = st.sidebar.slider(
        "분석 기간 (일)",
        min_value=30,
        max_value=365,
        value=60,
        help="지지선/저항선 분석에 사용할 최근 데이터 일수"
    )

min_touches = st.sidebar.slider(
    "최소 터치 횟수",
    min_value=2,
    max_value=5,
    value=3,
    help="지지선/저항선으로 인정할 최소 터치 횟수"
)

max_sr_levels = st.sidebar.slider(
    "최대 표시 개수",
    min_value=2,
    max_value=6,
    value=3,
    help="지지선과 저항선 각각 최대 표시할 개수"
)

# 현재 분석 설정 요약 표시
if stock_code is not None:
    st.sidebar.markdown("### 📋 현재 분석 설정")
    st.sidebar.write(f"**종목**: {stock_name} ({stock_code})")
    st.sidebar.write(f"**기간**: {start_date_str} ~ {end_date_str}")
    st.sidebar.write(f"**구간 수**: {num_ranges}개")
    st.sidebar.write(f"**상위 표시**: {top_zones}개")
    
    if use_full_period:
        st.sidebar.write(f"**지지/저항 분석**: 전체 기간 ({support_resistance_days}일)")
    else:
        st.sidebar.write(f"**지지/저항 분석**: {support_resistance_days}일")
    
    st.sidebar.write(f"**최소 터치**: {min_touches}회")
    st.sidebar.write(f"**지지/저항 표시**: 각 {max_sr_levels}개")
    st.sidebar.markdown("---")# 세션 상태 초기화
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'last_stock_code' not in st.session_state:
    st.session_state.last_stock_code = None
if 'last_analysis_params' not in st.session_state:
    st.session_state.last_analysis_params = None

# 세션 상태 초기화
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'last_analysis_params' not in st.session_state:
    st.session_state.last_analysis_params = None

# 현재 분석 파라미터 생성
current_params = {
    'stock_code': stock_code,
    'start_date': start_date_str,
    'end_date': end_date_str,
    'num_ranges': num_ranges,
    'top_zones': top_zones,
    'sr_days': support_resistance_days,
    'min_touches': min_touches,
    'max_sr_levels': max_sr_levels,
    'use_full_period': use_full_period
}

# 종목이나 분석 파라미터가 변경되었는지 확인하고 상태 초기화
if current_params != st.session_state.last_analysis_params:
    st.session_state.analysis_done = False
    st.session_state.analyzer = None
    st.session_state.analysis_data = None
    st.session_state.last_analysis_params = current_params
    st.session_state.last_stock_code = stock_code

# 분석 실행 버튼
if stock_code is not None:
    # 분석 상태 표시
    if st.session_state.analysis_done and st.session_state.analysis_data:
        # 현재 설정과 이전 분석 설정 비교
        last_params = st.session_state.last_analysis_params
        if (last_params and 
            (current_params['start_date'] != last_params.get('start_date') or
             current_params['end_date'] != last_params.get('end_date') or
             current_params['num_ranges'] != last_params.get('num_ranges') or
             current_params['top_zones'] != last_params.get('top_zones'))):
            st.sidebar.warning("⚠️ 설정이 변경되었습니다. 재분석이 필요합니다.")
        else:
            st.sidebar.success(f"✅ 분석 완료: {stock_name} ({stock_code})")
    else:
        st.sidebar.info(f"📋 선택됨: {stock_name} ({stock_code})")
    
    # 자동 분석 체크박스
    auto_analyze = st.sidebar.checkbox(
        "🔄 설정 변경 시 자동 재분석",
        value=True,
        help="종목이나 분석 설정이 변경되면 자동으로 재분석을 시작합니다"
    )
    
    # 설정 변경 감지 여부 표시
    params_changed = current_params != st.session_state.last_analysis_params
    if params_changed and auto_analyze:
        st.sidebar.info("🔄 설정 변경 감지됨 - 자동 재분석 중...")
    
    analyze_button = st.sidebar.button(
        "🔍 분석 시작" if not st.session_state.analysis_done else "🔄 재분석",
        type="primary",
        use_container_width=True,
        help="선택된 종목의 거래량 밀집도 분석을 시작합니다"
    )
    
    # 자동 분석 또는 버튼 클릭 시 분석 실행
    should_analyze = analyze_button or (auto_analyze and stock_code is not None and params_changed)
else:
    st.sidebar.warning("⚠️ 종목을 먼저 선택해주세요")
    should_analyze = False

# 메인 컨텐츠 영역
if should_analyze and stock_code is not None:
    with st.spinner('📊 데이터를 수집하고 분석하는 중...'):
        try:
            # 분석기 초기화
            analyzer = StockDensityAnalyzer()
            
            # 데이터 가져오기
            data = analyzer.fetch_data(stock_code, start_date_str, end_date_str)
            
            if data is None:
                st.error("❌ 데이터를 가져올 수 없습니다. 종목 코드와 날짜를 확인해주세요.")
            else:
                # 분석 실행
                price_ranges = analyzer.calculate_price_ranges(num_ranges=num_ranges)
                high_density_zones = analyzer.find_high_density_zones(price_ranges, top_n=top_zones)
                support_resistance = analyzer.calculate_support_resistance(
                    analysis_days=support_resistance_days,
                    min_touches=min_touches,
                    max_levels=max_sr_levels
                )
                
                # 세션 상태에 저장
                st.session_state.analyzer = analyzer
                st.session_state.analysis_data = {
                    'data': data,
                    'price_ranges': price_ranges,
                    'high_density_zones': high_density_zones,
                    'support_resistance': support_resistance,
                    'stock_name': stock_name,
                    'stock_code': stock_code,
                    'period': f"{start_date_str} ~ {end_date_str}"
                }
                st.session_state.analysis_done = True
                
                st.success("✅ 분석이 완료되었습니다!")
                
        except Exception as e:
            st.error(f"❌ 분석 중 오류가 발생했습니다: {str(e)}")

# 분석 결과 표시
if st.session_state.analysis_done and st.session_state.analysis_data:
    data = st.session_state.analysis_data
    analyzer = st.session_state.analyzer
    
    # 기본 정보 표시
    st.markdown("## 📊 기본 정보")
    
    col1, col2, col3, col4 = st.columns(4)
    
    current_price = data['data']['Close'].iloc[-1]
    max_price = data['data']['High'].max()
    min_price = data['data']['Low'].min()
    avg_volume = data['data']['Volume'].mean()
    
    with col1:
        st.metric(
            label="현재가",
            value=f"{current_price:,}원",
            delta=f"{((current_price - data['data']['Close'].iloc[-2]) / data['data']['Close'].iloc[-2] * 100):+.2f}%" if len(data['data']) > 1 else None
        )
    
    with col2:
        st.metric(
            label="기간 최고가",
            value=f"{max_price:,}원"
        )
    
    with col3:
        st.metric(
            label="기간 최저가", 
            value=f"{min_price:,}원"
        )
    
    with col4:
        st.metric(
            label="평균 거래량",
            value=f"{avg_volume:,.0f}주"
        )
    
    # 거래량 밀집 구간 분석
    st.markdown("## 🎯 거래량 밀집 구간 분석")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📈 상위 밀집 구간")
        
        # 상위 밀집 구간 테이블
        display_data = []
        for i, (_, zone) in enumerate(data['high_density_zones'].head().iterrows(), 1):
            display_data.append({
                "순위": f"{i}위",
                "가격 구간": f"{zone['range_start']:,.0f} ~ {zone['range_end']:,.0f}원",
                "총 거래량": f"{zone['total_volume']:,.0f}주",
                "해당 일수": f"{zone['days_count']:.0f}일",
                "평균 거래량": f"{zone['avg_volume']:,.0f}주"
            })
        
        df_display = pd.DataFrame(display_data)
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("### 🔻🔺 지지선/저항선")
        
        support_data = data['support_resistance']
        
        # 분석 기간 정보 표시
        if 'analysis_period' in support_data:
            st.info(f"📊 {support_data['analysis_period']} 데이터 기반 분석")
        
        if support_data['support_levels']:
            st.markdown("**🔻 주요 지지선:**")
            for level in support_data['support_levels']:
                st.write(f"• {level['price']:,}원 (터치 {level['touches']}회)")
        else:
            st.write("• 발견된 지지선이 없습니다")
        
        if support_data['resistance_levels']:
            st.markdown("**🔺 주요 저항선:**")
            for level in support_data['resistance_levels']:
                st.write(f"• {level['price']:,}원 (터치 {level['touches']}회)")
        else:
            st.write("• 발견된 저항선이 없습니다")
        
        # 거래량 집중도 계산
        total_volume = data['price_ranges']['total_volume'].sum()
        top_3_volume = data['high_density_zones'].head(3)['total_volume'].sum()
        concentration_ratio = (top_3_volume / total_volume) * 100
        
        st.markdown("**📊 거래량 집중도:**")
        st.write(f"상위 3개 구간: {concentration_ratio:.1f}%")
        
        if concentration_ratio > 30:
            concentration_level = "높음 🔥"
            color = "success"
        elif concentration_ratio > 20:
            concentration_level = "보통 📊"
            color = "warning"
        else:
            concentration_level = "낮음 📉"
            color = "info"
        
        st.markdown(f"집중도: :{color}[{concentration_level}]")
    
    # 차트 생성
    st.markdown("## 📈 시각화 분석")
    
    # 인터랙티브 차트 생성
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'{data["stock_name"]} 주가 차트',
            '일별 거래량',
            '가격 구간별 거래량 분포',
            '거래량 밀도 분석'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # 1. 주가 차트
    fig.add_trace(
        go.Scatter(
            x=data['data'].index,
            y=data['data']['Close'],
            mode='lines',
            name='종가',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='날짜: %{x}<br>종가: %{y:,}원<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 지지선/저항선 추가
    for level in support_data['support_levels']:
        fig.add_hline(
            y=level['price'],
            line_dash="dash",
            line_color="green",
            annotation_text=f"지지선 {level['price']:,}원",
            row=1, col=1
        )
    
    for level in support_data['resistance_levels']:
        fig.add_hline(
            y=level['price'],
            line_dash="dash", 
            line_color="red",
            annotation_text=f"저항선 {level['price']:,}원",
            row=1, col=1
        )
    
    # 2. 거래량 차트
    fig.add_trace(
        go.Bar(
            x=data['data'].index,
            y=data['data']['Volume'],
            name='거래량',
            marker_color='lightblue',
            hovertemplate='날짜: %{x}<br>거래량: %{y:,}주<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 3. 가격 구간별 거래량
    fig.add_trace(
        go.Bar(
            x=data['price_ranges']['range_center'],
            y=data['price_ranges']['total_volume'],
            name='구간별 거래량',
            marker_color='skyblue',
            hovertemplate='가격: %{x:,}원<br>거래량: %{y:,}주<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 4. 거래량 밀도 스캐터
    fig.add_trace(
        go.Scatter(
            x=data['price_ranges']['range_center'],
            y=data['price_ranges']['total_volume'],
            mode='markers',
            name='거래량 밀도',
            marker=dict(
                size=12,
                color=data['price_ranges']['volume_density'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="밀도")
            ),
            hovertemplate='가격: %{x:,}원<br>거래량: %{y:,}주<br>밀도: %{marker.color:.0f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 레이아웃 설정
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text=f"{data['stock_name']}({data['stock_code']}) 거래량 밀집도 분석 - {data['period']}",
        title_x=0.5
    )
    
    # 각 서브플롯의 축 설정
    fig.update_xaxes(title_text="날짜", row=1, col=1)
    fig.update_yaxes(title_text="가격 (원)", row=1, col=1)
    
    fig.update_xaxes(title_text="날짜", row=1, col=2)
    fig.update_yaxes(title_text="거래량", row=1, col=2)
    
    fig.update_xaxes(title_text="가격 (원)", row=2, col=1)
    fig.update_yaxes(title_text="총 거래량", row=2, col=1)
    
    fig.update_xaxes(title_text="가격 (원)", row=2, col=2)
    fig.update_yaxes(title_text="총 거래량", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 분석 보고서
    st.markdown("## 📋 분석 보고서")
    
    report = analyzer.generate_report(data['price_ranges'], data['high_density_zones'])
    
    # 보고서를 섹션별로 나누어 표시
    report_sections = report.split('【')
    
    for section in report_sections[1:]:  # 첫 번째는 헤더이므로 제외
        if section.strip():
            title = section.split('】')[0]
            content = section.split('】')[1] if '】' in section else section
            
            with st.expander(f"📊 {title}", expanded=True):
                st.text(content.strip())
    
    # 투자 팁
    st.markdown("## 💡 투자 활용 팁")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="analysis-result">
        <h4>🎯 밀집 구간 활용법</h4>
        <ul>
        <li>밀집 구간은 향후 지지/저항 역할 가능성</li>
        <li>구간 돌파 시 추세 전환 신호로 활용</li>
        <li>박스권 매매 전략 수립 가능</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="analysis-result">
        <h4>📈 지지선/저항선 활용법</h4>
        <ul>
        <li>지지선 근처: 매수 타이밍 고려</li>
        <li>저항선 근처: 매도 타이밍 고려</li>
        <li>돌파 시: 추가 움직임 기대</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 주의사항
    st.markdown("""
    <div class="warning-box">
    <h4>⚠️ 투자 주의사항</h4>
    <ul>
    <li>이 분석은 과거 데이터를 기반으로 하며, 미래를 보장하지 않습니다</li>
    <li>다른 기술적/기본적 분석과 함께 활용하시기 바랍니다</li>
    <li>모든 투자 결정은 개인의 판단과 책임 하에 이루어져야 합니다</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 보고서 다운로드
    st.markdown("## 💾 보고서 다운로드")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 텍스트 보고서 다운로드
        full_report = f"""
{data['stock_name']}({data['stock_code']}) 거래량 밀집도 분석 보고서
분석 기간: {data['period']}
생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{report}
        """
        
        st.download_button(
            label="📄 텍스트 보고서 다운로드",
            data=full_report,
            file_name=f"{data['stock_code']}_{data['stock_name']}_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col2:
        # CSV 데이터 다운로드
        csv_data = data['price_ranges'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📊 분석 데이터 (CSV)",
            data=csv_data,
            file_name=f"{data['stock_code']}_price_ranges_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    # 초기 화면
    st.markdown("## 🚀 시작하기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="analysis-result">
        <h4>📊 거래량 밀집도 분석</h4>
        <p>특정 가격대에서 거래가 집중된 구간을 식별하여 향후 지지/저항선 예측</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="analysis-result">
        <h4>🎯 지지선/저항선 분석</h4>
        <p>과거 데이터를 기반으로 주요 지지선과 저항선을 자동으로 식별</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="analysis-result">
        <h4>📈 시각화 및 보고서</h4>
        <p>인터랙티브 차트와 상세한 분석 보고서를 자동으로 생성</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📝 사용법")
    st.markdown("""
    1. **종목 검색**: 
       - 검색창에 종목명이나 종목코드를 입력하세요 
       - 예: "삼성전자", "005930", "펄어비스", "SK하이닉스", "카카오"
       - 종목명의 일부만 입력해도 검색됩니다
    2. **분석 기간**을 선택하세요 (1개월~5년 또는 사용자 정의)
    3. **분석 옵션**을 원하는 대로 조정하세요
    4. **'🔍 분석 시작'** 버튼을 클릭하거나 자동 분석을 기다리세요
    5. 분석 결과와 차트를 확인하고 보고서를 다운로드하세요
    """)
    
    st.markdown("### 🎯 주요 기능")
    st.markdown("""
    - **실시간 데이터**: FinanceDataReader를 통한 최신 주식 데이터
    - **스마트 분석**: AI 기반 거래량 밀집도 및 지지/저항선 분석
    - **인터랙티브 차트**: 확대/축소 가능한 고품질 차트
    - **상세 보고서**: 투자 전략 수립에 도움되는 분석 결과
    - **데이터 다운로드**: 분석 결과를 파일로 저장
    """)

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: var(--text-color-secondary, #666); margin-top: 2rem;'>"
    "주식 거래량 밀집도 분석기 v1.0 | "
    "⚠️ 투자 판단은 본인 책임입니다 | "
    "📊 과거 데이터 기반 분석"
    "</div>",
    unsafe_allow_html=True
)
