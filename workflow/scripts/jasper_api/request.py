import sys
import os
import requests
import yaml

# Import config files
config_file_paths = [os.path.join(os.path.realpath('..'), 'config', 'config.yml')]
config = {}
for cf in config_file_paths:
    f = open(cf,'r')
    conf = yaml.load(f, Loader=yaml.FullLoader)
    config.update(conf)
    f.close()


def format_cookie(cookie, hostname):
    result = {}
    ck = str(cookie)
    j_session_begin = ck.find('JSESSIONID=') + len('JSESSIONID=')
    jsessionid = ck[j_session_begin:ck.find(' ', j_session_begin + 1)]
    path_begin = ck.find(hostname) + len(hostname)
    path = ck[path_begin:ck.find('>,', path_begin + 1)]
    result.update({"Cookie": "$Version=0; JSESSIONID=" + jsessionid + "; $Path=" + path})
    return result


def main(output):

    # SET URLS

    hostname = config["jasperserver"]["hostname"]
    port = config["jasperserver"]["port"]
    root = os.path.join('http://' + str(hostname) + ':' + str(port) + '/jasperserver/rest_v2/')

    req_dict = {'urls': [
        {'name': 'auth', 'url': os.path.join(root, 'login'), 'headers': {"j_username": config["jasperserver"]["username"], "j_password": config["jasperserver"]["password"]}, 'method': 'post'},
        {'name': 'server', 'url': os.path.join(root, 'serverInfo'), 'headers': {}, 'method': 'get' },
        {'name': 'run', 'url': os.path.join(root, config["jasperserver"]["report_path"]), 'headers': {}, 'method': 'get' }
        ]}


    # SEND REQUESTS

    response_dict = {'responses': []}
    for entry in req_dict['urls']:

        # EXECUTUTE REQUEST
        try:
            if entry['method'] == 'get':
                response = requests.get(entry['url'], headers=entry['headers'])
            if entry['method'] == 'post':
                response = requests.post(entry['url'], data=entry['headers'])

            response_dict['responses'].append(
                {'name': entry['name'], 'url': response.url, 'status_code': response.status_code,
                 'reason': response.reason, 'content': response.content}
                )

            if entry['name'] == 'auth':
                cookie = format_cookie(str(response.cookies), hostname)
                for x in req_dict['urls']:
                    x['headers'].update(cookie)

        except:
            print('Unable to send the following request: '+ entry['url'])


    # WRITE RESULTS

    for response in response_dict['responses']:

        if response['name'] == 'run' and response['status_code'] == 200:
            with open(output, 'wb') as file:
                file.write(response['content'])

        elif response['status_code'] != 200:
            print('Content of failed request for ' + response['name'] + ':\n' )
            for key, val in response.items():
                print(key, " : ", val)
            print()

        else:
            pass


if __name__ == "__main__":
    output = sys.argv[1]
    main(output)