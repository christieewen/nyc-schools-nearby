import networkx as nx

def commute_search(stop, time):
    """
    Find and return a list of schools that are
    within *time* minutes of *stop*
    """
    time = float(time)  # I'm not using time yet
    return [s for s in school if set(reachable(s)) & set(trains[stop])]


def reachable(school):
    """
    return the trains of a school
    """
    trains = []
    routes = subways[school].split(';  ')
    for r in routes:
        trains+=r.split(' to ')[0].split(', ')
    return trains

#=========READ IN SCHOOL AND TRANSIT DATA========#

#read in schools from pediacities
import urllib
import ast
url = 'http://nycdoe.pediacities.com/api/action/datastore_search_sql?sql='
url+='SELECT "Printed_Name","BUS","SUBWAY"'
url+='FROM "45f6a257-c13a-431b-acb9-b1468c3ff1e9"'
s = urllib.urlopen(url).read()
list_string = s[s.index('['):s.index(']')+1]
data = ast.literal_eval(list_string)  # [ {'BUS':'M14AD, ...',
subways = {}
buses = {}
for d in data:
    buses[d['Printed_Name']] = d['BUS']
    subways[d['Printed_Name']] = d['SUBWAY']
school = buses.keys()

#read in subway lines from csv
import networkx as nx
f = open('mta_subways.csv','r')
f.readline()
trains = {}  # {stop : [ line1 , line2 , ... ]}
subway_map = nx.Graph()
previous = {}  # {train: previous_stop}
pos = {}  # {stop: position}
for file_line in f:
    file_line = file_line.strip().split(",")

    #line = file_line[1]
    stop = file_line[1] + " " + file_line[2]
    lines = file_line[5:16]
    while '' in lines:
        lines.remove('')
    trains[stop] = lines

    #add it to my subway graph
    for train in lines:
        if train in previous.keys() and previous[train] is not stop:
            subway_map.add_edge(stop, previous[train],{'train':train})
        previous[train] = stop
        pos[stop] = (file_line[-2],file_line[-1])

#nx.draw_networkx_nodes(subway_map,pos) 

stop = trains.keys()

#=========SCRIPT STARTS HERE===============#
import sys
if len(sys.argv) <= 1:
    print "No arguments provided. Here's some sample output though:"
    print "  stops[0:10] -> ", stop[:10]
    print "  schools[0:10] -> ", school[:10]
elif len(sys.argv)==2:
    if sys.argv[1] == 'stops':
        print stop
    elif sys.argv[1] == 'schools':
        print school
    else:
        print 'Unknown parameter options supplied:',sys.argv,'Try "stops" or "schools"'
else:
    try:
        print commute_search(sys.argv[1], sys.argv[2])
    except:
        print 'Unknown parameter options supplied:',sys.argv,'Try "Lawrence St" and 10'
