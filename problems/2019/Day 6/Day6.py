def get_orbit_map():
    f=open("/Users/sleitermann-long/Documents/AdventofCode/AdventofCode2019/Day 6/input.txt") #not with read because thats probably the whole file
    lines = [line.rstrip('\n').split(')') for line in f]
    return {l[1]:l[0] for l in lines}

#part 1
mapdata = get_orbit_map()
search = {"COM"}
disfromcenter = 1 #distance from COM
totaldistance = 0 #total distance of all planets already run through.

while len(mapdata)>0:
  new = {i[0]:i[1] for i in mapdata.items() if i[1] not in search} #determines planets that we have yet to reach on the tree
  search = mapdata.keys() - new.keys() #new planets to search for orbits of, removing the planets we have yet to reach. (new contains the planets we have yet to reach, mapdata contains all of the current planets, so removing the ones we haven't reached gives us our current locations)
  totaldistance+= disfromcenter*(len(mapdata)-len(new)) #take how many steps from center we've moved and multiply it by the number of planets just removed from the set. For example, if we are 5 orbit relationships away and we have found 2 orbit locations, we have just gained 10 paths, 5 for each.
  mapdata = new.copy() #the new map we're working from is the remaining orbit relationships.
  disfromcenter +=1 #we've now moved out from the center by one orbit relationship.

print(totaldistance)

# part 2
mapdata = get_orbit_map()
def get_path(poi):
    path = []
    while poi != 'COM': #We are plotting a path from YOU to COM. We quit when COM is reached.
        path.append(mapdata[poi]) #start at YOU and see what it is orbiting. Append that to the path of orbits.
        poi = mapdata[poi] #Change the position to the object that is being orbited
    return set(path)
you = get_path('YOU')
santa = get_path('SAN')

print(len(you ^ santa)) #The symmetric difference of our paths is the path between us. (Theres a balance here where we have two paths that shouldn't be counted (YOU and SAN) but the two intersections aren't in this set, so it balances out.) The symmetric difference works because it cuts out the mutual path to COM once we intersect.
