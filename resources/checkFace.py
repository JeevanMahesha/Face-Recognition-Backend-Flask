from flask_restful import Resource, reqparse
import numpy as np
import face_recognition as fr
import json

# get the encodeing of the employee
with open('Json/Face_Encoding_Data.json') as f:
    EncodeJsonData = json.load(f)
    personName = list(EncodeJsonData.keys())
    encodedImgList = list(EncodeJsonData.values())


class CheckUserFace(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'encode',
        action='append',
        required=True,
        help='encoded data is required'
    )

    def post(self):
        request_data = CheckUserFace.parser.parse_args()
        request_data['encode'] = list(map(float, request_data['encode']))
        encodeFace = np.array(request_data['encode'])
        matches = fr.compare_faces(encodedImgList, encodeFace, tolerance=0.5)
        faceDist = fr.face_distance(encodedImgList, encodeFace)
        matchIndex = np.argmin(faceDist)
        name = 'Unknow Person'
        if matches[matchIndex]:
            name = personName[matchIndex]
            return {'Name': name}, 200
        return {'Name': name}, 404


class GetStaffName(Resource):

    def get(self):
        return {'staffName': personName}