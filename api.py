import requests as r
import datetime
import tweepy
import creds
import chess
import chess.pgn
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os


def get_most_recent_game(most_recent_game):
    white_player = most_recent_game["white"]
    white_username = white_player["username"]
    white_rating = white_player["rating"]
    black_player = most_recent_game["black"]
    black_username = black_player["username"]
    black_rating = black_player["rating"]
    vs_text = f"♜{white_username}({white_rating}) vs ♖{black_username}({black_rating})"
    pgn_file = open("pgn_file.pgn", "r")
    pgn_termination1 = pgn_file.readlines()
    pgn_termination = pgn_termination1[16]
    # pgn line 16
    win_text = pgn_termination.replace('"', "").replace('[', "").replace(']', "").replace("Termination", "")
    vs_text = vs_text + f"\n{win_text}\n{most_recent_game['url']}"
    return vs_text


def tweet_game(text, image):
    consumer_key = creds.consumer_key
    consumer_secret = creds.consumer_secret
    access_token = creds.access_token
    access_token_secret = creds.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    api.update_with_media(image, text)


def generate_board():
    pgn = open("pgn_file.pgn")
    first_game = chess.pgn.read_game(pgn)
    board = first_game.board()
    for move in first_game.mainline_moves():
        board.push(move)
    os.remove("svg.svg")
    svg_file = open("svg.svg", "w")
    svg_file.write(chess.svg.board(board))
    svg_file.close()
    drawing = svg2rlg("svg.svg")
    renderPM.drawToFile(drawing, "png.jpg", fmt="jpg")
    # print(chess.svg.board(board))


def check_if_recent_game():
    d = datetime.date.today()
    month = f"{d.month:02d}"
    year = d.year
    all_games = r.get(f"http://api.chess.com/pub/player/xx_chess_x_queen_xx/games/{year}/{month}")
    most_recent_game = all_games.json()["games"][-1]
    game_url = most_recent_game["url"]
    f = open("most_recent.txt", "r")
    tweet = get_most_recent_game(most_recent_game)
    previous_game = f.read()
    f.close()
    # os.remove("png.jpg")
    # os.remove("svg.svg")
    if not previous_game == game_url:
        f = open("most_recent.txt", "w")
        f.write(game_url)
        f.close()
        pgn_file = open("pgn_file.pgn", "w")
        pgn_file.write(most_recent_game["pgn"])
        pgn_file.close()
        generate_board()
        tweet_game(tweet, "png.png")
        f.close()

check_if_recent_game()