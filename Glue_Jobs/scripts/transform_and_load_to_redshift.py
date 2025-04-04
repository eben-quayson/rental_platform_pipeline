import sys
import logging
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import (
    greatest, least, col, to_date, datediff, year, month, weekofyear, 
    dayofmonth, last_day
)
from awsglue.dynamicframe import DynamicFrame

# Configure Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Glue context
args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "redshift_connection", "redshift_db", "redshift_schema", "TempDir", "db_user", "db_password", "s3_bucket", "mysql_host", "mysql_db", "jdbc_url", "IAM_role"]
)
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

logger.info("Glue job initialized successfully.")

# Load data from Glue Data Catalog
logger.info("Loading data from Glue Data Catalog...")
redshift_db = args["redshift_db"]

try:
    bookings_df = glueContext.create_dynamic_frame.from_catalog(
        database=redshift_db, table_name="bookings"
    ).toDF()
    apartments_df = glueContext.create_dynamic_frame.from_catalog(
        database=redshift_db, table_name="apartments"
    ).toDF()
    apartment_attrs_df = glueContext.create_dynamic_frame.from_catalog(
        database=redshift_db, table_name="apartment_attributes"
    ).toDF()
    user_viewings_df = glueContext.create_dynamic_frame.from_catalog(
        database=redshift_db, table_name="user_viewing"
    ).toDF()
    logger.info("Data loaded successfully.")
except Exception as e:
    logger.error(f"Error loading data: {str(e)}")
    raise

# Join apartments data
logger.info("Joining apartment attributes with apartment data...")
apartments_curated_df = apartments_df.join(apartment_attrs_df, "id", "left") \
    .select("id", "title", "source", "price", "currency", "listing_created_on", 
            "is_active", "last_modified_timestamp", "category", "body", "amenities", 
            "bathrooms", "bedrooms", "fee", "has_photo", "pets_allowed", "price_display", 
            "price_type", "square_feet", "address", "cityname", "state", "latitude", "longitude")

# Convert date columns
logger.info("Converting date columns...")
bookings_df = bookings_df.withColumn("checkout_date", to_date(col("checkout_date"), "dd/MM/yyyy"))
bookings_df = bookings_df.withColumn("checkin_date", to_date(col("checkin_date"), "dd/MM/yyyy"))

# Assign check-in and check-out
logger.info("Assigning earliest date to checkin and latest to checkout...")
bookings_df = bookings_df.withColumn("checkin", to_date(least(col("checkin_date"), col("checkout_date")))) \
                         .withColumn("checkout", to_date(greatest(col("checkin_date"), col("checkout_date"))))

# Compute Booking Duration
logger.info("Computing booking duration...")
bookings_df = bookings_df.withColumn("booking_duration", datediff(col("checkout"), col("checkin")))

# Extract additional date components
logger.info("Extracting additional date components...")
bookings_df = bookings_df.withColumn("days_in_month", dayofmonth(last_day(col("checkin_date"))))
apartments_curated_df = apartments_curated_df.withColumn("listing_created_on", to_date(col("listing_created_on"), "dd/MM/yyyy"))
apartments_curated_df = apartments_curated_df.withColumn("year", year(col("listing_created_on"))) \
                                             .withColumn("month", month(col("listing_created_on"))) \
                                             .withColumn("week", weekofyear(col("listing_created_on")))

# Prepare curated data
logger.info("Preparing curated dataframes...")
bookings_curated_df = bookings_df.select(
    col("booking_id"), col("user_id"), col("apartment_id"), col("booking_date"),
    col("checkin_date"), col("checkout_date"), col("booking_duration"),
    col("total_price"), col("currency"), col("booking_status")
)

user_engagement_curated_df = user_viewings_df.select(
    col("user_id"), col("apartment_id"), col("viewed_at"),
    col("is_wishlisted"), col("call_to_action")
)

# Fact and Dimension tables
fact_bookings_df = bookings_curated_df.select(
    col("booking_id"), col("user_id"), col("apartment_id"),
    col("booking_date"), col("checkin"), col("checkout"),
    col("booking_duration"), col("total_price"), col("currency"),
    col("booking_status")
)

dim_users_df = user_engagement_curated_df
dim_apartments_df = apartments_curated_df

logger.info("Curated dataframes prepared.")

# Write data to Redshift
redshift_options = {
    "url": args["jdbc_urld"],
    "user": args["db_user"],
    "password": args["db_password"],
    "redshiftTmpDir": args["TempDir"],
    "aws_iam_role": args["IAM_role"]
}

try:
    for table_name, df in [("fact_bookings", fact_bookings_df), ("dim_users", dim_users_df), ("dim_apartments", dim_apartments_df)]:
        logger.info(f"Writing {table_name} to Redshift...")
        redshift_options["dbtable"] = f"{args['redshift_schema']}.{table_name}"
        dyf = DynamicFrame.fromDF(df, glueContext, f"{table_name}_dyf")
        glueContext.write_dynamic_frame.from_options(dyf, connection_type="redshift", connection_options=redshift_options)
    logger.info("Data successfully written to Redshift.")
except Exception as e:
    logger.error(f"Error writing data to Redshift: {str(e)}")
    raise

# Commit the Glue job
logger.info("Committing Glue job...")
job.commit()
logger.info("Glue job completed successfully.")