import json
import scrapy
import os

start_url = "https://satscampuseats.yale-nus.edu.sg/api/v1/staticmenus"


class apispider(scrapy.Spider):
    name = "scrapesatsapi"

    def start_requests(self):
        self.dt = os.environ.get("DT")
        self.sgt = os.environ.get("SGT")
        self.authorization = os.environ.get("AUTHORIZATION")
        self.xid = os.environ.get("XID")

        headers = {
            "Host": "satscampuseats.yale-nus.edu.sg",
            "dt": self.dt,
            "sgt": self.sgt,
            "Authorization": self.authorization,
            "xid": self.xid,
        }  # update as needed (check your network request headers in chrome)
        yield scrapy.Request(start_url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        yield data
