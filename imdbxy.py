#!/bin/env python
# -*- coding: utf-8 -*-
import imdbpie
import sqlite3

def init():
    with sqlite3.connect('imdb.db') as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE movie(
            movie_id STRING NOT NULL,
            rating INT,
            year INT,
            title STRING,
            votes INT,
            plot STRING,
            release_date INT,
            runtime INT,
            plot_outline STRING,
            PRIMARY KEY (movie_id) )''')
        cur.execute('''CREATE TABLE genre(
            movie_id STRING NOT NULL,
            genre STRING,
            PRIMARY KEY (movie_id, genre))''')
        cur.execute('''CREATE TABLE actor(
            actor_id INT NOT NULL,
            name STRING,
            PRIMARY KEY (actor_id))''')
        cur.execute('''CREATE TABLE movie_actor(
            movie_id INT NOT NULL,
            actor_id STRING,
            PRIMARY KEY (movie_id, actor_id))''')


def main():
    imdb = imdbpie.Imdb()
    with sqlite3.connect('imdb.db') as con:
        cur = con.cursor()
        for title in imdb.top_250()[0:5]:
            title = imdb.get_title_by_id(title['tconst'])
            print(title.title)
            cur.execute('''insert into movie
                        (movie_id, rating, year, title, votes, plot,
                        release_date, runtime, plot_outline) values
                        (?,?,?,?,?,?,?,?,?) ''',
                        (title.imdb_id, title.rating, title.year, title.title,
                        title.votes, title.plots[0], title.release_date,
                        title.runtime, title.plot_outline))
            for genre in title.genres:
                cur.execute('''insert into genre
                            (movie_id, genre) values (?,?) ''',
                            (title.imdb_id, genre))
            for person in title.cast_summary:
                cur.execute('''select name from actor where actor_id = ?''',
                            (person.imdb_id,))
                if not cur.fetchone():
                    cur.execute('''insert into actor (actor_id, name)
                                values (?,?)''', (person.imdb_id, person.name))
                cur.execute('''insert into movie_actor (movie_id, actor_id)
                            values (?,?)''',
                            (title.imdb_id, person.imdb_id))




if __name__ == '__main__':
    init()
    main()
