import datetime

#####################
#  Building the model
#####################

# this is the date development _starts_ for the release identified by release_base
first_tuesday = datetime.date(2011, 10, 18)

# that is, 1.4
release_base = 4

# corresponding Firefox release
firefox_release_base = 7

# number of Firefox releases that we test against
firefox_release_spread = 4

# number of Firefox releases to include
firefox_release_count = 15

# first firefox release date in the schedule
firefox_release_start_date = datetime.date(2011, 9, 27)

# number of releases to include
release_count = 11

# number of weeks to include
week_count = 64

class FirefoxReleaseSet(object):
     def __init__(self, firefox_release_ordinal):
        self.release_ordinal = firefox_release_ordinal
        self.start_date = firefox_release_start_date + (6* datetime.timedelta(weeks=firefox_release_ordinal))
        self.end_date = self.start_date + (6* datetime.timedelta(weeks=1))
        self.releases = [x + firefox_release_ordinal + firefox_release_base for x in range(0, 4)]

firefox_release_schedule_sets = [FirefoxReleaseSet(x) for x in range(0, firefox_release_count)]

def get_release_set(date):
    for x in firefox_release_schedule_sets:
        if x.start_date <= date < x.end_date:
            return x.releases

#for x in firefox_release_schedule_sets:
#    print(str(x.start_date)) + ":" + str(x.releases)

class Release(object):
    def __init__(self, release_ordinal):
        self.release_ordinal = release_ordinal
        self.release_number = release_base + release_ordinal
        self.development_start = first_tuesday + (6* datetime.timedelta(weeks=release_ordinal))
        self.stabilization_start = self.development_start + datetime.timedelta(weeks=6)
        self.release = self.stabilization_start + datetime.timedelta(weeks=6)
        firefox_release_set = get_release_set(self.release)
        self.max_firefox_version = firefox_release_set[1] # the beta

    def get_release_number(self):
        return self.release_number

    def get_supported_firefox_versions(self):
        return str(self.max_firefox_version)

    def get_milestone(self, date):
        if date < self.development_start:
            return None, None
        firefox_releases_supported = [x for x in get_release_set(date) if x <= self.max_firefox_version]
        print str(firefox_releases_supported)
        if date == self.development_start:
            return "DS", firefox_releases_supported
        if date < self.stabilization_start:
            return "D", firefox_releases_supported
        if date == self.stabilization_start:
            return "SS", firefox_releases_supported
        if date < self.release:
            return "S", firefox_releases_supported
        if date == self.release:
            return "R", firefox_releases_supported
        return None, None

releases = [Release(x) for x in range(0, release_count)]
tuesdays = [first_tuesday + (datetime.timedelta(weeks=x)) for x in range(0, week_count)]

####################
#  Building the HTML
####################

def tag_wrap(text, tag, attributes={}):
    result = '\n<' + tag
    for name in attributes.keys():
        result += ' ' + name + '=' + '"' + attributes[name] + '"'
    result +='>' + text + '</'+ tag + '>\n'
    return result

def get_heading(releases):
    return tag_wrap("", "th", {"style": "width:100px; padding:1px; color: black;"}) + \
           "".join([tag_wrap("1." + str(release.get_release_number()), "th", {"style": "width:40px; padding:1px; color: black;"}) \
                   for release in releases])

def get_cell(release, tuesday):
    status, firefox_versions = release.get_milestone(tuesday)
    firefox_support = "Firefox versions: " + str(firefox_versions)
    if status == "DS":
        return tag_wrap("Dev", "td", {"class":"development", \
                                      "style" : "background: #33FF33; padding:1px; color: black;", \
                                      "title" : firefox_support})
    if status == "D":
        return tag_wrap("", "td", {"class":"development", \
                                   "style" : "background: #33FF33; padding:1px; color: black;", \
                                   "title" : firefox_support})
    if status == "SS":
        return tag_wrap("Beta", "td", {"class":"stabilization", \
                                       "style" : "background: #FFFF00; padding:1px; color: black;", \
                                       "title" : firefox_support})
    if status == "S":
        return tag_wrap("", "td", {"class":"stabilization", \
                                   "style" : "background: #FFFF00; padding:1px; color: black;", \
                                   "title" : firefox_support})
    if status == "R":
        return tag_wrap("Ship", "td", {"class":"release", \
                                       "style" : "background: #FF3333; padding:1px; color: black;", \
                                       "title" : firefox_support})
    return tag_wrap("", "td", {"style": "width:40px; padding:1px; color: black;"})

def get_row(tuesday, releases):
    return tag_wrap(str(tuesday), "td", {"style": "width:100px; padding:1px; color: black;"}) + "".join([get_cell(release, tuesday) for release in releases])

theading = tag_wrap(get_heading(releases), "tr")
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
