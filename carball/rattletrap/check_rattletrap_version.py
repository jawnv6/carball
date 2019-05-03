import inspect
import os
from urllib import request
import json
import fnmatch
from distutils.version import StrictVersion

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

def update_rattletrap():
    print('updating rattletrap in path', path)
    files = os.listdir(path)
    print('files in path', files)

    cur_ver = '0.0.0'
    binaries = [f for f in files if not f.endswith('.py') and fnmatch.fnmatch(f, "*rattletrap*")]
    print('existing found', binaries)

    response = request.urlopen('https://api.github.com/repos/tfausak/rattletrap/releases/latest')

    js = json.loads(response.read())

    if len(binaries) > 0:
        cur_ver = binaries[0].split('-')[1]
    update = StrictVersion(js['name']) > StrictVersion(cur_ver)
    print (f'GitHub version: {js["name"]}\n'
           f'Current version: {cur_ver}\n'
           f'Update? {update}')
    if update:
        for file in binaries:
            os.remove(file)

        for asset in js['assets']:
            print('Downloading {}'.format(asset['name']))
            new_file = os.path.join(path, asset['name'])
            request.urlretrieve(asset['browser_download_url'], filename=new_file)
            print('making file executable', new_file)
            os.chmod(new_file, 0o777)


if __name__ == "__main__":
    update_rattletrap()
