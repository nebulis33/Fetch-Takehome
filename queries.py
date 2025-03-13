import duckdb

db = duckdb.connect(database="takehome-db.duckdb", read_only=False)

# What are the top 5 brands by receipts scanned for most recent month?
question_1 = db.sql(
    """
    SELECT
        name
    FROM
        brands
    JOIN purchases ON brands.cpg_id = purchases.brand_id
    GROUP BY
        name
    ORDER BY
        COUNT(DISTINCT receipt_id) DESC
    LIMIT
        5
    """
)

# When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
# When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
question_3_4 = db.sql(
    """
    SELECT
        status,
        ROUND(AVG(total_spent), 2) AS average_spend,
        SUM(purchased_item_count) AS total_items_purchased
    FROM
        receipts
    WHERE 
        status IN ('FINISHED', 'REJECTED')
    GROUP BY
        status
    """
)

# Which brand has the most spend among users who were created within the past 6 months?
question_5 = db.sql(
    """
    SELECT
        name
    FROM
        brands
    JOIN purchases on purchases.brand_id = brands.cpg_id
    JOIN receipts on receipts.id = purchases.receipt_id
    JOIN users on users.id = receipts.user_id
    WHERE
        users.creation_timestamp >= '2020-08-01'
    GROUP BY
        name
    ORDER BY
        SUM(total_spent) DESC
    LIMIT
        1
    """
)

# Which brand has the most transactions among users who were created within the past 6 months?
question_6 = db.sql(
    """
    SELECT
        name
    FROM
        brands
    JOIN purchases ON purchases.brand_id = brands.cpg_id
    JOIN receipts ON receipts.id = purchases.receipt_id
    JOIN users ON users.id = receipts.user_id
    WHERE
        users.creation_timestamp >= '2020-08-01'
    GROUP BY
        name
    ORDER BY
        COUNT(DISTINCT receipts.id) DESC
    LIMIT
        1
    """
)


if __name__ == "__main__":
    print(f"Here are the top 5 brands by numbers of reciepts scanned for the most recent month in the data:\n{question_1}")
    print("\n\n")
    print(f"Here is the averge spend and total number of items based on receipt status. Accepted (or Finished) had the most in both categories:\n{question_3_4}")
    print("\n\n")
    print(f"Here is the brand with the most spend among users created within the last 6 months of the data:\n{question_5}")
    print("\n\n")
    print(f"Here is the brand with the most transactions among users created within the last 6 months of the data:\n{question_5}")
    db.close()