# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
from werkzeug.routing import BaseConverter
import config
import time, json, os


class RegexConverter(BaseConverter):
    # flask URL regex converter
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def get_meeting_type(extension):
    if extension == "html":
        return "minutes"
    elif extension == "log.html":
        return "logs"
    else:
        # if plain-text file
        return "plain-text"

def get_json_cache(meeting_type):
    try:
        with open(config.json_cache_location, mode='r') as json_store:
            cache = json.load(json_store)

            unix_time_expiration = cache["expiry"]
            if time.time() > unix_time_expiration:
                raise RuntimeError("Cache expired, regenerate.")
            if meeting_type == "channel":
                return cache["channel"]
            elif meeting_type == "team":
                return cache["team"]
            else:
                raise Exception("Meeting type not found.")
    except IOError:
        raise RuntimeError("Cache not found.")

def check_folder_exist(file_path):
    split_file_path = os.path.split(file_path)
    directory = split_file_path[0]
    if not os.path.exists(directory):
        os.makedirs(directory)

def set_json_cache(channel, team, expiry_time):
    file_write = dict()
    file_write["team"] = team
    file_write["channel"] = channel
    current_unix_time = time.time()
    unix_time_expiration = expiry_time + current_unix_time
    file_write["expiry"] = unix_time_expiration
    try:
        check_folder_exist(config.json_cache_location)
        with open(config.json_cache_location, mode='w') as json_store:
            json.dump(file_write, json_store)
    except Exception as inst:
        print inst
    return True
