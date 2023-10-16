### Web Library Version Detecting Experiment Set


#### How To Run This Project

1. Install all needed Python packages.
2. Create a `.env` file under `/Exp` folder to enable remote MySQL database connection.
```
(.env format)
DB_HOST=xxx
DB_USERNAME=xxx
DB_PASSWORD=xxx
DB_NAME=xxx
```
3. Run `/Exp/crawler4.py` to crawl JS lib information from CDNJS, and the result will be stored as `/data/crawler4_res.pkl`.
4. Run `/Exp/ToJson2.py` to convert result into JSON format, which is stored in `/data/DetectFile.json`.
5. Run `app.py` to start the testing server. This server will read the data in `/data/DetectFile.json`.
6. Run `/Exp/GenPT_new.py` to aumatically generate pTree for all files in `/data/DetectFile.json`. pTrees will be uploaded to the remote database.
7. Run `/LabeledTree/mini_PTs.py` to minify the pTrees.


#### File Structure

**data:** stores all experiment results.

**script:** stores all experiment scripts.

**app.py:** hosts a trivial server to load library, should be run before experiment.



#### Requirement

Python3 and its libs

Chromedriver and Chrome



#### Other

cdnjs.json file is collected from the [cdnjs API](https://cdnjs.com/api).