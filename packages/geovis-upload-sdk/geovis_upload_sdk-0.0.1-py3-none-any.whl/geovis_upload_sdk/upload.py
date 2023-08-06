import json
import urllib.parse
import urllib.request
import uuid
from geovis_upload_sdk.sign import hmacSHA256, computeBufferHash


class Uploader:
    def __init__(
            self,
            host: str = "https://cloud.geovisearth.com/",
            # host: str = "http://192.168.160.73:38019/",
            appKey: str = "0e289666-d2e9-401b-a29d-94c75e0423b1",
            secretKey: str = "3dvKBBUNEoE+YjD9ES5E6+y2/XINDcwAAorLLTIi96eccz9F1aqEOALqX/s5EzRVYXmLG+oEL7kUMmvvg/3Vzg==",

    ):
        self.host = host
        self.appKey = appKey
        self.secretKey = secretKey

    def upload(self, categoryId, file):
        fileBuffer = file.read()
        file.seek(0, 2)
        file_size = file.tell()
        chunk_size = 1024 * 1024
        if file_size > chunk_size:
            result = self.normalUpload(categoryId, file, fileBuffer)
            return result
        else:
            result = self.normalUpload(categoryId, file, fileBuffer)
            return result

    def normalUpload(self, categoryId, file, buffer):
        url = self.host
        fileBuffer = buffer
        hashStr = computeBufferHash(fileBuffer)
        encodeFileName = file.filename.encode("utf-8").decode()
        param = "appKey={}&categoryId={}&filename={}&hash={}".format(self.appKey, categoryId, encodeFileName, hashStr)
        sign = hmacSHA256(param, self.secretKey)
        postUrl = "{}api/filecore/upload?{}&sign={}".format(url, param, urllib.parse.quote(sign))
        file.seek(0, 2)
        file_size = file.tell()
        print('file_size___' + str(file_size))
        headers = {
            'Content-Length': str(file_size)
        }
        request_lib = urllib.request.Request(postUrl, data=fileBuffer, method="POST", headers=headers)
        request_lib.add_header("Content-Type", "application/octet-stream")
        response = urllib.request.urlopen(request_lib)
        if response.getcode() == 200:
            result = response.read()
            decoded_data = json.loads(result)
            return decoded_data
        else:
            print("Request failed with status code:", response.getcode())

    def chunkUpload(self, categoryId, file, fileBuffer):
        checkResult = self.checkChunkExist(categoryId, file, fileBuffer)
        # if checkResult:
        #     uploadChunkResult = uploadChunk(categoryId, file)
        #     if uploadChunkResult:
        #         mergeResult = merge(categoryId, file)
        return ''

    def checkChunkExist(self, categoryId, file, fileBuffer):
        checkChunkExistUrl = self.host + 'api/filecore/checkChunkExist'
        chunk_size = 1024 * 1024  # 1MB
        file.seek(0, 2)
        file_size = file.tell()
        totalChunks = file_size // chunk_size
        uuid4Str = uuid.uuid4()
        uuidStr = str(uuid4Str)
        header = {
            "Content-Type": "application/json",
        }
        encodeFileName = file.filename.encode("utf-8").decode()
        # param = "appKey={}&categoryId={}&filename={}&identifier={}&totalChunks={}".format(AppKey, categoryId, encodeFileName, uuidStr,totalChunks)
        # todo - json字符串hash
        param = "appKey={}".format(self.appKey)
        sign = hmacSHA256(param, self.secretKey)
        data = {
            'appkey': self.appKey,
            'categoryId': categoryId,
            'filename': file.filename,
            'identifier': uuidStr,
            'totalChunks': totalChunks,
        }
        data_json = json.dumps(data)
        postUrl = "{}?appKey={}&sign={}".format(checkChunkExistUrl, self.appKey, sign)
        datas = data_json.encode('utf-8')
        request_lib = urllib.request.Request(postUrl, data=datas, method="POST", headers=header)
        request_lib.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(request_lib)
        if response.getcode() == 200:
            result = response.read()
            decoded_data = json.loads(result)
            return decoded_data
        else:
            print("Request failed with status code:", response.getcode())

    def uploadChunk(self, categoryId, file):
        print(self.host)

    def merge(self, categoryId, file):
        return ''
