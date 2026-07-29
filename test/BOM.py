import streamlit as st
import pandas as pd
from src.queries import (get_bom_list)
from src.ui import(
    setup_page,
    page_title,
    show_database_status,
    show_dataframe,
)

setup_page("BOM 관리")
page_title(title="BOM 관리", 
           description="완제품과 원자재의 구성 정보를 관리하는 화면\n",
           tables="bom,item\n",
           task="Bom 조회 및 CRUD")
show_database_status()
st.divider()
st.header("🧩 BOM 관리")

# BOM 목록 조회
st.divider()
st.header("🧩 BOM 목록")
bom_list = get_bom_list()

bom_dict=[dict(row) for row in bom_list]
df=pd.DataFrame(bom_dict)
show_dataframe(df, empty_message="등록된 BOM이 없습니다.")
