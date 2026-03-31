# Intelligent Environmental Travel-Safety System

## 1. Problem Statement
Travelers frequently face environmental and physical health risks due to unpredictable air quality and pollution levels in various cities. Existing platforms either ignore this data or present it in overly technical formats (like AQI values, PM2.5 concentrations) which are difficult for the average traveler to interpret. There is a need for an intelligent travel-safety decision-support application that translates complex environmental data into simple, actionable travel advisories without using technical machine-learning terminology.

## 2. Research Questions
1. How can long-term air quality data be transformed into actionable travel safety insights?
2. What are the dominant environmental factors determining the suitability of a destination for short-term vs. long-term stays?
3. How can complex predictive models (like Random Forests) be utilized in the backend to determine exposure drivers while maintaining a non-technical, user-friendly interface?
4. How can city-level AQI data serve as a reliable proxy for district-level exposure mapping?

## 3. Dataset Description
The application utilizes the `india_aqi_2015_2023_all_cities.csv` dataset.
- **Scope**: Indian cities from 2015 to 2023.
- **Attributes Used**: `date`, `City`, `Air Quality` (Categorical AQI), `Index Value` (Numerical AQI), and `Prominent Pollutant`.
- **Modifications**: The dataset is processed to extract temporal features such as `Year`, `Month`, and `Season` to understand long-term and seasonal exposure patterns.

## 4. Feature Engineering Workflow
1. **Temporal Extraction**: Parsed the `date` column to distinct `Year` and `Month` features.
2. **Seasonal Categorization**: Mapped months into distinct seasons: Winter (Dec-Feb), Summer (Mar-May), Monsoon (Jun-Aug), and Post-Monsoon (Sep-Nov).
3. **Safety Vocabulary Mapping**: Converted technical AQI categories into user-friendly vocabulary:
   - *Good / Satisfactory* $\rightarrow$ **Safe**
   - *Moderate* $\rightarrow$ **Moderate Exposure**
   - *Poor / Very Poor / Severe* $\rightarrow$ **High Exposure**
4. **Proxy Mapping**: District-level mapping proxy is achieved by grouping and classifying city-level data.

## 5. Backend Risk Estimation Logic
In the backend, a **Random Forest Classifier** is deployed to evaluate the structured environmental data. The model is trained to classify the exposure risk status based on time of year, city location, and primary pollutant. Following training, the **Feature Importance** mechanism is used to extract the major exposure drivers (e.g., Seasonal Timing, Long-term Trend). These drivers inform the advisory logic. *Crucially, all algorithmic terminology (Random Forest, accuracy, models) is strictly restricted to the backend and never exposed to the end-user.*

## 6. Travel Safety Insight Generation Logic
The insight engine aggregates historical exposure probabilities:
- **Safe Travel Window Detection**: Evaluates the percentage of "Safe" days per month. Months exceeding a 50% safety threshold are recommended.
- **Long-Stay Suitability Rating**: Calculated by assessing the overall percentage of "Safe" days across the selected timeline. A threshold of >65% grants an "Excellent for Long-Stay" rating.
- **Environmental Comfort Score**: A scaled 1-10 proxy score derived from overall environmental safety rates.

## 7. Streamlit Dashboard Implementation
The application is built using **Streamlit**. Key UI features include:
- **Clean Interface**: A non-technical dashboard styled as a premium travel advisory tool.
- **Controls**: Sidebar dropdown for City/District selection and sliders for timeframe analysis.
- **Visualizations**: 
  - *Monthly Exposure Heatmap* (Plotly)
  - *Environmental Stability Trend Graph* (Plotly Line Chart)
  - *Seasonal Disruption Risk Bar Chart* (Plotly)
  - *National Ranking Comparison Gauge* (Comparing selected city to national medians).
Libraries used: `streamlit`, `pandas`, `plotly`. No JavaScript or external front-end frameworks were used.

## 8. Travel Recommendation Engine
The recommendation engine synthesizes the insight logic directly into actionable text for the user:
- Identifies and explicitly lists the **Best Months to Travel**.
- Flags **Months Requiring Precautions** based on historical high-exposure percentages.
- Dictates **Precaution Levels** (e.g., "Precautions Highly Advised" vs "Short Visits Recommended").

## 9. District-Level Exposure Mapping
Due to the structure of the dataset, City-level AQI values are utilized as a direct proxy for District-level environmental exposure. The application allows users to select a destination, and the engine computes the district-level safety classification by evaluating the historical AQI footprint of the corresponding proxy city, plotting its ranking against global dataset medians.

## 10. Final Conclusion and Future Scope
### Conclusion
The developed Streamlit application successfully acts as an intelligent environmental travel-safety decision-support tool. It bridges the gap between raw, complex environmental datasets and practical travel planning, strictly adhering to the requirement of shielding the user from technical ML jargon.

### Future Scope
- **Live Data Integration**: Connecting to realtime AQI APIs to offer both historical and current travel advisories.
- **Broader Geographies**: Expanding the dataset to include global cities and international environmental indices.
- **Additional Environmental Risks**: Integrating complementary datasets like extreme weather warnings, flood risks, and temperature anomalies to build a holistic physical-safety travel engine.
