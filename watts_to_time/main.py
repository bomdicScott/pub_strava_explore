from watts_to_time.cycling_power import *
import requests,os
import matplotlib.pyplot as plt

class watts_to_time:

    def __init__(self):

        self.project_path = os.path.dirname(__file__)
        self.api_url = "https://www.strava.com/api/v3/segments/"
        self.api_url_append = "/streams/latlng,distance,altitude"
        self.header = {"Authorization": "Bearer 2f82bf84337cfa9de315378bbdc40509ffb3c8e8"}

    def compute_cadence(self, distance_list, altitude_list, distance_range):
        start_index = 0
        distance_temp,altitude_temp = [],[]
        for count in range(len(distance_list)):
            if distance_list[count] - distance_list[start_index] > distance_range:
                distance_temp += [distance_list[count]-distance_list[start_index]]
                altitude_temp += [altitude_list[count]-altitude_list[start_index]]
                start_index = count

        cadence_list = [ altitude_temp[count] / distance_temp[count]*100 for count in range(len(distance_temp)) ]
        return distance_temp,cadence_list

    def watt_to_time_plot(self,watt_list, time_list):
        figure1 = plt.figure(1,figsize=[10,5])
        picture = figure1.add_subplot(111)

        picture.set_ylim(min(watt_list)/2,max(watt_list)*1.1)
        picture.set_xlim(min(time_list)-1, max(time_list)*1.1)
        picture.set_xlabel("time (hr)")
        picture.set_ylabel("watts")

        picture.plot(time_list,watt_list)

        figure1.savefig(self.seg_id+".png",dpi=75,format="png")
        plt.close(1)

    def get_result(self, seg_id, pWeight, pBikeWeight):
        self.seg_id = str(seg_id)

        route = requests.get(self.api_url+self.seg_id+self.api_url_append,headers=self.header).json()
        distance_list = route[1]["data"]
        altitude_list = route[2]["data"]
        distance = max(distance_list)
        distance_list,cadence_list = self.compute_cadence(distance_list,altitude_list, 200)
        time_list = []
        for watt in range(100,500,10):
            time_list += [sum( distance_list[count]/get_speed_mps(watt,pWeight,pBikeWeight,cadence_list[count]) for count in range(len(cadence_list))) / 3600]

        self.watt_to_time_plot(range(100,500,10),time_list)

watts_to_time().get_result(2965631,75,10)