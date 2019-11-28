# Download Hawk

A script to monitor any changes to the bins and links on the url

## Installation 

Tested working only on Linux. 


To support PyVirtualDisplay (Needed for a VPS)

```
sudo apt-get install xvfb
sudo apt-get install x11-utils
```

Install firefox
```
sudo apt-get install firefox-esr

```
Install python pip3 and git (if required)
```
sudo apt-get install python3-pip
sudo apt-get install git
```

Clone the git repo

```
git clone https://github.com/degeri/DownloadHawk.git
cd DecredMon
pip3 install -r requirements.txt
```

Edit the ini file and simply run

```
python3 main.py
```

For continuous monitoring keep the terminal open or add it as a service. 

## How to edit the config.ini file

The current ini is configured for  https://decred.org/wallets 


It is very important that this be configured correctly to avoid false positives. 

programconfig

```
checktimemins : How mins to wait before doing an new check
useragent : Browser useragent
hide_ff : Set as "True" by default. Set as "False" for debugging
matrix_alert : Set True for a matrix box alert
```


matrixconfig

```
accesstoken  : Your private access token for the bot

example curl to obtain:

curl -XPOST -d '{"type":"m.login.password", "user":"USER_REPLACE", "password":"PASSWORD_REPLACE"}' "https://matrix.decred.org/_matrix/client/r0/login"

roomid: Internal room ID eg:!XXXXXXXXXXXXXXX:decred.org

server_url : Matrix Server URL eg: https://matrix.decred.org/


```

urls

```
siteurl : Your wallet page eg:https://decred.org/wallets/
```

This script supports two types of links. 

### Direct Bins.

bin_list_url_sha_check

```
do_check : Set as "True" by default. Give "Flase" if page has no direct bins.
list : List of sections that contain url,hash,xpath,attribute

```

Example section

```
[DecreditonLinux]
url=https://github.com/decred/decred-binaries/releases/download/v1.4.0/decrediton-v1.4.0.tar.gz
hash=2e70094600731cbddc7261f3c6095edca525d1f87030d4a7d3bf1720cefb548c
xpath=//*[@id="decreditonlinux"]
attribute=href
```



### Links that go to other pages.


link_list_url_check

```
do_check : Set as "True" by default. Give "Flase" if page has no links.
list : List of sections that contain url,xpath,attribute

```


Example section

```
[Android]
url=https://play.google.com/store/apps/details?id=com.decred.dcrandroid.mainnet
xpath=/html/body/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div[3]/a[1]
attribute=href

```

How to find xpath https://discourse.mozilla.org/t/how-can-i-get-the-xpath-of-an-element-in-developer-tools-as-firebug-is-not-supported-in-latest-ff/25934/2
