import sys
import os
import requests
import base64
import time



def main():

    # SET URLS

    hostname = '127.0.0.1'
    port = '8080'
    root = os.path.join('http://' + hostname + ':' + port + '/jasperserver/rest_v2/')
    zip_path = '/home/ubuntu/projects/nanoporeReport/jrxml/jasper.zip'
    myzip = open(zip_path,'rb').read()

    auth = ('jasperadmin', 'jasperadmin')

    zip_req = {'name': 'upload_report',
               'url': os.path.join(root, 'import?update=true&mergeOrganization=true'),
               'headers': {
                   "Content-Type": "application/zip"
                        },
               'data': myzip
            }


    server_info_url = os.path.join(root, 'serverInfo')
    

    import_status_url = root+'import/f43a8a84-dce0-4205-aa98-2d5adfafe6e5/state'


    # SEND REQUEST
    r = requests.post(url=zip_req['url'], headers=zip_req['headers'], auth=auth, data=zip_req['data'])

    # PARSE ID
    start_pos = str(r.content).find('<id>') + len('<id>')
    stop_pos = str(r.content).find('</id>')
    myid = str(r.content)[start_pos:stop_pos]

    import_status_url = root + 'import/' + myid + '/state'

    # SEND STATUS REQUEST
    time.sleep(2)
    status = requests.get(url=import_status_url, auth=auth)

    # PARSE RESPONSE MESSAGE
    start_pos = str(status.content).find('<message>') + len('<message>')
    stop_pos = str(status.content).find('</message>')
    message = str(status.content)[start_pos:stop_pos]

    # PRINT MESSAGE
    if message == 'Import succeeded.':
        print("Reports imported to Jasperserver")
    else:
        print("There was an error importing the reports to the Jasperserver")

if __name__ == "__main__":
    main()


