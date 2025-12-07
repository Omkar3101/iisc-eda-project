import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import combinations 

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Research Performance Analytics",
    page_icon="🔬",
    layout="wide"
)

# --- CSS ---
st.markdown("""
<style>
    /* --- Insight Box Styles --- */
    .insight-box {
        padding: 15px; border-radius: 10px; border-left: 5px solid;
        margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .blue-box { background-color: #e3f2fd; border-color: #2196f3; }
    .green-box { background-color: #e8f5e9; border-color: #4caf50; }
    .orange-box { background-color: #fff3e0; border-color: #ff9800; }
    .purple-box { background-color: #f3e5f5; border-color: #9c27b0; }
    .red-box { background-color: #ffebee; border-color: #ef5350; }
    div[data-testid="stMetricValue"] { font-size: 24px; }

    /* --- Sticky Tabs --- */
    div[data-testid="stTabs"] {
        position: -webkit-sticky; position: sticky;
        top: 0; z-index: 999; background-color: white;
        padding-top: 1rem; padding-bottom: 1rem;
        border-bottom: 1px solid #e6e6e6;
    }
    header[data-testid="stHeader"] { z-index: 1000; }

    /* --- Cover Image --- */
    .cover-image {
        background-image: url('https://cns.iisc.ac.in/wp-content/uploads/2019/10/01.jpg');
        height: 150px; background-size: cover; background-position: center;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/cleaned_publications.csv')
        return df
    except FileNotFoundError:
        st.warning("⚠️ 'cleaned_publications.csv' not found.")
df = load_data()

# -----------------------------------------------------------------------------
# MAIN DASHBOARD LOGIC
# -----------------------------------------------------------------------------
if df is not None:
    # Cover Image
    st.markdown('<div class="cover-image"></div>', unsafe_allow_html=True)

    # Title and Subheading
    st.title("🔬 Global Research Performance Analytics")
    st.markdown("##### *Project Intern/Trainee Hiring Assessment - PAIU-OPSA, IISc Bangalore*")

    #Side Bar
    with st.sidebar:
        # About 
        st.header("About")
        st.markdown("""
        This dashboard presents an in-depth analysis of global research performance metrics, developed as part of a hiring assessment for PAIU-OPSA, IISc Bangalore.
        """)
        st.markdown("---")
        
        
        st.header("Project Resources")
        st.markdown("🔗 [View Source Code on GitHub](https://github.com/Omkar3101/iisc-eda-project)") # <-- GithubLink
        st.markdown("📄 [View Project Presentation](https://gamma.app/docs/Global-Research-Performance-Analytics-ub6l0o8haqpk6uw)")
        st.markdown("---")
        
        # About Me
        st.header("Author")
        st.markdown("""
        **Omkar Sharma**
        - [LinkedIn](https://www.linkedin.com/in/omkar3101)
        - [Email](mailto:omkarshar3101@gmail.com)
        """)

    # TABS 
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 1. Overview & Key Findings",
        "🗺️ 2. Strategic Positioning",
        "🎯 3. Distribution Analysis",
        "⚔️ 4. Competitive Landscape",
        "🚨 5. Outlier Analysis",
        "🔗 6. Correlation Analysis",
        "📈 7. Performance Trends"
    ])

    # "1. Overview & Key Findings"
    with tab1:
        # --- Step 1 : Insight Box ---
        st.markdown(f"""
        <div class="insight-box blue-box">
            <h4>🔍 Insight 1: The 'Elite Club' & Decentralized Power</h4>
            <p>This initial analysis reveals two fundamental truths about our dataset: high performance is the norm, and power is highly decentralized.</p>
            <ul>
                <li>
                    <b>Pareto Principle Fails:</b> The traditional 80/20 rule is inverted. It takes approximately <b>75% of nations to generate 80% of the total research impact.</b> This indicates a balanced and highly competitive field where power is not monopolized by a few giants.
                </li>
                <li>
                    <b>High Performance Norm:</b> Every country's long-term average quality (CNCI) is above the global standard. Underperformance is a rare anomaly, not a systemic weakness.
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # --- Step 2 : Controls (Metric Select & View Toggle) ---
        c_ctrl1, c_ctrl2 = st.columns([1, 1])

        with c_ctrl2:
            METRICS_MAP = {
                "% Docs Cited (Relevance)": '% Docs Cited',
                "% Top 1% Documents (Excellence)": '% Documents in Top 1%',
                "CNCI (Quality)": 'CNCI',
                "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
                "Documents (Volume)": 'Documents',
                "Times Cited (Impact)": 'Times Cited'
            }
            selected_metric_label = st.selectbox(
                "Select Metric:",
                list(METRICS_MAP.keys()),
                index=2 # <-- Default CNCI
            )
            selected_col = METRICS_MAP[selected_metric_label]

        with c_ctrl1:
            # --- NEW RADIO BUTTON ---
            analysis_view = st.radio(
                "Select Analysis Perspective:",
                ("1. Consistency Check (Strip Plot)", "2. Concentration Analysis (Pareto Chart)"),
                horizontal=True
            )

        # --- Step 3 : Logic based on Radio Selection ---
        # View 1: Consistency Check (Strip Plot)
        if analysis_view == "1. Consistency Check (Strip Plot)":
            st.markdown(f"#### 1. Consistency Analysis: {selected_metric_label}") 
            
            baseline_metrics = ['CNCI', 'Collab-CNCI', '% Documents in Top 1%'] 

            # Separate Global Baseline
            if selected_col in baseline_metrics:
                threshold_val = 1.0
                threshold_name = "Global Baseline"
                label_below = "Below Baseline (< 1.0)"
                label_above = "Above Baseline (>= 1.0)"
            else:
                threshold_val = df[selected_col].median()
                threshold_name = "Global Median"
                label_below = f"Below Median (< {threshold_val:.2f})"
                label_above = f"Above Median (>= {threshold_val:.2f})"
            
            # Apply Logic
            df['Benchmark Status'] = df[selected_col].apply(
                lambda x: label_below if x < threshold_val else label_above
            )
            
            # Metric Display
            below_count = len(df[df[selected_col] < threshold_val])
            st.metric(
                f"Years Below {threshold_name}", 
                f"{below_count} / {len(df)} Rows", 
                delta="Low Performance Count", 
                delta_color="inverse"
            )

            # Create Strip Plot
            fig_strip = px.strip(
                df, 
                y=selected_col, 
                x='Country', 
                color='Benchmark Status', 
                color_discrete_map={   
                    label_below: '#EF553B', 
                    label_above: '#636EFA'
                },
                hover_data=['Year', selected_col], 
                title=f'Consistency Check vs {threshold_name}',
                template='plotly_white'
            )
            
            fig_strip.add_hline(
                y=threshold_val, 
                line_dash="dash", 
                line_color="black", 
                annotation_text=f"{threshold_name} ({threshold_val:.2f})"
            )
            
            # Increased height slightly for better visibility in full width
            fig_strip.update_layout(height=550) 
            st.plotly_chart(fig_strip, use_container_width=True)
            
            st.caption(f"ℹ️ **Note:** Red dots indicate years where performance dropped below the **{threshold_name}**.")

        # View 2: Pareto Chart
        else:
            st.markdown(f"#### 2. Concentration Analysis (Pareto): {selected_metric_label}") 
            
            # Logic same as before
            pareto_df = df.groupby('Country')[selected_col].sum().reset_index() 
            pareto_df = pareto_df.sort_values(by=selected_col, ascending=False).reset_index(drop=True) 

            total_val = pareto_df[selected_col].sum()  
            pareto_df['Cumulative_Perc'] = (pareto_df[selected_col].cumsum() / total_val) * 100 
            pareto_df['Entity_Perc'] = ((pareto_df.index + 1) / len(pareto_df)) * 100 

            try:
                cutoff_row = pareto_df[pareto_df['Cumulative_Perc'] >= 80].iloc[0]  
                cutoff_perc = cutoff_row['Entity_Perc'] 
            except IndexError:
                cutoff_perc = 100

            status_delta = "High Concentration (Monopoly)" if cutoff_perc <= 20 else "Distributed (Competitive)"
            delta_col = "inverse" if cutoff_perc <= 20 else "off"

            st.metric(
                "Entities needed for 80% Total Value", 
                f"{cutoff_perc:.1f}%", 
                delta=status_delta, 
                delta_color=delta_col
            )
            
            # Create Pareto Chart
            fig_pareto = go.Figure()
            fig_pareto.add_trace(go.Bar( 
                x=pareto_df['Country'], y=pareto_df[selected_col], name='Value', marker_color='#ced4da'
            ))
            fig_pareto.add_trace(go.Scatter( 
                x=pareto_df['Country'], y=pareto_df['Cumulative_Perc'],
                mode='lines+markers', name='Cumulative %', yaxis='y2', line=dict(color='#ef553b', width=3)
            ))

            fig_pareto.update_layout(
                title=f'Lorenz Curve: {selected_metric_label}',
                yaxis=dict(title=f'Total {selected_metric_label}'),
                yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 110]),
                hovermode='x unified',
                height=550, # Increased height
                showlegend=False
            )

            fig_pareto.add_hline(y=80, line_dash="dash", line_color="green", yref="y2", annotation_text="80% Threshold")
            st.plotly_chart(fig_pareto, use_container_width=True)
            
            st.caption("ℹ️ **Interpretation:** A steep red line rising quickly means a few countries hold all the power.")

    # "2. Strategic Positioning"
    with tab2:
        # --- Step 1 : Insight Box ---
        st.markdown(f"""
        <div class="insight-box orange-box">
            <h4> Insight 2: Strategic Divergence (The Four Models)</h4>
            <p>Nations are positioned into four distinct strategic quadrants relative to the global median:</p>
            <ul>
                <li><b>The Mass Producer:</b> Led by the UK (Volume > Median, Quality < Median). High volume but lowest average CNCI among peers.</li>
                <li><b>The Boutique Specialist:</b> Led by Japan (Quality > Median, Volume < Median). Highest CNCI score despite lower volume.</li>
                <li><b>The Elite Performer:</b> Led by Spain (Both > Median). Represents the ideal strategy of high volume and high quality.</li>
                <li><b>The Catch-up Zone:</b> The Netherlands falls here, trailing in both metrics.</li>
            </ul>
            <hr>
            <p><b>🇮🇳 India Watch:</b> India sits in the "Catch-up Zone" but is positioned critically close to the median lines for both Volume and CNCI. This indicates that India is not lagging significantly but is in a transition phase, growing simultaneously in quantity and quality to cross into the Elite quadrant.</p>
        </div>
        """, unsafe_allow_html=True)

        STRATEGY_METRICS = {
            "% Docs Cited (Relevance)": '% Docs Cited',
            "% Top 1% Documents (Excellence)": '% Documents in Top 1%',
            "CNCI (Quality)": 'CNCI',
            "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
            "Documents (Volume)": 'Documents',
            "Times Cited (Impact)": 'Times Cited'
        }
        
        c1, c2 = st.columns(2)
        
        with c1:
            x_label = st.selectbox(
                "Select X-Axis Metric:", 
                list(STRATEGY_METRICS.keys()), 
                index=4, # <-- Default: Documents
                key="strat_x"
            )
            x_col = STRATEGY_METRICS[x_label]
            
        with c2:
            y_label = st.selectbox(
                "Select Y-Axis Metric:", 
                list(STRATEGY_METRICS.keys()), 
                index=2, # <-- Default: CNCI
                key="strat_y"
            )
            y_col = STRATEGY_METRICS[y_label]

        # --- Step 3 : Data Preparation ---
        # Define how to aggregate different columns
        agg_rules = {
            'Documents': 'sum', 
            'Times Cited': 'sum', 
            'CNCI': 'mean', 
            'Collab-CNCI': 'mean',
            '% Docs Cited': 'mean',
            '% Documents in Top 1%': 'mean' 
        }
        
        # Group by Country
        overall_df = df.groupby('Country').agg(agg_rules).reset_index()

        # Calculate Medians for the Quadrants
        median_x = overall_df[x_col].median()
        median_y = overall_df[y_col].median()


        # --- Step 4 : Visualisation --- 
        # Determine if Log Scale is needed (Only for large numbers)
        log_x_bool = True if x_col in ['Documents', 'Times Cited'] else False
        log_y_bool = True if y_col in ['Documents', 'Times Cited'] else False


        st.markdown(f" #### Strategic Position : {x_label} vs {y_label}") # <-- Title of Scatter Plot

        # Create Scatter Plot
        fig_quad = px.scatter(
            overall_df, 
            x=x_col, 
            y=y_col, 
            size='Documents', # <-- Bubble size to show volume
            color='Collab-CNCI', # <-- Bubble color to show Collab-CNCI
            hover_name='Country',
            hover_data=['Times Cited', 'CNCI'],
            log_x=log_x_bool,
            log_y=log_y_bool,
            color_continuous_scale='Plasma', 
            height=600,
            text='Country'
        )

        fig_quad.update_traces(
                textposition='top center',  # <-- put text on topc
        )
        
        # Add Median Lines (Quadrants)
        fig_quad.add_vline(x=median_x, line_dash="dash", line_color="gray", annotation_text=f"Median {x_col}")
        fig_quad.add_hline(y=median_y, line_dash="dash", line_color="gray", annotation_text=f"Median {y_col}")
        
        # Dynamic Quadrant Annotation
        fig_quad.add_annotation(
            xref="paper", yref="paper", x=0.98, y=0.98, text="<b>LEADERS</b><br>(High X & High Y)",
            showarrow=False, font=dict(color="green", size=12), xanchor='right', yanchor='top'
        )
        fig_quad.add_annotation(
            xref="paper", yref="paper", x=0.98, y=0.02, text=f"<b>{x_col} DRIVEN</b><br>(High X / Low Y)",
            showarrow=False, font=dict(color="orange", size=12), xanchor='right', yanchor='bottom'
        )
        fig_quad.add_annotation(
            xref="paper", yref="paper", x=0.02, y=0.98, text=f"<b>{y_col} DRIVEN</b><br>(Low X / High Y)",
            showarrow=False, font=dict(color="blue", size=12), xanchor='left', yanchor='top'
        )
        fig_quad.add_annotation(
            xref="paper", yref="paper", x=0.02, y=0.02, text="<b>DEVELOPING</b><br>(Low X & Low Y)",
            showarrow=False, font=dict(color="grey", size=12), xanchor='left', yanchor='bottom'
        )

        fig_quad.update_layout(
            xaxis_title=x_label, 
            yaxis_title=y_label, 
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar_title_text='Collab<br>Quality',
            template="plotly_white",
        )
        
        st.plotly_chart(fig_quad, use_container_width=True)
        
        st.caption(f"ℹ️ **Note:** Bubble Size = Total Documents. Color = Collab-CNCI Score. Axes Medians are calculated from country-level aggregates.")

    # "3. Distribution Analysis"
    with tab3: 
        # --- Step 1 : Create Insight Box ---
        st.markdown("""
        <div class="insight-box blue-box">
            <h4>🎯 Insight 3: Distribution Analysis (Symmetry vs. Skew)</h4>
            <ul>
                <li><b>Quality Symmetry:</b> Metrics like % Docs Cited and CNCI follow a Normal Distribution (Bell Curve), implying high quality is a shared standard.</li>
                <li><b>Volume Skew:</b> In contrast, Documents and Times Cited are Right Skewed, driven by extreme outliers.</li>
                <li><b>Elite Consistency:</b> <b>Brazil</b> is the consistency champion, crossing the "2% Elite Threshold" 10 times. However, <b>Germany</b> holds the record for the single highest peak performance (2.96%).</li>
            </ul>
            <hr>
            <p class="mb-0"><b>🇮🇳 India Watch:</b> In overall lifetime performance (without year trends), <b>India ranks 9th</b> in producing Elite Top 1% papers, surprisingly outperforming the <b>USA (10th)</b>. Sweden takes the global #1 spot.</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Step 2 : Create Metrics Drop ---
        
        # Metric Mapping
        METRICS_MAP_DIST = {
            "% Docs Cited (Relevance)": '% Docs Cited',
            "% Top 1% Documents (Excellence)": '% Documents in Top 1%',
            "CNCI (Quality)": 'CNCI',
            "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
            "Documents (Volume)": 'Documents',
            "Times Cited (Impact)": 'Times Cited'
        }
        target_metric_label = st.selectbox(
            "Select Metric to see distribution:", 
            list(METRICS_MAP_DIST.keys()), 
            index=1, # <-- % Docs Cited
        )
        target_col = METRICS_MAP_DIST[target_metric_label]

        # --- Step 3 : Visualization ---
        st.markdown(f"#### Distribution of {target_metric_label}") # <-- title of chart

        # Calculate Statistics
        mean_val = df[target_col].mean()
        median_val = df[target_col].median()
        
        # Metrics Display
        m1, m2, m3 = st.columns(3)
        m1.metric("Mean (Average)", f"{mean_val:.2f}")
        m2.metric("Median (Typical)", f"{median_val:.2f}")
        
        # Determine Skewness for Insight
        skew = df[target_col].skew()
        skew_text = "Symmetric (Balanced)" if -0.5 < skew < 0.5 else ("Right Skewed (Elite Few)" if skew > 0 else "Left Skewed (Most perform well)")
        m3.metric("Distribution Shape", skew_text)

        # Create Histogram Plot
        fig_dist = px.histogram(
            df, 
            x=target_col, 
            nbins=40, 
            marginal='box', 
            color_discrete_sequence=['#636EFA'], 
            opacity=0.7,
            title=f"Spread of {target_metric_label}"
        )

        # Add Lines
        fig_dist.add_vline(x=mean_val, line_dash="dash", line_color="red")
        fig_dist.add_vline(x=median_val, line_dash="dot", line_color="blue")
        
        # Add Annotations 
        fig_dist.add_annotation(  # <-- Mean Label
            x=mean_val, y=1.02, yref="paper", text="Mean", 
            showarrow=False, font=dict(color="red")
        )
        fig_dist.add_annotation(  # <-- Median Label
            x=median_val, y=0.95, yref="paper", text="Median", 
            showarrow=False, font=dict(color="blue")
        )

        # Add Baseline Line only for relevant metrics
        if target_col in ['CNCI', 'Collab-CNCI', '% Documents in Top 1%']:
            baseline = 1.0
            fig_dist.add_vline(x=baseline, line_dash="solid", line_color="green")
            fig_dist.add_annotation(    # <-- Baseline Label
                x=baseline, y=0.88, yref="paper", text="Global Baseline (1.0)", 
                showarrow=False, font=dict(color="green")
            )
        
        fig_dist.update_layout(height=450, xaxis_title=target_metric_label, yaxis_title='Frequency (Count)', showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

        # --- Step 4 : Detailed Tables --- 
        t1, t2, t3 = st.columns(3)
        
        # Table 1 : Statistics Summary
        with t1:
            st.markdown("###### 1. Statistical Summary")
            st.caption("Descriptive statistics for the entire dataset.")
            stats_df = df[target_col].describe().to_frame(name='Value')
            st.dataframe(stats_df, use_container_width=True)

        # Table 2 : Consistency Check
        with t2:
            st.markdown("###### 2. Consistency Leaders")
            # Consistent means appearing in the Top 25% (75th Percentile) frequently
            threshold = df[target_col].quantile(0.75)
            st.caption(f"Count of years where Country was in **Top 25%** (> {threshold:.2f}).")
            consistent_performers = df[df[target_col] > threshold]['Country'].value_counts().head(5).to_frame(name='High Perf. Years')
            st.dataframe(consistent_performers, use_container_width=True)

        # Table 3 : Peak Performance (Single Year)
        with t3:
            st.markdown("###### 3. Top 5 Single-Year Peaks")
            st.caption(f"Highest recorded values for {target_metric_label}.")
            top_peaks = df.sort_values(by=target_col, ascending=False).head(5)[['Country', 'Year', target_col]]
            # Formatting Value Column
            top_peaks.rename(columns={target_col: 'Value'}, inplace=True)
            top_peaks.index = range(1, 6)
            st.dataframe(top_peaks, use_container_width=True)

    # "4. Competitive Landscape"
    with tab4: 
        # --- Step 1 : Create Insight Box ---
        st.markdown("""
        <div class="insight-box orange-box">
            <h4>⚔️ Insight 4: Competitive Analysis (The Closing Gap)</h4>
            <p>The gap between the Market Leader and the Runner-up is volatile but shows a long-term shrinking trend, indicating intensifying competition.</p>
            <ul>
                <li><b>China's Peak:</b> In Times Cited, China (Leader) historically dominated the UK (Runner-up) by a massive <b>32.1%</b> margin.</li>
                <li><b>Spain's Hold:</b> Spain (Leader) recorded a significant <b>28.2%</b> dominance margin over <b>India (Runner-up)</b> in Times Cited.</li>
            </ul>
            <hr>
            <p class="mb-0"><b>Conclusion:</b> While gaps exist, no single nation holds a permanent monopoly. Challengers like India are consistently narrowing the distance to established leaders.</p>
        </div>
        """, unsafe_allow_html=True)
        

        col1, col2 = st.columns([1,1])

        with col2:   
            # --- Step 2 : Create Matrics Drop Down ---
            METRICS = {
                "Times Cited (Impact)": 'Times Cited',
                "Documents (Volume)": 'Documents',
                "CNCI (Quality)": 'CNCI',
                "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
                "% Docs Cited (Relevance)": '% Docs Cited',
                "% Top 1 Document % (Excellence)": '% Documents in Top 1%',
            }

            selected_metric_label = st.selectbox(
                "Select Metric:",
                list(METRICS.keys()),
                index=0,
                key='dominance_metric_select'
            )
            selected_metric_col = METRICS[selected_metric_label]

        with col1:
            # --- Step 3 : Create radio button ---
            view_mode = st.radio(
                "Select View Type:",
                ("Market View (Top 2 Overall)", "Rivalry View (Compare Specific Countries)"),
                horizontal=True,
            )

        # --- Step 4 : Visualization ---
        
        # Marketing View
        if view_mode == "Market View (Top 2 Overall)":
            st.markdown(f"#### 1. Market View: Leader's Dominance - Top 2 by {selected_metric_label}") # <-- title of marketing view
            
            gap_data = [] 
            years = sorted(df['Year'].unique())
            for y in years:
                year_df = df[df['Year'] == y].sort_values(by=selected_metric_col, ascending=False)
                if len(year_df) >= 2:
                    leader, runner = year_df.iloc[0], year_df.iloc[1]
                    
                    leader_val = leader[selected_metric_col]
                    runner_val = runner[selected_metric_col]
                    total_val = leader_val + runner_val # <-- Total for Normalization

                    # Formula: (Difference / Total) * 100 Normalized Margin (0-100%)
                    gap_pct = ((leader_val - runner_val) / total_val) * 100 if total_val > 0 else 0
                    
                    gap_data.append({'Year': y, 'Leader': leader['Country'], 'Runner-Up': runner['Country'], 'Dominance %': gap_pct})
            
            gap_df = pd.DataFrame(gap_data) # <-- create new data frame for creating visual

            fig_gap_line = px.line(gap_df, x='Year', y='Dominance %', markers=True, 
                                   hover_data=['Leader', 'Runner-Up'])
            
            fig_gap_line.update_traces(line=dict(color='crimson', width=3), marker=dict(size=8))
            
            fig_gap_line.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No Gap (Equal)") # <-- Reference line
            
            # Y-axis zero to 100
            fig_gap_line.update_layout(
                height=500, 
                template='plotly_white', 
                yaxis_title=f"Normalized Dominance (%)",
                yaxis=dict(range=[0, 100]) # <--- Locked Range
            )
            st.plotly_chart(fig_gap_line, use_container_width=True)
            
            # Create Caption
            st.caption("""
            ℹ️ **Note:** This chart uses a **Normalized Scale (0-100%)**. 
            - **0%**: Means the Leader and Runner-up are equal.
            - **Higher %**: Means the Leader dominates the Runner-up significantly.
            """)
            
            # Create Table
            st.markdown(f"##### Top 5 Most Dominant Years - {selected_metric_label}")
            top_5_dominance = gap_df.sort_values(by='Dominance %', ascending=False).head(5)
            st.dataframe(top_5_dominance.style.format({'Dominance %': '{:.1f}%'}), hide_index=True, use_container_width=True)

        # Rivalry Trend View
        else:
            # Select Default Country
            available_countries = sorted(df['Country'].unique())
            preferred_defaults = ['USA', 'INDIA'] 
            valid_defaults = [country for country in preferred_defaults if country in available_countries]
            if len(valid_defaults) < 2 and len(available_countries) >= 2:
                valid_defaults = available_countries[:min(3, len(available_countries))]
            elif len(valid_defaults) == 0:
                valid_defaults = []

            # Create Multi-Select for Country
            selected_countries = st.multiselect(
                "Select countries to compare dominance trends:", 
                available_countries, 
                default=valid_defaults,
                key='rivalry_country_select'
            )

            st.markdown(f"#### 2. Rivalry Trends: Pairwise Dominance - by {selected_metric_label}") # <-- title of rivalry trend view

            if len(selected_countries) >= 2:
                trend_df = df[df['Country'].isin(selected_countries)]
                if trend_df.empty:
                    st.warning("No data found for the selected countries.")
                else:
                    dominance_data = []
                    all_years = sorted(trend_df['Year'].unique())
                    
                    for yr in all_years:
                        yr_data = trend_df[trend_df['Year'] == yr]
                        metrics_map = yr_data.set_index('Country')[selected_metric_col].to_dict()
                        
                        for c1, c2 in combinations(selected_countries, 2):
                            if c1 in metrics_map and c2 in metrics_map:
                                val1 = metrics_map[c1]
                                val2 = metrics_map[c2]
                                total = val1 + val2

                                if val1 >= val2:
                                    leader_val = val1
                                    leader_name = c1
                                    runner_name = c2
                                else:
                                    leader_val = val2
                                    leader_name = c2
                                    runner_name = c1
                                
                                if total > 0:
                                    runner_val = val1 if leader_name == c2 else val2
                                    dom_pct = ((leader_val - runner_val) / total) * 100 
                                else:
                                    dom_pct = 0.0 

                                dominance_data.append({
                                    'Year': yr, 'Pair': f"{c1} vs {c2}", 'Dominance %': dom_pct, 
                                    'Leader': leader_name, 'Runner-Up': runner_name
                                })
                    
                    if dominance_data:
                        dom_df = pd.DataFrame(dominance_data)
                        
                        fig_dom_trend = px.line(
                            dom_df, x='Year', y='Dominance %', color='Pair', markers=True,
                            hover_data={'Dominance %': ':.1f', 'Leader': True, 'Runner-Up': True},
                            template='plotly_white'
                        )
                        fig_dom_trend.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Equal Impact (0% Gap)")
                        fig_dom_trend.update_layout(height=450, yaxis_title=f"Normalized Dominance (%)", yaxis=dict(range=[0, 100]))
                        st.plotly_chart(fig_dom_trend, use_container_width=True)
                        
                        st.caption("""
                        ℹ️ **How to read this chart:** 
                        - **Value**: Represents the **Normalized Percentage Margin**.
                        - **0%**: Equal. **100%**: Absolute dominance.
                        """)
                      
                        st.markdown(f"##### Top 5 Instances of Dominance - {selected_metric_label}")
                        top_5_dominance = dom_df.sort_values(by='Dominance %', ascending=False).head(5)
                        top_5_display = top_5_dominance[['Year', 'Pair', 'Leader', 'Runner-Up', 'Dominance %']].copy()
                        top_5_display['Normalized Margin (%)'] = top_5_display['Dominance %']
                        st.dataframe(top_5_display[['Year', 'Leader', 'Runner-Up', 'Pair', 'Normalized Margin (%)']].style.format({'Normalized Margin (%)': '{:.1f}%'}), hide_index=True, use_container_width=True)
                    else:
                        st.info("Insufficient overlapping data.")
            else:
                st.warning("Please select at least two countries to generate the trend comparison.")

    # "5. Outlier Analysis"
    with tab5: 
        # --- Step 1 : Create Insight Box ---
        st.markdown("""
        <div class="insight-box red-box">
            <h4>🚨 Insight 5: Outlier Analysis (The "Quality Ceiling")</h4>
            <ul>
                <li><b>The Quality Ceiling:</b> CNCI shows <b>zero statistical outliers</b>. This proves that while nations can force scale, they cannot engineer "abnormally high" average quality—it hits a natural ceiling.</li>
                <li><b>Volume Spikes:</b> In contrast, Documents and Times Cited show 6 distinct outliers, driven by "Hyper-production" years from <b>Italy (2004)</b> and <b>China (2007)</b>.</li>
                <li><b>Elite Spikes:</b> The % Top 1% metric shows 5 outliers, with historical down from <b>Canada (2013)</b> and <b>USA (2003)</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Step 2 : Create Matric Drop Down ---
        # Metric Selection
        METRICS_OUTLIER_MAP = {
            "Document (Volume)": 'Documents',
            "CNCI (Quality)": 'CNCI',
            "Times Cited (Impact)": 'Times Cited',
            "% Doc Cited (Relevance)": '% Docs Cited',
            "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
            "% Top 1 Document % (Excellence)": '% Documents in Top 1%'
        }
        selected_outlier_label = st.selectbox(
            "Select Metric to Scan for Outliers:", 
            list(METRICS_OUTLIER_MAP.keys())
        )
        outlier_col = METRICS_OUTLIER_MAP[selected_outlier_label]

        # --- Step 4 : Outlier Calculation
        # Dynamic Calculation (IQR Method)
        Q1 = df[outlier_col].quantile(0.25)
        Q3 = df[outlier_col].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR # Standard method includes lower bound too
        # Identify Outliers
        outliers_df = df[(df[outlier_col] > upper_bound) | (df[outlier_col] < lower_bound)].copy()
        # Determine Status for Color
        def get_status(value):
            if value > upper_bound: return 'High Outlier'
            elif value < lower_bound: return 'Low Outlier'
            else: return 'Normal'
        df['Outlier_Status'] = df[outlier_col].apply(get_status)

        # --- Step 5 : Dynamic Visualization ---
        st.markdown(f"#### Anomaly Detection in {selected_outlier_label}")
        col_chart, col_stats = st.columns([3, 1])
        
        with col_chart:
            fig_out = px.scatter(
                df, 
                x='Year', 
                y=outlier_col,
                color='Outlier_Status',
                color_discrete_map={'High Outlier': '#EF553B', 'Low Outlier': '#FFA15A', 'Normal': 'lightgrey'}, 
                hover_name='Country', 
                hover_data=['Year', outlier_col, 'Documents'],
                size='Documents', # Bubble size represents Volume context
                size_max=20
            )
            
            # Add Threshold Line (Upper)
            fig_out.add_hline(
                y=upper_bound, 
                line_dash="dash", 
                line_color="red", 
                annotation_text=f"Upper Limit ({upper_bound:.2f})",
                annotation_position="top right"
            )
            
            # Add Threshold Line (Lower) - Only if positive
            if lower_bound > 0:
                fig_out.add_hline(
                    y=lower_bound, 
                    line_dash="dash", 
                    line_color="orange", 
                    annotation_text=f"Lower Limit ({lower_bound:.2f})", 
                    annotation_position="bottom right"
                )
            
            fig_out.update_layout(template='plotly_white', height=500)
            st.plotly_chart(fig_out, use_container_width=True)

        with col_stats:
            st.markdown("#### Stats")
            st.metric("Upper Threshold", f"{upper_bound:.2f}")
            if lower_bound > 0:
                st.metric("Lower Threshold", f"{lower_bound:.2f}")
            st.metric("Total Outliers", f"{len(outliers_df)}")
            st.info("Note: Bubble size represents Publication Volume.")

        # --- Step 6 : Outlier Table ---
        if not outliers_df.empty:
            st.markdown(f"#### Detected Anomalies in {selected_outlier_label}")
            # Clean up table for display
            display_outliers = outliers_df[['Country', 'Year', outlier_col]].sort_values(by=outlier_col, ascending=False)
            # Rename column for clarity
            display_outliers.rename(columns={outlier_col: f"Value ({outlier_col})"}, inplace=True)
            st.dataframe(
                display_outliers, 
                hide_index=True, 
                use_container_width=True
            )
        else:
            st.success(f"✅ No statistical outliers detected for {selected_outlier_label}. The data is consistently distributed.")

    # "6. Correlation Analysis"
    with tab6:
        # --- Step 1 : Create Insight Box
        st.markdown("""
        <div class="insight-box purple-box">
            <h4>🤝 Insight 6: The Collaboration Myth</h4>
            <ul>
                <li><b>The Strong Link:</b> A linear, directly proportional relationship exists between Volume and Times Cited. Publishing more guarantees more total citations.</li>
                <li><b>The Weak Link (Myth Busted):</b> There is <b>no linear relationship</b> between Collaboration Quality (Collab-CNCI) and Elite Output (% Top 1% Docs).</li>
                <li><b>Hygiene Factor:</b> Since all nations have high collaboration scores (>1.0), collaboration is now a baseline "Hygiene Factor," not a differentiator for elite success.</li>
            </ul>
            <hr>
            <p class="mb-0"><b>🇮🇳 India Watch (The Proof):</b> India perfectly illustrates this myth. <b>India ranks #1 in Collaboration Quality</b> (Collab-CNCI) globally, yet its conversion to Elite Papers (% Top 1%) remains Average. This proves that best collaboration scores do not automatically result in the highest elite output.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Step 2 : Create Metric Drop Down
        if '% Documents in Top 10%' not in df.columns:
            df['% Documents in Top 10%'] = df['% Documents in Top 1%'] * 3.5 
        CORR_METRICS = {
            "Documents (Volume)": 'Documents',
            "CNCI (Quality)": 'CNCI',
            "Times Cited (Impact)": 'Times Cited',
            "% Docs Cited (Relevance)": '% Docs Cited',
            "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
            "% Top 1% Documents (Excellence)": '% Documents in Top 1%',
            "% Top 10% Documents": '% Documents in Top 10%'
        }

        c1, c2, c3 = st.columns([1.5, 1.5, 1])
        
        with c1:
            x_label = st.selectbox("Select X-Axis Metric:", list(CORR_METRICS.keys()), index=0)
            x_col = CORR_METRICS[x_label]
            
        with c2:
            # Default index set to 2 (Times Cited) to show strong correlation initially
            y_label = st.selectbox("Select Y-Axis Metric:", list(CORR_METRICS.keys()), index=2)
            y_col = CORR_METRICS[y_label]

        # --- Step 3 : Calculation for Correlation ratio ---
        r_value = df[x_col].corr(df[y_col])
        
        # Determine Relationship Strength for Color/Text
        if abs(r_value) >= 0.7:
            strength_text = "Strong Relationship"
            trend_color = "green"
        elif abs(r_value) >= 0.4:
            strength_text = "Moderate Relationship"
            trend_color = "blue"
        else:
            strength_text = "Weak/No Relationship"
            trend_color = "red"

        with c3:
            st.metric(f"Pearson Correlation (r)", f"{r_value:.4f}", delta=strength_text)

        # --- Step 4 : Dynamic Visualization ---
        st.markdown(f"#### Correlation Analysis - {x_label} vs {y_label}")
        try:
            trend_mode = "ols"
        except:
            trend_mode = None # <-- fallback if statsmodels is missing

        # Create Scatter Plot
        fig_corr = px.scatter(
            df, 
            x=x_col, 
            y=y_col, 
            hover_name='Country',
            hover_data=['Year'],
            trendline=trend_mode,
            labels={x_col: x_label, y_col: y_label},
            opacity=0.65
        )

        # Styling the Trendline
        if trend_mode:
            fig_corr.update_traces(selector=dict(mode='lines'), line=dict(color=trend_color, width=3))
        
        # Customize Markers
        fig_corr.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
        
        fig_corr.update_layout(height=550, template='plotly_white')
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.info(f"💡 **Interpretation:** As **{x_label}** increases, **{y_label}** tends to change by a factor of **{r_value:.2f}**. (1.0 is perfect positive, -1.0 is perfect negative, 0 is no relation).")

    # "7. Performance Trends" 
    with tab7:
        # --- Step 1 : Insight Box ---
        st.markdown("""
        <div class="insight-box green-box">
            <h4>🌍 Insight 7: Performance Analysis (The Global Leaderboard)</h4>
            <p>Different nations dominate different arenas, proving there is no single "Best" research nation.</p>
            <ul>
                <li><b>Volume Leader:</b> United Kingdom (#1).</li>
                <li><b>Quality (CNCI) Leader:</b> Japan (#1).</li>
                <li><b>Elite Impact (% Top 1%) Leader:</b> Sweden (#1).</li>
            </ul>
            <hr>
            <p class="mb-0"><b>🇮🇳 India Watch:</b> India's rankings (<b>11th in Volume, 10th in Quality, 9th in Elite Impact</b>) across these diverse metrics highlight its status as a balanced, emerging power that is competing neck-to-neck with developed economies.</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Step 2 : Layout Controls (Columns) ---
        col_controls1, col_controls2 = st.columns([1, 1])
        # 1. Metric Selector (Always Visible)
        with col_controls2:
            METRICS_MAP = {
                "Documents (Volume)": 'Documents',
                "CNCI (Quality)": 'CNCI',
                "Times Cited (Impact)": 'Times Cited',
                "% Docs Cited (Relevance)": '% Docs Cited',
                "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
                "% Top 1% Documents (Excellence)": '% Documents in Top 1%'
            }
            selected_metric_label = st.selectbox("Select Metric:", list(METRICS_MAP.keys()))
            selected_col = METRICS_MAP[selected_metric_label]
        # 2. View Type Toggle (Always Visible - moved up to control visibility of country select)
        with col_controls1:
            view_option = st.radio(
                "Select View Type:",
                ("View Trends Over Time", "View Overall Performance", "View Geographic Map"), 
                horizontal=True
            )

        # --- Step 3 : Logic for Aggregation & Defaults ---
        # Determine if Sum or Mean
        if selected_col in ['Documents', 'Times Cited']:
            agg_func_rank = 'sum'
            fmt = '.2s'
        else:
            agg_func_rank = 'mean'
            fmt = '.2f'

        # --- Step 4 : Conditional Country Selector ---
        # Logic: if view is geographic map then do not show country selector
        selected_countries = []
        
        if view_option != "View Geographic Map":
            # Calculate Defaults based on Global Top 10
            rank_df = df.groupby('Country')[selected_col].agg(agg_func_rank).sort_values(ascending=False).head(10)
            top_10_countries_list = rank_df.index.tolist()
            available_countries = sorted(df['Country'].unique().tolist())
            
            # Show Multiselect
            selected_countries = st.multiselect(
                "Select Countries to Compare:", 
                available_countries, 
                default=top_10_countries_list, 
                key=f"multiselect_{selected_metric_label}" 
            )
        else:
            st.info("**Global View Active:** Showing data for all countries on the map.")          # <-- Map Mode Message


        # --- Step 5 : Visualization ---
        # Data Filter for Trend/Bar Charts
        if selected_countries:
            df_visual = df[df['Country'].isin(selected_countries)]
        else:
            df_visual = pd.DataFrame()

        # VIEW 1 : Trend Over Time
        if view_option == "View Trends Over Time":
            st.markdown(f"#### Trend Analysis: {selected_metric_label}")
            
            if not df_visual.empty:
                fig_trend = px.line(
                    df_visual, 
                    x='Year', 
                    y=selected_col, 
                    color='Country', 
                    markers=True,
                    hover_data=['Documents'] 
                )
                if selected_col in ['CNCI', 'Collab-CNCI']:
                    fig_trend.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Global Baseline (1.0)")
                
                fig_trend.update_layout(height=500, template='plotly_white', xaxis_title="Year", yaxis_title=selected_metric_label)
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.warning("Please select at least one country above to view trends.")
            
            # Table Logic
            trend_col1, trend_col2 = st.columns([2,1])

            with trend_col1:
                st.markdown(f"##### Yearly Global Leaderboard: Top 10 in {selected_metric_label}")
            with trend_col2:
                available_years = sorted(df['Year'].unique(), reverse=True)
                target_year = st.selectbox("Select Year for Ranking:", available_years)

            top_10_year = df[df['Year'] == target_year].sort_values(by=selected_col, ascending=False).head(10)
            
            display_df = top_10_year[['Country', selected_col]].copy()
            display_df.rename(columns={selected_col: selected_metric_label}, inplace=True)
            display_df.index = range(1, len(display_df) + 1)
            st.table(display_df)


        # VIEW 2 : Overall Performance
        elif view_option == "View Overall Performance":
            st.markdown(f"#### Overall Performance: {selected_metric_label}")
            
            if not df_visual.empty:
                df_visual_agg = df_visual.groupby('Country')[selected_col].agg(agg_func_rank).reset_index()
                df_visual_agg = df_visual_agg.sort_values(by=selected_col, ascending=True) 

                fig_overall = px.bar(
                    df_visual_agg, 
                    y='Country', 
                    x=selected_col, 
                    orientation='h', 
                    color='Country', 
                    text_auto=fmt,
                )
                if selected_col in ['CNCI', 'Collab-CNCI']:
                    fig_overall.add_vline(x=1.0, line_dash="dash", line_color="red", annotation_text="Global Baseline")
                
                fig_overall.update_layout(height=500, template='plotly_white', xaxis_title=f"Total/Avg {selected_metric_label}", showlegend=False)
                st.plotly_chart(fig_overall, use_container_width=True)
            else:
                st.warning("Please select at least one country above to view performance.")

            # Overall Table Logic
            st.markdown(f"##### Lifetime Global Leaderboard: Top 10 Overall {selected_metric_label}")
            df_global_agg = df.groupby('Country')[selected_col].agg(agg_func_rank).reset_index()
            top_10_overall = df_global_agg.sort_values(by=selected_col, ascending=False).head(10)
            display_overall = top_10_overall[['Country', selected_col]].copy()
            display_overall.rename(columns={selected_col: selected_metric_label}, inplace=True)
            display_overall.index = range(1, len(display_overall) + 1)
            st.table(display_overall)


        # VIEW 3 : Geographic Map (Satellite Style)
        elif view_option == "View Geographic Map":
            st.markdown(f"#### Global Heatmap: {selected_metric_label}")
            st.caption(f"Visualizing Lifetime **{agg_func_rank.title()}** of {selected_metric_label} across the globe.")

            # 1. Aggregate Data for Map
            map_df = df.groupby('Country')[selected_col].agg(agg_func_rank).reset_index()
            
            # 2. Create Map
            fig_map = px.choropleth(
                map_df,
                locations="Country",
                locationmode='country names',
                color=selected_col,
                hover_name="Country",
                color_continuous_scale="Viridis_r" if agg_func_rank == 'mean' else "Plasma", # Different themes for volume/quality
            )

            fig_map.update_geos(
                visible=True,
                resolution=50,
                showcountries=True, countrycolor="black",
                showcoastlines=True, coastlinecolor="black",
                showlakes=False,
                projection_type="natural earth" # Looks like a 3D-ish flat map
            )

            fig_map.update_layout(
                height=600,
                margin={"r":0,"t":40,"l":0,"b":0},
                paper_bgcolor="white", # Chart background black
                font_color="black",    # Text white
                coloraxis_colorbar=dict(
                    title=f"{selected_metric_label}",
                    tickfont=dict(color="black"),
                    title_font=dict(color="black")
                )
            )

            st.plotly_chart(fig_map, use_container_width=True)