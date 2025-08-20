#!/usr/bin/env python3
"""
주식 거래량 밀집도 분석기 실행 스크립트
간편한 실행을 위한 Python 스크립트
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """필요한 패키지들을 설치합니다."""
    print("📦 필요한 패키지들을 설치하는 중...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 패키지 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        return False

def run_streamlit():
    """Streamlit 앱을 실행합니다."""
    print("\n🌐 Streamlit 웹 서버를 시작합니다...")
    print("📱 브라우저에서 http://localhost:8501 을 열어주세요")
    print("⏹️  종료하려면 Ctrl+C를 누르세요\n")
    
    try:
        subprocess.run([
            "streamlit", "run", "streamlit_app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 프로그램을 종료합니다.")
    except FileNotFoundError:
        print("❌ Streamlit이 설치되지 않았습니다. 패키지를 다시 설치해주세요.")
        return False
    except Exception as e:
        print(f"❌ 실행 중 오류가 발생했습니다: {e}")
        return False
    
    return True

def main():
    """메인 함수"""
    print("🚀 주식 거래량 밀집도 분석기")
    print("=" * 50)
    
    # 현재 디렉토리가 프로젝트 루트인지 확인
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py 파일을 찾을 수 없습니다.")
        print("💡 프로젝트 루트 디렉토리에서 실행해주세요.")
        return False
    
    # 패키지 설치
    if not install_requirements():
        return False
    
    # Streamlit 앱 실행
    return run_streamlit()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
