# Gmail Automation Suite

A comprehensive web-based tool for creating and sending personalized Gmail drafts at scale. Use AI to generate personalized emails and automate your outreach campaigns with controlled timing and scheduling.

## Features

- **AI-Powered Email Creation**: Generate personalized emails using Perplexity AI
- **CSV Contact Import**: Upload contact lists with emails, names, and company information
- **Automated Draft Creation**: Bulk create personalized drafts in your Gmail account
- **Scheduled Sending**: Configure timing between emails and business hours for sending
- **Web Interface**: Clean, modern UI accessible from any device
- **Progress Tracking**: Monitor email creation and sending status in real-time

## Deployment Instructions

### GitHub to Railway Deployment (Recommended)

1. **Fork this Repository**:
   - Click the "Fork" button at the top right of this GitHub repository

2. **Deploy to Railway**:
   - Create a Railway account at [railway.app](https://railway.app/)
   - Go to your Railway dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
   - Railway will automatically detect the Python project and install dependencies

3. **Configure Environment Variables**:
   - In your Railway project, go to "Variables"
   - Add the following variables:
     - `SECRET_KEY` = [generate a secure random string]
     - `FLASK_ENV` = production
     - `PERPLEXITY_API_KEY` = [your Perplexity API key, if using AI features]

4. **Deploy the Project**:
   - Railway will automatically deploy when you push changes to your GitHub repository
   - The first deployment should happen automatically after connecting

### Local Development Setup

1. **Clone the Repository**:
   ```
   git clone https://github.com/your-username/gmail-automation-suite.git
   cd gmail-automation-suite
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Create a `.env` file in the project root:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-dev-secret-key
   ```

5. **Run the Application**:
   ```
   flask run
   ```

6. **Access the Application**:
   Open your browser and go to `http://localhost:5000`

## Project Structure

The project has a simplified structure optimized for cloud deployment:

```
gmail-automation-suite/
├── app.py                # Main Flask application
├── requirements.txt      # Project dependencies
├── Procfile              # For Railway deployment
├── static/               # Static assets (CSS, JS)
└── templates/            # HTML templates
```

## Troubleshooting Deployment

If you encounter issues deploying to Railway:

1. **Check Logs**:
   - In Railway, go to your project and click "Deployments"
   - Select the latest deployment and check the logs
   - Look for any error messages that might indicate the problem

2. **Common Issues**:
   - **Port configuration**: This is handled in the app.py file
   - **Missing requirements**: Check if all dependencies are in requirements.txt
   - **Environment variables**: Ensure all required env vars are set

3. **Manual Deployment Steps**:
   - If GitHub integration isn't working, you can use Railway CLI:
   ```
   npm i -g @railway/cli
   railway login
   railway link    # Link to your Railway project
   railway up      # Deploy your project
   ```

## Usage

### Creating Email Drafts

1. Go to the "Create Drafts" section
2. Upload your CSV file with contact information
3. Configure column mappings (email, first name, company)
4. Set up email template or enable AI generation
5. Configure AI settings if using Perplexity
6. Start automation to create drafts in your Gmail account

### Sending Email Drafts

1. Go to the "Send Drafts" section
2. Configure timing settings (delay between emails)
3. Set up schedule (optional) to only send during specific hours
4. Start automation to send drafts according to your schedule

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed for legitimate email campaigns. Please use responsibly and in compliance with email service provider policies and anti-spam regulations.
