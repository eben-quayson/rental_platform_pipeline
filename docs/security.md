# 🔒 Airbnb Data Pipeline - Security Documentation

## 📌 Overview

Security is a **top priority** for the Airbnb Data Pipeline. This document outlines the security **controls, policies, and best practices** implemented to ensure **data integrity, confidentiality, and compliance** across all components of the pipeline.

---

## 🔑 **Security Principles**
The security model is based on the **CIA Triad (Confidentiality, Integrity, and Availability)**:

1. **Confidentiality** – Data is **protected** from unauthorized access.
2. **Integrity** – Data is **accurate** and **has not been tampered with**.
3. **Availability** – Data is **accessible** only to authorized users when needed.

---

## 🔍 **Authentication & Access Control**

### **1️⃣ Identity and Access Management (IAM)**
- **IAM roles and policies** enforce **least privilege access**.
- IAM policies restrict:
  - Who can start the **AWS Step Functions** workflow.
  - Who can access **AWS Glue jobs** and **Redshift tables**.
  - Which services can interact with **Amazon S3, RDS, and Redshift**.
- Example **IAM Policy for Glue** (Restricting S3 bucket access):
  ```json
  {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::airbnb-data-pipeline-bucket/*"
  }
  ```

### **2️⃣ Amazon RDS Security**
- **Private VPC Deployment** – RDS instances are **not exposed** to the public internet.
- **IAM Authentication** – Instead of using **static passwords**, RDS uses **IAM-based authentication**.
- **Database User Roles**:
  - `admin`: Full control (restricted access).
  - `etl_user`: Only reads and writes to staging tables.
  - `analyst`: Read-only access to Redshift.

### **3️⃣ Amazon Redshift Security**
- **Cluster Encryption** – Redshift uses **AWS Key Management Service (KMS)** for encryption.
- **VPC Subnet Restrictions** – Redshift is **only accessible from within the VPC**.
- **Connection via IAM Roles** – Prevents **hardcoded passwords**.
- **Row-Level Security (RLS)** – Limits data access **based on user roles**.

### **4️⃣ Amazon S3 Security**
- **Private S3 Buckets** – Data is **only accessible via IAM roles**.
- **S3 Bucket Policies**:
  - Enforce **TLS encryption** during data transfer.
  - Block **public access** to sensitive data.
  - Enable **versioning** to track data modifications.

---

## 🔐 **Data Encryption**

### **1️⃣ Data at Rest**
- **Amazon S3**: Uses **AES-256 encryption**.
- **Amazon RDS & Redshift**: **Encrypted at rest** with **AWS KMS**.
- **AWS Glue**: Encrypts temporary storage in **Amazon S3**.

### **2️⃣ Data in Transit**
- **All connections use TLS (HTTPS) encryption**.
- **Redshift requires SSL for client connections**.
- **AWS Secrets Manager** securely stores credentials.

---

## 🏢 **Compliance & Regulatory Considerations**

### **1️⃣ Data Protection Compliance**
- Follows **GDPR, CCPA, and PCI DSS** best practices.
- User data in **RDS is anonymized** before being moved to Redshift.

### **2️⃣ Security Reviews & Penetration Testing**
- Periodic **penetration testing** simulates attacks.
- **Automated vulnerability scanning** for exposed credentials.

### **3️⃣ Backup & Disaster Recovery**
- **RDS automated backups** stored for **7–30 days**.
- **Redshift snapshots** stored in S3 for disaster recovery.

---

## 🚨 **Incident Response & Mitigation**
| **Scenario** | **Mitigation Strategy** |
|-------------|------------------------|
| **Unauthorized Access** | Use **IAM Access Analyzer** and **AWS Config** for misconfiguration alerts. |
| **Data Breach** | Rotate **IAM credentials** and enforce **MFA**. |
| **DDoS Attack** | AWS **Shield Standard** protects against DDoS threats. |
| **Data Loss** | **Automated backups** for recovery. |

---

## 🛠️ **Best Practices**
✅ **Use temporary credentials (IAM roles) instead of static passwords.**  
✅ **Regularly rotate AWS Secrets Manager credentials.**  
✅ **Limit access to sensitive data based on user roles.**  
✅ **Enable Redshift audit logging to track queries.**  
✅ **Use AWS Config to monitor security rule violations.**  

---

## 📜 **Conclusion**
This document outlines the security measures taken to **protect Airbnb data** across **Amazon RDS, Redshift, S3, and Glue**. By implementing **IAM roles, encryption, and compliance practices**, the pipeline ensures **secure data processing** while mitigating security risks.

```
