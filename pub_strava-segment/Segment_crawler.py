import os,sys,time,requests
from staticmap.staticmap import *
from plot_picture import *


class Segment_crawler:

    def __init__(self):
        self.color_list = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,176,0),(0,255,130),(0,136,255),(255,0,119)]
        self.project_path = os.path.dirname(__file__)
        self.api_url = "https://www.strava.com/api/v3/segments/explore"
        self.header = {"Authorization": "Bearer 2f82bf84337cfa9de315378bbdc40509ffb3c8e8"}

        self.west_south = "25.102807,121.422091" #left_down
        self.north_east = "25.186564,121.564570" #right_up
        self.bounds = "bounds="+self.west_south+","+self.north_east
        self.seg_id = ""

    def draw_route_line(self,route_list,width):
        m = StaticMap(450, 450, 10)
        for route in range(len(route_list)):
            for count in range(len(route_list[route])-3):
                line = Line([route_list[route][count],route_list[route][count+3]], self.color_list[route], width)
                m.add_line(line)
        image = m.render()
        image.save('map.png')

    def altitude_plot(self,route):
        X = route[1]["data"]
        Y1 = route[2]["data"]
        xlim = compute_limit(X)
        Y1lim = compute_limit(Y1) *1.2
        figure1 = plt.figure(1,figsize=[20,10])
        pic = draw_pic(X,Y1,Y1,xlim,Y1lim,Y1lim,"distance","Altitude(m)","Altitude(m)",111,figure1,"outdoor")
        pic.savefig(self.seg_id+".png",dpi=300,format="png")
        plt.close(1)

    def compute_Resolution(self,distance_list):
        total = 0
        for count in range(len(distance_list)-1):
            total += distance_list[count+1] - distance_list[count]

        return self.seg_id + " average : " + str(total / len(distance_list))

if __name__ == "__main__":
    S = Segment_crawler()

    time_start = time.time()
    res = requests.get(S.api_url+"?"+S.bounds,headers=S.header).json()
    route_list, latlng_list = [],[]
    for count in range(len(res["segments"])):
        S.seg_id = str(res["segments"][count]["id"])
        route = requests.get("https://www.strava.com/api/v3/segments/"+S.seg_id+"/streams/latlng,distance,altitude",headers=S.header).json()
        route_list += [route]
        latlng_list+= [[(x[1],x[0]) for x in route[0]["data"]]]
        print(S.compute_Resolution(route[1]["data"]))
    print("requests time : "+str(time.time()-time_start))

    time_start = time.time()
    for route in route_list:
        S.altitude_plot(route)
    print("distance plot time : "+str(time.time()-time_start))

    time_start = time.time()
    S.draw_route_line(latlng_list,3)
    print("plot map time : "+str(time.time()-time_start))