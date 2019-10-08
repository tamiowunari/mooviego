from flask import Flask, render_template, request
import urllib.request as url
import json
# https://api.nytimes.com/svc/movies/v2/reviews/search.json?query=lion+king&api-key=Dst0c9ltQ4bT2QkEIL1swRmGTLZIYXGQ
app = Flask(__name__)


@app.route('/result', methods=['POST'])
def movie_search():
    api_key = '&api-key=Dst0c9ltQ4bT2QkEIL1swRmGTLZIYXGQ'
    api_endpoint = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?query='

    query = request.form['user-movie']
    movie = query.replace(' ', '%20')
    movie_url = api_endpoint + movie + api_key
    movie_data = url.urlopen(movie_url)
    movie_json_data = json.load(movie_data)

    if(movie_json_data['status']=='OK' and bool(movie_json_data['results'])==True):
        movie_title = movie_json_data['results'][0]['display_title']
        movie_subtitle = movie_json_data['results'][0]['headline']
        movie_summary = movie_json_data['results'][0]['summary_short']
        movie_opening_date = movie_json_data['results'][0]['opening_date']
        movie_ratedPG = movie_json_data['results'][0]['mpaa_rating']
        movie_reviewlink = movie_json_data['results'][0]['link']['url']
        movie_imageSrc = movie_json_data['results'][0]['multimedia']['src']
        return render_template('index.html', movie_title=movie_title, movie_subtitle=movie_subtitle, movie_summary=movie_summary, movie_opening_date='Release date: '+ movie_opening_date, movie_imageSrc=movie_imageSrc, movie_reviewlink=movie_reviewlink, movie_ratedPG='Rated '+ movie_ratedPG, article_link='View news article')

    elif(movie_json_data['status']=='OK' and bool(movie_json_data['results'])==False):
        return render_template('error.html', error='Sorry, could not find movie!')
    else:
        return render_template('error.html', error='404 Page not found!')




@app.route('/')
def get_search_input():
    return render_template('index.html')









if __name__ == '__main__':
    app.run(debug=True)