**Logger** is an [Exaile](http://www.exaile.org/) plugin meant to log what you
listen. It's an open-source (GPLv3) alternative to your last.fm history, for
example.

# Logger

## Why ?

If you're like me, you connected exaile to your last.fm account so you can keep
an history of what you're listening and get some stats. Obviously you can't do
your own stats. Actually you can, since last.fm lets you export your data, but
it's a pain in the ass, it takes time and it's not real time.

What you want to do is keep your listening history local, and it's exactly what
**Logger** does.


## How ?

**Logger** keeps track of every song you play. Even if you're offline. It logs
everything to an SQLite database so you can do whatever you want with your
history. Like plotting with R, or reporting with Python, or whatever.


# Installation

Run `make ezx` and open Exaile. Go to *Edit* > *Preferences* > *Plugins* and
click *Install plugin*. Select file */path/to/logger/build/logger.exz*. You're
done !
