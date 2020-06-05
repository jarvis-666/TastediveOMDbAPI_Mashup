import requests
import json

def requestURL(baseurl, params = {}):
    # This function accepts a URL path and a params diction as inputs.
    # It calls requests.get() with those inputs,
    # and returns the full URL of the data you want to get.
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url


def get_movies_from_tastedive(movie_name):
    baseurl = "https://tastedive.com/api/similar"
    params_dict = {'q': movie_name, 'type': 'movies', 'limit': '5'}
    res = requests.get(baseurl, params_dict)
    # print(res.url)
    return res.text


def extract_movie_titles(movies_dict):
    list_of_names = []
    list_of_movies = movies_dict["Similar"]["Results"]
    for movies in list_of_movies:
        name = movies["Name"]
        list_of_names.append(name)
    return list_of_names


def get_related_titles(list_of_movies):
    list_of_related_movies = []
    for movie in list_of_movies:
        list_of_related_movies.append(extract_movie_titles(json.loads(get_movies_from_tastedive(movie))))
    flatten_list_of_movies = []
    for sublist in list_of_related_movies:
        for movie in sublist:
            if movie not in flatten_list_of_movies:
                flatten_list_of_movies.append(movie)
    return flatten_list_of_movies


def get_movie_data(movie_name):
    baseurl = "http://www.omdbapi.com/"
    params_dict = {'t': movie_name, 'r': 'json', 'apikey': 'hahahahaha'}
    res = requests.get(baseurl, params_dict)
    data = json.loads(res.text)
    return data


def get_movie_rating(movie_details):
    # print(movie_details)
    list_of_ratings = movie_details["Ratings"]
    score = 0
    for rating in list_of_ratings:
        if rating['Source'] == 'Rotten Tomatoes':
            score = rating['Value']
            score = int(score[:-1])
    return score


def get_sorted_recommendations(list_of_movie_titles):
    # print(list_of_movie_titles)
    related_movies_list = get_related_titles(list_of_movie_titles)
    # print(related_movies_list)
    rating_of_related_movies = dict()
    for movie in related_movies_list:
        rating_of_related_movies[movie] = get_movie_rating(get_movie_data(movie))
    # print(rating_of_related_movies)
    list_of_recommended_movies = []
    for movie, rating in rating_of_related_movies.items():
        list_of_recommended_movies.append((movie, rating))
    # print(list_of_recommended_movies)
    recommended_movies = sorted(list_of_recommended_movies, key=lambda x: (x[1], x[0]), reverse=True)
    result = [movie[0] for movie in recommended_movies]
    return result

if __name__ != '__main__':
    req = requests.get("https://www.google.com/search?tbm=isch&q=%22violins+and+guitars%22")
    print(req.text[:200])
    print(req.url)
    print(req.status_code)
    print(req.headers)
    params_dict = {'tbm': 'isch', 'q': '"violins and guitars"'}
    print(requestURL("https://www.google.com/search", params_dict))

if __name__ == '__main__':
    # dict_of_movies = get_movies_from_tastedive("Black Panther")
    # print(dict_of_movies)
    # dict_of_movies = json.loads(dict_of_movies)
    # print(type(dict_of_movies))
    # list_of_names = extract_movie_titles(dict_of_movies)
    # print(list_of_names)
    # list_of_related_movies = get_related_titles(list_of_names)
    #print(list_of_related_movies)
    recommendations = get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
    print(recommendations)