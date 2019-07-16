import requests
import urllib.request
import sys
import globals
import mailer
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

drag_city_list = [
    'Bill Callahan',
    'Bonnie "Prince" Billy',
    'Bonnie "Prince" Billy & The Cairo Gang',
    'Arnold Dreyblatt',
    'David Grubbs',
    'Eiko Ishibashi',
    "Jim O'Rourke",
    'Joanna Newsom',
    'Purple Mountains',
    'Edith Frost',
    'Loose Fur',
    'Scout Niblett',
    'Dead Rider',
    'Death'
]

# Grab the HTML code for the Drag City tours page and identify objects with the 'h1' tag.

url = 'https://www.dragcity.com/tours'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
a = soup.findAll('h1')

# Create a geolocator function per the geopy documentation.

geolocator = Nominatim(user_agent="drag_city_show_finder")

# Create a subset of the drag_city_list showing those artists on tour.

tour_list = []

for item in drag_city_list:
    for i in a:
        if item == i.string:
            tour_list.append(item)
            
print("The following artists of interest are on tour:\n", tour_list)

email_list = []
message = str()

# Create a function that extracts the venue and date for a given show.

def get_venue_and_date(x):
    venue = x.previous_siblings
    next(venue)
    ven = next(venue)
    next(venue)
    date = next(venue)
    return ven, date

# Create a function that grabs the state abbreviation associated with the city as well as the geographic coordinates of the city.

def get_state(x):
    state = x.next_siblings
    next(state)
    st = next(state)
    if st.string == None:
        pass
    else:
        location = x.string + " " + st.string
        location = geolocator.geocode(location)
        coords = (location.latitude, location.longitude)
        return coords
    
# Function that calculates the distance from a city a show is in to the 'home' city selected at the command line.

def dist_from_home(x):
    home = geolocator.geocode(globals.city)
    home_coords = (home.latitude, home.longitude)
    dist_home = geodesic(home_coords, x).miles
    return dist_home

# Create the main function that looks for a match between the city entered at the command line and artists that are on tour.
# The function also looks for shows within a certain distance of the home city.

def find_shows():
    global message
    message = str()
    local_count = 0
    near_count = 0
    for item in drag_city_list:
        for i in a:
            if item == i.string:
                bc = i.next_siblings
                bc_0 = next(bc)
                bc_1 = next(bc)
                city = bc_1.findAll("td", {"class": "city"})
                for item in city:
                    dist_home = dist_from_home(get_state(item))
                    if item.string == globals.city:
                        ven, date = get_venue_and_date(item)
                        ind_message = "Good news! " + str(i.string) + " is playing at " + \
                        str(ven.string) + " on " + str(date.string) + "\n"
                        message += ind_message
                        email_list.append(item)
                    if dist_home < 200:
                        ven_near, date_near = get_venue_and_date(item)
                        add_message = str(i.string) + " is playing at " + str(ven_near.string) + " in " + str(item.string) + " on " + \
                        str(date_near.string) + ".  That's " + str(round(dist_from_home(get_state(item)), 1)) + " miles away.\n"
                        message += add_message
                        near_count += 1
                        
if __name__ == "__main__":
    globals.initialize()
    find_shows()
    if len(email_list) > 0:
        mailer.email('edward.t.lindahl@gmail.com', message)