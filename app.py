from flask import Flask, render_template, send_file
import json
from news_fetcher import fetch_news_by_categories, automate_news_fetch

app = Flask(__name__)
automate_news_fetch(interval=3600, output_file="news_data.json")

@app.route('/')
def home():
    try:
        with open("news_data.json", "r", encoding="utf-8") as f:
            news_by_category = json.load(f)
    except Exception:
        news_by_category = fetch_news_by_categories()
    return render_template('index.html', news_by_category=news_by_category)

@app.route('/post/<int:post_id>')
def post(post_id):
    return render_template('post.html', post_id=post_id)

@app.route('/sitemap.xml')
def sitemap():
    urls = [
        {
            'loc': 'http://localhost:5000/',
            'changefreq': 'hourly',
            'priority': '1.0'
        },
        {
            'loc': 'http://localhost:5000/post/1',
            'changefreq': 'monthly',
            'priority': '0.5'
        }
    ]
    try:
        with open('news_data.json', 'r', encoding='utf-8') as f:
            news_by_category = json.load(f)
        post_id = 2
        for category, articles in news_by_category.items():
            for article in articles:
                urls.append({
                    'loc': f'http://localhost:5000/post/{post_id}',
                    'changefreq': 'daily',
                    'priority': '0.7'
                })
                post_id += 1
    except Exception:
        pass
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap_xml += f"    <url>\n        <loc>{url['loc']}</loc>\n        <changefreq>{url['changefreq']}</changefreq>\n        <priority>{url['priority']}</priority>\n    </url>\n"
    sitemap_xml += '</urlset>'
    return sitemap_xml, 200, {'Content-Type': 'application/xml'}

if __name__ == '__main__':
    app.run(debug=True)
