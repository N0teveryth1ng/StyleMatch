# Style Recommender

A beautiful web app that provides personalized fashion recommendations based on your style preferences.

## Features

- 🧥 Gender and occasion-based filtering
- 🎯 AI-powered product recommendations
- 💫 Beautiful, modern UI
- 📱 Mobile-responsive design
- 🔄 Real-time recommendations

## Deployment to Vercel

### Prerequisites

1. Install [Vercel CLI](https://vercel.com/docs/cli):
   ```bash
   npm i -g vercel
   ```

2. Make sure you have a Vercel account

### Deploy Steps

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy the app**:
   ```bash
   vercel
   ```

3. **Follow the prompts**:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `style-recommender` (or your preferred name)
   - Directory: `./` (current directory)
   - Override settings: `N`

4. **Your app will be deployed!** 🎉

### Alternative: Deploy via GitHub

1. Push your code to a GitHub repository
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Deploy automatically

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally**:
   ```bash
   python app.py
   ```

3. **Open** `http://localhost:5000`

## Project Structure

```
style-match-ai/
├── app.py              # Flask application
├── dashboard.py        # Original Streamlit app
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
├── templates/
│   └── index.html     # Web interface
└── src/
    ├── preprocess.py  # Data processing
    └── data_fetcher.py # Data fetching
```

## How it Works

1. **User Selection**: Choose gender and occasion
2. **Product Filtering**: Get relevant products based on preferences
3. **AI Recommendation**: Select a product you like
4. **Smart Matching**: Get 4 similar style recommendations using cosine similarity
5. **Stylish Descriptions**: Each recommendation comes with a stylist-style description

## Technologies Used

- **Backend**: Flask, Python
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Styling**: Custom CSS with gradients and animations

## API Endpoints

- `GET /` - Main application page
- `GET /api/products` - Get filtered products
- `POST /api/recommendations` - Get style recommendations

Enjoy your personalized style recommendations! ✨ 