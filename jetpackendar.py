import datetime

#####################
#  Building the model
#####################

# this is the date development _starts_ for the release identified by release_base
first_tuesday = datetime.date(2011, 10, 18)
# that is, 1.4
release_base = 4
# number of releases to include
release_count = 11
# number of weeks to include
week_count = 64

class Release(object):
    def __init__(self, start_date):
        self.development_start = start_date
        self.stabilization_start = start_date + datetime.timedelta(weeks=6)
        self.release = start_date + datetime.timedelta(weeks=12)

    def milestone(self, date):
        if date < self.development_start:
            return None
        if date == self.development_start:
            return "DS"
        if date < self.stabilization_start:
            return "D"
        if date == self.stabilization_start:
            return "SS"
        if date < self.release:
            return "S"
        if date == self.release:
            return "R"
        return None

shipdays = [ first_tuesday + (6* datetime.timedelta(weeks=x)) for x in range(0, release_count) ]
tuesdays = [ first_tuesday + (datetime.timedelta(weeks=x)) for x in range(0, week_count) ]
releases = [Release(shipday) for shipday in shipdays]

####################
#  Building the HTML
####################

def tag_wrap(text, tag, attributes={}):
    result = '\n<' + tag
    for name in attributes.keys():
        result += ' ' + name + '=' + '"' + attributes[name] + '"'
    result +='>' + text + '</'+ tag + '>\n'
    return result

def get_heading(release_count, release_base):
    return tag_wrap("", "th") + \
           "".join([tag_wrap("1." + str(release_number + release_base), "th") \
                   for release_number in range(0, release_count)])

def get_cell(status):
    if status == "DS":
        return tag_wrap("Dev", "td", {"class":"development"})
    if status == "D":
        return tag_wrap("", "td", {"class":"development"})
    if status == "SS":
        return tag_wrap("Beta", "td", {"class":"stabilization"})
    if status == "S":
        return tag_wrap("", "td", {"class":"stabilization"})
    if status == "R":
        return tag_wrap("Release", "td", {"class":"release"})
    return tag_wrap("", "td")

def get_row(tuesday, releases):
    return tag_wrap(str(tuesday), "td") + "".join([get_cell(release.milestone(tuesday)) for release in releases])

theading = tag_wrap(get_heading(len(releases), release_base), "tr")
thead = tag_wrap(theading, "thead", {"class" : "fixedHeader"})

rows = [tag_wrap(get_row(tuesday, releases), "tr") for tuesday in tuesdays]
tbody = tag_wrap("".join(rows), "tbody", {"class" : "scrollContent"})

table = tag_wrap(thead + tbody, "table", {"border": "0", "class" : "scrollTable"})
table_container = tag_wrap(table, "div", {"class" : "tableContainer"})

css = open("jpc-min.css", "r").read()
head = tag_wrap(tag_wrap(css, "style"), "head")
body = tag_wrap(table_container, "body")
html = tag_wrap(head + body, "html")
f = open("releases.html", "w")
f.write(html)
