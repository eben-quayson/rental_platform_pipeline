Sure! Below is the **Architecture Documentation** in **README format**, detailing the pipeline components, data flow, and execution process.  

---

```markdown
# 📐 Airbnb Data Pipeline - Architecture Documentation

## 📌 Overview

The **Airbnb Data Pipeline** is a fully automated **ETL (Extract, Transform, Load)** pipeline designed to process Airbnb-related data for analytics. It is built using **AWS Step Functions**, **Amazon RDS**, **Amazon Redshift**, and supporting AWS services. The pipeline extracts raw data from **Amazon RDS**, transforms it, and loads it into **Amazon Redshift** to generate key business metrics.

---

## 🏗️ **System Architecture**

### **1️⃣ Architecture Diagram**
### Image: ![Airbnb Data Pipeline Architecture](docs/architecture.png)
The diagram below illustrates how data flows through the pipeline:

```
┌──────────────────────────┐
│  📅 Amazon EventBridge   │  (Scheduled trigger)
└──────────┬──────────────┘
           ▼
┌──────────────────────────┐
│ 🏗️ AWS Step Functions    │  (Orchestrates ETL)
└──────────┬──────────────┘
           ▼
┌──────────────────────────┐
│  📡 Amazon RDS (MySQL)   │  (Raw Data Source)
└──────────┬──────────────┘
           ▼
┌──────────────────────────┐
│ 🛠️ AWS Glue (ETL Jobs)   │  (Transforms Data)
└──────────┬──────────────┘
           ▼
┌──────────────────────────┐
│  🛢️ Amazon Redshift      │  (Aggregated Metrics)
└──────────┬──────────────┘
           ▼
┌──────────────────────────┐
│ 📊 BI & Reporting        │  (Power BI, Tableau)
└──────────────────────────┘
```

---

## 🔄 **Pipeline Execution Flow**

### **1️⃣ Data Extraction**
- The pipeline is triggered **automatically** by an **Amazon EventBridge** schedule.
- **Step Functions** initiates an **AWS Glue job** to extract raw data from **Amazon RDS**.

### **2️⃣ Data Transformation**
- The Glue job:
  - **Cleans** and standardizes **booking dates, pricing, and currency**.
  - Computes **aggregated metrics**, such as occupancy rates and booking durations.
  - **Joins multiple tables** (e.g., bookings, apartments, users).

### **3️⃣ Data Loading**
- The transformed data is **written into Amazon Redshift**.
- Metrics tables such as **occupancy rate, repeat customers, and average price per listing** are updated.

### **4️⃣ Data Consumption**
- **Amazon Redshift** serves as the analytics data warehouse.
- BI tools like **Power BI** and **Tableau** query the data for business insights.

---

## 📂 **Component Breakdown**

### **1️⃣ Amazon RDS (Relational Database Service)**
- Stores raw Airbnb data.
- Contains tables:
  - `user_viewing`
  - `apartment`
  - `apartment_attributes`
  - `bookings`

### **2️⃣ AWS Step Functions**
- Orchestrates the **ETL process** in a **serverless** manner.
- Ensures proper sequencing of data extraction, transformation, and loading.

### **3️⃣ AWS Glue**
- Performs **data transformation** tasks, such as:
  - Parsing and cleaning `booking_date` formats.
  - Computing **aggregated booking metrics**.
  - Joining multiple tables into **a single analytical dataset**.

### **4️⃣ Amazon Redshift**
- Stores **aggregated data** for analytics.
- Contains tables:
  - `avg_listing_price_weekly`
  - `occupancy_rate_monthly`
  - `repeat_customer_rate`
  - `total_bookings_per_user_weekly`

### **5️⃣ Amazon EventBridge**
- **Schedules** the pipeline execution.

---

## 📊 **Key Metrics Processed**

| **Metric**                       | **Computation** |
|----------------------------------|----------------|
| `avg_listing_price_weekly`       | Avg. price of active listings per week. |
| `occupancy_rate_monthly`         | Booked nights ÷ available nights. |
| `repeat_customer_rate`           | Users with multiple bookings ÷ total users. |
| `total_bookings_per_user_weekly` | Total number of bookings per user per week. |

---

## 🚀 **How to Run the Pipeline**
### **1️⃣ Trigger the ETL Process Manually**
If needed, trigger execution via AWS CLI:
```sh
aws stepfunctions start-execution --state-machine-arn <state-machine-arn>
```

### **2️⃣ Query Data in Amazon Redshift**
```sql
SELECT * FROM avg_listing_price_weekly ORDER BY year DESC, month DESC, week DESC;
```

---

## 🏆 **Benefits of This Architecture**
✅ **Scalable:** Serverless ETL allows auto-scaling.  
✅ **Cost-Effective:** Only processes data when scheduled.  
✅ **Real-Time Analytics:** Metrics are continuously updated.  
✅ **Automated:** No manual intervention required.  

---

## 🔧 **Future Enhancements**
- Implement real-time streaming with **AWS Kinesis**.
- Optimize Redshift queries using **Materialized Views**.
- Apply **Machine Learning** to forecast demand.

---

## 📖 References
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon Redshift Best Practices](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices.html)
- [Amazon RDS Documentation](https://docs.aws.amazon.com/rds/index.html)

---

## 📜 License
This project is licensed under the **MIT License**.

```
