# Convert crawled data from CDNJS to json file in the static/libs_data folder, which will be used in the testing website
import json

# ExtJS no valid js file
# Skip Vue, React
file_select_dict = [
    {
        'libname': 'amplifyjs',
        'filenames': ['amplify.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js']
    },
    {
        'libname': 'backbone.js',
        'filenames': ["backbone-min.js", "backbone.js"],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.9.0/underscore-min.js']
    },
    {
        'libname': 'bootstrap',
        'filenames': ['js/bootstrap.js', 'bootstrap.js'],
        'part_deps': [{
            'versions': ['4.5.3', '4.6.0', '4.6.1', '4.6.2'],
            'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js']
        }]
    },
    {
        'libname': 'camanjs',
        'filenames': ['caman.js', 'caman.full.min.js'],
        # 'part_deps': [{
        #     'versions': ['1.0.0', '1.1.0', '1.2.0', '1.2.1', '2.0.0'],
        #     'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js']
        # }]
    },
    {
        'libname': 'core-js',
        'filenames': ['minified.js', 'core.min.js']
    },
    {
        'libname': 'd3',
        'filenames': ["d3.min.js", "d3.js", "d3.v2.js", "d3.v2.min.js"]
    },
    {
        'libname': 'dc',
        'filenames': ["dc.min.js", "dc.js"],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/d3/3.0.0/d3.min.js', 'https://cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.12/crossfilter.min.js'],
        'part_deps': [{
            'versions': ['>=3.0.0'],
            'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/d3/4.0.0/d3.min.js', 'https://cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.12/crossfilter.min.js']
        }]
    },
    {
        'libname': 'dojo',
        'filenames': ['dojo.js']
    },
    {
        'libname': 'extjs',
        'filenames': ['ext-all.js']
    },
    {
        'libname': 'fabric.js',
        'filenames': ['fabric.min.js', 'all.js', "fabric.all.min.js"]
    },
    {
        'libname': 'fastclick',
        'filenames': ["fastclick.min.js"]
    },
    {
        'libname': 'flexslider',
        'filenames': ['jquery.flexslider.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.0/jquery.min.js']
    },
    {
        'libname': 'flot',
        'filenames': ['jquery.flot.js', "jquery.flot.min.js"],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js'],
        'part_deps': [{
            'versions': ['>=2.1.1'],
            'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js', 'jquery.canvaswrapper.min.js']
        }]
    },
    {
        'libname': 'fuse.js',
        'filenames': ['fuse.js']
    },
    {
        'libname': 'google-closure-library',
        'filenames': ['base.js']
    },
    {
        'libname': 'graphiql',
        'filenames': ['graphiql.min.js', 'graphiql.js']
    },
    {
        'libname': 'hammer.js',
        'filenames': ['hammer.js']
    },
    {
        'libname': 'handlebars.js',
        'filenames': ['handlebars.js']
    },
    {
        'libname': 'handsontable',
        'filenames': ['handsontable.full.js', 'handsontable.js', 'jquery.handsontable.full.js', 'jquery.handsontable.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js']
    },
    {
        'libname': 'headjs',
        'filenames': ['head.min.js']
    },
    {
        'libname': 'highcharts',
        'filenames': ['highcharts.js']
    },
    {
        'libname': 'ifvisible',
        'filenames': ['ifvisible.js']
    },
    {
        'libname': 'ink',
        'filenames': ['js/ink-all.js', 'js/ink.js']
    },
    {
        'libname': 'jit',
        'filenames': ['jit.js']
    },
    {
        'libname': 'jquery',
        'filenames': ['jquery.min.js']
    },
    {
        'libname': 'jquery-mobile',
        'filenames': ['jquery.mobile.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js']
    },
    {
        'libname': 'jquery-tools',
        'filenames': ['jquery.tools.min.js']
    },
    {
        'libname': 'jquery.isotope',
        'filenames': ['jquery.isotope.js', 'isotope.pkgd.js']
    },
    {
        'libname': 'jqueryui',
        'filenames': ['jquery-ui.min.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js']
    },
    {
        'libname': 'knockout',
        'filenames': ['knockout-min.js']
    },
    {
        'libname': 'labjs',
        'filenames': ['LAB.min.js']
    },
    {
        'libname': 'leaflet',
        'filenames': ['leaflet.js']
    },
    {
        'libname': 'lodash.js',
        'filenames': ['lodash.js']
    },
    {
        'libname': 'mapbox.js',
        'filenames': ['mapbox.js']
    },
    {
        'libname': 'marionette',
        'filenames': ['marionette.js']
    },
    {
        'libname': 'material-design-lite',
        'filenames': ['material.js']
    },
    {
        'libname': 'matter-js',
        'filenames': ['matter.js']
    },
    {
        'libname': 'modernizr',
        'filenames': ['modernizr.min.js', 'modernizr.js', 'modernizr-1.7.min.js']
    },
    {
        'libname': 'moment-timezone',
        'filenames': ['moment-timezone.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js']
    },
    {
        'libname': 'moment.js',
        'filenames': ['moment.js']
    },
    {
        'libname': 'mootools',
        'filenames': ['mootools-core-full-nocompat-yc.min.js', "mootools-core-compat.js"]
    },
    {
        'libname': 'mustache.js',
        'filenames': ['mustache.min.js', 'mustache.js']
    },
    {
        'libname': 'numeral.js',
        'filenames': ['numeral.min.js']
    },
    {
        'libname': 'paper.js',
        'filenames': ['paper-core.js', 'paper.js', 'paper.min.js']
    },
    {
        'libname': 'pixi.js',
        'filenames': ['pixi.js', 'cjs/pixi.min.js', 'cjs/pixi.js']
    },
    {
        'libname': 'polymer',
        'filenames': ['polymer.min.js', 'polymer.js']
    },
    {
        'libname': 'preact',
        'filenames': ['preact.js']
    },
    {
        'libname': 'processing.js',
        'filenames': ['processing.min.js', 'processing.js']
    },
    {
        'libname': 'prototype',
        'filenames': ['prototype.js']
    },
    {
        'libname': 'pusher',
        'filenames': ['pusher.min.js', 'pusher.js']
    },
    {
        'libname': 'qooxdoo',
        'filenames': ['qooxdoo.js', "q.js", "q.min.js"]
    },
    {
        'libname': 'raphael',
        'filenames': ["raphael-min.js", 'raphael.js']
    },
    {
        'libname': 'require.js',
        'filenames': ['require.min.js']
    },
    {
        'libname': 'riot',
        'filenames': ['riot.js']
    },
    {
        'libname': 'sammy.js',
        'filenames': ['sammy.min.js', 'sammy.js'],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js']
    },
    {
        'libname': 'scriptaculous',
        'filenames': ['scriptaculous.js']
    },
    {
        'libname': 'scrollmagic',
        'filenames': ['ScrollMagic.min.js', 'jquery.scrollmagic.min.js', 'plugins/jquery.scrollmagic.min.js']
    },
    {
        'libname': 'seajs',
        'filenames': ['sea.js']
    },
    {
        'libname': 'socket.io',
        'filenames': ['socket.io.min.js', 'socket.io.js']
    },
    {
        'libname': 'spf',
        'filenames': ['spf.js']
    },
    {
        'libname': 'sugar',
        'filenames': ['sugar.min.js', 'sugar.js']
    },
    # { only one version
    #     'libname': 'swfobject',
    #     'filenames': ['.js']
    # },
    {
        'libname': 'three.js',
        'filenames': ['three.min.js', 'three.js', 'Three.js',  'ROME/Three.min.js']
    },
    {
        'libname': 'tween.js',
        'filenames': ["Tween.js", "Tween.min.js", "tween.esm.js", "tween.esm.min.js"]
    },
    {
        'libname': 'two.js',
        'filenames': ['two.js']
    },
    {
        'libname': 'underscore.js',
        'filenames': ['underscore-min.js', 'underscore-esm-min.js']
    },
    {
        'libname': 'velocity',
        'filenames': ["jquery.velocity.min.js", "jquery.velocity.js", "velocity.min.js", "velocity.js"],
        'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js'],
        'part_deps': [{
            'versions': ['>=1.0.0'],
            'out_deps': []
        }]
    },
    {
        'libname': 'visibility.js',
        'filenames': ['visibility.min.js']
    },
    {
        'libname': 'webfont',
        'filenames': ["webfont.min.js", 'webfont.js', 'webfontloader.js']
    },
    {
        'libname': 'yepnope',
        'filenames': ["yepnope.min.js", 'yepnope.js']
    },
    {
        'libname': 'yui',
        'filenames': ['yui/yui.js', 'yui.js']
    },
    {
        'libname': 'zepto',
        'filenames': ['zepto.min.js', 'zepto.js']
    }
]

def gen_libdata(file_select_item):
    file_dict = {}
    cnt = 1
    LIB_NAME = file_select_item['libname']
    FILE_NAMES = file_select_item['filenames']
    OUT_DEPS =  file_select_item['out_deps'] if 'out_deps' in file_select_item else []

    with open(f'data/lib_versions/{LIB_NAME}_v.json', 'r') as openfile:
        data = json.load(openfile)
    print(f'Start converting version data of {LIB_NAME}.')

    # Arrange dependencies
    deps_dict = {}
    if 'part_deps' in file_select_item:
        for part in file_select_item['part_deps']:
            for v in part['versions']:
                if v[:2] == '>=':
                    v_ = v[2:]
                    start_enter = False
                    for v_info in data:
                        version = v_info['version']
                        if version == v_:
                            start_enter = True
                        if start_enter: 
                            deps_dict[version] = part['out_deps']
                else:
                    deps_dict[v] = part['out_deps']

    # Start converting
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:

                # Check whether the version is mentioned in deps_dict
                version = v_info['version']
                out_deps = OUT_DEPS
                if version in deps_dict:
                    out_deps = deps_dict[version]
                
                # Handle non-url dependency
                for i in range(len(out_deps)):
                    df = out_deps[i]    # dependency file
                    if len(df) < 4 or df[:4] != 'http':   # Not a complete url
                        out_deps[i] = f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{version}/{df}"


                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{version}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': out_deps,
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"    File is not found in {v_info['version']}")

    with open(f'static/libs_data/{LIB_NAME}.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

if __name__ == '__main__':
    for fitem in file_select_dict:
        gen_libdata(fitem)
    print('Complete!')
    
