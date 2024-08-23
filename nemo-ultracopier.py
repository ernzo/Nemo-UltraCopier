#! /usr/bin/python
#  -*- coding: utf-8 -*-

# Nemo action: Nemo-UltraCopy
# Release Date: 09 May 2014
#
# Authors: Lester Carballo Pérez(https://github.com/lestcape).
#
#          Email: lestcape@gmail.com     Website: https://github.com/lestcape/Nemo-UltraCopy
#
# "This is an action for the Nemo browser, to paste files using ultracopier
# instead of the default nemo copier tool."
#
# This program is free software:
#
#    You can redistribute it and/or modify it under the terms of the
#    GNU General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------
#
# ernzo:
# "This modification fixes the integration between Nemo and Ultracopier, and uses CopyQ to make the actual copy.
#
# Caveat is: Sometimes initally you'll need to perform the Copy/Paste operation twice because,
# the first time you run the script CopyQ will not be running (unless you launch it manually), and so it won't be able to capture the clipboard contents..
#
# The second time you perform Copy/"Paste with Ultracopier" copyq will be running, and the script will work as intended.
#
# It works allright here with:
# Debian (trixie) + KDE Plasma/Wayland + latest stock Nemo + Ultracopier + CopyQ.
# (Gnome and Mate are installed too but not running)
#
#
# -Btw this script was made by torturing ChatGPT for hours until it made it right, or almost.. 
# The first version did perform the copy/paste allright, but failed to launch CopyQ on its own, so it needed to be launched manually.
#
# Then I asked Copilot to fix the script, 
# and it made one that could launch copyq automatically on its own.. but failed to perform the actual copy/paste.
#
# So I went back to ChatGPT and asked to integrate one thing into the other..
# And well, this is the final result!
#
# All credits to the Original Developer/s, Lester,
# and ChatGPT + Copilot who did the rough work..
#
# This is probably not a definitive solution, 
# but maybe there's something we can learn about it, and can be implemented in a more definitive one."
#
# ----------------------------------------------------------------------------
#
#
#! /usr/bin/python3
import subprocess
import sys
import urllib.parse
import os

def start_copyq():
    # Check if CopyQ server is already running
    result = subprocess.run(['pgrep', 'copyq'], capture_output=True, text=True)
    if result.returncode == 0:
        print("CopyQ is already running.")
    else:
        # Start CopyQ server
        os.system("copyq &")
        print("CopyQ started.")

def get_clipboard_data():
    try:
        # Fetch clipboard data using CopyQ
        result = subprocess.run(['copyq', 'read', '0'], capture_output=True, text=True)
        if result.returncode == 0:
            data = result.stdout.strip()
            print(f"Clipboard Data Retrieved: {data}")
            return data
        else:
            print(f"Error running CopyQ command: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: nemo-ultracopier.py <destination_directory>")
        sys.exit(1)

    # Start CopyQ if not running
    start_copyq()

    clipboard_data = get_clipboard_data()
    if clipboard_data:
        print(f"Clipboard text: {clipboard_data}")

        # Assuming clipboard_data might contain file URIs for copying
        destination = urllib.parse.unquote(sys.argv[1])

        # Format sources and destination
        sources = clipboard_data.split('\n')  # Assuming each line is a source file
        sources_formatted = ' '.join(f'"{source}"' for source in sources)

        # Construct UltraCopier command
        command = f"/usr/bin/ultracopier cp {sources_formatted} \"{destination}\""
        print(f"Executing command: {command}")

        # Execute the command
        os.system(command)
    else:
        print("No valid clipboard data found.")

if __name__ == "__main__":
    main()
