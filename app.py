import streamlit as st
import pandas as pd
import duckdb


def run():
    st.set_page_config(
        page_title="Duck SQL",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto"
    )
    st.title("Duck SQL")
    query = st.text_area(label="Query")
    run_columns = st.columns((3, 2, 1))
    with run_columns[-1]:
        run_button = st.button(label="Run", use_container_width=True)

    with st.sidebar:
        uploaded_files = st.file_uploader(
            label="Upload your data",
            type=["csv"],
            accept_multiple_files=True
        )
        columns_placeholder = st.empty()

    conn = duckdb.connect()
    table_infos = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file)
            table_name = uploaded_file.name.split('.')[0]
            table_info = {
                "table": table_name,
                "cols": df.columns.tolist()
            }
            table_infos.append(table_info)
            conn.register(table_name, df)

        schema = "Tables:\n"
        for info in table_infos:
            schema += f"- {info['table']}\n"
            for col in info["cols"]:
                schema += f"    - {col}\n"
        columns_placeholder.markdown(schema)

        if query and run_button:
            print(query)
            result = conn.execute(query).df()
            st.dataframe(
                data=result,
                use_container_width=True,
                hide_index=True
            )


if __name__ == "__main__":
    run()
