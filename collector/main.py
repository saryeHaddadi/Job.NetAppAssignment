#!/usr/bin/python
# coding: utf-8

from app.web import webapp


if __name__ == '__main__':
    app = webapp.create_app()
    app.run(host="0.0.0.0", port=5000)
