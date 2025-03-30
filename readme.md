# Airbnb Data Pipeline

## 📌 Project Overview

This project implements an **Airbnb data processing pipeline** using **AWS Step Functions**, which is automatically triggered by an **Amazon EventBridge** schedule. The pipeline extracts raw data from **Amazon RDS**, processes it, and loads **aggregated business metrics** into **Amazon Redshift** for analytics.

### **Goals**
- Automate the ETL process to handle Airbnb bookings and apartment listings.
- Compute key business insights, such as occupancy rates, average booking durations, and repeat customer rates.
- Store aggregated metrics in **Amazon Redshift** for reporting and decision-making.

---

## 🏗️ Architecture & Workflow

### **1️⃣ Data Sources (Amazon RDS)**
The **source data** is stored in **Amazon RDS** and consists of multiple tables:

- **`user_viewing`**: Tracks user interactions with listings.
- **`apartment`**: Contains details of rental properties.
- **`apartment_attributes`**: Stores additional apartment metadata.
- **`bookings`**: Captures booking transactions, including check-in/check-out dates and pricing.

### **2️⃣ ETL Orchestration (AWS Step Functions)**
- **Amazon EventBridge** triggers the Step Function **on a scheduled basis**.
- The Step Function:
  - **Extracts** data from **Amazon RDS**.
  - **Transforms** and aggregates the data.
  - **Loads** processed data into **Amazon Redshift**.

### **3️⃣ Data Processing & Storage**
- Extract raw data from **Amazon RDS**.
- Perform **aggregations** and calculations.
- Store results in **Amazon Redshift** for analytical queries.

---

## 📊 Business Metrics

| **Metric**                        | **Description** |
|-----------------------------------|---------------|
| `avg_listing_price_weekly`        | Average price of active rental listings per week. |
| `occupancy_rate_monthly`          | Percentage of available nights booked each month. |
| `most_popular_locations_weekly`   | Top locations based on bookings per week. |
| `top_performing_listings_weekly`  | Properties with the highest revenue per week. |
| `total_bookings_per_user_weekly`  | Number of rentals booked per user per week. |
| `avg_booking_duration_monthly`    | Average length of stay per month. |
| `repeat_customer_rate`            | Percentage of users making multiple bookings. |

---

## 📂 **Database Schema**

### **Amazon RDS (Raw Data Tables)**

#### **user_viewing**
```sql
CREATE TABLE user_viewing (
    user_id BIGINT,
    apartment_id BIGINT,
    viewed_at TIMESTAMP,
    is_wishlisted BOOLEAN,
    call_to_action VARCHAR(255)
);
```

#### **apartment**
```sql
CREATE TABLE apartment (
    id BIGINT PRIMARY KEY,
    title VARCHAR(255),
    source VARCHAR(255),
    price DOUBLE PRECISION,
    currency VARCHAR(10),
    listing_created_on DATE,
    is_active BOOLEAN,
    last_modified TIMESTAMP
);
```

#### **apartment_attributes**
```sql
CREATE TABLE apartment_attributes (
    apartment_id BIGINT PRIMARY KEY,
    attribute_name VARCHAR(255),
    attribute_value VARCHAR(255)
);
```

#### **bookings**
```sql
CREATE TABLE bookings (
    booking_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    apartment_id BIGINT,
    booking_date VARCHAR(255),
    checkin_date DATE,
    checkout_date DATE,
    booking_duration INT,
    total_price DOUBLE PRECISION,
    currency VARCHAR(10),
    booking_status VARCHAR(50)
);
```

---

### **Amazon Redshift (Metrics Tables)**

#### **Average Listing Price Per Week**
```sql
CREATE TABLE avg_listing_price_weekly (
    year INT,
    month INT,
    week INT,
    avg_price DOUBLE PRECISION
);
```
##### **Query to Populate the Table**
```sql
INSERT INTO avg_listing_price_weekly
SELECT 
    EXTRACT(YEAR FROM listing_created_on) AS year,
    EXTRACT(MONTH FROM listing_created_on) AS month,
    EXTRACT(WEEK FROM listing_created_on) AS week,
    AVG(price) AS avg_price
FROM dim_apartments
WHERE is_active = TRUE
GROUP BY 1, 2, 3;
```

#### **Occupancy Rate Per Month**
```sql
CREATE TABLE occupancy_rate_monthly (
    year INT,
    month INT,
    apartment_id BIGINT,
    booked_nights INT,
    total_available_nights INT,
    occupancy_rate DOUBLE PRECISION
);
```
##### **Query to Populate the Table**
```sql
INSERT INTO occupancy_rate_monthly
SELECT 
    EXTRACT(YEAR FROM checkin_date) AS year,
    EXTRACT(MONTH FROM checkin_date) AS month,
    apartment_id,
    SUM(booking_duration) AS booked_nights,
    30 AS total_available_nights,
    (SUM(booking_duration) * 100.0) / 30 AS occupancy_rate
FROM fact_bookings
WHERE booking_status = 'confirmed'
GROUP BY 1, 2, 3;
```

#### **Repeat Customer Rate**
```sql
CREATE TABLE repeat_customer_rate (
    booking_date DATE NOT NULL,
    total_users INT,
    repeat_customers INT,
    repeat_customer_rate DOUBLE PRECISION
);
```
##### **Query to Populate the Table**
```sql
WITH repeat_customers AS (
    SELECT 
        user_id,
        COUNT(DISTINCT TO_DATE(booking_date, 'DD/MM/YYYY')) AS booking_count
    FROM fact_bookings
    GROUP BY user_id
    HAVING COUNT(DISTINCT TO_DATE(booking_date, 'DD/MM/YYYY')) > 1
)
INSERT INTO repeat_customer_rate
SELECT 
    TO_DATE(booking_date, 'DD/MM/YYYY') AS booking_date,
    COUNT(user_id) AS total_users,
    COUNT(DISTINCT CASE WHEN rc.user_id IS NOT NULL THEN b.user_id END) AS repeat_customers,
    (COUNT(DISTINCT CASE WHEN rc.user_id IS NOT NULL THEN b.user_id END) * 100.0) / NULLIF(COUNT(user_id), 0) AS repeat_customer_rate
FROM fact_bookings b
LEFT JOIN repeat_customers rc ON b.user_id = rc.user_id
GROUP BY 1;
```

---

## ⚙️ **Pipeline Execution Flow**
1. **Amazon EventBridge** triggers the **AWS Step Function** on a scheduled basis.
2. **Step Functions** executes:
   - Extract data from **Amazon RDS**.
   - Transform and aggregate the data.
   - Load the processed data into **Amazon Redshift**.
3. **Redshift tables** are updated with new insights.

---

## 🛠️ **How to Run the Pipeline**
### **1️⃣ Triggering the Pipeline (AWS CLI)**
```sh
aws stepfunctions start-execution --state-machine-arn <state-machine-arn>
```
Alternatively, you can trigger the execution from the **AWS Console**.

### **2️⃣ Querying Data in Amazon Redshift**
Example query to fetch the latest **average listing price**:
```sql
SELECT * FROM avg_listing_price_weekly ORDER BY year DESC, month DESC, week DESC;
```
Replace with the relevant table to fetch other metrics.

---

## 🚀 Future Enhancements
- Implement real-time streaming of booking data using **AWS Kinesis**.
- Optimize Redshift queries with **materialized views**.
- Add machine learning models to predict **occupancy rates**.

---

## 📖 References
- [AWS Step Functions Documentation](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon Redshift Best Practices](https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices.html)
- [Amazon RDS Documentation](https://docs.aws.amazon.com/rds/index.html)

---

## 📜 License
This project is licensed under the **MIT License**.
Author: Ebenezer Quayson

```