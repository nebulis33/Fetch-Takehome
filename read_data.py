import json

import duckdb
from pandas import DataFrame


def create_users(connection):
    connection.execute(
        """
        CREATE OR REPLACE TABLE users (
            id TEXT PRIMARY KEY,
            active BOOLEAN,
            created_date TIMESTAMP,
            last_login TIMESTAMP,
            role TEXT,
            sign_up_source TEXT,
            state TEXT
        );
        """
    )

    connection.execute(
        """
        BEGIN TRANSACTION;
        INSERT OR IGNORE INTO users
        SELECT
            "_id"."$oid" AS id,
            active, 
            to_timestamp("createdDate"."$date"/1000) AS created_date, 
            to_timestamp("lastLogin"."$date"/1000) AS last_login, 
            role, 
            signUpSource AS sign_up_source, 
            state
        FROM read_json('raw_data/users.json');
        COMMIT;
        """)


def create_brands(connection):
    connection.execute(
        """
        CREATE OR REPLACE TABLE brands (
            id TEXT PRIMARY KEY,
            name TEXT,
            barcode TEXT,
            brand_code TEXT,
            category TEXT,
            category_code TEXT,
            cpg_id TEXT,
            top_brand BOOLEAN
            );
        """
    )

    connection.execute(
        """
        BEGIN TRANSACTION;
        INSERT OR IGNORE INTO brands
        SELECT
            "_id"."$oid" AS id,
            name,
            barcode,
            brandCode AS brand_code,
            category,
            categoryCode AS category_code,
            "cpg"."$id"."$oid" AS cpg_id,
            topBrand AS top_brand
        FROM read_json('raw_data/brands.json');
        COMMIT;
        """
    )


def create_receipts(connection):
    connection.execute(
        """
        CREATE OR REPLACE TABLE receipts (
            id TEXT PRIMARY KEY,
            bonus_points_earned INT,
            bonus_points_reason TEXT,
            creation_date TIMESTAMP,
            scan_date TIMESTAMP,
            finish_date TIMESTAMP,
            modified_date TIMESTAMP,
            points_awarded_date TIMESTAMP,
            points_earned INT,
            purchase_date TIMESTAMP,
            purchased_item_count INT,
            status TEXT,
            total_spent FLOAT,
            user_id TEXT
            );
        """
    )

    connection.execute(
        """
        BEGIN TRANSACTION;
        INSERT OR IGNORE INTO receipts
        SELECT
            "_id"."$oid" AS id,
            bonusPointsEarned AS bonus_points_earned,
            bonusPointsEarnedReason AS bonus_points_reason,
            to_timestamp("createDate"."$date" / 1000) AS creation_date,
            to_timestamp("dateScanned"."$date" / 1000) AS scan_date,
            to_timestamp("finishedDate"."$date" / 1000) AS finish_date,
            to_timestamp("modifyDate"."$date" / 1000) AS modified_date,
            to_timestamp("pointsAwardedDate"."$date" / 1000) AS points_awarded_date,
            pointsEarned AS points_earned,
            to_timestamp("purchaseDate"."$date" / 1000) AS purchase_date,
            purchasedItemCount AS purchase_item_count,
            rewardsReceiptStatus AS status,
            totalSpent AS total_spent,
            userID AS user_id
        FROM read_json('raw_data/receipts.json');
        COMMIT;
        """
    )


def create_purchases(connection):
    connection.execute(
        """
        CREATE OR REPLACE TABLE purchases (
            id TEXT PRIMARY KEY,
            receipt_id TEXT,
            barcode TEXT,
            description TEXT,
            brand_id TEXT,
            item_price FLOAT,
            discounted_price FLOAT,
            final_price FLOAT,
            purchase_quantity INT,
            needs_fetch_review BOOLEAN,
            prevent_target_gap_points BOOLEAN,
            user_flagged_barcode TEXT,
            user_flagged_new_item BOOLEAN,
            user_flagged_price FLOAT,
            user_flagged_purchase_quantity INT
            );
        """
    )

    items_data = []
    with open("raw_data/receipts.json", "r") as f:
        for line in f:
            entry = json.loads(line)
            receipt_id = entry["_id"]["$oid"]
            if "rewardsReceiptItemList" in entry:
                for item in entry["rewardsReceiptItemList"]:
                    items_data.append({
                        "receipt_id": receipt_id,
                        "barcode": item.get("barcode"),
                        "description": item.get("description"),
                        "brand_id": item.get("rewardsProductPartnerId"),
                        "item_price": item.get("itemPrice"),
                        "dicscounted_price": item.get("discountedItemPrice"),
                        "final_price": item.get("finalPrice"),
                        "purchase_quantity": item.get("quantityPurchased"),
                        "needs_fetch_review": item.get("needsFetchReview"),
                        "prevent_target_gap_points": item.get("preventTargetGapPoints"),
                        "user_flagged_barcode": item.get("userFlaggedBarcode"),
                        "user_flagged_new_item": item.get("userFlaggedNewItem"),
                        "user_flagged_price": item.get("userFlaggedPrice"),
                        "user_flagged_purchase_quantity": item.get("userFlaggedQuantity")
                    })
    purchases_df = DataFrame(items_data)

    connection.execute(
        """
            INSERT OR IGNORE INTO purchases
            SELECT ROW_NUMBER() OVER() AS id, *
            FROM purchases_df
        """
    )


if __name__ == "__main__":
    db = duckdb.connect(database="takehome-db.duckdb", read_only=False)
    create_users(db)
    create_brands(db)
    create_receipts(db)
    create_purchases(db)
    db.close()
