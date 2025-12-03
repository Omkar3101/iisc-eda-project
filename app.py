import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import combinations  # <--- YAHAN MISSING THA, MAINE ADD KAR DIYA HE

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global Research Performance Analytics",
    page_icon="🔬",
    layout="wide"
)

# --- ( All CSS is now in ONE block at the top) ---
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
# 2. DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def create_dummy_data():
    """Generates sample data if CSV is missing"""
    countries = ['USA', 'China', 'UK', 'Germany', 'India', 'Japan', 'France', 'Italy', 'Canada', 'Australia', 'Brazil', 'Spain', 'South Korea', 'Netherlands', 'Russia']
    years = [2018, 2019, 2020, 2021, 2022]
    data = []
    
    for country in countries:
        base_quality = np.random.uniform(0.8, 1.8)
        for year in years:
            docs = np.random.randint(500, 20000)
            if country in ['USA', 'China']: docs *= 5
            
            cnci = base_quality + np.random.normal(0, 0.1)
            times_cited = int(docs * cnci * np.random.uniform(5, 15))
            collab_cnci = cnci * np.random.uniform(0.9, 1.3)
            
            data.append([country, year, docs, times_cited, cnci, collab_cnci, np.random.uniform(40, 90)])
            
    return pd.DataFrame(data, columns=['Country', 'Year', 'Documents', 'Times Cited', 'CNCI', 'Collab-CNCI', '% Docs Cited', '% Documents in Top 1%'])

@st.cache_data
def load_data():
    try:
        # Note: Added logic to handle missing col if using dummy data logic fully
        df = pd.read_csv('data/cleaned_publications.csv')
        return df
    except FileNotFoundError:
        st.warning("⚠️ 'cleaned_publications.csv' not found. Using Generated Demo Data.")
        df = create_dummy_data()
        # Dummy data fix for Top 1% column if it was missing in generator
        if '% Documents in Top 1%' not in df.columns:
             df['% Documents in Top 1%'] = df['CNCI'] * np.random.uniform(0.5, 1.5)
        return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. MAIN DASHBOARD LOGIC
# -----------------------------------------------------------------------------
if df is not None:
    
    # Cover Image
    st.markdown('<div class="cover-image"></div>', unsafe_allow_html=True)

    # Title and Subheading
    st.title("🔬 Global Research Performance Analytics")
    st.markdown("##### *Project Intern/Trainee Hiring Assessment - PAIU-OPSA, IISc Bangalore*")
    st.markdown("---")

    #Side Bar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This dashboard presents an in-depth analysis of global research performance metrics, developed as part of a hiring assessment for IISc Bangalore.
        """)
        
        st.markdown("---")
        
        st.header("Project Resources")
        st.markdown("🔗 [View Source Code on GitHub](https://github.com/Omkar3101/iisc-eda-project)")
        
        st.markdown("---")
        
        st.header("Author")
        st.markdown("""
        **Omkar Sharma**
        - [LinkedIn](https://www.linkedin.com/in/omkar3101)
        - [Email](mailto:omkarshar3101@gmail.com)
        """)

    # TABS (Renamed for professional context)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview & Key Findings",
        "🗺️ Strategic Positioning",
        "🎯 Quality Spectrum",
        "⚔️ Competitive Landscape",
        "🚨 Outlier Analysis",
        "🔗 Correlation Analysis",
        "📈 Performance Trends"
    ])

    # ... (Tab 1 remains same) ...
    with tab1:
        st.markdown("""
        <div class="insight-box blue-box">
            <h4>🔍 Insight 1: Welcome to the "Topper's Batch"</h4>
            <p>This initial analysis reveals two fundamental truths about our dataset: high performance is the norm, and power is highly decentralized.</p>
            <ul>
                <li>
                    <b>Structural Strength (Left Chart):</b> Every nation's long-term average performance is <b>above the global standard (CNCI > 1.0)</b>. Underperformance (Red Dots) is a rare, year-specific anomaly, not a systemic weakness.
                </li>
                <li>
                    <b>Pareto Principle Fails (Right Chart):</b> The 80/20 rule is inverted. It takes <b>~75% of nations to generate 80% of the impact</b>. This proves a balanced competitive landscape, not a "winner-takes-all" market.
                </li>
            </ul>
            <hr>
            <p class="mb-0"><b>Conclusion:</b> In this high-stakes environment, 'good' performance is just the entry ticket. True differentiation must be measured by more extreme metrics, like producing "Blockbuster" research (Top 1%).</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # --- VISUAL 1: STRIP PLOT ---
        with col1:
            st.markdown("#### 1. Consistency Check (Granular View)")
            
            df['Benchmark Status'] = df['CNCI'].apply(lambda x: 'Below Average (< 1.0)' if x < 1.0 else 'Above Average (>= 1.0)')
            below_count = len(df[df['CNCI'] < 1.0])
            
            st.metric("Rare Failures ( < 1.0)", f"{below_count} / {len(df)} Rows", delta="Anomalies", delta_color="inverse")

            fig_strip = px.strip(
                df, 
                y='CNCI', 
                x='Country', 
                color='Benchmark Status', 
                color_discrete_map={'Below Average (< 1.0)': '#EF553B', 'Above Average (>= 1.0)': '#636EFA'},
                hover_data=['Year', 'CNCI'], 
                title='Granular Check: Structural Strength vs Occasional Dips',
                template='plotly_white'
            )
            fig_strip.add_hline(y=1.0, line_dash="dash", line_color="black", annotation_text="Global Baseline")
            fig_strip.update_layout(height=450)
            st.plotly_chart(fig_strip, use_container_width=True)
            
            st.caption("ℹ️ **Note:** Each dot is a specific **Year**. While every country passes on average, the red dots show rare years where they slipped.")

        # --- VISUAL 2: PARETO CHART ---
        with col2:
            st.markdown("#### 2. Power Concentration (Pareto)")
            
            pareto_df = df.groupby('Country')['Times Cited'].sum().reset_index()
            pareto_df = pareto_df.sort_values(by='Times Cited', ascending=False).reset_index(drop=True)
            
            total_citations = pareto_df['Times Cited'].sum()
            pareto_df['Cumulative_Cit_Perc'] = (pareto_df['Times Cited'].cumsum() / total_citations) * 100
            pareto_df['Entity_Perc'] = ((pareto_df.index + 1) / len(pareto_df)) * 100
            
            try:
                cutoff_row = pareto_df[pareto_df['Cumulative_Cit_Perc'] >= 80].iloc[0]
                cutoff_perc = cutoff_row['Entity_Perc']
            except IndexError:
                cutoff_perc = 100

            st.metric("Entities needed for 80% Impact", f"{cutoff_perc:.1f}%", delta="Pareto Principle Failed", delta_color="off")
            
            fig_pareto = go.Figure()
            fig_pareto.add_trace(go.Bar(
                x=pareto_df['Country'], y=pareto_df['Times Cited'], name='Citations', marker_color='#ced4da'
            ))
            fig_pareto.add_trace(go.Scatter(
                x=pareto_df['Country'], y=pareto_df['Cumulative_Cit_Perc'],
                mode='lines+markers', name='Cumulative %', yaxis='y2', line=dict(color='#ef553b', width=3)
            ))

            fig_pareto.update_layout(
                title='Lorenz Curve: Impact is Distributed, Not Monopolized',
                yaxis=dict(title='Total Citations'),
                yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 110]),
                hovermode='x unified',
                height=450,
                showlegend=False
            )
            fig_pareto.add_hline(y=80, line_dash="dash", line_color="green", yref="y2", annotation_text="80% Threshold")
            st.plotly_chart(fig_pareto, use_container_width=True)
            
            st.caption("ℹ️ **Note:** The curve is flat, meaning research power is shared among many nations, not hoarded by just one.")

# "🗺️2. Strategic Positioning"
    with tab2:
        st.markdown("""
        <div class="insight-box orange-box">
            <h4>🗺️ Insight 2: Strategic Positioning & The Collaboration Myth</h4>
            <p>This deep dive first maps each nation's research strategy and then investigates a key differentiator: Does better collaboration lead to more "Blockbuster" papers?</p>
            <ul>
                <li><b>The Four Models (Left Chart):</b> Nations are segmented into strategic quadrants. The bubble color now indicates their average collaboration quality.</li>
                <li><b>The Collaboration Myth (Right Chart):</b> Contrary to belief, for these top-tier nations, better collaboration quality shows <b>zero correlation</b> with producing more elite (Top 1%) papers, as proven by the flat red trendline.</li>
            </ul>  
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 1. The Four Strategic Models")
            overall_df = df.groupby('Country').agg({
                'Documents': 'sum', 'Times Cited': 'sum', 'CNCI': 'mean', 'Collab-CNCI': 'mean'
            }).reset_index()
            median_docs = overall_df['Documents'].median()
            median_cnci = overall_df['CNCI'].median()

            fig_quad = px.scatter(
                overall_df, 
                x='Documents', 
                y='CNCI', 
                size='Times Cited', 
                color='Collab-CNCI', 
                hover_name='Country', 
                log_x=True, 
                color_continuous_scale='Plasma', 
                height=550
            )
            fig_quad.add_vline(x=median_docs, line_dash="dash", line_color="gray")
            fig_quad.add_hline(y=median_cnci, line_dash="dash", line_color="gray")
            
            annotations = {
                "🏆 ELITE": (0.98, 0.98, "green"),
                "🏭 MASS PRODUCER": (0.98, 0.02, "orange"),
                "💎 BOUTIQUE": (0.02, 0.98, "blue"),
                "🔻 LAGGING": (0.02, 0.02, "grey")
            }
            for text, (x, y, color) in annotations.items():
                fig_quad.add_annotation(
                    xref="paper", yref="paper", x=x, y=y, text=f"<b>{text}</b>",
                    showarrow=False, font=dict(color=color, size=12),
                    xanchor='right' if x > 0.5 else 'left', yanchor='top' if y > 0.5 else 'bottom'
                )

            fig_quad.update_layout(
                xaxis_title="Total Documents (Log Scale)", 
                yaxis_title="Average Quality (CNCI)", 
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis_colorbar_title_text='Collab<br>Quality'
            )
            st.plotly_chart(fig_quad, use_container_width=True)

        with col2:
            st.markdown("##### 2. The Collaboration Myth")
            elite_data = df.groupby('Country')[['Collab-CNCI', '% Documents in Top 1%']].mean().reset_index()
            correlation = elite_data['Collab-CNCI'].corr(elite_data['% Documents in Top 1%'])

            fig_elite = px.scatter(
                elite_data,
                x='Collab-CNCI',
                y='% Documents in Top 1%',
                hover_name='Country',
                trendline="ols"
            )
            fig_elite.update_traces(selector=dict(mode='lines'), line=dict(color='red', width=3, dash='solid'))
            fig_elite.update_traces(selector=dict(mode='markers'), marker=dict(opacity=0.6, color='#636EFA'))
            fig_elite.add_annotation(
                xref="paper", yref="paper", x=0.95, y=0.05,
                text=f"<b>Pearson's r = {correlation:.2f}</b>",
                showarrow=False, font=dict(size=14, color="red")
            )
            fig_elite.update_layout(
                height=550,
                xaxis_title="Average Collaboration Quality",
                yaxis_title="Average % in Top 1%",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_elite, use_container_width=True)

# "🎯3. Quality Spectrum"
    with tab3: 
        st.markdown("""
        <div class="insight-box blue-box">
            <h4>🎯 Insight 3: The Quality Spectrum (Baseline vs. Ceiling)</h4>
            <p>We analyze research impact at two distinct levels: <b>Consistency</b> (Left) and <b>Elite Performance</b> (Right).</p>
            <ul>
                <li><b>Left Chart (Relevance):</b> "Getting Cited" is now a "Table Stakes" metric. The curve is centered at <b>~97.5%</b>.</li>
                <li><b>Right Chart (Excellence):</b> The real differentiator is the <b>Top 1% Conversion</b>. The dataset average (<b>1.77%</b>) is nearly double the global theoretical baseline (1%).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            mean_val = df['% Docs Cited'].mean()
            median_val = df['% Docs Cited'].median()
            st.markdown("##### 1. Dist. of Relevance (% Docs Cited)")
            m1, m2 = st.columns(2)
            m1.metric("Mean Relevance", f"{mean_val:.2f}%")
            m2.metric("Median Relevance", f"{median_val:.2f}%")

            fig_dist = px.histogram(
                df, x='% Docs Cited', nbins=30, marginal='box', color_discrete_sequence=['#00CC96'], opacity=0.8
            )
            fig_dist.add_vline(x=mean_val, line_dash="dash", line_color="red")
            fig_dist.add_vline(x=median_val, line_dash="dot", line_color="blue")
            fig_dist.add_annotation(x=mean_val, y=1.15, yref="paper", text=f"Mean", showarrow=False, font=dict(color="red"))
            fig_dist.add_annotation(x=median_val, y=1.08, yref="paper", text=f"Median", showarrow=False, font=dict(color="blue"))
            fig_dist.update_layout(height=450, xaxis_title='Percentage of Documents Cited', yaxis_title='Count', showlegend=False)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            st.markdown("###### Statistical Summary (% Docs Cited)")
            stats_rel = df['% Docs Cited'].describe().to_frame(name='Value')
            st.dataframe(stats_rel, use_container_width=True)

        with col2:
            avg_elite = df['% Documents in Top 1%'].mean()
            median_elite = df['% Documents in Top 1%'].median()
            elite_performers = df[df['% Documents in Top 1%'] > 2.0][['Country', 'Year', '% Documents in Top 1%']]
            
            st.markdown("##### 2. Dist. of Excellence (% Top 1%)")
            m1, m2 = st.columns(2)
            m1.metric("Mean Elite %", f"{avg_elite:.2f}%")
            m2.metric("Median Elite %", f"{median_elite:.2f}%")

            fig_elite_dist = px.histogram(
                df, x='% Documents in Top 1%', nbins=40, marginal='box', color_discrete_sequence=['gold'], 
                labels={'% Documents in Top 1%': '% in Top 1%'}
            )
            fig_elite_dist.add_vline(x=1.0, line_dash="dash", line_color="red") 
            fig_elite_dist.add_vline(x=avg_elite, line_dash="dot", line_color="blue") 
            fig_elite_dist.add_annotation(x=1.0, y=1.08, yref="paper", text="Global (1%)", showarrow=False, font=dict(color="red", size=10))
            fig_elite_dist.add_annotation(x=avg_elite, y=1.15, yref="paper", text=f"Avg", showarrow=False, font=dict(color="blue", size=10))
            fig_elite_dist.update_layout(height=450, xaxis_title='Percentage in Top 1%', yaxis_title='Count', showlegend=False)
            st.plotly_chart(fig_elite_dist, use_container_width=True)

            st.markdown("###### Statistical Summary (% Top 1%)")
            stats_elite = df['% Documents in Top 1%'].describe().to_frame(name='Value')
            st.dataframe(stats_elite, use_container_width=True)

            st.markdown("###### Top 5 Countries Consistently Performing (> 2%)")
            consistency_check = elite_performers['Country'].value_counts().head(5).to_frame(name='Records > 2%')
            consistency_check.index.name = 'Country'
            st.dataframe(consistency_check, use_container_width=True)

            st.markdown("###### Top 5 Single Year Elite Performances")
            top_5_years = elite_performers.sort_values(by='% Documents in Top 1%', ascending=False).head(5).reset_index(drop=True)
            st.dataframe(top_5_years, use_container_width=True)

# "⚔️4. Competitive Landscape"
    # "⚔️4. Competitive Landscape"
    with tab4: 
        st.markdown("""
        <div class="insight-box orange-box">
            <h4>⚔️ Insight 4: The Ebb and Flow of Dominance</h4>
            <p>Analyze market dominance using two powerful modes. Use the toggle below to switch between a high-level "Market View" and a detailed "Rivalry View".</p>
            <ul>
                <li>Peak Dominance: Highlights years where one country holds the largest lead margin over its nearest competitor for the selected metric.</li>
                <li>Trend Analysis: A falling line indicates the research field is becoming more competitive, while a rising line indicates a leader is solidifying their position.</li>
            </ul>        
        </div>
        """, unsafe_allow_html=True)
        
        METRICS = {
            "Times Cited (Impact)": 'Times Cited',
            "Documents (Volume)": 'Documents',
            "CNCI (Quality)": 'CNCI',
            "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
            "% Docs Cited (Relevance)": '% Docs Cited',
            "% Top 1 Document % (Excellence)": '% Documents in Top 1%',
        }

        selected_metric_label = st.selectbox(
            "Select Metric for Dominance Analysis:",
            list(METRICS.keys()),
            index=0,
            key='dominance_metric_select'
        )
        selected_metric_col = METRICS[selected_metric_label]

        view_mode = st.radio(
            "Select Analysis Mode:",
            ("Market View (Top 2 Overall)", "Rivalry View (Compare Specific Countries)"),
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("---")

        # ==============================================================================
        # --- MODE 1: MARKET VIEW (UPDATED TO 0-100% SCALE) ---
        # ==============================================================================
        if view_mode == "Market View (Top 2 Overall)":
            st.markdown(f"##### 1. Market View: Overall Leader's Dominance (Top 2 by {selected_metric_label})")
            
            gap_data = []
            years = sorted(df['Year'].unique())
            for y in years:
                year_df = df[df['Year'] == y].sort_values(by=selected_metric_col, ascending=False)
                if len(year_df) >= 2:
                    leader, runner = year_df.iloc[0], year_df.iloc[1]
                    
                    leader_val = leader[selected_metric_col]
                    runner_val = runner[selected_metric_col]
                    total_val = leader_val + runner_val # Total for Normalization

                    # UPDATED FORMULA: Normalized Margin (0-100%)
                    # Formula: (Difference / Total) * 100
                    gap_pct = ((leader_val - runner_val) / total_val) * 100 if total_val > 0 else 0
                    
                    gap_data.append({'Year': y, 'Leader': leader['Country'], 'Runner-Up': runner['Country'], 'Dominance %': gap_pct})
            
            gap_df = pd.DataFrame(gap_data)

            fig_gap_line = px.line(gap_df, x='Year', y='Dominance %', markers=True, 
                                   title=f'Trend of the Overall Market Leader\'s Advantage (Normalized 0-100%)', 
                                   hover_data=['Leader', 'Runner-Up'])
            
            fig_gap_line.update_traces(line=dict(color='crimson', width=3), marker=dict(size=8))
            
            # Add Reference Lines
            fig_gap_line.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No Gap (Equal)")
            
            # FORCE Y-AXIS TO 0-100 RANGE
            fig_gap_line.update_layout(
                height=500, 
                template='plotly_white', 
                yaxis_title=f"Normalized Margin (%)",
                yaxis=dict(range=[0, 100]) # <--- Locked Range
            )
            st.plotly_chart(fig_gap_line, use_container_width=True)

            st.caption("""
            ℹ️ **Note:** This chart uses a **Normalized Scale (0-100%)**. 
            - **0%**: Means the Leader and Runner-up are equal.
            - **Higher %**: Means the Leader dominates the Runner-up significantly.
            """)

            st.markdown("---")
            st.markdown(f"##### 🏆 Top 5 Most Dominant Years (Overall Market by {selected_metric_label})")
            top_5_dominance = gap_df.sort_values(by='Dominance %', ascending=False).head(5)
            st.dataframe(top_5_dominance.style.format({'Dominance %': '{:.1f}%'}), hide_index=True, use_container_width=True)

        # ==============================================================================
        # --- MODE 2: RIVALRY TREND VIEW (Already Correct) ---
        # ==============================================================================
        else:
            st.markdown(f"##### 2. Rivalry Trends: Pairwise Dominance Evolution (by {selected_metric_label})")
            
            available_countries = sorted(df['Country'].unique())
            preferred_defaults = ['USA', 'CHINA'] 
            valid_defaults = [country for country in preferred_defaults if country in available_countries]
            if len(valid_defaults) < 2 and len(available_countries) >= 2:
                valid_defaults = available_countries[:min(3, len(available_countries))]
            elif len(valid_defaults) == 0:
                valid_defaults = []
            
            selected_countries = st.multiselect(
                "Select countries to compare dominance trends:", 
                available_countries, 
                default=valid_defaults,
                key='rivalry_country_select'
            )

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
                        
                        st.markdown(f"###### ⚔️ Dominance Trend: Normalized Competition Margin (%) - {selected_metric_label}")
                        fig_dom_trend = px.line(
                            dom_df, x='Year', y='Dominance %', color='Pair', markers=True,
                            hover_data={'Dominance %': ':.1f', 'Leader': True, 'Runner-Up': True},
                            title=f'Normalized Margin (0-100%): How wide is the {selected_metric_label} gap?',
                            template='plotly_white'
                        )
                        fig_dom_trend.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Equal Impact (0% Gap)")
                        fig_dom_trend.update_layout(height=450, yaxis_title=f"Normalized Dominance Margin (%) - {selected_metric_label}", yaxis=dict(range=[0, 100]))
                        st.plotly_chart(fig_dom_trend, use_container_width=True)
                        
                        st.caption("""
                        ℹ️ **How to read this chart:** - **Value**: Represents the **Normalized Percentage Margin**.
                        - **0%**: Equal. **100%**: Absolute dominance.
                        """)
                        
                        st.markdown("---")
                        st.markdown(f"##### 🏆 Top 5 Instances of Dominance (Largest Normalized Margin by {selected_metric_label})")
                        top_5_dominance = dom_df.sort_values(by='Dominance %', ascending=False).head(5)
                        top_5_display = top_5_dominance[['Year', 'Pair', 'Leader', 'Runner-Up', 'Dominance %']].copy()
                        top_5_display['Normalized Margin (%)'] = top_5_display['Dominance %']
                        st.dataframe(top_5_display[['Year', 'Leader', 'Runner-Up', 'Pair', 'Normalized Margin (%)']].style.format({'Normalized Margin (%)': '{:.1f}%'}), hide_index=True, use_container_width=True)
                    else:
                        st.info("Insufficient overlapping data.")
            else:
                st.warning("Please select at least two countries to generate the trend comparison.")

# "🚨5. Outlier Analysis"
    with tab5: 
        st.markdown("""
        <div class="insight-box red-box">
            <h4>🚨 Insight 5: The "Quality Ceiling" & Volume Spikes</h4>
            <p><b>Fundamental Asymmetry:</b> Our outlier analysis reveals a distinct difference in how Quantity and Quality behave:</p>
            <ul>
                <li><b>🏭 Mega-Producers (Volume Extremes):</b> The <code>Documents</code> distribution is highly skewed. Nations like <b>China</b> and <b>Italy</b> show extreme spikes.</li>
                <li><b>💎 The Quality Ceiling:</b> In contrast, <b>Quality (CNCI) has NO statistical outliers</b>.</li>
                <li><b>📉 Isolated Events:</b> These volume spikes are typically <b>one-off events</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        Q1 = df['Documents'].quantile(0.25)
        Q3 = df['Documents'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[df['Documents'] > upper_bound]

        fig_out = px.scatter(
            df, x='Year', y='Documents',
            color=df['Documents'].apply(lambda x: 'Outlier' if x > upper_bound else 'Normal'),
            color_discrete_map={'Outlier': '#EF553B', 'Normal': 'lightgrey'}, 
            hover_name='Country', hover_data=['Year', 'Documents'],
            title='Identifying Years of "Hyper-Production" (Outliers > 1.5 IQR)',
            size='Documents', size_max=20
        )
        fig_out.add_hline(y=upper_bound, line_dash="dash", line_color="red", annotation_text=f"Statistical Threshold ({int(upper_bound)} Docs)", annotation_position="top right")
        fig_out.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig_out, use_container_width=True)
        
        if not outliers.empty:
            st.markdown("#### 🚩 Detected Anomalies (Mega-Production Years)")
            st.dataframe(outliers[['Country', 'Year', 'Documents']].sort_values(by='Documents', ascending=False), hide_index=True, use_container_width=True)

# "🔗6. Correlation Analysis"
    with tab6:
        corr_weak = df['Collab-CNCI'].corr(df['CNCI'])
        corr_strong = df['Documents'].corr(df['Times Cited'])
        
        st.markdown(f"""
        <div class="insight-box purple-box">
            <h4>🤝 Insight 6: Correlation Contrast (The Weak vs. The Strong)</h4>
            <ul>
                <li><b>❌ The Weak Link ({corr_weak:.4f}):</b> Collaboration Quality has <b>no linear relation</b> with Overall Research Quality.</li>
                <li><b>✅ The Strong Link ({corr_strong:.4f}):</b> Volume (Documents) has a <b>near-perfect positive correlation</b> with Impact (Citations).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"##### 1. Paradox: Collab vs Quality (r = {corr_weak:.2f})")
            fig_weak = px.scatter(
                df, x='Collab-CNCI', y='CNCI', hover_data=['Country', 'Year'],
                trendline="ols", opacity=0.6, title='<b>Weak Correlation</b>',
                labels={"Collab-CNCI": "Collab Impact", "CNCI": "Overall Quality"}
            )
            fig_weak.update_traces(selector=dict(mode='lines'), line=dict(color='red', width=3))
            fig_weak.update_layout(height=450, template='plotly_white')
            st.plotly_chart(fig_weak, use_container_width=True)

        with col_c2:
            st.markdown(f"##### 2. Predictable: Quantity vs Impact (r = {corr_strong:.2f})")
            fig_strong = px.scatter(
                df, x='Documents', y='Times Cited', hover_data=['Country', 'Year'],
                trendline="ols", opacity=0.6, title='<b>Strong Correlation</b>',
                labels={"Documents": "Total Documents", "Times Cited": "Total Citations"}
            )
            fig_strong.update_traces(selector=dict(mode='lines'), line=dict(color='green', width=3))
            fig_strong.update_layout(height=450, template='plotly_white')
            st.plotly_chart(fig_strong, use_container_width=True)

# "📈7. Performance Trends" 
    # "📈7. Performance Trends"
    with tab7:
        st.markdown("""
        <div class="insight-box green-box">
            <h4>🌍 Insight 7: A Dynamic Geopolitical Landscape</h4>
            <p><b>1. The Volume Race (Quantity):</b> It is not a static hierarchy but a <b>Three-Way Race</b> between the <b>UK, Spain, and Brazil</b>.</p>
            <p><b>2. The Quality Consistency (Impact):</b> Among top publishers, <b>Spain</b> demonstrates superior and consistent quality.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- 1. CONFIGURATION & WIDGETS ---
        available_countries = sorted(df['Country'].unique().tolist())
        defaults = ['UNITED KINGDOM', 'SPAIN', 'BRAZIL', 'CANADA', 'SWITZERLAND'] 
        valid_defaults = [c for c in defaults if c in available_countries]
        if not valid_defaults: valid_defaults = available_countries[:5]
        
        col_controls1, col_controls2 = st.columns([1, 1])
        
        with col_controls1:
            selected_countries = st.multiselect("Select Countries to Compare", available_countries, default=valid_defaults)
        
        with col_controls2:
            # Metric Mapping (Display Name -> Column Name)
            METRICS_MAP = {
                "Documents (Volume)": 'Documents',
                "CNCI (Quality)": 'CNCI',
                "Times Cited (Impact)": 'Times Cited',
                "% Docs Cited (Relevance)": '% Docs Cited',
                "Collab-CNCI (Collab Quality)": 'Collab-CNCI',
                "% Top 1% Documents (Excellence)": '% Documents in Top 1%'
            }
            selected_metric_label = st.selectbox("Select Performance Metric:", list(METRICS_MAP.keys()))
            selected_col = METRICS_MAP[selected_metric_label]

        # View Toggle
        view_option = st.radio(
            "Select View Type:",
            ("View Trends Over Time", "View Overall Performance"),
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("---")

        # --- 2. LOGIC & VISUALIZATION ---
        if selected_countries:
            df_filtered = df[df['Country'].isin(selected_countries)]
            
            # ==============================================================================
            # VIEW 1: TRENDS OVER TIME (Line Chart + Yearly Leaderboard)
            # ==============================================================================
            if view_option == "View Trends Over Time":
                st.markdown(f"#### 📈 Trend Analysis: {selected_metric_label}")
                
                # A. Line Chart
                fig_trend = px.line(
                    df_filtered, 
                    x='Year', 
                    y=selected_col, 
                    color='Country', 
                    markers=True,
                    title=f"Year-wise Evolution of {selected_metric_label}",
                    hover_data=['Documents'] 
                )
                
                if selected_col in ['CNCI', 'Collab-CNCI']:
                    fig_trend.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Global Baseline (1.0)")
                
                fig_trend.update_layout(height=500, template='plotly_white', xaxis_title="Year", yaxis_title=selected_metric_label)
                st.plotly_chart(fig_trend, use_container_width=True)
                
                st.markdown("---")
                
                # B. Top 5 Table (Specific Year)
                col_tbl_desc, col_tbl_widget = st.columns([3, 1])
                with col_tbl_desc:
                    st.markdown(f"##### 🗓️ Yearly Leaderboard: Top 5 in {selected_metric_label}")
                    st.caption("Check the ranking for a specific year among selected countries.")
                with col_tbl_widget:
                    # Year Selector (Default to latest year)
                    available_years = sorted(df_filtered['Year'].unique(), reverse=True)
                    target_year = st.selectbox("Select Year:", available_years)

                # Filter & Sort Data for Table
                top_5_year = df_filtered[df_filtered['Year'] == target_year].sort_values(by=selected_col, ascending=False).head(5)
                
                # Formatting columns for display
                display_df = top_5_year[['Country', selected_col]].copy()
                display_df.rename(columns={selected_col: selected_metric_label}, inplace=True)
                display_df.index = range(1, len(display_df) + 1) # Rank 1 to 5
                
                st.table(display_df)

            # ==============================================================================
            # VIEW 2: OVERALL PERFORMANCE (Bar Chart + Lifetime Leaderboard)
            # ==============================================================================
            else:
                st.markdown(f"#### 📊 Overall Performance: {selected_metric_label}")
                
                # Determine Aggregation Type
                if selected_col in ['Documents', 'Times Cited']:
                    agg_func = 'sum'
                    y_label = f"Total {selected_col}"
                    title_text = f"Lifetime Total: {selected_metric_label}"
                    fmt = '.2s' 
                else:
                    agg_func = 'mean'
                    y_label = f"Average {selected_col}"
                    title_text = f"Lifetime Average: {selected_metric_label}"
                    fmt = '.2f' 
                
                # Group & Aggregate
                df_overall = df_filtered.groupby('Country')[selected_col].agg(agg_func).reset_index()
                df_overall = df_overall.sort_values(by=selected_col, ascending=True) 

                # A. Bar Chart
                fig_overall = px.bar(
                    df_overall, 
                    y='Country', 
                    x=selected_col, 
                    orientation='h', 
                    color='Country', 
                    text_auto=fmt,
                    title=title_text
                )
                
                if selected_col in ['CNCI', 'Collab-CNCI']:
                    fig_overall.add_vline(x=1.0, line_dash="dash", line_color="red", annotation_text="Global Baseline")
                
                fig_overall.update_layout(height=500, template='plotly_white', xaxis_title=y_label, showlegend=False)
                st.plotly_chart(fig_overall, use_container_width=True)

                st.markdown("---")

                # B. Top 5 Table (Overall)
                st.markdown(f"##### 🏆 Lifetime Leaderboard: Top 5 Overall ({selected_metric_label})")
                
                # Sort Descending for Table (Highest first)
                top_5_overall = df_overall.sort_values(by=selected_col, ascending=False).head(5)
                
                # Formatting
                display_overall = top_5_overall[['Country', selected_col]].copy()
                display_overall.rename(columns={selected_col: selected_metric_label}, inplace=True)
                display_overall.index = range(1, len(display_overall) + 1)
                
                st.table(display_overall)

        else:
            st.warning("⚠️ Please select at least one country to view performance.")