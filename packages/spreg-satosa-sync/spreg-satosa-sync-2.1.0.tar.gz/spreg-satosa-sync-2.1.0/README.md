# spreg_satosa_sync.py

Script to read clients attributes from perun rpc and write them to mongoDB.

## Usage

Install script requirements.

```
pip install -r ./requirements.txt
```

Script argument is path to config file.

```
./spreg_satosa_sync.py ~/Documents/spreq-satosa-sync/config_template.yml
```

Script uses [perun.connector](https://pypi.org/project/perun.connector/) library. Because of this, you have to
fill `adapters_manager` and `attrs_cfg_path` configuration options in `config_template.yml`. `attrs_cfg_path` is path to
yaml file, which specifies mapping of attributes. You can find inspiration for the configuration in `config_templates`
directory in perun.connector repository.
