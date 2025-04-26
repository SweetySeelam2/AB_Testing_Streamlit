import streamlit as st
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Marketing A/B Testing Analysis", layout="wide")

# Title
st.title('🚀 Amazon Marketing A/B Testing Analysis')

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('data/Marketing_AB_Testing.csv')
    return data

# Load data
data = load_data()

# Data Preview
st.subheader('📊 Sample of Marketing Dataset')
st.dataframe(data.head())

# Conversion Rate Calculation
st.subheader('Conversion Rate by Group')

# Map Test Group
data['test group'] = data['test group'].map({'psa': 0, 'ad': 1})
data['converted'] = data['converted'].astype(int)

# Group by Test Group
conversion_rates = data.groupby('test group')['converted'].mean().reset_index()
conversion_rates.columns = ['Test Group', 'Conversion Rate']

st.dataframe(conversion_rates)

# Extract rates
psa_rate = conversion_rates[conversion_rates['Test Group'] == 0]['Conversion Rate'].values[0]
ad_rate = conversion_rates[conversion_rates['Test Group'] == 1]['Conversion Rate'].values[0]

# Calculate % uplift
uplift_percentage = ((ad_rate - psa_rate) / psa_rate) * 100

# Show Uplift
st.metric("Ad Group Conversion Rate", f"{ad_rate*100:.2f}%")
st.metric("PSA Group Conversion Rate", f"{psa_rate*100:.2f}%")
st.metric("Uplift in Conversion (%)", f"{uplift_percentage:.2f}%")

# T-test
ad = data[data['test group'] == 1]['converted']
psa = data[data['test group'] == 0]['converted']

t_stat, p_value = stats.ttest_ind(ad, psa)

# T-test results
st.subheader('🧪 Hypothesis Testing Results')
st.write(f"T-statistic: **{t_stat:.4f}**")
st.write(f"P-value: **{p_value:.4f}**")

if p_value < 0.05:
    st.success('✅ Statistically Significant: The new ad strategy significantly improves conversion rates!')
else:
    st.error('❌ Not Statistically Significant: No strong evidence for conversion improvement.')

# Conversion by Hour
st.subheader('📈 Conversion Rate by Hour')
conversion_by_hour = data.groupby('most ads hour')['converted'].mean().reset_index()
fig, ax = plt.subplots()
ax.plot(conversion_by_hour['most ads hour'], conversion_by_hour['converted'], marker='o')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Conversion Rate')
ax.set_title('Conversion Rate by Hour')
st.pyplot(fig)

# Conversion by Day
st.subheader('📅 Conversion Rate by Day')
conversion_by_day = data.groupby('most ads day')['converted'].mean().reset_index()
fig2, ax2 = plt.subplots()
ax2.bar(conversion_by_day['most ads day'], conversion_by_day['converted'])
ax2.set_xlabel('Day of Week')
ax2.set_ylabel('Conversion Rate')
ax2.set_title('Conversion Rate by Day')
st.pyplot(fig2)

# Upload your already created combined visualization
st.subheader('🖼️ Combined Conversion Rate Trends')
st.image('images/Conversion_by_hour&Conversion_by_day.png', caption='Conversion Rate by Hour and Day')

# Business Impact
st.subheader('💼 Business Impact and Recommendations')
st.markdown("""
- **Statistically Significant Uplift:** 43.09% increase in conversion rate.
- **Financial Impact:** Over $3.5M monthly and $42M yearly revenue increase.
- **Peak Hours:** Focus marketing between **4 PM to 9 PM**.
- **Best Days:** Prioritize Monday and Tuesday campaigns.
- **Example:** Companies like Netflix can apply such A/B Testing to maximize marketing ROI by focusing ad spend during high-converting times and days.

Recommendations:
- Optimize Ad Campaign Timing between 2 PM - 9 PM.
- Launch Promotions Early Week (Monday, Tuesday).
- Behavioral Segmentation for personalized targeting.
- Dynamic Bidding during peak hours.
- Continuous A/B Testing of creative formats and landing pages.
""")

st.success('✅ Analysis Completed Successfully!')