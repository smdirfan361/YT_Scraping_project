from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import service
from bs4 import  BeautifulSoup as bs
import  requests
from urllib.request import urlopen as  uqrl
from flask import Flask,request,render_template,jsonify
import  time
import os

app=Flask(__name__)


def yt_info_extrater(bshtm):
    video_info_list = []
    video_titles = bshtm.find_all("div", {"id": "meta"})
    channel_name = bshtm.find_all("div", {"id": "text-container"})
    views = bshtm.find_all("span", {"class": "inline-metadata-item style-scope ytd-video-meta-block"})
    uploaded_at = bshtm.find_all("span", {"class": "inline-metadata-item style-scope ytd-video-meta-block"})

    for a, b, c, d in zip(video_titles, channel_name, views, uploaded_at):
        info = []
        video_hyper_link = a.find("a")
        if video_hyper_link:
            video_title = video_hyper_link.text.replace("\n", "")
            info.append(video_title)
        name = b.text.replace("\n", "")
        info.append(name)
        view_numbers = c.text.replace("\n", "")
        if "view" in view_numbers:
            info.append(view_numbers)
        duration = d.text.replace("\n", "")
        if "views" not in duration:
            info.append(duration)

        video_info_list.append(info)
    return video_info_list

@app.route("/",methods=["POST","GET"])
def yt_get_info():
    if request.method=="POST":
        url = input(').replace(" ", "")
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        htm = driver.page_source
        driver.quit()
        bshtm = bs(htm, "html.parser")
        video_info_list = yt_info_extrater(bshtm)

    return jsonify(video_info_list)

if __name__ == "__main__":
    app.run()
