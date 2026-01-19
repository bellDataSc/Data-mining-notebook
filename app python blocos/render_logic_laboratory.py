def render_logic_laboratory():
    st.markdown('<div class="section-header">Extraction Logic Simulator</div>', unsafe_allow_html=True)
    st.write("This module allows real-time validation of the Regex anchoring strategy used to bypass unstructured layouts.")
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.markdown("**Input: Raw PDF Line**")
        test_line = st.text_input(
            "Paste a line from the PDF to test:",
            value="B010000004       AJUDANTE DE ASSENTADOR            H          R$ 7,35"
        )
        
        st.markdown("**System State Configuration**")
        simulated_family = st.text_input("Current Family Context:", value="LABOR FORCE")
        simulated_flag = st.checkbox("Previous line was a header?", value=False)
        
    with col_output:
        st.markdown("**Output: Parsed Structured Data**")
        
        status, data, new_fam, is_header = parse_line_logic(test_line, simulated_family, simulated_flag)
        
        if status == "PRODUCT":
            st.markdown('<div class="status-box status-success">TYPE: PRODUCT DETECTED</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([data]), use_container_width=True)
            
        elif status == "HIERARCHY":
            st.markdown('<div class="status-box status-info">TYPE: HIERARCHY HEADER DETECTED</div>', unsafe_allow_html=True)
            st.write(f"Updated Context: {new_fam}")
            
        else:
            st.markdown('<div class="status-box">TYPE: IGNORED / METADATA</div>', unsafe_allow_html=True)
            
    st.markdown("---")
    st.markdown("**Visual Logic Flow**")
    st.graphviz_chart("""
    digraph {
        rankdir=LR;
        node [shape=box, style="rounded,filled", fillcolor="#F1F5F9", fontname="Arial"];
        START [label="Input Line", shape=circle, fillcolor="#3B82F6", fontcolor="white"];
        CHECK_CODE [label="Regex: Code Anchor"];
        CHECK_PRICE [label="Regex: Price Anchor"];
        IS_PROD [label="Classify: Product", fillcolor="#DCFCE7"];
        IS_FAM [label="Classify: Hierarchy", fillcolor="#DBEAFE"];
        PARSE_TXT [label="Parse: Reverse Unit Logic"];
        UPDATE_CTX [label="Update: Parent | Child"];
        
        START -> CHECK_CODE;
        CHECK_CODE -> CHECK_PRICE [label="Match"];
        CHECK_PRICE -> IS_PROD [label="Match"];
        CHECK_PRICE -> IS_FAM [label="No Match"];
        IS_PROD -> PARSE_TXT;
        IS_FAM -> UPDATE_CTX;
    }
    """)
