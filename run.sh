#!/bin/bash

echo "🚀 주식 거래량 밀집도 분석기를 시작합니다..."
echo "📦 패키지 설치를 확인하는 중..."

# 필요한 패키지 설치
pip install -r requirements.txt

echo "🌐 Streamlit 웹 서버를 시작합니다..."
echo "📱 브라우저에서 http://localhost:8501 을 열어주세요"
echo "⏹️  종료하려면 Ctrl+C를 누르세요"
echo ""

# Streamlit 앱 실행
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
