# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# (Your API key setup remains the same)
client = OpenAI(api_key="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")

# --- 1. Data Loading and Analysis (Encapsulated) ---
# This runs once when the app starts
try:
    df = pd.read_excel('media_data.xlsx')
    channel_performance = df.groupby('channel').agg(
        total_spends=('spends', 'sum'),
        total_leads=('leads', 'sum'),
        total_traffic=('website_traffic', 'sum'),
        total_clicks=('ad_clicks', 'sum')
    ).reset_index()
    channel_performance['cost_per_lead'] = channel_performance['total_spends'] / channel_performance['total_leads']
    channel_performance['cost_per_click'] = channel_performance['total_spends'] / channel_performance['total_clicks']
    DATA_SUMMARY_STRING = channel_performance.to_string()
except FileNotFoundError:
    DATA_SUMMARY_STRING = "Error: The Excel file was not found."
    print(DATA_SUMMARY_STRING)
except Exception as e:
    DATA_SUMMARY_STRING = f"An error occurred while reading the Excel file: {e}"
    print(DATA_SUMMARY_STRING)

# --- 2. AI Agent Core Logic ---
def get_ai_response(prompt_messages):
    """Sends a list of messages to the AI model and gets a response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- 3. The API Endpoint ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    conversation_history = data.get('history')

    # Add the user's new message to the history
    conversation_history.append({"role": "user", "content": user_input})

    # Check if this is the first message to add the system prompt
    if len(conversation_history) == 1:
        system_prompt = {
            "role": "system",
            "content": f"""
            You are MediaPlan, an expert AI media strategist. Your primary objective is to assist users in creating a simple, effective media plan by leveraging historical campaign performance data.

            My recommendations will be based exclusively on the following historical data:
            {DATA_SUMMARY_STRING}

            To begin, I require some essential information about your new campaign. Please provide me with the following details:
            Campaign Objectives: What are you hoping to achieve with this campaign? (e.g., brand awareness, lead generation, sales)
            Total Budget: What is the total amount of money you have allocated for this campaign?
            Key Performance Indicator (KPI): How will you measure the success of this campaign? (e.g., Cost Per Click (CPC), Cost Per Acquisition (CPA), Return on Ad Spend (ROAS))
            Platform Preference: Are there any specific advertising platforms you are interested in using?
            I cannot generate a data-driven media plan without this information. Please provide these details so I can create a tailored strategy for you.
            Workflow:
            Initial Plan Proposal: Once I have the necessary information, I will propose an initial media plan. This plan will include a recommended budget allocation across different platforms, justified by specific performance metrics from the historical data.
            Iterative Refinement: You may provide feedback on the proposed plan. I will then iteratively update the strategy based on your preferences and new information you provide.
            Data-Driven Constraint: I will adhere strictly to the provided historical data. I will not introduce new advertising channels, creative formats, or performance metrics that are not present in the {DATA_SUMMARY_STRING}.
            Justification: Every plan update will be accompanied by a clear explanation of how the changes are supported by the historical data and your feedback.
            My expertise is strictly limited to media planning and ad placement on various platforms. I will not be able to answer questions outside of this domain.
            """
        }
        conversation_history.insert(0, system_prompt)

    # Get the AI's response
    ai_response = get_ai_response(conversation_history)
    conversation_history.append({"role": "assistant", "content": ai_response})

    return jsonify({
        'response': ai_response,
        'history': conversation_history
    })

if __name__ == '__main__':
    app.run(debug=True)