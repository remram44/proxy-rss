tweet-rss -- RSS feed generator from Twitter timelines

# Motivation

Twitter recently [retired its API version 1](https://dev.twitter.com/blog/api-v1-retirement-final-dates), which offered an unauthentified RSS endpoint for user timelines. This was useful to some, as it allowed to read these in your RSS client and to sort them efficiently. This app provides a similar functionality using the API version 1.1.

# Description

tweet-rss is a web application written in [Python](http://www.python.org/), using [Django](https://www.djangoproject.com/). It acts as a sort of proxy, reading timelines from Twitter using [its API](https://dev.twitter.com/) (in JSON format) through the very good [tweepy](https://github.com/tweepy/tweepy) and generating the requested RSS feed dynamically.

It currently works (and I use it daily) but the setup is non-trivial; a proper installation wizard should be implemented soon.
