### Web Library Version Detecting Experiment Set


#### How To Run This Project

1. Install all needed Python packages. Download a chrome driver to `/bin/chromedriver`.
2. Create a `.env` file under `/Exp` folder to enable remote MySQL database connection. ([PlanetScale](https://planetscale.com/) is recommended)
```
(.env format)
DB_HOST=xxx
DB_USERNAME=xxx
DB_PASSWORD=xxx
DB_NAME=xxx
```
3. Run `/crawler/get_versions.py` to crawl JS lib version information from CDNJS, and the result will be stored as `/data/lib_versions/<lib name>_v.json`.
4. Run `/crawler/gen_libsdata.py` to organize result from **step 3** into `/static/libs_data/<lib name>.json`, which will be read by the local testing website.
5. Run `app.py` to start the local testing website server. The website provides two basic routes: `test` and `deps`. The `test` routes will load the given library and dependencies, and the `deps` routes will only load all outer dependencies of this library. You need also assign the library name and version index in the url. Following shows an example.
```python
example url: 127.0.0.1:6543/test/jquery/12
# <6543>: port
# <test>: basic route
# <jquery>: library name, must match the file name in the "/static/libs_data/" folder
# <12>: the 12th version
```
6. Run `/exp/gen_pT.py` to aumatically generate pTree for all libraries. pTrees will be uploaded to the local database. Log information will be stored to `/log/gen_pTs` folder.
7. Run `/exp/mini_PTs.py` to minify the pTrees.


#### File Structure

**crawler:** data collection scripts.

**data:** collection results.

**exp:** experiment scripts.

**log:** experiment log.

**static:** static files for the testing website.

**app.py:** hosts a local server to load library, should be run before pTree generation.



#### Requirement

Python3 and its libs

Chromedriver and Chrome



#### Other

Library information is collected from the [cdnjs API](https://cdnjs.com/api).