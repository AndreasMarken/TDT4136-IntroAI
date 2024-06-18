import Map
import AStarSearch

# for i in range(1, 5):
#     print("Task %d" % i)
#     map_obj = Map.Map_Obj(task=i)
#     path = AStarSearch.aStarSearch(map_obj)
#     map_obj.show_map()

map_obj = Map.Map_Obj(task=4)
path = AStarSearch.aStarSearch(map_obj)
map_obj.show_map()