import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
# ... (Aapka Data Loading ka code yahan waisa hi rahega) ...
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
            
    return pd.DataFrame(data, columns=['Country', 'Year', 'Documents', 'Times Cited', 'CNCI', 'Collab-CNCI', '% Docs Cited'])

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/cleaned_publications.csv')
        return df
    except FileNotFoundError:
        st.warning("⚠️ 'cleaned_publications.csv' not found. Using Generated Demo Data.")
        return create_dummy_data()

df = load_data()
# -----------------------------------------------------------------------------
# 3. MAIN DASHBOARD LOGIC
# -----------------------------------------------------------------------------
if df is not None:
    
    # --- (FIX 2: The HTML div for the cover image is added here) ---
    st.markdown('<div class="cover-image"></div>', unsafe_allow_html=True)
    st.title("🔬 Global Research Performance Analytics")
    st.markdown("##### *Project Intern/Trainee Hiring Assessment - PAIU-OPSA, IISc Bangalore*")
    st.markdown("---")

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

    # ... (Aapka baaki ka code waisa hi rahega, koi change ki zaroorat nahi) ...
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
            
            # Note added for clarity
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
            <h4>⚖️ Insight 2: Strategy & The Collaboration Myth</h4>
            <p>This deep dive first maps each nation's research strategy and then investigates a key differentiator: Does better collaboration lead to more "Blockbuster" papers?</p>
            <ul>
                <li><b>The Four Models (Left Chart):</b> Nations are segmented into strategic quadrants like "Mass Producers" (e.g., UK) and "Boutique" specialists (e.g., Japan).</li>
                <li><b>The Collaboration Myth (Right Chart):</b> Contrary to belief, for these top-tier nations, better collaboration quality shows <b>zero correlation</b> with producing more elite (Top 1%) papers. Collaboration is a baseline requirement, not a competitive advantage.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the charts
        col1, col2 = st.columns(2)

        # --- LEFT CHART: STRATEGY MATRIX ---
        with col1:
            st.markdown("##### 1. The Four Strategic Models")
            
            # Data prep for Quadrant chart
            overall_df = df.groupby('Country').agg({
                'Documents': 'sum', 'Times Cited': 'sum', 'CNCI': 'mean', 'Collab-CNCI': 'mean'
            }).reset_index()
            median_docs = overall_df['Documents'].median()
            median_cnci = overall_df['CNCI'].median()

            fig_quad = px.scatter(
                overall_df, x='Documents', y='CNCI', size='Times Cited', color='CNCI',
                hover_name='Country', log_x=True, 
                color_continuous_scale='Viridis', height=500, text='Country'
            )
            fig_quad.add_vline(x=median_docs, line_dash="dash", line_color="red")
            fig_quad.add_hline(y=median_cnci, line_dash="dash", line_color="red")
            fig_quad.update_traces(textposition='top center')
            
            # 1. Elite Players (Top-Right)
            fig_quad.add_annotation(
                xref="paper", yref="paper",
                x=0.98, y=0.98,  
                text="<b>CONSISTENT ELITE</b><br>(High Qty / High Qual)",
                showarrow=False, font=dict(size=13, color="green"),
                xanchor="right", yanchor="top"
            )

            # 2. Mass Producers (Bottom-Right)
            fig_quad.add_annotation(
                xref="paper", yref="paper",
                x=0.98, y=0.02,  
                text="<b>MASS PRODUCERS</b><br>(High Qty / Low Qual)",
                showarrow=False, font=dict(size=12, color="orange"),
                xanchor="right", yanchor="bottom"
            )

            # 3. Niche Players (Top-Left)
            fig_quad.add_annotation(
                xref="paper", yref="paper",
                x=0.02, y=0.98,  
                text="<b>NICHE / BOUTIQUE</b><br>(Low Qty / High Qual)",
                showarrow=False, font=dict(size=12, color="blue"),
                xanchor="left", yanchor="top"
            )

            # 4. Underperformers (Bottom-Left)
            fig_quad.add_annotation(
                xref="paper", yref="paper",
                x=0.02, y=0.02,  
                text="<b>LAGGING</b><br>(Low Qty / Low Qual)",
                showarrow=False, font=dict(size=12, color="gray"),
                xanchor="left", yanchor="bottom"
            )


            fig_quad.update_layout(xaxis_title="Total Documents (Log)", yaxis_title="Avg Quality (CNCI)", margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False)
            
            st.plotly_chart(fig_quad, use_container_width=True)

        # --- RIGHT CHART: ELITE CONVERSION (COLLABORATION IMPACT) ---
        with col2:
            st.markdown("##### 2. The Collaboration Myth")
            
            # Data prep for Elite Conversion chart
            elite_data = df.groupby('Country')[['Collab-CNCI', '% Documents in Top 1%', 'Documents', 'CNCI']].mean().reset_index()
            elite_data = elite_data[elite_data['% Documents in Top 1%'] > 0]
            
            fig_elite = px.scatter(
                elite_data,
                x='Collab-CNCI',
                y='% Documents in Top 1%',
                size='Documents',
                color='CNCI',
                hover_name='Country',
                trendline="ols",
                color_continuous_scale='Plasma',
                text='Country'
            )
            fig_elite.update_traces(marker=dict(opacity=0.8))
            fig_elite.update_layout(
                height=500,
                xaxis_title="Avg Collaboration Quality",
                yaxis_title="Avg % in Top 1%",
                coloraxis_showscale=False,
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
                <li><b>Left Chart (Relevance):</b> "Getting Cited" is now a "Table Stakes" metric. The data shows a symmetric curve centered at <b>~97.5%</b>. There is almost no skew, meaning there are no real underperformers.</li>
                <li><b>Right Chart (Excellence):</b> The real differentiator is the <b>Top 1% Conversion</b>. The dataset average (<b>1.77%</b>) is nearly double the global theoretical baseline (1%).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # --- Data Prep ---
        impact_df = df.groupby('Country')[['% Docs Cited', '% Documents in Top 1%']].mean().reset_index()

        col1, col2 = st.columns(2)

        # --- LEFT CHART: RELEVANCE ---
        with col1:
            st.markdown("##### 1. Relevance: % Docs Cited (The Baseline)")
            top_rel = impact_df.sort_values(by='% Docs Cited', ascending=False).head(10)
            
            # Zoom Logic
            min_val = top_rel['% Docs Cited'].min()
            zoom_min = int(min_val - 2)

            fig_rel = px.bar(
                top_rel, x='% Docs Cited', y='Country', orientation='h',
                color='% Docs Cited', color_continuous_scale='Blues', text_auto='.2f'
            )
            fig_rel.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis=dict(range=[zoom_min, 100], title="Avg % Docs Cited (Zoomed)"),
                height=400, coloraxis_showscale=False, margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_rel, use_container_width=True)
            st.caption("✅ **Insight:** High symmetry (Skew 0.05). Almost every paper published gets cited.")

        # --- RIGHT CHART: EXCELLENCE ---
        with col2:
            st.markdown("##### 2. Excellence: % Top 1% Papers (The Ceiling)")
            top_elite = impact_df.sort_values(by='% Documents in Top 1%', ascending=False).head(10)

            fig_elite = px.bar(
                top_elite, x='% Documents in Top 1%', y='Country', orientation='h',
                # Custom Gold Gradient
                color='% Documents in Top 1%', 
                color_continuous_scale=['#FFF8E1', '#FFC107', '#FF6F00'], 
                text_auto='.2f'
            )
            fig_elite.add_vline(x=1.0, line_dash="dash", line_color="red", annotation_text="Global Baseline (1%)")
            
            fig_elite.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis=dict(title="Avg % in Top 1%"),
                height=400, coloraxis_showscale=False, margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_elite, use_container_width=True)
            
            # Specific Country Insights from your EDA
            st.info("""
            🏆 **Key Performers:**
            - **🇸🇪 Sweden:** Overall Leader (Avg **1.93%**).
            - **🇧🇷 Brazil:** Most Consistent (Crossed 2% threshold **10 times**).
            - **🇩🇪 Germany:** Highest Single-Year Peak (**2.96%**).
            """)

# "⚔️4. Competitive Landscape"
    with tab4: 
        st.markdown("""
        <div class="insight-box orange-box">
            <h4>⚔️ Insight 4: The Ebb and Flow of Dominance</h4>
            <p>This timeline shows how the gap between the #1 and #2 performer has changed over the years, revealing periods of intense monopoly and close competition.</p>
            <ul>
                <li><b>Peak Dominance (2007):</b> China's massive spike shows a year of near-total market control.</li>
                <li><b>Trend Analysis:</b> A falling line indicates the research field is becoming more competitive, while a rising line indicates a leader is solidifying their position.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # --- Data Prep (No changes needed here) ---
        gap_data = []
        years = sorted(df['Year'].unique())
        
        for y in years:
            year_df = df[df['Year'] == y].sort_values(by='Times Cited', ascending=False)
            
            if len(year_df) >= 2:
                leader = year_df.iloc[0]
                runner = year_df.iloc[1]
                
                if runner['Times Cited'] > 0:
                    gap_pct = ((leader['Times Cited'] - runner['Times Cited']) / runner['Times Cited']) * 100
                else:
                    gap_pct = 0
                
                gap_data.append({
                    'Year': y, 
                    'Leader': leader['Country'], 
                    'Runner-Up': runner['Country'], 
                    'Dominance %': gap_pct, 
                    'Leader Citations': leader['Times Cited']
                })
        
        gap_df = pd.DataFrame(gap_data)

        # --- Visual: Replaced Bar Chart with Line Chart ---
        st.markdown("##### 📊 Trend of the Dominance Gap")
        
        fig_gap_line = px.line(
            gap_df,
            x='Year',
            y='Dominance %',
            markers=True,  # Add dots for each year
            title='How has the Leader\'s Advantage Changed Over Time?',
            hover_data=['Leader', 'Runner-Up', 'Leader Citations'], # Hover to see who was #1
            labels={'Dominance %': 'Lead Margin Over Runner-Up (%)'}
        )
        
        # Styling the line and markers for better visibility
        fig_gap_line.update_traces(
            line=dict(color='crimson', width=3),
            marker=dict(size=8, symbol='diamond')
        )

        # Adding a baseline for context
        fig_gap_line.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No Gap (Equal Performance)")
        
        fig_gap_line.update_layout(height=500, template='plotly_white')
        st.plotly_chart(fig_gap_line, use_container_width=True)

        # --- Top 5 Table (This is still very useful and kept) ---
        st.markdown("---")
        st.markdown("##### 🏆 Top 5 Most Dominant Years")
        top_5_dominance = gap_df.sort_values(by='Dominance %', ascending=False).head(5)
        display_table = top_5_dominance[['Year', 'Leader', 'Runner-Up', 'Dominance %']].copy()
        display_table['Dominance %'] = display_table['Dominance %'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            display_table, 
            hide_index=True, 
            use_container_width=True
        )

# "🚨5. Outlier Analysis"
    with tab5: 
        st.markdown("""
        <div class="insight-box red-box">
            <h4>🚨 Insight 5: The "Quality Ceiling" & Volume Spikes</h4>
            <p><b>Fundamental Asymmetry:</b> Our outlier analysis reveals a distinct difference in how Quantity and Quality behave:</p>
            <ul>
                <li><b>🏭 Mega-Producers (Volume Extremes):</b> The <code>Documents</code> distribution is highly skewed. Nations like <b>China</b> and <b>Italy</b> show extreme spikes, producing output far beyond the global median in specific years.</li>
                <li><b>💎 The Quality Ceiling:</b> In contrast, <b>Quality (CNCI) has NO statistical outliers</b>. This proves that while you can exponentially scale paper count (Quantity), you cannot engineer "abnormally high" impact scores (Quality). Quality stays within a predictable range.</li>
                <li><b>📉 Isolated Events:</b> These volume spikes are typically <b>one-off events</b> rather than sustained trends. They are likely driven by temporary factors (like policy shifts) rather than a permanent state of overproduction.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # --- Outlier Logic (No changes needed in logic, just visualization) ---
        Q1 = df['Documents'].quantile(0.25)
        Q3 = df['Documents'].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[df['Documents'] > upper_bound]

        # --- Visual ---
        fig_out = px.scatter(
            df, x='Year', y='Documents',
            color=df['Documents'].apply(lambda x: 'Outlier' if x > upper_bound else 'Normal'),
            color_discrete_map={'Outlier': '#EF553B', 'Normal': 'lightgrey'}, # Red for outliers
            hover_name='Country', 
            hover_data=['Year', 'Documents'],
            title='Identifying Years of "Hyper-Production" (Outliers > 1.5 IQR)',
            size='Documents',
            size_max=20 # Adjust bubble size
        )
        
        # Add Threshold Line
        fig_out.add_hline(
            y=upper_bound, 
            line_dash="dash", 
            line_color="red", 
            annotation_text=f"Statistical Threshold ({int(upper_bound)} Docs)",
            annotation_position="top right"
        )
        
        fig_out.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig_out, use_container_width=True)
        
        # Table Logic (Refined)
        if not outliers.empty:
            st.markdown("#### 🚩 Detected Anomalies (Mega-Production Years)")
            st.dataframe(
                outliers[['Country', 'Year', 'Documents']].sort_values(by='Documents', ascending=False), 
                hide_index=True,
                use_container_width=True
            )

# "🔗6. Correlation Analysis"
    with tab6:
        # 1. Calculate Correlations
        corr_weak = df['Collab-CNCI'].corr(df['CNCI'])
        corr_strong = df['Documents'].corr(df['Times Cited'])
        
        # 2. Insight Box (Comparing both)
        st.markdown(f"""
        <div class="insight-box purple-box">
            <h4>🤝 Insight 6: Correlation Contrast (The Weak vs. The Strong)</h4>
            <p>We analyzed two key relationships to see what drives success:</p>
            <ul>
                <li><b>❌ The Weak Link ({corr_weak:.4f}):</b> Collaboration Quality has <b>no linear relation</b> with Overall Research Quality. The trendline is flat.</li>
                <li><b>✅ The Strong Link ({corr_strong:.4f}):</b> Volume (Documents) has a <b>near-perfect positive correlation</b> with Impact (Citations). If you publish more, you get cited more (Quantity drives Total Impact).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Create 2 Columns for Side-by-Side Comparison
        col_c1, col_c2 = st.columns(2)
        
        # --- LEFT CHART: WEAK CORRELATION ---
        with col_c1:
            st.markdown(f"##### 1. Paradox: Collab vs Quality (r = {corr_weak:.2f})")
            try:
                trend_mode = "ols"
            except ImportError:
                trend_mode = None

            fig_weak = px.scatter(
                df, x='Collab-CNCI', y='CNCI', hover_data=['Country', 'Year'],
                trendline=trend_mode, opacity=0.6,
                title='<b>Weak Correlation</b><br><sup>Collaboration Impact does NOT predict Quality</sup>',
                labels={"Collab-CNCI": "Collab Impact", "CNCI": "Overall Quality"}
            )
            if trend_mode:
                fig_weak.update_traces(selector=dict(mode='lines'), line=dict(color='red', width=3))
            
            fig_weak.update_layout(height=450, template='plotly_white')
            st.plotly_chart(fig_weak, use_container_width=True)

        # --- RIGHT CHART: STRONG CORRELATION (NEW) ---
        with col_c2:
            st.markdown(f"##### 2. Predictable: Quantity vs Impact (r = {corr_strong:.2f})")
            
            fig_strong = px.scatter(
                df, x='Documents', y='Times Cited', hover_data=['Country', 'Year'],
                trendline=trend_mode, opacity=0.6,
                title='<b>Strong Correlation</b><br><sup>Volume strongly predicts Total Citations</sup>',
                labels={"Documents": "Total Documents", "Times Cited": "Total Citations"}
            )
            
            # Styling: Use Green line for Strong Positive Correlation
            if trend_mode:
                fig_strong.update_traces(selector=dict(mode='lines'), line=dict(color='green', width=3))
            
            fig_strong.update_layout(height=450, template='plotly_white')
            st.plotly_chart(fig_strong, use_container_width=True)
            
        st.info("💡 **Key Takeaway:** You can easily scale your **Total Citations** by publishing more papers (Right Chart), but you cannot easily scale your **Quality** just by signing collaborations (Left Chart).")

# "📈7. Performance Trends"
    with tab7:
        st.markdown("""
        <div class="insight-box green-box">
            <h4>🌍 Insight 7: A Dynamic Geopolitical Landscape</h4>
            <p><b>1. The Volume Race (Quantity):</b> It is not a static hierarchy but a <b>Three-Way Race</b> between the <b>UK, Spain, and Brazil</b>.</p>
            <ul>
                <li><b>The Challenger:</b> Brazil has emerged as a major powerhouse since 2010.</li>
            </ul>
            <p><b>2. The Quality Consistency (Impact):</b> High volume does not guarantee high quality.</p>
            <ul>
                <li><b>The Leader:</b> Among top publishers, <b>Spain</b> demonstrates superior and consistent quality (CNCI) over time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        available_countries = df['Country'].unique().tolist()
        defaults = ['UNITED KINGDOM', 'SPAIN', 'BRAZIL', 'CANADA', 'SWITZERLAND'] 
        valid_defaults = [c for c in defaults if c in available_countries]
        if not valid_defaults: 
            valid_defaults = available_countries[:5]
        
        # --- WIDGETS AT THE TOP ---
        selected_countries = st.multiselect("Select Countries to Compare", available_countries, default=valid_defaults)
        
        view_option = st.radio(
            "Select View Type:",
            ("View Trends Over Time", "View Overall Performance"),
            horizontal=True,
            label_visibility="collapsed" # Hide the label "Select View Type" to save space
        )
        st.markdown("---") # Visual Separator

        # --- CONDITIONAL DISPLAY LOGIC ---
        if selected_countries:
            # --- VIEW 1: TRENDS OVER TIME (Line Charts) ---
            if view_option == "View Trends Over Time":
                df_trend = df[df['Country'].isin(selected_countries)]
                col_t1, col_t2 = st.columns(2)
                
                with col_t1:
                    st.markdown("**📈 Volume Race (Year-wise)**")
                    fig_vol = px.line(df_trend, x='Year', y='Documents', color='Country', markers=True)
                    fig_vol.update_layout(legend=dict(orientation="h", y=-0.2, x=0)) 
                    st.plotly_chart(fig_vol, use_container_width=True)
                    
                with col_t2:
                    st.markdown("**💎 Quality Race (Year-wise)**")
                    fig_qual = px.line(df_trend, x='Year', y='CNCI', color='Country', markers=True)
                    fig_qual.add_hline(y=1.0, line_dash="dot", annotation_text="Global Avg", line_color="red")
                    fig_qual.update_layout(legend=dict(orientation="h", y=-0.2, x=0))
                    st.plotly_chart(fig_qual, use_container_width=True)

            # --- VIEW 2: OVERALL PERFORMANCE (Bar Charts) ---
            else:
                # Prepare Aggregated Data
                df_overall = df[df['Country'].isin(selected_countries)]
                overall_stats = df_overall.groupby('Country').agg(
                    Total_Documents=('Documents', 'sum'),
                    Average_CNCI=('CNCI', 'mean')
                ).reset_index()

                col_o1, col_o2 = st.columns(2)

                with col_o1:
                    st.markdown("**📊 Total Volume (Lifetime)**")
                    fig_vol_bar = px.bar(
                        overall_stats.sort_values('Total_Documents', ascending=True),
                        y='Country', x='Total_Documents', 
                        orientation='h', color='Country', text_auto='.2s'
                    )
                    fig_vol_bar.update_layout(showlegend=False, xaxis_title="Total Documents (Sum)")
                    st.plotly_chart(fig_vol_bar, use_container_width=True)

                with col_o2:
                    st.markdown("**✨ Average Quality (Lifetime)**")
                    fig_cnci_bar = px.bar(
                        overall_stats.sort_values('Average_CNCI', ascending=True),
                        y='Country', x='Average_CNCI',
                        orientation='h', color='Country', text_auto='.2f'
                    )
                    fig_cnci_bar.add_vline(x=1.0, line_dash="dot", annotation_text="Global Avg")
                    fig_cnci_bar.update_layout(showlegend=False, xaxis_title="Average Quality (CNCI)")
                    st.plotly_chart(fig_cnci_bar, use_container_width=True)
        else:
            st.warning("Please select at least one country.")
            
else:
    st.error("Could not load data.")