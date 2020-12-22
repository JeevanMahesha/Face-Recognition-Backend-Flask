from flask_restful import Resource, reqparse
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

# database connection
client = MongoClient(
    "mongodb+srv://ezhil55:ezhil55@cluster0.xaim7.mongodb.net/<dbname>?retryWrites=true&w=majority")
# print("Client Connected ...")
db = client.get_database("Ezhilarasi_5591")
records = db.Ezhil_5591
# records = db.Ezhil_2_12_2020
# print("Database Connected ...")


class UserToDB(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'Name',
        type=str,
        required=True,
        help='Name data is required'
    )

    def post(self, check):
        request_data = UserToDB.parser.parse_args()
        Name = request_data['Name']
        Time = datetime.now().strftime("%H:%M:%S %p")
        Date = datetime.now().strftime("%d-%m-%Y")
        checkdata = list(records.find({'Name': Name, 'Date': Date}))
        if check == 'checkIn':
            if checkdata == []:
                a = []
                a.append(Time)
                a = json.dumps(a)
                data = {
                    "Name": Name,
                    "Status": "Present",
                    "Date": Date,
                    "Check_in_Time": a,
                    "Check_out_Time": "",
                    "Working_Hours": ""
                }
                records.insert_one(data)
            else:
                get_Time = checkdata[0]["Check_in_Time"]
                data = jsonDecoder(get_Time)
                data.append(Time)
                datas = {
                    "Check_in_Time": json.dumps(data)
                }
                records.update_one(
                    {"Name": Name, 'Date': Date}, {"$set": datas})
            # print("Database Inserted ...")
            return {'Message': "Database Inserted ..."}
        elif check == 'checkOut' and checkdata != []:
            if checkdata[0]['Check_out_Time'] == "":
                b = []
                Decoded_Start = jsonDecoder(
                    checkdata[0]['Check_in_Time'])
                Start = str(Decoded_Start[0])
                End = Time
                b.append(Time)
                time_diff_date = datetime.now().strftime("%Y %m %d")
                Working_Hours = TimeDiff(
                    Start, End, time_diff_date)
                data = {
                    "Check_out_Time": json.dumps(b),
                    "Working_Hours": Working_Hours
                }
                records.update_one(
                    {"Name": Name, 'Date': Date}, {"$set": data})
            else:
                Decoded_End = jsonDecoder(checkdata[0]['Check_out_Time'])
                Decoded_Start = jsonDecoder(checkdata[0]['Check_in_Time'])
                Decoded_End.append(str(Time))
                Start = str(Decoded_Start[0])
                End = str(Decoded_End[-1])
                time_diff_date = datetime.now().strftime("%Y %m %d")
                Working_Hours = TimeDiff(Start, End, time_diff_date)
                data = {
                    "Check_out_Time": json.dumps(Decoded_End),
                    "Working_Hours": Working_Hours
                }
                records.update_one(
                    {"Name": Name, 'Date': Date}, {"$set": data})
            # print("Database Updated ...")
            return {'Message': "Database Updated ..."}