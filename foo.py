import os
import os.path as path
import xml.etree.ElementTree as ET

STRINGS_FILENAME = "strings.xml"
ANDROID_RES_DIR = "foobar/values"
FOO_PATH = ANDROID_RES_DIR + "/" + STRINGS_FILENAME

LANGS_ANUI_DIR = "foobar/langs_anui"

def log(type, error):
    print "[%s] %s" % (type, error)


def sanity_check_android(path):
    if not os.path.exists(path):
        log("F", "Path '%s' does not exist" % path)
        return False

    for file in os.listdir(path):
        if(file == STRINGS_FILENAME):
            return True

    log("F", STRINGS_FILENAME + " not found in '%s'" % path)
    return False


def sanity_check_langs(path):
    if not os.path.exists(path):
        log("F", "Path '%s' does not exist" % path)
        return False

    files = os.listdir(path)
    if not files:
        log("F", "No .lang files?")
        return False

    return True


def check_lang(android_child, lang_child):
    if not "id" in lang_child.attrib:
        log("LE", "Lang [%s] missing 'id' attribute" % lang_child)
        return False

    if not "text" in lang_child.attrib:
        log("LE", "Lang [%s] missing 'text' attribute" % lang_child)
        return False

    if not lang_child.attrib["text"]:
        log("LE", "Lang's text is empty")
        return False

def check_lang_file(android_tree, lang_tree):
    # Sanitize langs in this file
    lang_root = lang_tree.getroot()
    for lang_child in lang_root.findall("*"):
        if not "id" in lang_child.attrib:
            log("LE", "Lang [%s] missing 'id' attribute" % lang_child)
            lang_root.remove(lang_child)
            continue

        if not "text" in lang_child.attrib:
            log("LE", "Lang [%s] missing 'text' attribute" % lang_child)
            lang_root.remove(lang_child)
            continue

        if not lang_child.attrib["text"]:
            log("LE", "Lang's text is empty")
            lang_root.remove(lang_child)
            continue

    # Check for matches
    for android_child in android_tree.getroot():
        found = False
        for lang_child in lang_tree.getroot():
            if android_child.text == lang_child.attrib["id"]:
                found = True
                break

        if not found:
            log("LE", "String with id '%s' not found" % android_child.attrib["name"])

########


# BEGIN
#######
if not sanity_check_android(ANDROID_RES_DIR):
    print "Quitting..."
    quit()

if not sanity_check_langs(LANGS_ANUI_DIR):
    print "Quitting..."
    quit()

print "///// Sanity check\n[OK]\n"

# try:
lang_filesnames = os.listdir(LANGS_ANUI_DIR)

# Parse android strings contents
try:
    android_tree = ET.parse(path.join(ANDROID_RES_DIR, STRINGS_FILENAME))
except ET.ParseError:
    log("F", "%s is not a valid xml document!!!" % STRINGS_FILENAME)
    print "Quitting..."
    quit()

# print "BEFORE"
# for android_child in android_tree.getroot():
#         print android_child.tag

# Clean BS android xml elements
root = android_tree.getroot()
for android_child in root.findall("*"): # toto mi da kopiu na ktorej mozem mazat ale da mi to len stringy tak treba aby to alo secko nejako
    if android_child.tag != "string":
        log("AW", "Ignoring tag <%s>" % android_child.tag)
        root.remove(android_child)
        continue

    if not android_child.text:
        log("AE", "string with id '%s' has empty body" % android_child.attrib["name"])
        root.remove(android_child)
        continue

print

# Every .lang file
for lang_filename in lang_filesnames:
    print "///// Checking " + lang_filename
    if not lang_filename.endswith(".lang"):
        log("?", "'%s' is not a lang file. Skipping..." % lang_filename)
        continue

    # Parse lang file contents
    try:
        lang_tree = ET.parse(path.join(LANGS_ANUI_DIR, lang_filename))
    except  ET.ParseError:
        log("F", "%s is not a valid xml document!!!\n" % lang_filename)
        continue

    # Check na na na
    check_lang_file(android_tree, lang_tree)
    print
    # print "[OK]\n"

# END


