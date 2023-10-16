from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import json
import os

file_list = {}
libfiles_list = os.listdir('static/libs_data')

for libfiles in libfiles_list:
    if libfiles[-5:] != '.json':
        print('Only JSON files are allowed in the static/libs_data folder.')
        exit(-1)
    with open(f'static/libs_data/{libfiles}', 'r') as openfile:
        libname = libfiles[:-5]
        file_list[libname] = json.load(openfile)


## Page Template Language (PTL) Reference:
##    Chamelon language reference: chameleon.readthedocs.io/en/latest/reference.html
##    Blog: majornetwork.net/2021/03/templating-your-python-output-with-chameleon
@view_config(route_name='lib_test', renderer='test_page.pt')
def lib_testing(request):
    index = str(request.matchdict['file_index'])
    lib = str(request.matchdict['lib'])

    file_info = file_list[lib][index]
    lib_list = file_info['out_deps'][:]
    lib_list.append(file_info['url'])
    return dict(libname = file_info['libname'], 
                filename = file_info['filename'],
                version = file_info['version'],
                libs = lib_list)

@view_config(route_name='only_deps', renderer='test_page.pt')
def dep_testing(request):
    index = str(request.matchdict['file_index'])
    lib = str(request.matchdict['lib'])

    file_info = file_list[lib][index]
    lib_list = file_info['out_deps'] + file_info['in_deps']
    return dict(libname = file_info['libname'], 
                filename = file_info['filename'],
                version = file_info['version'],
                libs = lib_list)




if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('lib_test', '/test/{lib}/{file_index}')
        config.add_route('only_deps', '/deps/{lib}/{file_index}')
        
        config.include('pyramid_chameleon')

        config.scan('app')
        config.add_static_view(name='static', path='static')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    print('Website is hold on 127.0.0.1:6543')
    print('More information refer to README. Try to visit: 127.0.0.1:6543/test/jquery/1')
    server.serve_forever()


# 127.0.0.1:6543/test/tween.js@18.6.4@tween.umd.min.js