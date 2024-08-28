import streamlit as st
import pandas as pd
import duckdb


def run():
    st.set_page_config(
        page_title="Duck SQL",
        page_icon="🦆",
        layout="wide",
        initial_sidebar_state="auto"
    )
    title_columns = st.columns((3, 2, 1))
    with title_columns[0]:
        st.title("🗄️ Duck SQL")
    with title_columns[-1]:
        st.text("")
        st.text("")
        run_button = st.button(label="Run", use_container_width=True)

    query = st.text_area(label="Query")

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

        st.divider()
        if query and run_button:
            result = conn.execute(query).df()
            st.dataframe(
                data=result,
                use_container_width=True,
                hide_index=True
            )


if __name__ == "__main__":
    run()
