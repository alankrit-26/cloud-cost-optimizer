Cloud Cost Optimizer (LLM-Powered)

A menu-driven CLI tool that helps users analyze and optimize cloud infrastructure costs using LLM-based reasoning combined with deterministic cost analysis.

Users provide a plain-English project description, and the system:

1. Extracts a structured project profile

2. Generates realistic, budget-aware synthetic cloud billing

3. Performs cost analysis

4. Produces actionable, multi-cloud cost optimization recommendations

Features

1. Project Profile Extraction (LLM-based)

2. Synthetic Cloud Billing Generation (budget-aware)

3. Deterministic Cost Analysis (Python logic)

4. LLM-Based Cost Optimization Recommendations

5. Menu-Driven CLI Orchestrator

6. Cloud-Agnostic & Multi-Cloud Recommendations

7. Open-Source & Free-Tier Suggestions


Setup Instructions:

Clone the repository:
git clone <repository-url>
cd cloud-cost-optimizer


Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows


Install dependencies
pip install -r requirements.txt


Configure Hugging Face API Key:
Create a .env file in the root directory:
HF_API_TOKEN=your_huggingface_api_token_here


How to Run:-

python cli.py

 Cloud Cost Optimizer CLI
1. Enter new project description
2. Run complete cost analysis
3. View recommendations
4. Export report
5. Exit


Example Workflow

Step 1: Enter Project Description

choose option 1

Hi, I want to build a market analysis tool for e-commerce. The tool should track
the highest-selling products each month. For the front end, I am using React, for the backend
Node.js, and MongoDB for storing the data. I’ll use Nginx as a proxy server and AWS for hosting.
My monthly budget is 3000.

Step 2: Run Complete Cost Analysis

choose option 2

This will automatically:
Extract project profile → project_profile.json
Generate synthetic billing → mock_billing.json
Analyze costs and generate recommendations → cost_optimization_report.json

Step 3: View Recommendations
Choose option 3 to view a summary of optimization recommendations directly in the CLI.

Step 4: Export Report
Choose option 4 to export the final optimization report to a custom location.
