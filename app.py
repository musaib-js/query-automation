from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
import os
import logging
from queryclassification import classify_query
from get_recommendation import get_recommendation
from notifications import init_mail, send_email

dotenv.load_dotenv()

app = Flask(__name__)

DB_URI = os.getenv("MONGO_URI")
client = MongoClient(DB_URI, server_api=ServerApi("1"))

db = client["CustQueries"]
queries_collection = db["Queries"]

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

init_mail(app)

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

logging.basicConfig(level=logging.INFO)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY environment variable.")


@app.route("/submit-dispute", methods=["POST"])
def submit_dispute():
    try:
        data = request.json

        query = data["query"]
        cust_id = data["cust_id"]
        transaction_id = data["transaction_id"]

        classification = classify_query(query)

        category = classification["category"]
        risk_level = classification["risk_level"]

        existing_query = queries_collection.find({"transaction_id": transaction_id})
        existing_query = list(existing_query)

        num_existing_queries = len(existing_query)

        priority = "Normal"

        if num_existing_queries > 3:
            priority = "High"
        elif num_existing_queries > 1 and num_existing_queries <= 3:
            priority = "Medium"

        recommendation = get_recommendation(query, category)

        queries_collection.insert_one(
            {
                "cust_id": cust_id,
                "transaction_id": transaction_id,
                "query": query,
                "category": category,
                "risk_level": risk_level,
                "priority": priority,
                "recommendation": recommendation,
            }
        )

        # Route to the specific customer service team
        send_email(
            to="b120061@iiit-bh.ac.in",
            subject=f"Query - Customer ID: {cust_id}".format(cust_id=cust_id),
            body=f"""Dear Team,
            
            The customer with ID {cust_id} has raised a query with the following details:
            
            Query: {query}
            
            The query has been classified as follows:
            
            Category: {category}
            
            Risk Level: {risk_level}
            
            Priority: {priority}
            
            Recommendation: {recommendation}
            
            Best,
            
            Banking Automation Team
            """,
        )

        return jsonify(
            {
                "category": category,
                "risk_level": risk_level,
                "priority": priority,
                "recommendation": recommendation,
            }
        )

    except Exception as e:
        logging.error(f"Error submitting dispute: {e}")
        return jsonify({"error": "Error submitting dispute"}), 500


if __name__ == "__main__":
    app.run(debug=True)
