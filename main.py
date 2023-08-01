# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.

import datetime
import json
import os
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
import requests

waka_key = os.getenv("INPUT_WAKATIME_API_KEY")
waka_key= "waka_50c90df3-e72a-443a-b4bb-ad83522e4523"
stats_range = os.getenv("INPUT_STATS_RANGE", "last_7_days")

def this_range(dates: list) -> str:
    """Returns streak within given range"""
    range_end = datetime.datetime.strptime(dates[4], "%Y-%m-%dT%H:%M:%SZ")
    range_start = datetime.datetime.strptime(dates[3], "%Y-%m-%dT%H:%M:%SZ")
    print("range header created")
    return f"From {range_start.strftime('%d %B, %Y')} to {range_end.strftime('%d %B, %Y')}: {dates[5]}"
def make_graph(data: list, file: str):
    """Make progress graph from API graph"""
    fig, ax = plt.subplots(1, 2, figsize=(16, 5), gridspec_kw = {"width_ratios": [2, 1]})
    with open("/colors.json") as json_file:
        color_data = json.load(json_file)
    BG_WHITE = "#fbf9f4"
    BLUE = "#2a475e"
    GREY70 = "#b3b3b3"
    GREY_LIGHT = "#f2efe8"
    COLORS = ["#FF5A5F", "#FFB400", "#007A87"]
    fig.patch.set_facecolor(BG_WHITE)
    ax[0].set_facecolor(BG_WHITE)
    y_pos = np.arange(len(data[-2]))

    bars = ax[0].barh(y_pos,data[-1], height=0.5)
    ax[0].set_yticks(y_pos)
    ax[0].get_xaxis().set_ticks([])
    ax[0].set_yticklabels(data[-2], color="#586069",weight="bold", fontsize = 20)
    #ax[0].set_title(this_range(data),fontname="Spectral",color=BLUE,weight="bold")
    ax[0].set_title("Projects touched :",color=BLUE,weight="bold")
    ax[0].invert_yaxis()

    ax[0].spines[['right', 'top']].set_visible(False)
    ax[1].spines[['right', 'top', 'bottom', 'left']].set_visible(False)

    for i, bar in enumerate(bars):
        if data[-2][i] in color_data:
            bar.set_color(color_data[data[0][i]]["color"])
        else:
            bar.set_color(
                (
                    "#"
                    + "".join(
                        [random.choice("0123456789ABCDEF") for _ in range(6)]
                    )
                )
            )
        x_value = bar.get_width()
        y_values = bar.get_y() + bar.get_height() / 2
        ax[0].annotate(
            data[-3][i],
            (x_value, y_values),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            color="#586069",
            weight="bold",
            fontsize = 15
        )
    #plt.show()

    myexplode = np.zeros(len(data[2]))
    myexplode[1:] = 0.1
    pie_data = np.array(data[2])
    max_d = np.max(pie_data)
    max_arg = np.argmax(pie_data)
    print(max_d, max_arg, pie_data)
    if max_d > 85:
        pie_data[max_arg] = 85
        diff = max_d - 85
        for i in range(len(pie_data)):
            if  i != max_arg:
                pie_data[i] = pie_data[i] + diff/(len(pie_data)-1) 


    wedges, texts = ax[1].pie(pie_data,  startangle=10, explode = myexplode,
                              shadow = True, labeldistance=1.15, wedgeprops = { 'linewidth' : 4, 'edgecolor' : 'white', 'width':0.5})

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax[1].annotate(data[0][i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),color=BLUE,weight="bold", fontsize = 12,
                    horizontalalignment=horizontalalignment, **kw)
    ax[1].text(s = "Languages", x = 0, y = 0, horizontalalignment='center',verticalalignment='center', fontname="Spectral",color=BLUE,weight="bold", fontsize = 10)
    ax[1].set_title("Languages exploited :",color=BLUE,weight="bold")

    fig.suptitle(this_range(data),color="Black",weight="bold", fontsize = 30)
    fig.tight_layout(pad = 0.5)
    plt.savefig(f"stat{file}.svg", bbox_inches="tight", transparent=True)
    print("new image generated")


def get_stats(stats_range : str) -> list:
    """Gets API data and returns markdown progress"""
    data = requests.get(
        f"https://wakatime.com/api/v1/users/current/stats/{stats_range}?api_key={waka_key}"
    ).json()

    try:
        lang_data = data["data"]["languages"]
        proj_data = data["data"]["projects"]
        start_date = data["data"]["start"]
        end_date = data["data"]["end"]
        range_total = data["data"]["human_readable_total_including_other_language"]
    except KeyError:
        print("error: please add your WakaTime API key to the Repository Secrets")
        sys.exit(1)

    lang_list = []
    time_list = []
    percent_list = []
    project_list = []
    proj_perc_list = []
    proj_time_list = []

    for lang in lang_data[:5]:
        lang_list.append(lang["name"])
        time_list.append(lang["text"])
        percent_list.append(lang["percent"])
    for proj in proj_data[:6]:
        project_list.append(proj["name"])
        proj_perc_list.append(proj["percent"])
        proj_time_list.append(proj["text"])
        
    data_list = [lang_list, time_list, percent_list,
                 start_date, end_date, range_total, proj_time_list, project_list, proj_perc_list]
    print("coding data collected")
    return data_list



if __name__ == "__main__":
    stats_range = "last_7_days"
    waka_stat = get_stats(stats_range)
    make_graph(waka_stat, "file1")
    stats_range = "last_30_days"
    waka_stat = get_stats(stats_range)
    make_graph(waka_stat, "file2")
    
    print("python script run successful")
