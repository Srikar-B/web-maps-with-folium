"""
folium is a third party library for python which has maps.
first create map object
then everything that I add to the map is called child. usage  add_child.
>>There are multiple layers on the map. ex : map, markers, rivers, polygons etc 
"""
import folium
import pandas
import itertools

data=pandas.read_csv("Volcanoes.txt")

# here map object is created
# location is a list of latitude and longitude
# zoom_start tells how much the map should be zoomed when the page loads
# tiles tell about the type of maps example: Terrain 

map = folium.Map(location=[38.58,-99.09],zoom_start=4.5,tiles="cartodbpositron")

"""tiles ex: Mapbox Bright, openstreetmap, mapquestopen, MapQuest Open Aerial, 
Mapbox Control Room, stamenterrain, stamentoner, stamenwatercolor,ccartodbdark matter etc"""

latitudes=list(data['LAT']) # data['LAT'] is a pandas series type so im converting it to list coz list is fast
longitudes=list(data['LON'])
names=list(data['NAME'])
altitude=list(data['ELEV'])
html="""<h4 style='color:red'>Volcano info</h4><br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>"""
# this is a way of searching in google search?q=%%22searchname%%22

fgv = folium.FeatureGroup(name="Volcanoes")# fgv is a featuregroup object used to add child to map (here volcanoes)

for i,j,k,l in zip(latitudes,longitudes,names,altitude): # also use just i instead of i,j,k . if only i is used i will be a tuple of three values
	if (l<=1000):
		color="green"
	elif(l<=2500):
		color="orange"
	else:
		color="red"

	iframe= folium.IFrame(html=html %(k+" Volcano",k.upper()),width=200, height=100)
	# IFrame is html for popups
	fgv.add_child( folium.CircleMarker( location=[i,j],radius=6, popup=folium.Popup(iframe) ,
		fill_color=color,color='black', fill_opacity=0.8) ) # child 1

fgp = folium.FeatureGroup(name="population")# fgv is a featuregroup object used to add child to map (here population)

fgp.add_child(folium.GeoJson(data=(open('world.json','r',encoding='utf-8-sig').read()),
	style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<1032000 
	else 'violet' if x['properties']['POP2005']<10102000 else 'orange' if x['properties']['POP2005']<110000000
	else 'red' })) # child 2

"""icon=folium.Icon(color='color') for normal icons"""
# Markers on the maps can be added using Marker method which takes location, icon, and message(popup)

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl()) #  this should be added only after the previous line
map.save("mymap.html") # this creates a html file in the directory