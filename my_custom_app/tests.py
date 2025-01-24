from django.test import TestCase

# Create your tests here.
import http.client

conn = http.client.HTTPSConnection("dev-3zzyd33uzb338uth.us.auth0.com")

payload = '{"client_id":"6FclbGpfkPpk7vhHtTb8DlTrU0WBCWQu","client_secret":"r7tAaNR2EvzMRpC7mV_ZcyODCbP38Bwn7Tkb14QLgcRgE5zaU7FvWHja2lWuQ5ax","audience":"this-is-grnlite-project-api","grant_type":"client_credentials"}'

headers = {"content-type": "application/json"}

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

conn = http.client.HTTPConnection("path_to_your_api")

headers = {
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBpNHp2dXR5SGwzMFVoZ3hHWTFNRiJ9.eyJpc3MiOiJodHRwczovL2Rldi0zenp5ZDMzdXpiMzM4dXRoLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiI2RmNsYkdwZmtQcGs3dmhIdFRiOERsVHJVMFdCQ1dRdUBjbGllbnRzIiwiYXVkIjoidGhpcy1pcy1ncm5saXRlLXByb2plY3QtYXBpIiwiaWF0IjoxNzM0ODEwNjQ1LCJleHAiOjE3MzQ4OTcwNDUsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IjZGY2xiR3Bma1Bwazd2aEh0VGI4RGxUclUwV0JDV1F1In0.oBsaHYnnMfX5aFHZtLrlWrxJC1bKcIYhNCgORGeaSaAwoBADdx90ve_5OrGkAR6-A3VdrQhwFqQGp9-43Kmz30LHKloQ0ROjz7n6GYznDz9b7Lni1ygFus5WxDuJSDFyvZrGag1FAZi1XKwu120upJTS4ZcbpaDWRQS9yePk3gtgLci18jcSN2SI494GXh24stljsNLEEO7_nzntY4GEmsPjSf98ZrgJGrNbSofueC1TAZol2aeB__7P2pP3lRDlZkNbgOXLzjciNxHf3n9gGEw3t2XuNx58LH42YBDq67ngNa-ZG_SttQdk8ksSRxomjXo8zT8q1sRTF1PLzYmINw"
}

conn.request("GET", "/", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
