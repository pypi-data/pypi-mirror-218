import traceback

from layerx.datalake.constants import MULTI_PART_UPLOAD_CHUNK_SIZE

import requests


class StorageInterface:

    def __init__(self):
        self.e_tag = ""

    ''''
    Upload file to the storage bucket (common code for AWS/Google/Azure)
    '''

    def upload_to_storage(self, url, path, upload_type, start_byte = 0, read_bytes = MULTI_PART_UPLOAD_CHUNK_SIZE):
        try:
            with open(path, 'rb') as object_file:
                # Read chunk of file from start_byte
                object_file.seek(start_byte)
                file_data = object_file.read(read_bytes)
                #print('Uploading ' + str(read_bytes) + ' bytes from ' + str(start_byte))
                #Set content type based on upload type
                if(upload_type == "image"):
                    content_type = "image/jpeg"
                elif(upload_type == "video"):
                    content_type = "video/mp4"
                else:
                    content_type = "application/octet-stream"
                res = requests.put(url, data=file_data, headers={'Content-Type': content_type})
                if(res.status_code != 200):
                    print("Error in uploading file to storage: Status code: " + str(res.status_code))
                    print(res.text)
                    return {"isSuccess": False}
                
                if("ETag" not in res.headers):
                    print("Error in uploading file to storage: ETag not found in response header")
                    print(res.text)
                    return {"isSuccess": False}
                
                self.e_tag = res.headers["ETag"][1:-1]

                return {
                    "isSuccess": True,
                    "e_tag": self.e_tag
                }
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred in upload_to_s3")
            return {"isSuccess": False}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error occurred in upload_to_s3")
            return {"isSuccess": False}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred in upload_to_s3")
            return {"isSuccess": False} 
        #Handle other errors
        except requests.exceptions.RequestException as e:
            print("An exception occurred in upload_to_s3")
            traceback.print_exc()
            return {"isSuccess": False}

        except Exception as e1:
            print("An exception occurred in upload_to_s3")
            traceback.print_exc()
            return {"isSuccess": False}

