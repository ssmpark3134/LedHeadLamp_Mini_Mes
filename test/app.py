import streamlit as st
import sqlite3
import pandas as pd

# import src.ui as ui
from src import queries
from src.ui import setup_page, page_title, show_database_status, DB_PATH, metric_row, show_dataframe


# 페이지 설정
setup_page("Dashboard")

# 제목
page_title(
    title="LED Head Lamp Mini MES",
    description="LED Head Lamp 생산관리 시스템\n",
    tables="-\n",
    task="Dashboard"
)

# 데이터베이스 연결 상태 표시
show_database_status()

st.divider()

st.header("📊 Dashboard")

st.write("Mini MES Dashboard")

st.info("왼쪽 메뉴에서 기능을 선택하세요.")
