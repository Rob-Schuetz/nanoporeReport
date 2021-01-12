import sys
import os
import requests
import base64


def format_cookie(cookie, hostname):
    print('STEP 1')
    result = {}
    ck = str(cookie)
    print('STEP 2')
    j_session_begin = ck.find('JSESSIONID=') + len('JSESSIONID=')
    jsessionid = ck[j_session_begin:ck.find(' ', j_session_begin + 1)]
    path_begin = ck.find(hostname) + len(hostname)
    print('STEP 3')
    path = ck[path_begin:ck.find('>,', path_begin + 1)]
    result.update({"Cookie": "$Version=0; JSESSIONID=" + jsessionid + "; $Path=" + path})
    print('STEP 4')
    print(result)
    return result


def main():

    # SET URLS

    hostname = '3.83.85.120'
    port = '8080'
    root = os.path.join('http://' + hostname + ':' + port + '/jasperserver/rest_v2/')
    jrxml_path = r'C:\Users\RSchuetz\Downloads\nanoporeReport_notpresent.jrxml'
    jasper_report = open(jrxml_path, 'rb').read()
    encoded_jasper_report = base64.b64encode(jasper_report)
    
    req_dict = {'urls': [
        {'name': 'auth', 'url': os.path.join(root, 'login'), 'headers': {}, 'data': {"j_username": "jasperadmin", "j_password": "jasperadmin"}, 'method': 'post'},
        {'name': 'server_info', 'url': os.path.join(root, 'serverInfo'), 'headers': {}, 'method': 'get' },
        {'name': 'upload_report', 'url': os.path.join(root, 'resources/public'), 'headers': {"Content-Type": "application/repository.dataType+json"}, 'data': {
                "label": "Sample",
                "jrxml": {
                    "jrxmlFile": {
                        "label": "MyJRXML",
                        "type":"jrxml",
                        ## encode your file in Base64 and put here
                        "content": encoded_jasper_report
                    }
                }
            }, 'method': 'post' }
        ]}


    # SEND REQUESTS

    response_dict = {'responses': []}
    for entry in req_dict['urls']:

        print(entry)

        # EXECUTE REQUEST
        try:
            if entry['name'] == 'server_info':
                response = requests.get(entry['url'], headers=entry['headers'])
            if entry['name'] ==  'upload_report':
                response = requests.post(entry['url'], data=entry['data'], headers=entry['headers'])
            if entry['name'] ==  'auth':
                response = requests.post(entry['url'], data=entry['data'])
                print('got an auth response!')
                print(response.cookies)

            response_dict['responses'].append(
                {'name': entry['name'], 'url': response.url, 'status_code': response.status_code,
                 'reason': response.reason, 'content': response.content}
                )

            print('Hello!')

            if entry['name'] == 'auth':
                print('AYYY')
                cookie = format_cookie(str(response.cookies), hostname)
                print(cookie)
                for x in req_dict['urls']:
                    print(x['name'])
                    x['headers'].update(cookie)

        except:
            print('Unable to send the following request: '+ entry['url'])

    print(response_dict)
##
##
##    # WRITE RESULTS
##
##    for response in response_dict['responses']:
##
##        if response['name'] == 'run' and response['status_code'] == 200:
##            with open(output, 'wb') as file:
##                file.write(response['content'])
##
##        elif response['status_code'] != 200:
##            print('Content of failed request for ' + response['name'] + ':\n' )
##            for key, val in response.items():
##                print(key, " : ", val)
##            print()
##
##        else:
##            pass


if __name__ == "__main__":
    #output = sys.argv[1]
    main()

