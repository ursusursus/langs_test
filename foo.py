import os
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

    if android_child.text == lang_child.attrib["text"]:
        return False

def check_lang_file(android_tree, lang_tree):
    for android_child in android_tree.getroot():
        if android_child.tag != "string":
            log("AW", "Skipping tag <%s>" % android_child.tag)
            continue

        if not android_child.text:
            log("AE", "<string> with id '%s' has empty body" % android_child.attrib["name"])
            continue

        # ESTE check whitelist

        for lang_child in lang_tree.getroot():
            if check_lang(android_child, lang_child):
                return True

            # POZOR toto neni ten ocisteny list
    return False


# BEGIN
if not sanity_check_android(ANDROID_RES_DIR):
    print "Quitting..."
    quit()

if not sanity_check_langs(LANGS_ANUI_DIR):
    print "Quitting..."
    quit()

print "///// Sanity check: OK\n"

# try:
lang_files = os.listdir(LANGS_ANUI_DIR)

# Parse android strings contents
# BLBY PATH!
android_tree = ET.parse(STRINGS_FILENAME)


# Every .lang file
for lang_file in lang_files:
    print "///// Checking " + lang_file
    if not lang_file.endswith(".lang"):
        log("?", "'%s' is not a lang file. Skipping..." % lang_file)
        continue

    # Parse lang file contents
    try:
        lang_tree = ET.parse(LANGS_ANUI_DIR + "/" + lang_file)
    except  ET.ParseError:
        log("F", "%s not a valid xml document!!!\n" % lang_file)
        continue

    if check_lang_file(android_tree, lang_tree):
        print "[OK]\n"

# END


