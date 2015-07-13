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


def check_lang(android_child, lang_filename):
    print "///// Checking " + lang_filename

    lang_tree = ET.parse(lang_filename)
    missing = True
    for lang_child in lang_tree.getroot():
        if not "id" in lang_child.attrib:
            log("E", "Lang [%s] missing 'id' attribute" % lang_child)
            continue

        if not "text" in lang_child.attrib:
            log("E", "Lang [%s] missing 'text' attribute" % lang_child)
            continue

        if not lang_child.attrib["text"]:
            log("E", "Lang's text is empty")
            continue

        # if android_child.text == lang_child.attrib["id"]:
        #     missing = False
        #     break


if not sanity_check_android(ANDROID_RES_DIR):
    print "Quitting..."
    quit()

if not sanity_check_langs(LANGS_ANUI_DIR):
    print "Quitting..."
    quit()

print "///// Sanity check: OK"

# try:
lang_files = os.listdir(LANGS_ANUI_DIR)
# BLBY PATH!
android_tree = ET.parse(STRINGS_FILENAME)

for lang_file in lang_files:
    print "///// Checking " + lang_file
    if not lang_file.endswith(".lang"):
        log("?", "'%s' is not a lang file" % lang_file)
        continue

    lang_tree = ET.parse(LANGS_ANUI_DIR + "/" + lang_file)
    for android_child in android_tree.getroot():
        if android_child.tag != "string":
            log("AW", "Skipping tag <%s>" % android_child.tag)
            continue

        if not android_child.text:
            log("AE", "<string> with id '%s' has empty body" % android_child.attrib["name"])
            continue


        # ESTE check whitelist

        for lang_child in lang_tree.getroot():
            if()

        # POZOR toto neni ten ocisteny list

        # missing = True
        # for lang_child in lang_tree.getroot():
        #     if "id" in lang_child.attrib:
        #         if android_child.text == lang_child.attrib["id"]:
        #             missing = False
        #             break
        #
        # if missing == True:
        #     # print "<%s> with value is missing" %android_child.tag + " \"" + android_child.text + "\" missing"
        #     log("E", "<%s> with value '%s' is missing" % (android_child.tag, android_child.text))
# except ET.ParseError:
    # print "Napicu v czech.lang"



