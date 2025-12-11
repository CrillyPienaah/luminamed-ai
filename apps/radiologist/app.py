"""LuminaMed AI - Radiologist Portal."""
import streamlit as st
import requests
import time
from PIL import Image
import io
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="LuminaMed - Radiologist Portal",
    page_icon="🩻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
import os
API_BASE_URL = os.getenv("API_URL", "https://luminamed-ai-production.up.railway.app")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'report_status' not in st.session_state:
    st.session_state.report_status = "draft"

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=LuminaMed+AI", use_column_width=True)
    st.markdown("---")
    
    st.subheader("📊 Session Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Reports Generated", len(st.session_state.reports))
    with col2:
        approved_count = sum(1 for r in st.session_state.reports if r.get('status') == 'approved')
        st.metric("Approved", approved_count)
    
    st.markdown("---")
    st.subheader("⚙️ Settings")
    
    modality = st.selectbox(
        "Default Modality",
        ["xray", "ct", "mri", "ultrasound"],
        index=0
    )
    
    auto_verify = st.checkbox("Auto-verify reports", value=True)
    show_citations = st.checkbox("Show knowledge citations", value=True)
    
    st.markdown("---")
    st.caption("LuminaMed AI v0.1.0")
    st.caption("Multi-agent radiology report generation")

# Main header
st.markdown('<p class="main-header">🩻 Radiologist Portal</p>', unsafe_allow_html=True)
st.markdown("Generate AI-powered radiology reports with verifiable citations")

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Generate Report", "📋 Review Reports", "📊 Analytics"])

with tab1:
    st.subheader("Upload Medical Image")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg", "dcm"],
            help="Supported formats: PNG, JPEG, DICOM"
        )
        
        clinical_hint = st.text_area(
            "Clinical Indication / History",
            placeholder="e.g., Patient with persistent cough and fever...",
            height=100
        )
        
        selected_modality = st.selectbox(
            "Image Modality",
            ["xray", "ct", "mri", "ultrasound"],
            index=0,
            key="modality_select"
        )
        
        generate_btn = st.button("🚀 Generate Report", type="primary", use_container_width=True)
    
    with col2:
        if uploaded_file:
            st.markdown("**Image Preview:**")
            try:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                
                # Image metadata
                st.caption(f"Filename: {uploaded_file.name}")
                st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
    
    # Generate report
    if generate_btn and uploaded_file:
        with st.spinner("🤖 AI agents are analyzing the image..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Prepare request
                files = {
                    "image": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                data = {
                    "clinical_hint": clinical_hint or "No clinical context provided",
                    "modality": selected_modality
                }
                
                # Simulate agent progress
                status_text.text("🔍 Findings Agent analyzing image...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                status_text.text("📝 Impression Agent synthesizing summary...")
                progress_bar.progress(50)
                
                # Call API
                start_time = time.time()
                response = requests.post(
                    f"{API_BASE_URL}/v1/report",
                    files=files,
                    data=data,
                    timeout=60
                )
                
                status_text.text("🏥 Coding Agent generating ICD/CPT codes...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                status_text.text("✅ Verification Agent checking for hallucinations...")
                progress_bar.progress(90)
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    progress_bar.progress(100)
                    status_text.empty()
                    
                    report_data = response.json()
                    report_data['generated_at'] = datetime.now().isoformat()
                    report_data['status'] = 'draft'
                    report_data['elapsed_time'] = elapsed_time
                    
                    # Store in session
                    st.session_state.reports.append(report_data)
                    st.session_state.current_report = report_data
                    
                    st.success(f"✅ Report generated successfully in {elapsed_time:.1f} seconds!")
                    
                    # Display report preview
                    st.markdown("---")
                    st.subheader("📄 Generated Report Preview")
                    
                    with st.expander("🔍 Findings", expanded=True):
                        for idx, finding in enumerate(report_data['findings'], 1):
                            st.markdown(f"**Finding {idx}:**")
                            st.write(finding['text'])
                            st.caption(f"Confidence: {finding['confidence']:.2%}")
                    
                    with st.expander("💡 Impression"):
                        st.write(report_data['impression'])
                    
                    with st.expander("🏥 Medical Codes"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**ICD-10 Codes:**")
                            for code in report_data['icd_codes']:
                                st.code(code)
                        with col2:
                            st.markdown("**CPT Codes:**")
                            for code in report_data['cpt_codes']:
                                st.code(code)
                    
                    if report_data['metadata'].get('verification_status'):
                        verification = report_data['metadata']['verification_status']
                        with st.expander("🔬 Verification Results"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Verified", "✅" if verification['is_verified'] else "❌")
                            with col2:
                                st.metric("Confidence", f"{verification['confidence']:.1%}")
                            with col3:
                                st.metric("Hallucination Score", f"{verification['hallucination_score']:.1%}")
                    
                    st.info("💡 Go to the **Review Reports** tab to edit and approve this report.")
                    
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The AI is taking longer than expected.")
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")
            finally:
                progress_bar.empty()
                status_text.empty()

with tab2:
    st.subheader("📋 Review Generated Reports")
    
    if not st.session_state.reports:
        st.info("No reports generated yet. Upload an image in the 'Generate Report' tab to get started.")
    else:
        # Report selection
        report_options = [
            f"Report {i+1} - {r['metadata']['study_id']} ({r['status']})"
            for i, r in enumerate(st.session_state.reports)
        ]
        
        selected_idx = st.selectbox(
            "Select Report to Review",
            range(len(report_options)),
            format_func=lambda i: report_options[i]
        )
        
        selected_report = st.session_state.reports[selected_idx]
        
        st.markdown("---")
        
        # Report editor
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Edit Report")
            
            edited_impression = st.text_area(
                "Impression",
                value=selected_report['impression'],
                height=150,
                key=f"impression_{selected_idx}"
            )
            
            edited_findings = st.text_area(
                "Findings",
                value=selected_report['findings'][0]['text'] if selected_report['findings'] else "",
                height=200,
                key=f"findings_{selected_idx}"
            )
        
        with col2:
            st.markdown("### ⚡ Actions")
            
            current_status = selected_report.get('status', 'draft')
            st.info(f"**Current Status:** {current_status.upper()}")
            
            if st.button("💾 Save Changes", use_container_width=True):
                selected_report['impression'] = edited_impression
                if selected_report['findings']:
                    selected_report['findings'][0]['text'] = edited_findings
                st.success("✅ Changes saved!")
            
            st.markdown("---")
            
            if current_status == 'draft':
                if st.button("✅ Approve Report", type="primary", use_container_width=True):
                    selected_report['status'] = 'approved'
                    selected_report['approved_at'] = datetime.now().isoformat()
                    st.success("✅ Report approved!")
                    st.rerun()
            
            if st.button("🗑️ Delete Report", use_container_width=True):
                st.session_state.reports.pop(selected_idx)
                st.success("🗑️ Report deleted!")
                st.rerun()
            
            st.markdown("---")
            
            # Metadata
            st.markdown("### 📊 Metadata")
            metadata = selected_report['metadata']
            st.caption(f"Study ID: {metadata['study_id']}")
            st.caption(f"Modality: {metadata['modality']}")
            st.caption(f"Processing: {metadata['processing_time_ms']}ms")
            if 'generated_at' in selected_report:
                st.caption(f"Generated: {selected_report['generated_at'][:19]}")

with tab3:
    st.subheader("📊 Analytics Dashboard")
    
    if not st.session_state.reports:
        st.info("No data available yet. Generate some reports to see analytics.")
    else:
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        
        # Prepare data
        reports_df = pd.DataFrame([
            {
                "study_id": r['metadata']['study_id'][:16],
                "modality": r['metadata']['modality'],
                "status": r.get('status', 'draft'),
                "processing_time_ms": r['metadata']['processing_time_ms'],
                "confidence": r['metadata']['verification_status']['confidence'] if r['metadata'].get('verification_status') else 0.92,
                "hallucination": r['metadata']['verification_status']['hallucination_score'] if r['metadata'].get('verification_status') else 0.08,
                "timestamp": r.get('generated_at', '')
            }
            for r in st.session_state.reports
        ])
        
        # Top-level metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Reports", len(st.session_state.reports))
        
        with col2:
            approved = sum(1 for r in st.session_state.reports if r.get('status') == 'approved')
            st.metric("Approved", approved, f"{approved/len(st.session_state.reports)*100:.0f}%")
        
        with col3:
            avg_time = reports_df['processing_time_ms'].mean()
            st.metric("Avg Time", f"{avg_time/1000:.1f}s")
        
        with col4:
            avg_confidence = reports_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        with col5:
            avg_hallucination = reports_df['hallucination'].mean()
            color = "inverse" if avg_hallucination < 0.1 else "normal"
            st.metric("Avg Hallucination", f"{avg_hallucination:.1%}", delta=f"{-avg_hallucination:.1%}", delta_color=color)
        
        st.markdown("---")
        
        # Charts in tabs
        chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
            "📈 Trends", "📊 Distribution", "🎯 Quality", "📋 Details"
        ])
        
        with chart_tab1:
            st.subheader("Processing Time Trends")
            
            # Processing time line chart
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=list(range(len(reports_df))),
                y=reports_df['processing_time_ms'] / 1000,
                mode='lines+markers',
                name='Processing Time',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=10)
            ))
            
            fig_time.update_layout(
                title="Processing Time per Report",
                xaxis_title="Report Number",
                yaxis_title="Time (seconds)",
                height=400,
                template="plotly_dark",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Confidence over time
            st.subheader("Confidence Trends")
            
            fig_conf = go.Figure()
            fig_conf.add_trace(go.Scatter(
                x=list(range(len(reports_df))),
                y=reports_df['confidence'] * 100,
                mode='lines+markers',
                name='Confidence',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=10),
                fill='tozeroy',
                fillcolor='rgba(44, 160, 44, 0.2)'
            ))
            
            fig_conf.add_trace(go.Scatter(
                x=list(range(len(reports_df))),
                y=reports_df['hallucination'] * 100,
                mode='lines+markers',
                name='Hallucination',
                line=dict(color='#d62728', width=3),
                marker=dict(size=10)
            ))
            
            fig_conf.update_layout(
                title="Quality Metrics Over Time",
                xaxis_title="Report Number",
                yaxis_title="Percentage (%)",
                height=400,
                template="plotly_dark",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_conf, use_container_width=True)
        
        with chart_tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Status Distribution")
                
                # Status pie chart
                status_counts = reports_df['status'].value_counts()
                fig_status = go.Figure(data=[go.Pie(
                    labels=status_counts.index,
                    values=status_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#2ca02c', '#ff7f0e'])
                )])
                
                fig_status.update_layout(
                    title="Report Status",
                    height=400,
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                st.subheader("Modality Distribution")
                
                # Modality bar chart
                modality_counts = reports_df['modality'].value_counts()
                fig_modality = go.Figure(data=[go.Bar(
                    x=modality_counts.index,
                    y=modality_counts.values,
                    marker=dict(color='#1f77b4')
                )])
                
                fig_modality.update_layout(
                    title="Reports by Modality",
                    xaxis_title="Modality",
                    yaxis_title="Count",
                    height=400,
                    template="plotly_dark"
                )
                
                st.plotly_chart(fig_modality, use_container_width=True)
            
            st.subheader("Confidence Distribution")
            
            # Histogram of confidence scores
            fig_hist = go.Figure(data=[go.Histogram(
                x=reports_df['confidence'] * 100,
                nbinsx=10,
                marker=dict(color='#2ca02c'),
                name='Confidence'
            )])
            
            fig_hist.update_layout(
                title="Confidence Score Distribution",
                xaxis_title="Confidence (%)",
                yaxis_title="Number of Reports",
                height=400,
                template="plotly_dark"
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with chart_tab3:
            st.subheader("Quality Assurance Metrics")
            
            # Quality score calculation
            quality_scores = []
            for idx, row in reports_df.iterrows():
                # Quality score: high confidence + low hallucination + reasonable time
                time_score = max(0, 1 - (row['processing_time_ms'] / 30000))  # Penalize >30s
                conf_score = row['confidence']
                hal_penalty = 1 - row['hallucination']
                
                quality = (conf_score * 0.5 + hal_penalty * 0.3 + time_score * 0.2) * 100
                quality_scores.append(quality)
            
            reports_df['quality_score'] = quality_scores
            
            # Quality gauge
            avg_quality = reports_df['quality_score'].mean()
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg_quality,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Quality Score"},
                delta={'reference': 85},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 90], 'color': "lightgreen"},
                        {'range': [90, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 85
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=400,
                template="plotly_dark"
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Quality breakdown
            col1, col2, col3 = st.columns(3)
            
            with col1:
                excellent = sum(1 for q in quality_scores if q >= 90)
                st.metric("Excellent (≥90%)", excellent, f"{excellent/len(quality_scores)*100:.0f}%")
            
            with col2:
                good = sum(1 for q in quality_scores if 75 <= q < 90)
                st.metric("Good (75-90%)", good, f"{good/len(quality_scores)*100:.0f}%")
            
            with col3:
                needs_review = sum(1 for q in quality_scores if q < 75)
                st.metric("Needs Review (<75%)", needs_review, f"{needs_review/len(quality_scores)*100:.0f}%")
        
        with chart_tab4:
            st.subheader("Detailed Report Table")
            
            # Enhanced report table
            display_df = reports_df.copy()
            display_df['processing_time_s'] = (display_df['processing_time_ms'] / 1000).round(1)
            display_df['confidence_%'] = (display_df['confidence'] * 100).round(1)
            display_df['hallucination_%'] = (display_df['hallucination'] * 100).round(1)
            display_df['quality_%'] = display_df['quality_score'].round(1)
            
            st.dataframe(
                display_df[[
                    'study_id', 'modality', 'status', 
                    'processing_time_s', 'confidence_%', 
                    'hallucination_%', 'quality_%'
                ]],
                use_container_width=True,
                height=400
            )
            
            # Export option
            if st.button("📥 Export Data as CSV"):
                csv = reports_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="luminamed_reports.csv",
                    mime="text/csv"
                )

