# Copyright 2011 Thomas Quemard
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.

import os.path
import time
import xl.event

import plugin
import loggerprefs

LOGGER_PLUGIN = None


def enable(exaile):
    if (exaile.loading):
        xl.event.add_callback(_enable, 'exaile_loaded')
    else:
        _enable(None, exaile, None)

def disable(exaile):
    global LOGGER_PLUGIN
    LOGGER_PLUGIN.disable()

def get_preferences_pane():
    return loggerprefs

def _enable(eventname, exaile, nothing):
    global LOGGER_PLUGIN
    store_path = "/home/thomas/exaile_log.sqlite"
    LOGGER_PLUGIN = plugin.Plugin(store_path)

    if LOGGER_PLUGIN.panic:
        plugin.LOG.error("Panic mode. Disabling.")
        disable(exaile)
    else:
        xl.event.add_callback(on_track_start, "playback_track_start")
        xl.event.add_callback(on_track_end, "playback_track_end")
        xl.event.add_callback(on_track_pause, "playback_player_pause")
        xl.event.add_callback(on_track_resume, "playback_player_resume")

def on_track_start (event_name, exaile, data):
    print "TRACK_START"
    global LOGGER_PLUGIN
    LOGGER_PLUGIN.song.started_playing_at = time.time()
    LOGGER_PLUGIN.song.played_for = 0

def on_track_pause (event_name, exaile, data):
    global LOGGER_PLUGIN
    LOGGER_PLUGIN.song.played_for += \
        time.time() - LOGGER_PLUGIN.song.started_playing_at
    LOGGER_PLUGIN.song.started_playing_at = None
    print "TRACK_PAUSE"

def on_track_resume (event_name, exaile, data):
    global LOGGER_PLUGIN
    LOGGER_PLUGIN.song.started_playing_at = time.time()
    print "TRACK_RESUME"

def on_track_end(event_name, exaile, song):
    print "TRACK_END"
    global LOGGER_PLUGIN
    if LOGGER_PLUGIN.song.started_playing_at:
        LOGGER_PLUGIN.song.played_for = \
            time.time() - LOGGER_PLUGIN.song.started_playing_at
        LOGGER_PLUGIN.song.started_playing_at = None

        LOGGER_PLUGIN.store.insert_log( \
            song.local_file_name(), \
            song.get_tag_display("artist"), \
            song.get_tag_display("album"), \
            song.get_tag_display("title"), \
            round(song.get_tag_raw("__length"), 2), \
            round(LOGGER_PLUGIN.song.played_for, 2) \
        )
