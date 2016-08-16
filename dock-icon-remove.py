#!/usr/bin/env python
import sys, getopt
import subprocess
import urllib

def _restart_dock(user):
    command = "sudo -u "+user+" osascript -e 'delay 3' -e 'tell Application \"Dock\"' -e 'quit' -e 'end tell' -e 'delay 3'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()

def _remove_icon(user, positions):
    for position in positions:
        command = 'sudo -u '+user+' /usr/libexec/PlistBuddy -c "Delete persistent-apps:'+str(position)+'" /Users/'+user+'/Library/Preferences/com.apple.dock.plist'
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()


def _get_users():
    command = "dscacheutil -q user | grep -A 3 -B 2 -e uid:\\ 5'[0-9][0-9]' | grep name"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.strip()
    lines = out.split("\n")
    users = []
    for line in lines:
        users.append(line.replace("name: ", "").strip())
    print "Users:", users
    return users

def _get_doc_icon_positions(app_name, user):
    app_name = urllib.quote(app_name)
    app_name = app_name.replace("/", "\\/")
    print "Encoded App name:", app_name
    command = "sudo -u "+user+" defaults read com.apple.dock persistent-apps | grep _CFURLString\\\" | awk '/"+app_name+"/ {print NR}'"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.strip()
    lines = out.split("\n")
    positions = []
    try:
        for line in lines:
            pos = int(line) - 1
            positions.append(pos)
    except Exception as e:
        pass
    return positions

def main(argv):
    app_name = None
    app_ignore = []
    try:
        opts, args = getopt.getopt(argv,"hr:i:",["remove=","ignore="])
    except getopt.GetoptError:
        print 'dock-icon-remove.py -r <partial_name_to_remove> -i <partial_name_to_ignore>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'dock-icon-remove.py -r <partial_name_to_remove> -i <partial_name_to_ignore>'
            sys.exit()
        elif opt in ("-i", "--ignore"):
            app_ignore_raw = app_ignore.append(arg)
        elif opt in ("-r", "--remove"):
            app_name = arg

    if app_name is None:
        print "Missing remove flag"
        sys.exit(1)

    print "Removing", app_name, "icon from dock and ignoring:", app_ignore

    users = _get_users()
    for user in users:
        ignored_positions = set()
        doc_positions = _get_doc_icon_positions(app_name, user)
        for app in app_ignore:
            ignore_positions = _get_doc_icon_positions(app, user)
            for p in ignore_positions:
                ignored_positions.add(p)

        clean_positions = []
        for pos in doc_positions:
            if pos not in ignored_positions:
                clean_positions.append(pos - len(clean_positions))

        print "Ignored Positions:", ignored_positions
        if len(clean_positions) == 0:
            print "User", user, "does not have it in dock"
            continue

        print "User", user, "has it in dock"+str(clean_positions)
        _remove_icon(user, clean_positions)
        _restart_dock(user)

if __name__ == "__main__":
    main(sys.argv[1:])
