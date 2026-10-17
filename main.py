import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. फोल्डर स्ट्रक्चर बनाना
os.makedirs("data", exist_ok=True)
os.makedirs("outputs/charts", exist_ok=True)

# 2. डमी डेटासेट तैयार करना (यदि फाइल मौजूद न हो)
data_path = "data/customer_data.csv"
if not os.path.exists(data_path):
    df_sample = pd.DataFrame({
        'CustomerID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'Age': [25, 32, 47, 51, 23, 35, 40, 29, 44, 38],
        'Gender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
        'AnnualIncome': [35000, 50000, 120000, 110000, 20000, 65000, 85000, 45000, 95000, 70000],
        'SpendingScore': [60, 45, 90, 85, 30, 55, 75, 50, 80, 65]
    })
    df_sample.to_csv(data_path, index=False)

# 3. डेटा लोड करना और क्लीनिंग (Data Cleaning)
print("--- डेटा लोड और क्लीनिंग प्रक्रिया शुरू ---")
df = pd.read_csv(data_path)

# मिसिंग वैल्यूज (Missing Values) को हटाना या भरना
df = df.dropna()
# डुप्लीकेट पंक्तियाँ हटाना
df = df.drop_duplicates()
print("डेटा सफलताપूर्वक क्लीन हो गया है। कुल रिकॉर्ड्स:", len(df))

# 4. डेटा एनालिसिस और इनसाइट्स (Analysis & Insights)
print("--- डेटा एनालिसिस किया जा रहा है ---")
avg_income = df['AnnualIncome'].mean()
avg_spending = df['SpendingScore'].mean()
summary_text = f"औसत वार्षिक आय (Average Income): {avg_income:.2f}\nऔसत स्पेंडिंग स्कोर (Average Spending Score): {avg_spending:.2f}"
print(summary_text)

# 5. चार्ट्स जनरेट करना (Charts Generation)
print("--- चार्ट्स बनाए जा रहे हैं ---")
sns.set(style="whitegrid")

# चार्ट 1: Age Distribution
plt.figure(figsize=(6, 4))
sns.histplot(df['Age'], bins=5, kde=True, color='blue')
plt.title('Customer Age Distribution')
plt.xlabel('Age')
plt.ylabel('Count')
chart1_path = 'outputs/charts/age_distribution.png'
plt.savefig(chart1_path)
plt.close()

# चार्ट 2: Spending vs Income
plt.figure(figsize=(6, 4))
sns.scatterplot(x='AnnualIncome', y='SpendingScore', hue='Gender', data=df, s=100)
plt.title('Annual Income vs Spending Score')
plt.xlabel('Annual Income')
plt.ylabel('Spending Score')
chart2_path = 'outputs/charts/spending_vs_income.png'
plt.savefig(chart2_path)
plt.close()
print("चार्ट्स सफलताપूर्वक सेव हो गए हैं।")

# 6. ऑटोमैटेड PDF रिपोर्ट जनरेशन (Report Generation)
print("--- PDF रिपोर्ट जनरेट की जा रही है ---")
pdf_path = 'outputs/customer_report.pdf'
c = canvas.Canvas(pdf_path, pagesize=letter)
width, height = letter

c.setFont("Helvetica-Bold", 18)
c.drawString(50, height - 50, "Customer Behavior Analysis Report")

c.setFont("Helvetica", 12)
c.drawString(50, height - 90, f"Total Customers Analyzed: {len(df)}")
c.drawString(50, height - 115, f"Average Annual Income: {avg_income:.2f}")
c.drawString(50, height - 140, f"Average Spending Score: {avg_spending:.2f}")

c.drawString(50, height - 180, "Key Insights:")
c.drawString(70, height - 200, "- Young customers show high spending scores relative to their income.")
c.drawString(70, height - 220, "- Middle-aged customer segments have stable annual incomes.")

# PDF में चार्ट जोड़ना
c.drawImage(chart1_path, 50, height - 480, width=220, height=150)
c.drawImage(chart2_path, 290, height - 480, width=220, height=150)

c.save()
print(f"सफलता! रिपोर्ट यहाँ सेव हुई: {pdf_path}")