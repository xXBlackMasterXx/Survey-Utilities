# Survey Utilities


This repo is an set of utilities that allows you to:

1. Download data from a project ID (only linked surveys in it)
2. Generate a reconciliations file from providers using the data collected in the project's surveys
3. A pipeline to generate the report for Lynxeye using the `merged_data.sav` template
4. Match the downloaded SPSS and match the providers target group names (for control purposes)

This folder should contain a `.env` file with the following environmental variables that are used for the scripts

```sh
LUCID_DIR=lucid/
SYNO_EMAIL=val@synoint.com
CINT_ACCESS_DIR=cint_access/
DISTRIBUTION_DIR=distribution/
SYNO_PASSWORD=
PURESPECTRUM_DIR=purespectrum/
EMAIL_SENDER=
DATA_DIR=data/
REMOTE_SERVER=http://localhost:4444
EMAIL_PASSWORD=
```

Here a description of each variable:

`DISTRIBUTION_DIR`: The relative folder path to the distribution background data

`PURESPECTRUM_DIR`: The relative folder path to the purespectrum background data

`LUCID_DIR`: The folder relative path to the lucid background data

`CINT_ACCESS_DIR`: The relative folder path to the Cint Access background data

`SYNO_EMAIL`: The email of the Manager account

`SYNO_PASSWORD`: The password of the Syno Manager account (not Google)

`EMAIL_SENDER`: Usually, the email from Syno (see lesssecureapps in Google to send python emails)

`EMAIL_PASSWORD`: The password of the App to send emails using Python 

`REMOTE_SERVER`: The Selenium grid URL to execute Selenium automate scripts for data retrieval

# Additional notes of the dev environment

1. Check that Docker deamon is running using the following command: 

```bash
sudo service docker status
```

If stopped, you can start it using
```bash
sudo service docker start
```

and use the previous code to check status back again


2. Start the docker container for Selenium Grid using the following command:

```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-edge
```

You can access to the Selenium grid UI using this link once this docker container is running: http://localhost:4444

(Optional) To see what is happening inside the container, head to http://localhost:7900/?autoconnect=1&resize=scale&password=secret.


Please, see the docs for this here:
https://hub.docker.com/r/selenium/standalone-edge