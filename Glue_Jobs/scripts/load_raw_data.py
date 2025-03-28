import sys
import logging
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse AWS Glue job arguments
args = getResolvedOptions(sys.argv, [
    "db_user", "db_password", "s3_bucket", "redshift_db", "redshift_schema", "TempDir",
    "jdbc_url", "awsuser", "aws_password", "aws_iam_role"
])

db_user = args["db_user"]
db_password = args["db_password"]
s3_output_path = f"s3://{args['s3_bucket']}/raw/"
jdbc_url = args["jdbc_url"]
awsuser = args["awsuser"]
aws_password = args["aws_password"]
aws_iam_role = args["aws_iam_role"]

logger.info("🚀 Glue job started...")
logger.info(f"🛢️ Database user: {db_user}")
logger.info(f"🗄️ Data will be saved to S3 bucket: {s3_output_path}")
logger.info(f"🛢️ Using JDBC URL: {jdbc_url}")

# Initialize Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Tables to process
tables = ["apartments", "apartment_attributes", "bookings", "user_viewing"]
logger.info(f"📋 Tables to process: {tables}")

# Load raw data from Glue Data Catalog
def load_table_from_catalog(table_name):
    return glueContext.create_dynamic_frame.from_catalog(
        database="airbnb_db",
        table_name=table_name
    ).toDF()

raw_bookings_df = load_table_from_catalog("bookings")
raw_apartments_df = load_table_from_catalog("apartments")
raw_apartment_attr_df = load_table_from_catalog("apartment_attributes")
raw_user_viewing_df = load_table_from_catalog("user_viewing")

# Define Redshift connection options
redshift_options = {
    "url": f"jdbc:redshift://redshift-cluster-1.ch5oimb3dzp5.eu-west-1.redshift.amazonaws.com:5439/{args['redshift_db']}",
    "user": awsuser,
    "password": aws_password,
    "redshiftTmpDir": f"{args['TempDir']}",
    "aws_iam_role": aws_iam_role
}

def write_to_redshift(df, table_name):
    try:
        logger.info(f"Writing {table_name} to Redshift...")
        redshift_options["dbtable"] = f"{args['redshift_schema']}.{table_name}"
        dyf = DynamicFrame.fromDF(df, glueContext, table_name)
        glueContext.write_dynamic_frame.from_options(dyf, connection_type="redshift", connection_options=redshift_options)
        logger.info(f"✅ Successfully written {table_name} to Redshift.")
    except Exception as e:
        logger.error(f"❌ Error writing {table_name} to Redshift: {str(e)}", exc_info=True)
        raise

write_to_redshift(raw_bookings_df, "raw_bookings")
write_to_redshift(raw_apartments_df, "raw_apartments")
write_to_redshift(raw_apartment_attr_df, "raw_apartment_attr")
write_to_redshift(raw_user_viewing_df, "raw_user_viewing")

logger.info("✅ Glue job completed successfully!")
job.commit()