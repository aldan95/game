# ~~PyGame Breakout~~ PyGame sample game

(cloned from https://gitlab.com/the-gigi/pygame-breakout and mutated)

This is a simple implementation with Python 3 and PyGame of the classic [Breakout](https://en.wikipedia.org/wiki/Breakout_(video_game)) game. The purpose is to serve as a demo game for a
series of articles on building games with Python 3 and PyGame:

- [Building Games With Python 3 and Pygame: Part 1](https://code.tutsplus.com/tutorials/building-games-with-python-3-and-pygame-part-1--cms-30081)
- [Building Games With Python 3 and Pygame: Part 2](https://code.tutsplus.com/tutorials/building-games-with-python-3-and-pygame-part-2--cms-30082)
- [Building Games With Python 3 and Pygame: Part 3](https://code.tutsplus.com/tutorials/building-games-with-python-3-and-pygame-part-3--cms-30083)
- [Building Games With Python 3 and Pygame: Part 4](https://code.tutsplus.com/tutorials/building-games-with-python-3-and-pygame-part-4--cms-30084)
- [Building Games With Python 3 and Pygame: Part 5](https://code.tutsplus.com/tutorials/building-games-with-python-3-and-pygame-part-5--cms-30085)

# Features

- Simple generic GameObject and TextObject
- Simple generic Game object
- Simple generic button
- Config file
- Handling keyboard and mouse events
- Bricks, paddle and ball
- Managing paddle movement
- Handling collisions of the ball with everything
- Background image
- Sound effects
- Extensible special effects system

# Installation and usage

The prerequisites are:
- [Python 3.8](https://docs.python.org/3.8/) 
- [Pipenv](https://pipenv.readthedocs.io/en/latest/) 

Then clone the [repository](https://gitlab.com/the-gigi/pygame-breakout) and type:

```
pipenv install
```

You should see something like:

```
$ pipenv install
Creating a virtualenv for this project…
Pipfile: /Users/gigi.sayfan/git/pygame-breakout/Pipfile
Using /Users/gigi.sayfan/.pyenv/versions/3.8.0/bin/python3 (3.8.0) to create virtualenv…
⠙ Creating virtual environment...Using base prefix '/Users/gigi.sayfan/.pyenv/versions/3.8.0'
New python executable in /Users/gigi.sayfan/.local/share/virtualenvs/pygame-breakout-mgkKDQCD/bin/python3
Also creating executable in /Users/gigi.sayfan/.local/share/virtualenvs/pygame-breakout-mgkKDQCD/bin/python
Installing setuptools, pip, wheel...
done.
Running virtualenv with interpreter /Users/gigi.sayfan/.pyenv/versions/3.8.0/bin/python3

✔ Successfully created virtual environment!
Virtualenv location: /Users/gigi.sayfan/.local/share/virtualenvs/pygame-breakout-mgkKDQCD
Installing dependencies from Pipfile.lock (b269cc)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 1/1 — 00:00:08
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

To run the game type:

```
pipenv run python breakout.py
```

# Credits

I used some color constants I found in this nice article: https://www.webucator.com/blog/2015/03/python-color-constants-module/
