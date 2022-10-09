from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/get_trends")
async def get_trends():
    trends_df = pd.read_csv('data/trends.csv')
    return {'trends': trends_df.iloc[:, 1].tolist()}


@app.get("/get_digest")
async def get_digest(role: str = 'businessman'):
    filename = 'data/best_news_business.csv'
    if role == 'bookkeeper':
        filename = 'data/best_news_buh.csv'

    news_df = pd.read_csv(filename)

    return {'digest': news_df.iloc[:3].to_dict('records')}

