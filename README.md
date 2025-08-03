# MediaPlan AI Strategist
Welcome to **MediaPlan**, your expert AI media strategist!  
My purpose is to help you create simple media plans for your advertising campaigns. I leverage historical campaign performance data to provide recommendations on budget allocation and platform selection, ensuring your campaigns are optimized for success.

---

## How to Use
To get started with MediaPlan, provide the following key information:
- **Campaign Objectives**: What are you aiming to achieve?  
  _Examples: brand awareness, lead generation, sales_
- **Total Budget**: How much are you willing to spend on this campaign?
- **Key Performance Indicator (KPI)**: How will you measure success?  
  _Examples: Cost Per Click (CPC), Cost Per Acquisition (CPA), Return on Ad Spend (ROAS)_
- **Platform Preference**: Do you have specific platforms in mind for your ads?
Once you submit these details, MediaPlan will generate a tailored media plan. You can then provide feedback, and the plan will be refined accordingly.

---

## Features
- **Smart Budget Allocation**  
  Get suggestions on how to distribute your budget across different platforms.
- **KPI-Focused Planning**  
  Media plans are tailored to meet your specific success metrics.
- **Iterative Refinement**  
  Provide feedback and receive updated plans with clear reasoning for each adjustment.
- **Platform-Specific Insights**  
  Understand where your ads perform best based on historical trends.

---
## How to Run This Project
This project uses **Flask** for the backend API and **React.js** for the frontend.

### 1. install all dependencies
```bash
pip install flask flask-cors pandas openai
```
### 2. insert your API key in backend.py line 12

### 3. Start the Flask Backend
Make sure you have Python installed and the required packages. Install dependencies:
```bash
pip install flask flask-cors pandas openai
python backend.py
```

### 4. Start the React Frontend
Navigate to the frontend directory and start the React app:
```bash
cd media-agent
npm install
npm start
```


