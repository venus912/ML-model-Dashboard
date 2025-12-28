# venus912 dashboard backend
You can use `setting.yml` as your configuration file. See [template](./template/settings.yml-tpl).


## Run it!
### DB
##### help
```bash
$ venus912_dashboard db -h
```

##### initialization
```bash
$ venus912_dashboard db --settings settings.yml init
$ venus912_dashboard db --settings settings.yml migrate
```

##### migration
```bash
$ venus912_dashboard db --settings settings.yml migrate
$ venus912_dashboard db --settings settings.yml upgrade
```


### Server
##### help
```bash
$ venus912_dashboard server -h
```

##### boot
```bash
$ venus912_dashboard server --settings settings.yml
```

Launched on `http://0.0.0.0:18080` as a default.
