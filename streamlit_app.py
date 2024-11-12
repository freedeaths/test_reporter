import streamlit as st
import pandas as pd
import numpy as np

# 创建随机数据
def create_random_df():
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Value1': np.random.randn(len(dates)),
        'Value2': np.random.randint(0, 100, len(dates)),
        'Category': np.random.choice(['A', 'B', 'C'], len(dates))
    })
    return df

# 创建页面
st.title('Random DataFrame Demo')

# 显示数据
df = create_random_df()
st.dataframe(df)

# 添加一个简单的图表
st.line_chart(df[['Value1', 'Value2']])