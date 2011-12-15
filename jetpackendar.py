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
    return tag_wrap("", "th", {"style": "width:100px; padding:1px; color: black;"}) + \
           "".join([tag_wrap("1." + str(release_number + release_base), "th", {"style": "width:40px; padding:1px; color: black;"}) \
                   for release_number in range(0, release_count)])

def get_cell(status):
    if status == "DS":
        return tag_wrap("Dev", "td", {"class":"development", \
                                      "style" : "background: #33FF33; padding:1px; color: black;"})
    if status == "D":
        return tag_wrap("", "td", {"class":"development", \
                                   "style" : "background: #33FF33; padding:1px; color: black;"})
    if status == "SS":
        return tag_wrap("Beta", "td", {"class":"stabilization", \
                                       "style" : "background: #FFFF00; padding:1px; color: black;"})
    if status == "S":
        return tag_wrap("", "td", {"class":"stabilization", \
                                   "style" : "background: #FFFF00; padding:1px; color: black;"})
    if status == "R":
        return tag_wrap("Ship", "td", {"class":"release", \
                                          "style" : "background: #FF3333; padding:1px; color: black;"})
    return tag_wrap("", "td", {"style": "width:40px; padding:1px; color: black;"})

def get_row(tuesday, releases):
    return tag_wrap(str(tuesday), "td", {"style": "width:100px; padding:1px; color: black;"}) + "".join([get_cell(release.milestone(tuesday)) for release in releases])

theading = tag_wrap(get_heading(len(releases), release_base), "tr")
table_heading = tag_wrap(theading, "table", {"class" : "fixedHeader horizontal-stripes", \
                                             "style" : "display: block;  table-layout:fixed; width: 590px;"})

rows = [tag_wrap(get_row(tuesday, releases), "tr") for tuesday in tuesdays]
table_rows = tag_wrap("".join(rows), "table", {"class" : "scrollContent horizontal-stripes", \
                                               "style" : "display: block;  table-layout:fixed; width:606px; height: 450px; overflow: auto;"})


table_container = tag_wrap(table_heading + table_rows, "div", {"class" : "tableContainer", \
                                                               "style" : "clear: both; border: 1px solid #963; height: 485px; width: 615px;"})

css = open("jpc-min.css", "r").read()
head = tag_wrap(tag_wrap(css, "style"), "head")
body = tag_wrap(table_container, "body")
html = tag_wrap(head + body, "html")
f = open("releases.html", "w")
f.write(html)
