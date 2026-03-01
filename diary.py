import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

plt.rcParams['font.family'] = 'Meiryo'

if 'is_submitted' not in st.session_state:#
    st.session_state.is_submitted = False #

st.title('📝 私の成長日記 ')

# --- 1deta集める ---
csv_file = 'diary_data.csv'

def load_data():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        
        return pd.DataFrame(columns=[
            '日付', '天気', 'ランニング', '予定達成', '授業数', 
            '満足度', '集中度', '問題数', '解決数', '未解決問題', '良かったこと'
        ])
        
if st.session_state.is_submitted:
   
    
    # header
    st.markdown("<h1 style='text-align: center; color: #FF69B4; font-size: 4em;'>BORIDE様:</h1>", unsafe_allow_html=True)
    
    # 心を言葉
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'>今日一日もお疲れ様でした。<br>昨日より成長しましたね！😊✨</h2>", unsafe_allow_html=True)
    
    
    
    # 满屏撒气球庆祝！
    st.balloons()
    
    st.divider()
    
    # return button
    if st.button("⬅️ 日記画面に戻る (main pageに戻る)"):
        st.session_state.is_submitted = False
        st.rerun() 
else:
    
    df = load_data()

    # --- 2. インプット書くところ ---
    st.subheader('📌 今日の記録')

    date_input = st.date_input("今日の日付を入力してください。")

    radio_weather = st.radio("今日の天気は？", ('晴れ', '曇り', '雨'))
    radio_run = st.radio("今日ランニングしましたか？（跑步了吗）", ('はい', 'いいえ'))
    radio_plan = st.radio("今日は予定を全部こなせそう？（完成计划了吗）", ('はい', 'いいえ'))

    option_selectbox = st.selectbox(
        "今日の授業何コマ受けましたか？",
        (0, 1, 2, 3, 4, 5)
    )

    st.write("今日の授業の質はどうでしたか？")
    slider_satisfaction = st.slider("授業の満足度（满足度）", min_value=0, max_value=100, value=50)
    slider_focus = st.slider("授業の集中度（集中程度）", min_value=0, max_value=100, value=50)

    problems_total = st.number_input("今日発生した問題の数（遇到了几个问题）", min_value=0, value=0)
    problems_solved = st.number_input("そのうち、解決できた問題の数（解决了几个）", min_value=0, max_value=int(problems_total), value=0)
    text_unsolved = st.text_input("未解決の問題は何ですか？（没解决的问题是什么）")

    text_good = st.text_area("今日あった良かったこと（有什么好事发生吗？）")

# --- 3. 輸出 ---
    if st.button("💾 記録を保存する (保存日记)"):
        # 将今天的输入打包成一行数据
        new_data = pd.DataFrame([{
            '日付': str(date_input), 
            '天気': radio_weather, 
            'ランニング': radio_run, 
            '予定達成': radio_plan,
            '授業数': option_selectbox, 
            '満足度': slider_satisfaction, 
            '集中度': slider_focus,
            '問題数': problems_total, 
            '解決数': problems_solved, 
            '未解決問題': text_unsolved, 
            '良かったこと': text_good
        }])
        
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file, index=False)
        
        
        st.session_state.is_submitted = True
        st.rerun()

    # --- 4. データ可視化 ---
    st.divider()
    st.subheader('📊 過去の蓄積データと分析')

    if not df.empty:
        # (1) 展示累计的大表格
        st.write("▼ 全データ（これまでの記録）")
        st.dataframe(df)
        
        st.write("▼ データビジュアライゼーション（チャート分析）")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**累計：問題の解決割合（pie）**")
            total_p = df['問題数'].sum()
            total_s = df['解決数'].sum()
            total_u = total_p - total_s
            
            if total_p > 0:
                fig1, ax1 = plt.subplots()
                ax1.pie([total_s, total_u], labels=['解決済み(已解决)', '未解決(未解决)'], 
                        autopct='%1.1f%%', colors=['#00A968', '#FF6B6B'], startangle=90)
                st.pyplot(fig1)
            else:
                st.info("これまでに発生した問題はありません！")
                
        with col2:
            st.write("**日々の集中度と満足度の推移**")
            fig2, ax2 = plt.subplots()
            ax2.plot(df['日付'], df['満足度'], label='満足度', marker='o', color='#3498DB')
            ax2.plot(df['日付'], df['集中度'], label='集中度', marker='s', color='#F39C12')
            plt.xticks(rotation=45)
            ax2.legend()
            st.pyplot(fig2)

    else:
        st.info("まだデータがありません。今日の記録を入力して「保存」を押してください。")