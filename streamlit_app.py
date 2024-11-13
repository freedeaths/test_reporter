import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


username = st.secrets["DB_USERNAME"]
password = st.secrets["DB_PASSWORD"]
url = st.secrets["DB_URL"]

show_executions_sql = st.secrets["SHOW_EXECUTIONS_SQL"]
stat_wo_method_in_execution_sql = st.secrets["STAT_WO_METHOD_IN_EXECUTION_SQL"]
detail_per_operation_in_execution_sql = st.secrets["DETAIL_PER_OPERATION_IN_EXECUTION_SQL"]
list_operations_in_execution_sql = st.secrets["LIST_OPERATIONS_IN_EXECUTION_SQL"]


connection_string = f"mysql+pymysql://{username}:{password}@{url}"
engine = create_engine(connection_string)


st.title('Dedicated API Test Report')

st.subheader('Recent 20 Execution IDs')

try:
    with engine.connect() as conn:
        df_executions = pd.read_sql_query(text(show_executions_sql), conn)
        st.dataframe(df_executions)
except Exception as e:
    st.error(f"Error executing SQL: {str(e)}")



execution_id = st.text_input(
    label='**Execution ID**',
    placeholder='Please input execution_id',
    label_visibility='visible',
)

if execution_id:
    execution_id = str(execution_id)
    
    try:
        with engine.connect() as conn:
            stat_query = text(stat_wo_method_in_execution_sql).bindparams(execution_id=execution_id)
            stat_df = pd.read_sql_query(
                stat_query,
                conn,
            )
            list_operations_query = text(list_operations_in_execution_sql).bindparams(execution_id=execution_id)
            list_operations_df = pd.read_sql_query(
                list_operations_query,
                conn,
            )
            st.subheader("Statistics (without INVALID_METHOD)")
            st.dataframe(stat_df)

            st.subheader("Details")
        
            for i, operation in list_operations_df.iterrows():
                detail_query = text(detail_per_operation_in_execution_sql).bindparams(execution_id=execution_id, operation_id=operation['operation'])
                detail_df = pd.read_sql_query(
                    detail_query,
                    conn,
                )
                if not detail_df.empty:
                    st.markdown(f"##### {operation['operation']}")
                    st.dataframe(detail_df)

    except Exception as e:
        st.error(f"Error executing SQL: {str(e)}")