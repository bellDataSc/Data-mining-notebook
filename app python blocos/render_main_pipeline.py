def render_main_pipeline():
    st.sidebar.markdown("### Control Panel")
    uploaded_file = st.sidebar.file_uploader("Source PDF File", type="pdf")
    
    st.sidebar.markdown("### Parameterization")
    page_limit = st.sidebar.number_input("Max Pages (0 = All)", min_value=0, value=10)
    
    st.markdown('<div class="main-header">ETL Execution Pipeline</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Logic Laboratory", "Batch Processing"])
    
    with tabs[0]:
        render_logic_laboratory()
        
    with tabs[1]:
        if uploaded_file:
            if st.button("Initialize Extraction Sequence"):
                with st.spinner("Processing unstructured data stream..."):
                    dataset = []
                    
                    with pdfplumber.open(uploaded_file) as pdf:
                        total_pages = len(pdf.pages)
                        target_pages = total_pages if page_limit == 0 else min(page_limit, total_pages)
                        
                        current_fam = "ROOT"
                        seq_flag = False
                        
                        progress_bar = st.progress(0)
                        
                        for i in range(target_pages):
                            page = pdf.pages[i]
                            text = page.extract_text()
                            
                            if text:
                                for line in text.split('\n'):
                                    clean_line = line.strip()
                                    if not clean_line: continue
                                    
                                    status, payload, new_fam, new_flag = parse_line_logic(
                                        clean_line, current_fam, seq_flag
                                    )
                                    
                                    if status == "PRODUCT":
                                        payload["Source Page"] = i + 1
                                        dataset.append(payload)
                                        current_fam = new_fam
                                        seq_flag = False
                                    elif status == "HIERARCHY":
                                        current_fam = new_fam
                                        seq_flag = new_flag
                                        
                            progress_bar.progress((i + 1) / target_pages)
                            
                    df_results = pd.DataFrame(dataset)
                    
                    if not df_results.empty:
                        st.markdown('<div class="section-header">Extraction Telemetry</div>', unsafe_allow_html=True)
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Records", len(df_results))
                        m2.metric("Unique Families", df_results["Family Hierarchy"].nunique())
                        m3.metric("Processed Pages", target_pages)
                        
                        st.dataframe(df_results, use_container_width=True)
                        
                        csv_buffer = df_results.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
                        st.download_button(
                            "Export Structured Dataset (CSV)",
                            data=csv_buffer,
                            file_name="structured_output.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No valid data patterns found in the provided pages.")
        else:
            st.info("Awaiting source file upload to initiate pipeline.")

if __name__ == "__main__":
    render_main_pipeline()
