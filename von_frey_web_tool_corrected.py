
import streamlit as st
import pandas as pd

# 加载修正后的 von Frey 对照表
@st.cache_data
def load_data():
    df = pd.read_csv("von_frey_thresholds_corrected.csv", dtype={"Binary_Pattern": str})
    return df

df = load_data()
df["Binary_Pattern"] = df["Binary_Pattern"].astype(str)

st.title("von Frey 阈值查询工具")
st.markdown("输入反应序列（由 0 表示阴性，1 表示阳性组成，如 000010），可单个或多个查询。")

input_text = st.text_area("请输入序列（每行一个）")

if st.button("查询阈值"):
    if input_text.strip() == "":
        st.warning("请输入至少一个序列")
    else:
        query_list = [line.strip() for line in input_text.splitlines() if line.strip()]
        result_df = pd.DataFrame(query_list, columns=["Binary_Pattern"])
        merged_df = result_df.merge(df, on="Binary_Pattern", how="left")
        st.write("查询结果如下：")
        st.dataframe(merged_df)
        csv = merged_df.to_csv(index=False).encode('utf-8')
        st.download_button("下载结果 CSV", csv, "von_frey_results.csv", "text/csv")
