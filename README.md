RSS feed proxy for Twitter & Spotify

# Motivation

Fewer and fewer services offer RSS feeds. However many have their own HTTP API. This project allows you to speak those APIs to make an RSS feed you can use in your reader.

This project retrieves information from APIs and renders them as RSS, so you can add them to your feed reader. It knows how to talk to specific APIs (the ones that I care about enough to implement).

# Description

proxy-rss is a web application written in [Python](http://www.python.org/), using [Flask](http://flask.pocoo.org/). It acts as a sort of proxy, reading information from specific APIs and rendering them as RSS dynamically.
