#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import feedparser
from twython import Twython, TwythonError
from datetime import datetime
from dateutil import parser


class Settings:
    """Twitter bot application settings.

    Enter the RSS feed you want to tweet, or keywords you want to retweet.
    """
    # RSS feed to read and post tweets from EDITORIA AMAZONIA.
    feed_url = "COLOQUE AQUI A URL DO RSS" 

    # Log file to save all tweeted RSS links (one URL per line).
    posted_urls_output_file = "NOME-DO-ARQUIVO.log"

    # Log file to save all retweeted tweets (one tweetid per line).
    posted_retweets_output_file = "NOME-DO-ARQUIVO.log"

    # Include tweets with these words when retweeting.
    retweet_include_words = ["Retuitado por ....."]

    # Do not include tweets with these words when retweeting.
    retweet_exclude_words = []
    
    # Include tweets with these words when tweeting.
    


class TwitterAuth:

    consumer_key = "COLOQUE AQUI A CHAVE consumer_key" 
    consumer_secret = "COLOQUE AQUI A CHAVE consumer_secret"
    access_token = "COLOQUE AQUI A CHAVE access_token"
    access_token_secret = "COLOQUE AQUI A CHAVE access_token_secret"


def compose_message(item: feedparser.FeedParserDict) -> str:
    hashtag = "COLOQUE AQUI QUANTAS E QUAIS HASHTGS VOCÊ QUISER" 

    title, link, _ = item["title"], item["link"], item["description"]
    message = shorten_text(title, maxlength=500) + " " + hashtag + " " + link
    return message


def shorten_text(text: str, maxlength: int) -> str:

    return (text[:maxlength] + '...') if len(text) > maxlength else text


def post_tweet(message: str):

    try:
        twitter = Twython(TwitterAuth.consumer_key,
                          TwitterAuth.consumer_secret,
                          TwitterAuth.access_token,
                          TwitterAuth.access_token_secret)
        twitter.update_status(status=message)
    except TwythonError as e:
        print(e)


def read_rss_and_tweet(url: str):

    feed = feedparser.parse(url)
    if feed:
        for item in feed["items"]:
            link = item["link"]
            publication_date = item["published"]
            publication_date = parser.parse(publication_date)
            publication_date_str = publication_date.strftime("Data: %d/%m/%Y Hora: %H:%M:%S")
            if is_in_logfile(link, publication_date_str, Settings.posted_urls_output_file):
                print("Já Postado:", link, publication_date_str)
            else:
                post_tweet(message=compose_message(item))
                write_to_logfile(link, publication_date_str, Settings.posted_urls_output_file)
                print("Postado:", link, publication_date_str)
    else:
        print("Nada foi encontrado no feed", url)


def get_query() -> str:

    include = " OR ".join(Settings.retweet_include_words)
    exclude = " -".join(Settings.retweet_exclude_words)
    exclude = "-" + exclude if exclude else ""
    return include + " " + exclude


def search_and_retweet(query: str, count=10):

    try:
        twitter = Twython(TwitterAuth.consumer_key,
                          TwitterAuth.consumer_secret,
                          TwitterAuth.access_token,
                          TwitterAuth.access_token_secret)
        search_results = twitter.search(q=query, count=count)
    except TwythonError as e:
        print(e)
        return
    for tweet in search_results["statuses"]:
        # Make sure we don't retweet any dubplicates.
        if not is_in_logfile(
                    tweet["id_str"], Settings.posted_retweets_output_file):
            try:
                twitter.retweet(id=tweet["id_str"])
                write_to_logfile(
                    tweet["id_str"], Settings.posted_retweets_output_file)
                print("Retweeted {} (id {})".format(shorten_text(
                    tweet["text"], maxlength=40), tweet["id_str"]))
            except TwythonError as e:
                print(e)
        else:
            print("Already retweeted {} (id {})".format(
                shorten_text(tweet["text"], maxlength=40), tweet["id_str"]))


def is_in_logfile(content: str, publication_date_str: str, filename: str) -> bool:

    if os.path.isfile(filename):
        with open(filename) as f:
            lines = f.readlines()
        if (content + " - " + publication_date_str + "\n" or content + " - " + publication_date_str) in lines:
            return True
    return False


def write_to_logfile(content: str, publication_date_str: str, filename: str):

    try:
        with open(filename, "a") as f:
            f.write(content + " - " + publication_date_str + "\n")
    except IOError as e:
        print(e)



def display_help():
    print("Syntax: python {} [command]".format(sys.argv[0]))
    print()
    print(" Commands:")
    print("    rss    Read URL and post new items to Twitter")
    print("    rt     Search and retweet keywords")
    print("    help   Show this help screen")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "rss":
            read_rss_and_tweet(url=Settings.feed_url)
        elif sys.argv[1].lower() == "rt":
            search_and_retweet(query=get_query())
        else:
            display_help()
    else:
        display_help()
