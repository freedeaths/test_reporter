import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# 获取数据库连接配置
username = st.secrets["DB_USERNAME"]
password = st.secrets["DB_PASSWORD"]
url = st.secrets["DB_URL"]
sql1 = st.secrets["STAT_WO_METHOD_SQL"]
sql2 = st.secrets["DETAIL_SQL"]
list1 = st.secrets["OPERATION_LIST"]

# 创建数据库连接
connection_string = f"mysql+pymysql://{username}:{password}@{url}"
engine = create_engine(connection_string)

# 页面标题
st.title('TiDB Query Demo')

# 用户输入
execution_id = st.text_input('execution_id')

if execution_id:
    # 转换为字符串
    execution_id = str(execution_id)
    
    # 查询SQL1
    try:
        with engine.connect() as conn:
            df1 = pd.read_sql(
                text(sql1),
                conn,
                params={"execution_id": execution_id}
            )
        st.subheader("Query 1 Results")
        st.dataframe(df1)
        
        # 下拉选择框
        selected_value = st.selectbox("Select a value", list1)
        
        if selected_value:
            # 查询SQL2
            try:
                with engine.connect() as conn:
                    df2 = pd.read_sql(
                        text(sql2),
                        conn,
                        params={
                            "execution_id": execution_id,
                            "operation_id": selected_value
                        }
                    )
                st.subheader("Query 2 Results")
                st.dataframe(df2)
            except Exception as e:
                st.error(f"Error executing SQL2: {str(e)}")
                
    except Exception as e:
        st.error(f"Error executing SQL1: {str(e)}")