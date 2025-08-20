"""
주식 거래량 밀집도 분석기
FinanceDataReader를 이용하여 특정 종목의 거래가 밀집된 금액대를 분석하는 프로그램
"""

import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


class StockDensityAnalyzer:
    """주식 거래량 밀집도 분석 클래스"""
    
    def __init__(self):
        self.data = None
        self.symbol = None
        self.start_date = None
        self.end_date = None
        
    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        주식 데이터를 가져오는 함수
        
        Args:
            symbol: 종목 코드 (예: '005930' for 삼성전자)
            start_date: 시작 날짜 ('YYYY-MM-DD')
            end_date: 종료 날짜 ('YYYY-MM-DD')
            
        Returns:
            DataFrame: 주식 데이터
        """
        try:
            self.symbol = symbol
            self.start_date = start_date
            self.end_date = end_date
            
            print(f"종목 {symbol}의 {start_date}부터 {end_date}까지 데이터를 가져오는 중...")
            self.data = fdr.DataReader(symbol, start_date, end_date)
            
            if self.data.empty:
                raise ValueError("데이터를 가져올 수 없습니다. 종목 코드와 날짜를 확인해주세요.")
                
            print(f"총 {len(self.data)}일의 데이터를 성공적으로 가져왔습니다.")
            return self.data
            
        except Exception as e:
            print(f"데이터 가져오기 실패: {e}")
            return None
    
    def calculate_price_ranges(self, num_ranges: int = 20) -> pd.DataFrame:
        """
        가격 구간별 거래량 분석
        
        Args:
            num_ranges: 분석할 가격 구간 수
            
        Returns:
            DataFrame: 가격 구간별 거래량 정보
        """
        if self.data is None:
            raise ValueError("먼저 데이터를 가져와야 합니다.")
        
        # 최고가와 최저가 기준으로 가격 구간 설정
        min_price = self.data['Low'].min()
        max_price = self.data['High'].max()
        
        # 가격 구간 생성
        price_bins = np.linspace(min_price, max_price, num_ranges + 1)
        price_ranges = []
        
        for i in range(len(price_bins) - 1):
            range_start = price_bins[i]
            range_end = price_bins[i + 1]
            range_center = (range_start + range_end) / 2
            
            # 해당 구간에 포함되는 일자들의 거래량 합계
            condition = (
                (self.data['Low'] <= range_end) & 
                (self.data['High'] >= range_start)
            )
            
            volume_in_range = self.data[condition]['Volume'].sum()
            days_in_range = condition.sum()
            avg_volume = volume_in_range / days_in_range if days_in_range > 0 else 0
            
            price_ranges.append({
                'range_start': range_start,
                'range_end': range_end,
                'range_center': range_center,
                'total_volume': volume_in_range,
                'days_count': days_in_range,
                'avg_volume': avg_volume,
                'volume_density': volume_in_range / (range_end - range_start) if range_end != range_start else 0
            })
        
        return pd.DataFrame(price_ranges)
    
    def find_high_density_zones(self, price_ranges_df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """
        거래량이 밀집된 상위 구간 찾기
        
        Args:
            price_ranges_df: 가격 구간별 거래량 데이터
            top_n: 상위 몇 개 구간을 반환할지
            
        Returns:
            DataFrame: 거래량 밀집 상위 구간
        """
        # 거래량 밀도 기준으로 정렬
        top_zones = price_ranges_df.nlargest(top_n, 'total_volume')
        
        print(f"\n=== 거래량 상위 {top_n}개 구간 ===")
        for idx, zone in top_zones.iterrows():
            print(f"구간 {idx+1}: {zone['range_start']:,.0f} ~ {zone['range_end']:,.0f}원")
            print(f"  - 총 거래량: {zone['total_volume']:,.0f}")
            print(f"  - 해당 일수: {zone['days_count']:,.0f}일")
            print(f"  - 평균 거래량: {zone['avg_volume']:,.0f}")
            print(f"  - 거래량 밀도: {zone['volume_density']:,.0f}")
            print()
        
        return top_zones
    
    def calculate_support_resistance(self, analysis_days=60, min_touches=3, max_levels=3) -> Dict:
        """
        지지선/저항선 분석
        
        Args:
            analysis_days: 분석할 최근 일수 (기본값: 60일)
            min_touches: 최소 터치 횟수 (기본값: 3회)
            max_levels: 최대 표시할 지지선/저항선 개수 (기본값: 3개)
        
        Returns:
            Dict: 지지선/저항선 정보
        """
        if self.data is None:
            raise ValueError("먼저 데이터를 가져와야 합니다.")
        
        # 분석 기간 설정 (사용자 지정 가능)
        recent_data = self.data.tail(analysis_days)
        
        # 지지선: 최저가 중에서 여러 번 터치된 가격대
        support_levels = []
        resistance_levels = []
        
        # 가격대별 터치 횟수 계산
        price_touches = {}
        
        for _, row in recent_data.iterrows():
            low_range = int(row['Low'] / 1000) * 1000  # 1000원 단위로 반올림
            high_range = int(row['High'] / 1000) * 1000
            
            for price in range(low_range, high_range + 1000, 1000):
                if price not in price_touches:
                    price_touches[price] = 0
                price_touches[price] += 1
        
        # 터치 횟수가 많은 상위 가격대
        sorted_touches = sorted(price_touches.items(), key=lambda x: x[1], reverse=True)
        
        current_price = self.data['Close'].iloc[-1]
        
        for price, touches in sorted_touches[:20]:  # 상위 20개 중에서 선별
            if touches >= min_touches:  # 사용자 지정 최소 터치 횟수
                if price < current_price:
                    support_levels.append({'price': price, 'touches': touches})
                else:
                    resistance_levels.append({'price': price, 'touches': touches})
        
        return {
            'support_levels': support_levels[:max_levels],  # 사용자 지정 개수
            'resistance_levels': resistance_levels[:max_levels],  # 사용자 지정 개수
            'current_price': current_price,
            'analysis_period': f"최근 {analysis_days}일",
            'min_touches_used': min_touches
        }
    
    def plot_price_volume_analysis(self, price_ranges_df: pd.DataFrame, save_path: str = None):
        """
        가격-거래량 분석 차트 생성
        
        Args:
            price_ranges_df: 가격 구간별 거래량 데이터
            save_path: 차트 저장 경로 (선택사항)
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. 가격 차트
        ax1.plot(self.data.index, self.data['Close'], label='종가', linewidth=1)
        ax1.fill_between(self.data.index, self.data['Low'], self.data['High'], 
                        alpha=0.3, label='고가-저가 범위')
        ax1.set_title(f'{self.symbol} 주가 차트')
        ax1.set_ylabel('가격 (원)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 거래량 차트
        ax2.bar(self.data.index, self.data['Volume'], alpha=0.7, width=1)
        ax2.set_title('일별 거래량')
        ax2.set_ylabel('거래량')
        ax2.grid(True, alpha=0.3)
        
        # 3. 가격 구간별 거래량 분포
        ax3.bar(range(len(price_ranges_df)), price_ranges_df['total_volume'], 
                alpha=0.7, color='skyblue')
        ax3.set_title('가격 구간별 총 거래량')
        ax3.set_xlabel('가격 구간')
        ax3.set_ylabel('총 거래량')
        ax3.grid(True, alpha=0.3)
        
        # 4. 거래량 밀도 히트맵
        density_matrix = price_ranges_df[['range_center', 'total_volume']].values
        ax4.scatter(price_ranges_df['range_center'], price_ranges_df['total_volume'], 
                   s=100, alpha=0.7, c=price_ranges_df['volume_density'], cmap='YlOrRd')
        ax4.set_title('가격대별 거래량 밀도')
        ax4.set_xlabel('가격 (원)')
        ax4.set_ylabel('총 거래량')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"차트가 {save_path}에 저장되었습니다.")
        
        plt.show()
    
    def create_interactive_chart(self, price_ranges_df: pd.DataFrame, save_path: str = None):
        """
        인터랙티브 차트 생성 (Plotly)
        
        Args:
            price_ranges_df: 가격 구간별 거래량 데이터
            save_path: 차트 저장 경로 (선택사항)
        """
        from plotly.subplots import make_subplots
        
        # 서브플롯 생성
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('주가 차트', '일별 거래량', '가격 구간별 거래량', '거래량 밀도'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. 주가 차트
        fig.add_trace(
            go.Scatter(x=self.data.index, y=self.data['Close'], 
                      name='종가', line=dict(color='blue')),
            row=1, col=1
        )
        
        # 2. 거래량 차트
        fig.add_trace(
            go.Bar(x=self.data.index, y=self.data['Volume'], 
                   name='거래량', marker_color='lightblue'),
            row=1, col=2
        )
        
        # 3. 가격 구간별 거래량
        fig.add_trace(
            go.Bar(x=price_ranges_df['range_center'], y=price_ranges_df['total_volume'],
                   name='구간별 거래량', marker_color='skyblue'),
            row=2, col=1
        )
        
        # 4. 거래량 밀도 스캐터
        fig.add_trace(
            go.Scatter(x=price_ranges_df['range_center'], y=price_ranges_df['total_volume'],
                      mode='markers', name='거래량 밀도',
                      marker=dict(size=10, color=price_ranges_df['volume_density'], 
                                 colorscale='YlOrRd', showscale=True)),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f'{self.symbol} 거래량 밀집도 분석',
            height=800,
            showlegend=True
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"인터랙티브 차트가 {save_path}에 저장되었습니다.")
        
        fig.show()
    
    def generate_report(self, price_ranges_df: pd.DataFrame, high_density_zones: pd.DataFrame) -> str:
        """
        분석 보고서 생성
        
        Args:
            price_ranges_df: 가격 구간별 거래량 데이터
            high_density_zones: 거래량 밀집 구간
            
        Returns:
            str: 분석 보고서
        """
        support_resistance = self.calculate_support_resistance()
        
        report = f"""
=== {self.symbol} 거래량 밀집도 분석 보고서 ===
분석 기간: {self.start_date} ~ {self.end_date}
분석 일수: {len(self.data)}일

【기본 정보】
- 현재가: {self.data['Close'].iloc[-1]:,.0f}원
- 기간 최고가: {self.data['High'].max():,.0f}원
- 기간 최저가: {self.data['Low'].min():,.0f}원
- 평균 거래량: {self.data['Volume'].mean():,.0f}주

【거래량 밀집 구간 TOP 5】
"""
        
        for i, (_, zone) in enumerate(high_density_zones.head().iterrows(), 1):
            report += f"""
{i}. {zone['range_start']:,.0f} ~ {zone['range_end']:,.0f}원
   총 거래량: {zone['total_volume']:,.0f}주
   해당 일수: {zone['days_count']:.0f}일
   평균 거래량: {zone['avg_volume']:,.0f}주
"""
        
        report += "\n【지지선/저항선 분석】"
        
        if support_resistance['support_levels']:
            report += "\n<주요 지지선>"
            for level in support_resistance['support_levels']:
                report += f"\n- {level['price']:,.0f}원 (터치 {level['touches']}회)"
        
        if support_resistance['resistance_levels']:
            report += "\n<주요 저항선>"
            for level in support_resistance['resistance_levels']:
                report += f"\n- {level['price']:,.0f}원 (터치 {level['touches']}회)"
        
        # 거래량 집중도 계산
        total_volume = price_ranges_df['total_volume'].sum()
        top_3_volume = high_density_zones.head(3)['total_volume'].sum()
        concentration_ratio = (top_3_volume / total_volume) * 100
        
        report += f"""

【거래량 집중도】
- 상위 3개 구간 거래량 비중: {concentration_ratio:.1f}%
- 거래 집중도: {"높음" if concentration_ratio > 30 else "보통" if concentration_ratio > 20 else "낮음"}

【투자 참고사항】
- 거래량이 집중된 구간은 향후 지지/저항 역할을 할 가능성이 높습니다.
- 현재가 기준으로 위/아래 밀집 구간을 참고하여 매매 전략을 수립하세요.
- 거래량 집중도가 높을수록 해당 가격대에서 치열한 매매가 이루어졌음을 의미합니다.
"""
        
        return report


def main():
    """메인 함수"""
    analyzer = StockDensityAnalyzer()
    
    print("=== 주식 거래량 밀집도 분석기 ===")
    print("FinanceDataReader를 이용한 거래량 분석 프로그램")
    print()
    
    # 사용자 입력
    symbol = input("종목 코드를 입력하세요 (예: 005930): ").strip()
    start_date = input("시작 날짜를 입력하세요 (YYYY-MM-DD): ").strip()
    end_date = input("종료 날짜를 입력하세요 (YYYY-MM-DD): ").strip()
    
    try:
        # 데이터 가져오기
        data = analyzer.fetch_data(symbol, start_date, end_date)
        if data is None:
            return
        
        # 가격 구간별 거래량 분석
        print("\n가격 구간별 거래량을 분석하는 중...")
        price_ranges = analyzer.calculate_price_ranges(num_ranges=20)
        
        # 거래량 밀집 구간 찾기
        high_density_zones = analyzer.find_high_density_zones(price_ranges, top_n=10)
        
        # 분석 보고서 생성
        report = analyzer.generate_report(price_ranges, high_density_zones)
        print(report)
        
        # 보고서 저장
        report_filename = f"{symbol}_density_analysis_{start_date}_{end_date}.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n분석 보고서가 {report_filename}에 저장되었습니다.")
        
        # 차트 생성 여부 확인
        create_charts = input("\n차트를 생성하시겠습니까? (y/n): ").lower().strip() == 'y'
        
        if create_charts:
            print("차트를 생성하는 중...")
            
            # 정적 차트
            chart_filename = f"{symbol}_analysis_{start_date}_{end_date}.png"
            analyzer.plot_price_volume_analysis(price_ranges, save_path=chart_filename)
            
            # 인터랙티브 차트
            interactive_filename = f"{symbol}_interactive_{start_date}_{end_date}.html"
            analyzer.create_interactive_chart(price_ranges, save_path=interactive_filename)
        
        print("\n분석이 완료되었습니다!")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
