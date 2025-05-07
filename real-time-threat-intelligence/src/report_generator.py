import psycopg2
import os
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../api/osint.env'))

# Database connection setup
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Function to fetch threat data from database
def fetch_threat_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query to get threat data with the updated threat_name column
        cursor.execute("""
            SELECT ip_address, threat_name, vt_score, abuse_score
            FROM threat_data
            WHERE threat_name IS NOT NULL;
        """)
        
        threat_data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return threat_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Function to generate the threat report in PDF format
def generate_report():
    # Fetch threat data
    threat_data = fetch_threat_data()
    
    if not threat_data:
        print("No data available to generate the report.")
        return

    # Create a PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add a header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Threat Intelligence Report", ln=True, align="C")
    
    # Add the threat data to the report
    pdf.set_font("Arial", "", 12)
    
    for ip_address, threat_name, vt_score, abuse_score in threat_data:
        pdf.ln(10)  # Add line break
        pdf.cell(200, 10, f"IP Address: {ip_address}", ln=True)
        pdf.cell(200, 10, f"Threat Name: {threat_name}", ln=True)
        pdf.cell(200, 10, f"VT Score: {vt_score}", ln=True)
        pdf.cell(200, 10, f"Abuse Score: {abuse_score}", ln=True)

    # Save the PDF report
    pdf.output("threat_report.pdf")
    print("Report generated: threat_report.pdf")

# Main execution
if __name__ == "__main__":
    generate_report()
