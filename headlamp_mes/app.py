import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from src import queries
from src import chart_queries

from src.ui import (
    setup_page,
    page_title,
    show_database_status,
    setup_matplotlib
)


# ============================================================
# 페이지 설정
# ============================================================

setup_page("Dashboard")
setup_matplotlib()


# ============================================================
# 제목
# ============================================================

page_title(
    title="LED Head Lamp Mini MES",
    description="LED Head Lamp 생산관리 시스템",
    tables="-",
    task="Dashboard"
)


# ============================================================
# DB 상태
# ============================================================

show_database_status()

st.divider()


# ============================================================
# Dashboard
# ============================================================

st.header("📊 Dashboard")

st.caption(
    "LED Head Lamp 생산관리 시스템의 재고, 생산, 품질 현황을 "
    "한 화면에서 확인합니다."
)


# ============================================================
# 데이터 조회
# ============================================================

try:

    # --------------------------------------------------------
    # 기본 MES 데이터
    # --------------------------------------------------------

    fg_stock = queries.get_fg_stock_list()

    rm_stock = queries.get_rm_stock_list()

    today_production = queries.get_today_production_list()

    remaining_orders = (
        queries.get_remaining_production_order_list()
    )


    # --------------------------------------------------------
    # Dashboard 차트 데이터
    # --------------------------------------------------------

    production_chart_list = (
        chart_queries.get_production_chart_list()
    )

    defect_rate_list = (
        chart_queries.get_defect_rate_list()
    )


    # ========================================================
    # KPI 계산
    # ========================================================

    # 완제품 총 재고
    fg_total = sum(
        row["current_stock"]
        for row in fg_stock
    )

    # 원자재 총 재고
    rm_total = sum(
        row["current_stock"]
        for row in rm_stock
    )

    # 오늘 생산량
    today_production_total = sum(
        row["production_qty"]
        for row in today_production
    )

    # 진행 중 생산지시
    remaining_order_count = len(
        remaining_orders
    )


    # ========================================================
    # 주요 현황 KPI
    # ========================================================

    st.subheader("📌 주요 현황")

    k1, k2, k3, k4 = st.columns(4)


    # --------------------------------------------------------
    # 완제품 재고
    # --------------------------------------------------------

    with k1:

        with st.container(border=True):

            st.metric(
                label="📦 완제품 재고",
                value=f"{fg_total:,} EA"
            )

            st.caption(
                "완제품 LOT 현재 재고"
            )


    # --------------------------------------------------------
    # 원자재 재고
    # --------------------------------------------------------

    with k2:

        with st.container(border=True):

            st.metric(
                label="🧱 원자재 재고",
                value=f"{rm_total:,} EA"
            )

            st.caption(
                "원자재 LOT 현재 재고"
            )


    # --------------------------------------------------------
    # 오늘 생산
    # --------------------------------------------------------

    with k3:

        with st.container(border=True):

            st.metric(
                label="🏭 오늘 생산량",
                value=f"{today_production_total:,} EA"
            )

            st.caption(
                "금일 생산실적 기준"
            )


    # --------------------------------------------------------
    # 생산지시
    # --------------------------------------------------------

    with k4:

        with st.container(border=True):

            st.metric(
                label="📋 진행 생산지시",
                value=f"{remaining_order_count} 건"
            )

            st.caption(
                "완료되지 않은 생산지시"
            )


    st.divider()


    # ========================================================
    # 완제품 재고
    # ========================================================

    st.subheader("📦 완제품 재고 현황")


    if fg_stock:

        fg_df = pd.DataFrame(
            [dict(row) for row in fg_stock]
        )


        left, right = st.columns(2)


        # ----------------------------------------------------
        # 완제품별 재고
        # ----------------------------------------------------

        with left:

            with st.container(border=True):

                st.markdown(
                    "**완제품별 현재 재고**"
                )

                fig, ax = plt.subplots(
                    figsize=(6, 4)
                )

                ax.plot(
                    fg_df["item_name"],
                    fg_df["current_stock"],
                    marker="o"
                )

                ax.set_xlabel(
                    "완제품"
                )

                ax.set_ylabel(
                    "현재 재고 (EA)"
                )

                ax.set_title(
                    "완제품별 현재 재고",
                    fontweight="bold"
                )

                ax.tick_params(
                    axis="x",
                    rotation=20
                )

                plt.tight_layout()

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


        # ----------------------------------------------------
        # 완제품 재고 구성비
        # ----------------------------------------------------

        with right:

            with st.container(border=True):

                st.markdown(
                    "**완제품 재고 구성비**"
                )

                fig, ax = plt.subplots(
                    figsize=(6, 4)
                )

                ax.pie(
                    fg_df["current_stock"],
                    labels=fg_df["item_name"],
                    autopct="%1.1f%%",
                    startangle=90,
                    wedgeprops=dict(
                        width=0.4
                    ),
                    textprops=dict(
                        fontsize=7
                    )
                )

                ax.set_title(
                    "완제품 재고 구성비",
                    fontweight="bold"
                )

                plt.tight_layout()

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


    else:

        st.info(
            "완제품 재고 데이터가 없습니다."
        )


    # ========================================================
    # 원자재 재고
    # ========================================================

    st.divider()

    st.subheader("🧱 원자재 재고 현황")


    if rm_stock:

        rm_df = pd.DataFrame(
            [dict(row) for row in rm_stock]
        )


        left, right = st.columns(2)


        # ----------------------------------------------------
        # 원자재별 재고
        # ----------------------------------------------------

        with left:

            with st.container(border=True):

                st.markdown(
                    "**원자재별 현재 재고**"
                )

                fig, ax = plt.subplots(
                    figsize=(6, 4)
                )

                ax.barh(
                    rm_df["item_name"],
                    rm_df["current_stock"]
                )

                ax.set_xlabel(
                    "현재 재고 (EA)"
                )

                ax.set_ylabel(
                    "원자재"
                )

                ax.set_title(
                    "원자재별 현재 재고",
                    fontweight="bold"
                )

                plt.tight_layout()

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


        # ----------------------------------------------------
        # 원자재 재고 구성비
        # ----------------------------------------------------

        with right:

            with st.container(border=True):

                st.markdown(
                    "**원자재 재고 구성비**"
                )

                fig, ax = plt.subplots(
                    figsize=(6, 4)
                )

                ax.pie(
                    rm_df["current_stock"],
                    labels=rm_df["item_name"],
                    autopct="%1.1f%%",
                    startangle=90,
                    wedgeprops=dict(
                        width=0.4
                    ),
                    textprops=dict(
                        fontsize=7
                    )
                )

                ax.set_title(
                    "원자재 재고 구성비",
                    fontweight="bold"
                )

                plt.tight_layout()

                st.pyplot(
                    fig,
                    use_container_width=True
                )

                plt.close(fig)


    else:

        st.info(
            "원자재 재고 데이터가 없습니다."
        )


    # ========================================================
    # 생산 / 품질 현황
    # ========================================================

    st.divider()

    st.subheader("🏭 생산 / 품질 현황")


    if production_chart_list:

        production_df = pd.DataFrame(
            [dict(row) for row in production_chart_list]
        )


        left, right = st.columns(2)


        # ====================================================
        # 왼쪽 - 생산 현황
        # ====================================================

        with left:

            with st.container(border=True):

                st.markdown(
                    "**품목별 생산 현황**"
                )


                # 같은 품목의 생산지시 합산
                chart_df = (
                    production_df
                    .groupby(
                        "item_code",
                        as_index=False
                    )
                    .agg(
                        item_name=(
                            "item_name",
                            "first"
                        ),
                        order_qty=(
                            "order_qty",
                            "sum"
                        ),
                        produced_qty=(
                            "produced_qty",
                            "sum"
                        )
                    )
                )


                fig, ax = plt.subplots(
                    figsize=(6, 4)
                )


                # 품목별 색상
                colors = [
                    "#4C78A8",
                    "#F58518",
                    "#54A24B",
                    "#E45756"
                ]


                legend_handles = []


                for i, row in chart_df.iterrows():

                    color = (
                        colors[
                            i % len(colors)
                        ]
                    )


                    # 생산지시량
                    ax.barh(
                        i,
                        row["order_qty"],
                        color=color,
                        alpha=0.3,
                        height=0.6
                    )


                    # 실제 생산량
                    ax.barh(
                        i,
                        row["produced_qty"],
                        color=color,
                        alpha=1.0,
                        height=0.6
                    )


                    legend_handles.append(
                        Patch(
                            facecolor=color,
                            label=row["item_name"]
                        )
                    )


                ax.set_yticks(
                    range(len(chart_df))
                )

                ax.set_yticklabels(
                    chart_df["item_name"]
                )


                ax.set_xlabel(
                    "수량 (EA)"
                )

                ax.set_ylabel(
                    "완제품"
                )


                ax.set_title(
                    "품목별 생산 현황",
                    fontweight="bold"
                )


                ax.legend(
                    handles=legend_handles,
                    title="제품",
                    loc="upper right",
                    fontsize=6
                )


                plt.tight_layout()


                st.pyplot(
                    fig,
                    use_container_width=True
                )


                plt.close(fig)


    # ========================================================
    # 오른쪽 - 전체 품질 현황
    # ========================================================

        with right:

            with st.container(border=True):

                st.markdown(
                    "**전체 품질 현황**"
                )


                if defect_rate_list:

                    defect_df = pd.DataFrame(
                        [
                            dict(row)
                            for row in defect_rate_list
                        ]
                    )


                    # ----------------------------------------
                    # 전체 양품 / 불량
                    # ----------------------------------------

                    good_qty = (
                        defect_df["good_qty"]
                        .sum()
                    )

                    defect_qty = (
                        defect_df["defect_qty"]
                        .sum()
                    )


                    total_qty = (
                        good_qty
                        + defect_qty
                    )


                    if total_qty > 0:

                        defect_rate = (
                            defect_qty
                            / total_qty
                        ) * 100


                        # ------------------------------------
                        # 전체 품질 도넛
                        # ------------------------------------

                        fig, ax = plt.subplots(
                            figsize=(6, 4)
                        )


                        ax.pie(
                            [
                                good_qty,
                                defect_qty
                            ],
                            labels=[
                                "양품",
                                "불량"
                            ],
                            autopct="%1.1f%%",
                            startangle=90,
                            wedgeprops=dict(
                                width=0.4
                            ),
                            textprops=dict(
                                fontsize=8
                            )
                        )


                        ax.set_title(
                            f"전체 불량률 : "
                            f"{defect_rate:.1f}%",
                            fontweight="bold"
                        )


                        plt.tight_layout()


                        st.pyplot(
                            fig,
                            use_container_width=True
                        )


                        plt.close(fig)


                        st.metric(
                            "전체 불량률",
                            f"{defect_rate:.1f}%"
                        )


                    else:

                        st.info(
                            "품질검사 데이터가 없습니다."
                        )


                else:

                    st.info(
                        "품질검사 데이터가 없습니다."
                    )


    else:

        st.info(
            "생산지시 데이터가 없습니다."
        )


    # ========================================================
    # 완제품별 품질 현황
    # ========================================================

    st.divider()

    st.subheader(
        "⚠️ 완제품별 품질 현황"
    )


    if defect_rate_list:

        quality_df = pd.DataFrame(
            [
                dict(row)
                for row in defect_rate_list
            ]
        )


        # 불량률 계산
        quality_df["defect_rate"] = (
            quality_df["defect_qty"]
            / quality_df["inspection_qty"]
            * 100
        )


        # 보기 좋은 컬럼으로 변경
        quality_table = quality_df[
            [
                "item_code",
                "item_name",
                "inspection_qty",
                "good_qty",
                "defect_qty",
                "defect_rate"
            ]
        ].copy()


        quality_table.columns = [
            "품목코드",
            "제품명",
            "검사수량",
            "양품수량",
            "불량수량",
            "불량률 (%)"
        ]


        quality_table["검사수량"] = (
            quality_table["검사수량"]
            .map(lambda x: f"{x:,.0f}")
        )


        quality_table["양품수량"] = (
            quality_table["양품수량"]
            .map(lambda x: f"{x:,.0f}")
        )


        quality_table["불량수량"] = (
            quality_table["불량수량"]
            .map(lambda x: f"{x:,.0f}")
        )


        quality_table["불량률 (%)"] = (
            quality_table["불량률 (%)"]
            .map(lambda x: f"{x:.1f}%")
        )


        st.dataframe(
            quality_table,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "품질검사 데이터가 없습니다."
        )


    # ========================================================
    # 오늘 생산실적
    # ========================================================

    st.divider()

    st.subheader(
        "📋 오늘 생산실적"
    )


    if today_production:

        today_df = pd.DataFrame(
            [
                dict(row)
                for row in today_production
            ]
        )


        st.dataframe(
            today_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "오늘 생산실적이 없습니다."
        )


    # ========================================================
    # 진행 중 생산지시
    # ========================================================

    st.subheader(
        "📋 진행 중 생산지시"
    )


    if remaining_orders:

        order_df = pd.DataFrame(
            [
                dict(row)
                for row in remaining_orders
            ]
        )


        st.dataframe(
            order_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.success(
            "현재 진행 중인 생산지시가 없습니다."
        )


except Exception as exc:

    st.error(
        "대시보드 데이터를 불러오지 못했습니다."
    )

    st.exception(exc)
