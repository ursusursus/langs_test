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

    if android_child.text == lang_child.attrib["text"]:
        return False

def check_lang_file(android_tree, lang_tree):
    for android_child in android_tree.getroot():
        print android_child.tag
        # ESTE check whitelist

        for lang_child in lang_tree.getroot():
            if check_lang(android_child, lang_child):
                return True

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
lang_filesnames = os.listdir(LANGS_ANUI_DIR)

# Parse android strings contents
android_tree = ET.parse(path.join(ANDROID_RES_DIR, STRINGS_FILENAME))

# print "BEFORE"
# for android_child in android_tree.getroot():
#         print android_child.tag

# Clean BS android xml elements
root = android_tree.getroot()
print len(root)
for android_child in root:
    print android_child.tag

    if android_child.tag != "string":
        log("AW", "Skipping tag <%s>" % android_child.tag)
        root.remove(android_child)
        continue

    if not android_child.text:
        log("AE", "<string> with id '%s' has empty body" % android_child.attrib["name"])
        root.remove(android_child)
        continue


# print "AFTER"
# for android_child in android_tree.getroot():
#         print android_child.tag

# # Every .lang file
# for lang_filename in lang_filesnames:
#     print "///// Checking " + lang_filename
#     if not lang_filename.endswith(".lang"):
#         log("?", "'%s' is not a lang file. Skipping..." % lang_filename)
#         continue
#
#     # Parse lang file contents
#     try:
#         lang_tree = ET.parse(path.join(LANGS_ANUI_DIR, lang_filename))
#     except  ET.ParseError:
#         log("F", "%s not a valid xml document!!!\n" % lang_filename)
#         continue
#
#     # Check na na na
#     if check_lang_file(android_tree, lang_tree):
#         print "[OK]\n"
#
# # END


