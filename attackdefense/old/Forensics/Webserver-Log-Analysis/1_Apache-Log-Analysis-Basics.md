#### 1. Apache Log Analysis Basics

----

Apache web access logs are in the file apache_access.log. Answer the following questions using basic Linux utilities like grep, awk, sort, uniq etc.

```sh
student@attackdefense:~$ ls -l
total 1900
-rw-r--r-- 1 root root 1943341 Oct  1  2018 apache_access.log
student@attackdefense:~$
```

- How many logs are present in the log file?

```sh
student@attackdefense:~$ cat apache_access.log | wc -l
10000
student@attackdefense:~$
```

```
10000
```

----

- Print top 5 clients IPs by number of requests made

```sh
student@attackdefense:~$ awk '{print $1}' apache_access.log | sort | uniq -c | sort -b -n -k1 | tail -5
    139 91.141.1.150
    160 37.1.206.196
    241 195.212.98.190
    434 213.150.254.81
   1929 148.251.50.49
student@attackdefense:~$
```

```
91.141.1.150
37.1.206.196
195.212.98.190
213.150.254.81
148.251.50.49
```

----

- Print top 5 user agents by number of requests made

```sh
student@attackdefense:~$ awk -F\" '{print $6}' apache_access.log | sort | uniq -c | sort -n  | tail -6
    165 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36
    185 Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
    332 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
    434 Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
   1949 -
   5135 Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0
student@attackdefense:~$
```

```
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0\
```

----

- Print top 5 requested URLs by HTTP method (Request method and URL side by side)

```sh
student@attackdefense:~$ awk -F\" '{print $2}' apache_access.log | sort | uniq -c | sort -fn | tail -5
    281 GET / HTTP/1.1
    962 POST /administrator/index.php HTTP/1.0
    978 GET /administrator/index.php HTTP/1.0
   2576 GET /administrator/ HTTP/1.1
   2621 POST /administrator/index.php HTTP/1.1
student@attackdefense:~$
```

```
GET / HTTP/1.1
POST /administrator/index.php HTTP/1.0
GET /administrator/index.php HTTP/1.0
GET /administrator/ HTTP/1.1
POST /administrator/index.php HTTP/1.1
```

----

- Print top 5 requested URLs

```sh
student@attackdefense:~$ awk -F\" '{print $2}' apache_access.log | cut -d " " -f2 | sort | uniq -c | sort -fn | tail -5
    106 /robots.txt
    117 /templates/_system/css/general.css
    322 /
   2587 /administrator/
   4669 /administrator/index.php
student@attackdefense:~$
```

```
/robots.txt
/templates/_system/css/general.css
/
/administrator/
/administrator/index.php
```

----

- Print all URLs which did not receive a 200 OK response status

```sh
student@attackdefense:~$ grep -v 200 apache_access.log | awk -F\" '{print $3 $2 }'| sort | uniq -c | sort -fn
      1
      1  304 - GET /configuration.php-dist HTTP/1.1
      1  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_l_almhuette_raith.jpg HTTP/1.1
      1  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_l_almhuette_raith_016.jpg HTTP/1.1
      1  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_l_terasse.jpg HTTP/1.1
      1  304 - GET /images/stories/raith/almhuette_raith.jpg HTTP/1.1
      1  304 - GET /images/stories/raith/garage.jpg HTTP/1.1
      1  304 - GET /images/stories/raith/grillplatz.jpg HTTP/1.1
      1  304 - GET /images/stories/raith/wohnraum.jpg HTTP/1.1
      1  304 - GET /robots.txt HTTP/1.1
      1  404 1397 GET /index.php?option=com_easyblog&view=dashboard&layout=write HTTP/1.1
      1  404 206 GET /wp-login.php HTTP/1.0
      1  404 206 GET /wp-login.php?action=register HTTP/1.0
      1  404 214 GET //xxu.php HTTP/1.1
      1  404 214 GET http://almhuette-raith.at/ejou.php?bnjxmi HTTP/1.1
      1  404 216 GET /config.php HTTP/1.1
      1  404 218 GET /wp/wp-admin/ HTTP/1.1
      1  404 219 GET /old/wp-admin/ HTTP/1.1
      1  404 220 GET /blog/wp-admin/ HTTP/1.1
      1  404 220 GET /test/wp-admin/ HTTP/1.1
      1  404 221 GET //images/xxu.php HTTP/1.1
      1  404 221 GET /apache-log/access.log.69.gz HTTP/1.0
      1  404 221 GET /js/lib/ccard.js HTTP/1.1
      1  404 223 GET /libraries/css.php HTTP/1.1
      1  404 223 GET /libraries/lol.php HTTP/1.1
      1  404 225 GET /wordpress/wp-admin/ HTTP/1.1
      1  404 232 GET /apache-log/error.log.20.gz HTTP/1.1
      1  404 232 GET /apache-log/error.log.44.gz HTTP/1.1
      1  404 232 GET /apache-log/error.log.55.gz HTTP/1.1
      1  404 233 GET /apache-log/access.log.17.gz HTTP/1.1
      1  500 88 GET / HTTP/1.1
      2  301 256 GET /administrator HTTP/1.1
      2  304 - GET /images/stories/raith/almenland_logo.jpg HTTP/1.1
      2  304 - GET /images/stories/raith/oststeiermark.png HTTP/1.1
      2  304 - GET /images/stories/raith/steiermark_herz.png HTTP/1.1
      2  304 - GET /images/stories/raith/wohnung_1_web.jpg HTTP/1.1
      2  304 - GET /templates/jp_hotel/images/module_heading.gif HTTP/1.1
      2  404 213 GET /cfg.php HTTP/1.1
      2  404 220 GET /icons/text.gif HTTP/1.1
      2  404 223 GET /browserconfig.xml HTTP/1.1
      2  404 227 GET /wp-admin/wp-login.php HTTP/1.1
      2  404 257 POST /media/editors/tinymce/skins/lightgray/img/thumb.php HTTP/1.1
      3  304 - GET /components/com_phocagallery/assets/images/icon-folder-medium.gif HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_001.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_002.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_003.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_004.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_005.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_006.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_007.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_008.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_009.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_010.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_011.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_012.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_aussicht.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_garage.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_grillplatz.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_jaegerzaun_gr.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_terasse.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_wohnraum.jpg HTTP/1.1
      3  304 - GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_zimmer.jpg HTTP/1.1
      3  404 213 GET /contact HTTP/1.1
      3  404 215 GET /wp-admin/ HTTP/1.1
      3  405 242 PUT /i\xafdonesia.htm HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/images/icon-up-images.gif HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/images/icon-view.gif HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/images/shadow1.gif HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/shadowbox.js HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/lang/shadowbox-en.js HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/player/shadowbox-img.js HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/close.png HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/next.png HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/pause.png HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/play.png HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/previous.png HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/loading.gif HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/skin.css HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/skin.js HTTP/1.1
      5  304 - GET /components/com_phocagallery/assets/phocagallery.css HTTP/1.1
      5  304 - GET /media/system/css/modal.css HTTP/1.1
      5  304 - GET /media/system/js/modal.js HTTP/1.1
      5  304 - GET /templates/jp_hotel/images/content_heading.gif HTTP/1.1
      5  404 225 GET /media/jui/js/cms.js HTTP/1.1
      6  404 235 POST /libraries/joomla/exporter.php HTTP/1.1
      8  500 88 GET /administrator/ HTTP/1.1
      9  304 - GET /media/system/js/caption.js HTTP/1.1
     12  304 - GET /modules/mod_bowslideshow/tmpl/images/image_shadow.png HTTP/1.1
     14  404 218 GET /wp-login.php?action=register HTTP/1.1
     15  304 - GET /images/bg_raith.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_01.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_02.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_03.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_04.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_05.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_06.jpg HTTP/1.1
     15  304 - GET /images/stories/slideshow/almhuette_raith_07.jpg HTTP/1.1
     15  304 - GET /media/system/js/mootools.js HTTP/1.1
     15  304 - GET /modules/mod_bowslideshow/tmpl/css/bowslideshow.css HTTP/1.1
     15  304 - GET /modules/mod_bowslideshow/tmpl/js/sliderman.1.3.0.js HTTP/1.1
     15  304 - GET /templates/jp_hotel/css/layout.css HTTP/1.1
     15  304 - GET /templates/jp_hotel/css/menu.css HTTP/1.1
     15  304 - GET /templates/jp_hotel/css/suckerfish.css HTTP/1.1
     15  304 - GET /templates/jp_hotel/css/template.css HTTP/1.1
     15  304 - GET /templates/jp_hotel/images/logo.jpg HTTP/1.1
     15  304 - GET /templates/jp_hotel/js/moomenu.js HTTP/1.1
     15  404 218 GET /wp-login.php HTTP/1.1
     19  404 221 GET /apache-log/access.log.61.gz HTTP/1.0
     23  404 217 GET /favicon.ico HTTP/1.1
    115  404 239 GET /templates/_system/css/general.css HTTP/1.1
student@attackdefense:~$
```

----

- Print all the URLs requested by the client with IP 91.141.1.150. Order (descending) by number of times the URL was requested.

```sh
student@attackdefense:~$ grep "91.141.1.150" apache_access.log | awk -F\" '{print $2 }'| sort | uniq -c | sort -fn
      1 GET /components/com_phocagallery/assets/images/icon-folder-medium.gif HTTP/1.1
      1 GET /components/com_phocagallery/assets/images/icon-up-images.gif HTTP/1.1
      1 GET /components/com_phocagallery/assets/images/icon-view.gif HTTP/1.1
      1 GET /components/com_phocagallery/assets/images/shadow1.gif HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/shadowbox.js HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/lang/shadowbox-en.js HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/player/shadowbox-img.js HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/close.png HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/next.png HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/pause.png HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/play.png HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/icons/previous.png HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/loading.gif HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/skin.css HTTP/1.1
      1 GET /components/com_phocagallery/assets/js/shadowbox/src/skin/classic/skin.js HTTP/1.1
      1 GET /components/com_phocagallery/assets/phocagallery.css HTTP/1.1
      1 GET /images/bg_raith.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_1_essecke.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_2_wohnkche.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_3_wohnkche1.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_4_schlafzimmer.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_5_bad.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_l_6_wc.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_1_essecke.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_2_wohnkche.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_3_wohnkche1.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_4_schlafzimmer.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_5_bad.jpg HTTP/1.1
      1 GET /images/phocagallery/Ferienwohnung_2/thumbs/phoca_thumb_m_6_wc.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_001.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_002.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_003.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_004.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_005.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_006.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_007.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_008.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_009.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_010.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_011.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_012.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_aussicht.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_garage.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_grillplatz.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_jaegerzaun_gr.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_terasse.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_wohnraum.jpg HTTP/1.1
      1 GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_zimmer.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%201.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2010.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2011.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2012.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2013.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2014.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2015.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2016.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2017.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2018.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2019.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%202.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%2020.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%203.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%204.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%205.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%206.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%207.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto%209.jpg HTTP/1.1
      1 GET /images/phocagallery/thumbs/phoca_thumb_m_winterfoto.jpg HTTP/1.1
      1 GET /images/stories/raith/almenland_logo.jpg HTTP/1.1
      1 GET /images/stories/raith/almhuette_raith.jpg HTTP/1.1
      1 GET /images/stories/raith/garage.jpg HTTP/1.1
      1 GET /images/stories/raith/grillplatz.jpg HTTP/1.1
      1 GET /images/stories/raith/oststeiermark.png HTTP/1.1
      1 GET /images/stories/raith/steiermark_herz.png HTTP/1.1
      1 GET /images/stories/raith/wohnraum.jpg HTTP/1.1
      1 GET /images/stories/raith/wohnung_1_web.jpg HTTP/1.1
      1 GET /images/stories/raith/wohnung_2_web.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_01.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_02.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_03.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_04.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_05.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_06.jpg HTTP/1.1
      1 GET /images/stories/slideshow/almhuette_raith_07.jpg HTTP/1.1
      1 GET /index.php?option=com_phocagallery&view=category&id=2:winterfotos&Itemid=53 HTTP/1.1
      1 GET /index.php?option=com_phocagallery&view=category&id=4:ferienwohnung2&Itemid=53 HTTP/1.1
      1 GET /media/system/css/modal.css HTTP/1.1
      1 GET /media/system/js/caption.js HTTP/1.1
      1 GET /media/system/js/modal.js HTTP/1.1
      1 GET /media/system/js/mootools.js HTTP/1.1
      1 GET /modules/mod_bowslideshow/tmpl/css/bowslideshow.css HTTP/1.1
      1 GET /modules/mod_bowslideshow/tmpl/images/image_shadow.png HTTP/1.1
      1 GET /modules/mod_bowslideshow/tmpl/js/sliderman.1.3.0.js HTTP/1.1
      1 GET /templates/jp_hotel/css/layout.css HTTP/1.1
      1 GET /templates/jp_hotel/css/menu.css HTTP/1.1
      1 GET /templates/jp_hotel/css/suckerfish.css HTTP/1.1
      1 GET /templates/jp_hotel/css/template.css HTTP/1.1
      1 GET /templates/jp_hotel/images/content_heading.gif HTTP/1.1
      1 GET /templates/jp_hotel/images/logo.jpg HTTP/1.1
      1 GET /templates/jp_hotel/images/module_heading.gif HTTP/1.1
      1 GET /templates/jp_hotel/js/moomenu.js HTTP/1.1
      2 GET /favicon.ico HTTP/1.1
      2 GET /index.php?option=com_content&view=article&id=50&Itemid=56 HTTP/1.1
      2 GET /index.php?option=com_phocagallery&view=category&id=1&Itemid=53 HTTP/1.1
      3 GET / HTTP/1.1
      3 GET /index.php?option=com_content&view=article&id=46&Itemid=54 HTTP/1.1
      3 GET /index.php?option=com_content&view=article&id=49&Itemid=55 HTTP/1.1
     22 GET /templates/_system/css/general.css HTTP/1.1
student@attackdefense:~$
```

----

###### Reference

- [Dataset](http://www.almhuette-raith.at/apache-log/access.log)
- [explainshell](https://explainshell.com/)

----

EOF