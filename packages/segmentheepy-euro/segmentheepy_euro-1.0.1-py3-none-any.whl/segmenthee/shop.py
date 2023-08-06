from typing import Dict, List
from segmenthee.cart_api import *
from datetime import datetime as dt
import json
import re
from urllib.parse import urlparse, parse_qs, unquote


CATEGORY_MAP: Dict[str, int] = {
    '/haztartasi-nagygepek': 0,
    '/haztartasi-nagygepek/mosogepek': 0,
    '/haztartasi-nagygepek/mosogepek/eloltoltos-mosogep': 0,
    '/haztartasi-nagygepek/mosogepek/felultoltos-mosogep': 0,
    '/haztartasi-nagygepek/mosogepek/moso-es-szaritogep': 0,
    '/haztartasi-nagygepek/mosogepek/beepitheto-mosogepek': 0,
    '/haztartasi-nagygepek/mosogepek/moso-es-szaritogep-tartozekok': 0,
    '/haztartasi-nagygepek/szaritogepek': 0,
    '/haztartasi-nagygepek/szaritogepek/hoszivattyus-szaritogep': 0,
    '/haztartasi-nagygepek/szaritogepek/kondenzacios-szaritogep': 0,
    '/haztartasi-nagygepek/mosogatogepek': 0,
    '/haztartasi-nagygepek/mosogatogepek/normal-mosogatogep': 0,
    '/haztartasi-nagygepek/mosogatogepek/keskeny-mosogatogep': 0,
    '/haztartasi-nagygepek/mosogatogepek/asztali-mosogatogep': 0,
    '/haztartasi-nagygepek/hutoszekrenyek': 0,
    '/haztartasi-nagygepek/hutoszekrenyek/alulfagyasztos-kombinalt-hutoszekreny': 0,
    '/haztartasi-nagygepek/hutoszekrenyek/felulfagyasztos-kombinalt-hutoszekreny': 0,
    '/haztartasi-nagygepek/hutoszekrenyek/side-by-side-hutoszekreny': 0,
    '/haztartasi-nagygepek/hutoszekrenyek/egyajtos-hutoszekreny': 0,
    '/haztartasi-nagygepek/hutoszekrenyek/borhuto': 0,
    '/haztartasi-nagygepek/fagyasztok': 0,
    '/haztartasi-nagygepek/fagyasztok/fagyasztoszekreny': 0,
    '/haztartasi-nagygepek/fagyasztok/fagyasztolada': 0,
    '/haztartasi-nagygepek/tuzhelyek': 0,
    '/haztartasi-nagygepek/tuzhelyek/kombinalt-tuzhely': 0,
    '/haztartasi-nagygepek/tuzhelyek/villanytuzhely': 0,
    '/haztartasi-nagygepek/tuzhelyek/gaztuzhely': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/fozolapok': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/fozolapok/beepitheto-keramia-fozolap': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/fozolapok/beepitheto-dominolap': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/fozolapok/beepitheto-indukcios-fozolap': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/fozolapok/beepitheto-gaz-fozolap': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-suto': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mikrohullamu-suto': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/sziget-elszivo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/kurtobe-epitheto-paraelszivo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/teleszkopos-paraelszivo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/fali-paraelszivo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/hagyomanyos-paraelszivo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/paraelszivok/elszivo-tartozek': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mosogatogep': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mosogatogep/beepitheto-elolvezerelt-mosogatogep': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mosogatogep/beepitheto-integralt-mosogatogep': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mosogep': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-mosogep/beepitheto-moso-szaritogep': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-hutoszekreny': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-hutoszekreny/beepitheto-borhuto': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-hutoszekreny/beepitheto-kombinalt-hutoszekreny': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-hutoszekreny/beepitheto-egyajtos-hutoszekreny': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-fagyasztoszekreny': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-kavefozo': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/mini-konyha': 0,
    '/haztartasi-nagygepek/beepitheto-keszulekek/beepitheto-keszulek-tartozek': 0,
    '/telefon-tablet-okosora': 1,
    '/telefon-tablet-okosora/telefonok': 1,
    '/telefon-tablet-okosora/telefonok/okostelefonok': 1,
    '/telefon-tablet-okosora/telefonok/nyomogombos-mobiltelefonok': 1,
    '/telefon-tablet-okosora/telefonok/dect-es-vezetekes-telefonok': 1,
    '/telefon-tablet-okosora/okosora-karkoto-kiegeszitok': 1,
    '/telefon-tablet-okosora/okosora-karkoto-kiegeszitok/okosorak': 1,
    '/telefon-tablet-okosora/okosora-karkoto-kiegeszitok/okoskarkotok': 1,
    '/telefon-tablet-okosora/okosora-karkoto-kiegeszitok/okosora-okoskarkoto-kiegeszitok': 1,
    '/telefon-tablet-okosora/tablagepek-es-e-book-olvasok': 1,
    '/telefon-tablet-okosora/tablagepek-es-e-book-olvasok/tablet': 1,
    '/telefon-tablet-okosora/tablagepek-es-e-book-olvasok/e-book-olvaso': 1,
    '/telefon-tablet-okosora/kiegeszitok': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/vezetekes-toltes': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/vezetek-nelkuli-toltes': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/mobiltelefon-tok': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/mobiltelefon-folia': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/autos-tartok': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/autos-toltes': 1,
    '/telefon-tablet-okosora/kiegeszitok/mobiltelefon-kiegeszito/selfie-bot': 1,
    '/telefon-tablet-okosora/kiegeszitok/tablet-kiegeszitok': 1,
    '/telefon-tablet-okosora/kiegeszitok/tablet-kiegeszitok/tablet-es-e-book-olvaso-tok': 1,
    '/telefon-tablet-okosora/kiegeszitok/tablet-kiegeszitok/tablet-billentyuzet': 1,
    '/telefon-tablet-okosora/kiegeszitok/tablet-kiegeszitok/tablet-folia': 1,
    '/telefon-tablet-okosora/kiegeszitok/tablet-kiegeszitok/autos-kiegeszitok-tartok': 1,
    '/tv-audio-jatekkonzol': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/televizio-led-tv-oled-tv-qled-tv': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/taviranyitok-billentyuzetek': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/taviranyitok-billentyuzetek/taviranyitok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/fali-konzolok-allvanyok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/fali-konzolok-allvanyok/fali-konzolok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/fali-konzolok-allvanyok/allvanyok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/antennak-es-belteri-egysegek': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/antennak-es-belteri-egysegek/mindigtv-premium': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/antennak-es-belteri-egysegek/belteri-egysegek': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/antennak-es-belteri-egysegek/antennak': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/antennak-es-belteri-egysegek/antenna-csatlakozok-szerelekek': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/mediabox-dvd-bd-lejatszok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/mediabox-dvd-bd-lejatszok/dvd-bd-lejatszok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/mediabox-dvd-bd-lejatszok/dvd-bd-lejatszok/asztali-blu-ray-lejatszofelvevo': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/mediabox-dvd-bd-lejatszok/mediabokszok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/projektorok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/projektorok/projektor': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/projektorok/vasznak-allvanyok-fali-tartok': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/projektorok/vasznak-allvanyok-fali-tartok/vetitovaszon': 2,
    '/tv-audio-jatekkonzol/televiziok-es-tartozekok/audio-video-kabel-kiegeszito': 2,
    '/tv-audio-jatekkonzol/audio': 2,
    '/tv-audio-jatekkonzol/audio/hangprojektorok-hazimozik': 2,
    '/tv-audio-jatekkonzol/audio/hangprojektorok-hazimozik/hangprojektor': 2,
    '/tv-audio-jatekkonzol/audio/hangprojektorok-hazimozik/kompakt-hazimozi': 2,
    '/tv-audio-jatekkonzol/audio/hangprojektorok-hazimozik/hazimozi-komponensek': 2,
    '/tv-audio-jatekkonzol/audio/hangprojektorok-hazimozik/hazimozi-komponensek/hazimozi-erosito': 2,
    '/tv-audio-jatekkonzol/audio/otthoni-hifi': 2,
    '/tv-audio-jatekkonzol/audio/otthoni-hifi/hifi-rendszerek': 2,
    '/tv-audio-jatekkonzol/audio/otthoni-hifi/hifi-rendszerek/mikro-es-minihifi-rendszer': 2,
    '/tv-audio-jatekkonzol/audio/otthoni-hifi/hifi-komponensek-hangfalak': 2,
    '/tv-audio-jatekkonzol/audio/otthoni-hifi/lemezjatszo': 2,
    '/tv-audio-jatekkonzol/audio/bluetooth-hangszorok': 2,
    '/tv-audio-jatekkonzol/audio/bluetooth-hangszorok/bluetooth-audio-rendszer': 2,
    '/tv-audio-jatekkonzol/audio/party-hangszorok': 2,
    '/tv-audio-jatekkonzol/audio/autohifi': 2,
    '/tv-audio-jatekkonzol/audio/autohifi/autohangszorok-hangladak': 2,
    '/tv-audio-jatekkonzol/audio/autohifi/autohifi-fejegysegek': 2,
    '/tv-audio-jatekkonzol/audio/autohifi/autohifi-csatlakozok-tartozekok': 2,
    '/tv-audio-jatekkonzol/audio/autohifi/autohifi-csatlakozok-tartozekok/autohifi-erosito': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/media-lejatszo': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/cd-lejatszok': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/radio': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/radio/radio': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/radio/ebresztooras-radio': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/radio/zsebradio': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/radio/taskaradio': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/diktafon': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/mikrofon-karaoke': 2,
    '/tv-audio-jatekkonzol/audio/hordozhato-audio-termekek/ado-vevo-transzmitter': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato/vezetekes-fejhallgato': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato/vezetek-nelkuli-fejhallgato': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato/bluetooth-fejhallgato': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato/vezetekes-fulhallgato': 2,
    '/tv-audio-jatekkonzol/audio/fej-fulhallgato/bluetooth-fulhallgato': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzolok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzolok/nintendo-konzolok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzolok/nintendo-konzolok/nintendo': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzolok/xbox-konzolok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzolok/playstation-konzolok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-live-kartya': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-live-kartya/xbox': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-live-kartya/xbox/xbox-live': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-live-kartya/playstation': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-kontroller': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-kontroller/xbox': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-kontroller/playstation': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-kontroller/nintendo': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-kontroller/egyeb': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/playstation-jatekok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/playstation-jatekok/playstation-jatek': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/nintendo-jatekok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/nintendo-jatekok/nintendo-jatek': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/xbox-jatekok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/xbox-jatekok/xbox-360-jatekok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-szoftverek/xbox-jatekok/xbox-one-jatek': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok/tolto-toltoallomas': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok/kabel': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok/kormany-joystick': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok/headset': 2,
    '/tv-audio-jatekkonzol/jatekkonzolok/jatekkonzol-egyeb-kiegeszitok/egyeb-konzol-kiegeszito': 2,
    '/haztartasi-kisgepek': 3,
    '/haztartasi-kisgepek/kavezas': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/automata-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/nespresso-kapszulas-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/dolce-gusto-kapszulas-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/cremesso-kapszulas-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/senseo-kapszulas-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/tchibo-kapszulas-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/presszo-kavefozo-15-bar': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/kotyogos-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/filteres-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozogepek/presszo-kavefozo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozo-es-kavezas-kiegeszitok': 3,
    '/haztartasi-kisgepek/kavezas/kavefozo-es-kavezas-kiegeszitok/kavedaralo': 3,
    '/haztartasi-kisgepek/kavezas/kavefozo-es-kavezas-kiegeszitok/tejhabosito': 3,
    '/haztartasi-kisgepek/kavezas/kavefozo-es-kavezas-kiegeszitok/kavezas-kiegeszito': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/ndg-kapszula': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/senseo-kaveparna': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/nespresso-kapszula': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/cremesso-kapszula': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/tchibo-kapszula': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/szemes-kave': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/instant-kave': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/orolt-kave': 3,
    '/haztartasi-kisgepek/kavezas/kavek-kapszulak-teak/filteres-teak': 3,
    '/haztartasi-kisgepek/padloapolas': 3,
    '/haztartasi-kisgepek/padloapolas/porzsakos-porszivo': 3,
    '/haztartasi-kisgepek/padloapolas/porzsak-nelkuli-porszivo': 3,
    '/haztartasi-kisgepek/padloapolas/robotporszivo': 3,
    '/haztartasi-kisgepek/padloapolas/kezi-porszivo': 3,
    '/haztartasi-kisgepek/padloapolas/morzsaporszivo': 3,
    '/haztartasi-kisgepek/padloapolas/takaritogep': 3,
    '/haztartasi-kisgepek/padloapolas/goztisztito': 3,
    '/haztartasi-kisgepek/padloapolas/padloapolas-kiegeszitok': 3,
    '/haztartasi-kisgepek/padloapolas/padloapolas-kiegeszitok/porzsak': 3,
    '/haztartasi-kisgepek/padloapolas/padloapolas-kiegeszitok/porszivo-tartozek': 3,
    '/haztartasi-kisgepek/padloapolas/padloapolas-kiegeszitok/porszivo-akkumulator': 3,
    '/haztartasi-kisgepek/etel-elokeszites': 3,
    '/haztartasi-kisgepek/etel-elokeszites/aprito': 3,
    '/haztartasi-kisgepek/etel-elokeszites/botmixer': 3,
    '/haztartasi-kisgepek/etel-elokeszites/kezimixer': 3,
    '/haztartasi-kisgepek/etel-elokeszites/etelparolok': 3,
    '/haztartasi-kisgepek/etel-elokeszites/turmixgep': 3,
    '/haztartasi-kisgepek/etel-elokeszites/mix-go': 3,
    '/haztartasi-kisgepek/etel-elokeszites/talas-mixer': 3,
    '/haztartasi-kisgepek/etel-elokeszites/robotgep': 3,
    '/haztartasi-kisgepek/etel-elokeszites/robotgep/robotgep-tartozek': 3,
    '/haztartasi-kisgepek/etel-elokeszites/robotgep/robotgep': 3,
    '/haztartasi-kisgepek/etel-elokeszites/food-proceszor': 3,
    '/haztartasi-kisgepek/etel-elokeszites/aszalok': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vizforralo': 3,
    '/haztartasi-kisgepek/etel-elokeszites/husdaralo': 3,
    '/haztartasi-kisgepek/etel-elokeszites/salatakeszitok': 3,
    '/haztartasi-kisgepek/etel-elokeszites/gyumolcsfacsaras': 3,
    '/haztartasi-kisgepek/etel-elokeszites/gyumolcsfacsaras/gyumolcspres': 3,
    '/haztartasi-kisgepek/etel-elokeszites/gyumolcsfacsaras/citruspres': 3,
    '/haztartasi-kisgepek/etel-elokeszites/gyumolcsfacsaras/gyumolcscentrifuga': 3,
    '/haztartasi-kisgepek/etel-elokeszites/elektromos-kesek': 3,
    '/haztartasi-kisgepek/etel-elokeszites/szeletelok': 3,
    '/haztartasi-kisgepek/etel-elokeszites/szeletelok/szeletelo': 3,
    '/haztartasi-kisgepek/etel-elokeszites/so-es-borsorlo': 3,
    '/haztartasi-kisgepek/etel-elokeszites/konyhamerleg': 3,
    '/haztartasi-kisgepek/etel-elokeszites/jegkockakeszito': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vizszuro-kancso': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vizszuro-kancso/vizszuro-tartozek': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vakuum-technika': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vakuum-technika/vakuumfoliazo': 3,
    '/haztartasi-kisgepek/etel-elokeszites/vakuum-technika/vakuumfolia': 3,
    '/haztartasi-kisgepek/etel-elokeszites/etel-elokeszites-tartozek': 3,
    '/haztartasi-kisgepek/szepsegapolas': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/ferfi-borotva': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/ferfi-borotva/borotva-tartozek': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/ferfi-borotva/borotva': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/orrszorvago': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/testszorvago': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/multigroom': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/szakallvago': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/hajvago': 3,
    '/haztartasi-kisgepek/szepsegapolas/ferfi-szepsegapolas/szepsegapolas-tartozek': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/hajszarito': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/hajvasalo': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/kupvas': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/hajsutovas': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/hajformazo': 3,
    '/haztartasi-kisgepek/szepsegapolas/hajapolas/hajapolas-tartozek-kiegeszito': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites/epilator': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites/ipl-szortelenito': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites/gyantazo': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites/noi-borotva': 3,
    '/haztartasi-kisgepek/szepsegapolas/noi-szortelenites/szepsegapolas-tartozek': 3,
    '/haztartasi-kisgepek/sutes-fozes': 3,
    '/haztartasi-kisgepek/sutes-fozes/grillsuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/grillsuto/asztali-grill': 3,
    '/haztartasi-kisgepek/sutes-fozes/grillsuto/kontakt-grill': 3,
    '/haztartasi-kisgepek/sutes-fozes/grillsuto/grill-tartozek': 3,
    '/haztartasi-kisgepek/sutes-fozes/elektromos-fozoedeny': 3,
    '/haztartasi-kisgepek/sutes-fozes/elektromos-fozolap': 3,
    '/haztartasi-kisgepek/sutes-fozes/kenyersuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/minisuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/olajsuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/kenyerpirito': 3,
    '/haztartasi-kisgepek/sutes-fozes/szendvicssuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/party-termekek': 3,
    '/haztartasi-kisgepek/sutes-fozes/party-termekek/palacsintasuto': 3,
    '/haztartasi-kisgepek/sutes-fozes/party-termekek/kukoricapattogtato': 3,
    '/haztartasi-kisgepek/sutes-fozes/joghurtkeszito': 3,
    '/haztartasi-kisgepek/sutes-fozes/fagylaltgep': 3,
    '/haztartasi-kisgepek/sutes-fozes/gofrisuto': 3,
    '/haztartasi-kisgepek/mikrohullamu-sutok': 3,
    '/haztartasi-kisgepek/mikrohullamu-sutok/mikrohullamu-sutok': 3,
    '/haztartasi-kisgepek/mikrohullamu-sutok/mikro-tartozek': 3,
    '/haztartasi-kisgepek/szajapolas': 3,
    '/haztartasi-kisgepek/szajapolas/elektromos-fogkefe': 3,
    '/haztartasi-kisgepek/szajapolas/szajzuhany': 3,
    '/haztartasi-kisgepek/szajapolas/szajcenter': 3,
    '/haztartasi-kisgepek/szajapolas/elektromos-fogkefe-fej': 3,
    '/haztartasi-kisgepek/szajapolas/szajzuhany-fej': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/agymelegito-melegitoparna': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/inhalator': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/alkoholszonda': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/ekg': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/infralampa': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/arcapolas': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/kez-es-labapolas': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/digitalis-lazmero': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/masszirozo': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/szemelymerleg': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/vercukorszint-mero': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/vernyomasmero': 3,
    '/haztartasi-kisgepek/egeszsegmegorzes/veroxigenmero': 3,
    '/haztartasi-kisgepek/ruhaapolas': 3,
    '/haztartasi-kisgepek/ruhaapolas/vasalo': 3,
    '/haztartasi-kisgepek/ruhaapolas/gozallomas': 3,
    '/haztartasi-kisgepek/ruhaapolas/kezigozolo': 3,
    '/haztartasi-kisgepek/ruhaapolas/allvanyos-gozolo': 3,
    '/haztartasi-kisgepek/ruhaapolas/textilborotva': 3,
    '/haztartasi-kisgepek/ruhaapolas/varrogep': 3,
    '/haztartasi-kisgepek/ruhaapolas/vasalas-kiegeszitok': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/elektromos-kandallo': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/elektromos-konvektor-radiator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/fali-hosugarzo': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/hosugarzo': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/ventilatoros-hosugarzo': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/keramia-hosugarzo': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/olajradiator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/futes-termekek/elektromos-vizmelegitok': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/alloventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/asztali-ventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/oszlopventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/mennyezeti-ventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/padlo-ventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/leghuto': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/mobil-klima': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/hutotaska': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/szunyogriaszto': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/usb-ventilator': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/hutes-termekek/klima-tartozek': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/parasito-paratlanito': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/parasito-paratlanito/legtisztito': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/parasito-paratlanito/paratlanito': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/parasito-paratlanito/parasito': 3,
    '/haztartasi-kisgepek/levego-tisztitok-parasitok-paratlanitok/parasito-paratlanito/levego-tartozek': 3,
    '/haztartasi-kisgepek/szodagepek': 3,
    '/haztartasi-kisgepek/szodagepek/szodagep': 3,
    '/haztartasi-kisgepek/szodagepek/szorp': 3,
    '/haztartasi-kisgepek/szodagepek/szodagep-palack': 3,
    '/szamitastechnika-gamer': 4,
    '/szamitastechnika-gamer/szamitastechnika': 4,
    '/szamitastechnika-gamer/szamitastechnika/notebook-szamitogep': 4,
    '/szamitastechnika-gamer/szamitastechnika/notebook-szamitogep/notebook': 4,
    '/szamitastechnika-gamer/szamitastechnika/notebook-szamitogep/gamer-notebook': 4,
    '/szamitastechnika-gamer/szamitastechnika/notebook-szamitogep/asztali-pc': 4,
    '/szamitastechnika-gamer/szamitastechnika/notebook-szamitogep/multifunkcios-pc-all-in-one': 4,
    '/szamitastechnika-gamer/szamitastechnika/monitor-projektor': 4,
    '/szamitastechnika-gamer/szamitastechnika/monitor-projektor/monitor': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/multifunkcios-nyomtatok': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/lezernyomtato': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/tintasugaras-nyomtato': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/szkenner-fax-egyeb-nyomtatok': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/szkenner-fax-egyeb-nyomtatok/nyomtato': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/nyomtato-toner': 4,
    '/szamitastechnika-gamer/szamitastechnika/nyomtatok/nyomtato-tintapatron': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/operacios-rendszer-irodai-programok': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/virusirtok-vedelmi-programok': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/belso-hddssd': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/szamitogephaz': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/egyeb-periferia': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/tapegyseg': 4,
    '/szamitastechnika-gamer/szamitastechnika/szoftver-reszegyseg/processzor-es-videokartya-hutok': 4,
    '/szamitastechnika-gamer/periferiak': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/eger-egerpad': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/eger-billentyuzet-szettek': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/webkamera': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/szamitogepes-hangfal': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/headset': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/billentyuzet': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/irodatechnika-kiegeszito': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/notebook-huto': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/notebook-huto/notebook-kiegeszito': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/kulso-hddssd': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/kulso-hddssd/kulso-merevlemez': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/szamitastechnikai-kiegeszitok': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/szamitastechnikai-kiegeszitok/optikai-meghajto': 4,
    '/szamitastechnika-gamer/periferiak/office-kiegeszitok/streaming-eszkozok': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/billentyuzet': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/eger-billentyuzet-szett': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/egerek-egerpadok': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/gamer-headset': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/gamer-hangfal': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/jatekvezerlo': 4,
    '/szamitastechnika-gamer/periferiak/gamer-kiegeszitok/gamer-butor': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/irhato-cddvdblue-ray-lemez': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/pendrive': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/kulso-akkumulator': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/memoriakartya': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/memoriakartya/kartyaolvaso': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/memoria-powerbank/notebook-adapter-es-tolto': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/notebook-taska-hatizsak': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/notebook-taska-hatizsak/notebook-hatizsak': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/notebook-taska-hatizsak/notebook-taska': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/notebook-taska-hatizsak/notebook-tok': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/elemek-es-toltok': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/szamitogep-pc-kiegeszito': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/szamitogep-pc-kiegeszito/forgoszek': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/kabel': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/kabel/szamitastechnikai-kabelek': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/kabel/halozati-elosztok-hosszabbitok': 4,
    '/szamitastechnika-gamer/notebook-es-szamitastechnikai-kiegeszitok/kiegeszito-tartozek/izzo': 4,
    '/szamitastechnika-gamer/otthon-automatizalas': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/halozat': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/halozat/routerek': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/halozat/switchek': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/halozat/usb-stickek': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/halozat/jelerosito-jeltovabbito': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/wifi-s-kamera': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/kamera-szettek': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/beengedes-vezerlok': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/beengedes-vezerlok/vezetek-nelkuli-csengo': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/riaszto-rendszerek-es-kiegeszitok': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/okos-vilagitastechnika': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/okos-konnektorok-elosztok': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/vezerlo-rendszerek-hub': 4,
    '/szamitastechnika-gamer/otthon-automatizalas/okosotthon-biztonsagtechnika/okosotthon-erzekelok': 4,
    '/foto-video-optika': 5,
    '/foto-video-optika/dron': 5,
    '/foto-video-optika/foto': 5,
    '/foto-video-optika/foto/kompakt-fenykepezogep': 5,
    '/foto-video-optika/kamera': 5,
    '/foto-video-optika/kamera/menetrogzito-kamera': 5,
    '/foto-video-optika/kamera/akciokamera': 5,
    '/foto-video-optika/kamera/vadkamera': 5,
    '/foto-video-optika/foto-video-kiegeszitok': 5,
    '/foto-video-optika/foto-video-kiegeszitok/fenykepezogep-objektiv': 5,
    '/foto-video-optika/foto-video-kiegeszitok/fenykepezogep-allvany': 5,
    '/foto-video-optika/foto-video-kiegeszitok/fenykepezogep-tok-taska': 5,
    '/foto-video-optika/foto-video-kiegeszitok/akkumulator': 5,
    '/foto-video-optika/foto-video-kiegeszitok/digitalis-fotokeret': 5,
    '/foto-video-optika/foto-video-kiegeszitok/foto-es-video-tartozek': 5,
    '/foto-video-optika/termeszet-megfigyeles': 5,
    '/foto-video-optika/termeszet-megfigyeles/binokularok': 5,
    '/foto-video-optika/termeszet-megfigyeles/tavcsovek': 5,
    '/foto-video-optika/termeszet-megfigyeles/tavcso-allvanyok-es-kiegeszitok': 5,
    '/foto-video-optika/termeszet-megfigyeles/mikroszkopok': 5,
    '/foto-video-optika/termeszet-megfigyeles/vadasz-tavcsovek': 5,
    '/kert-barkacs-autofelszereles': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok/furogepek-utvefurok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok/furo-csavarozok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok/furo-csavarozok/akkus-furo-csavarozo': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok/furo-csavarozok/akkus-csavarozo': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/furok/furokalapacsok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/csiszolo-gepek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/csiszolo-gepek/sarokcsiszolok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/csiszolo-gepek/csiszolok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/csiszolo-gepek/csiszolok/polirozogep': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/vagoeszkozok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/gyaluk-marogepek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/holegfuvok-festekszorok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/geptartozekok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/geptartozekok/furo-csavarozo-tartozek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/geptartozekok/csiszolo-tartozekok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/geptartozekok/gyalu-maro-tartozekok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/geptartozekok/multiszerszam-tartozekok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/akkumulatorok-aramfejlesztok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/akkumulatorok-aramfejlesztok/akkumulatorok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/akkumulatorok-aramfejlesztok/akkumulatorok/akkumulator': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/akkumulatorok-aramfejlesztok/akkutoltok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek/asztali-korfuresz': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek/gervago-furesz': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek/dekopir-furesz': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek/szablyafuresz': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/fureszgepek/kezi-korfuresz': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/kompresszorok': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/kompresszorok/kompresszor': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/kompresszorok/kompresszor-tartozek': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/multiszerszam': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/multiszerszam/multifunkcios-gep': 6,
    '/kert-barkacs-autofelszereles/barkacsgepek/forrasztasragasztas-rogzites': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/keziszerszamok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/keziszerszamok/keziszerszamok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/keziszerszamok/keziszerszam-keszletek': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/szerszamtarolas': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/szerszamtarolas/muanyag-szerszamosladak': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/szerszamtarolas/muanyag-rendszerezok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/szerszamtarolas/fem-szerszamtaskak-ladak': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/szerszamtarolas/szerszamtarolo-taskak-ovek': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok/kezi-meroeszkoz': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok/meroszalagok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok/lezeres-meroeszkoz': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok/vizmertekek-szintezok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/meroeszkozok/multimeterek': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/munkavedelmi-eszkozok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/munkavedelmi-eszkozok/vedoszemuvegek': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/munkavedelmi-eszkozok/fulvedok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/munkavedelmi-eszkozok/kezvedok': 6,
    '/kert-barkacs-autofelszereles/szerszamok-tarolas-meres/festoszerszam': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/magasnyomasu-mosok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/magasnyomasu-mosok/magasnyomasu-mosok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/magasnyomasu-mosok/magasnyomasu-moso-tartozekok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/ipari-porszivok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/ipari-porszivok/porszivok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/ipari-porszivok/porszivo-tartozekok': 6,
    '/kert-barkacs-autofelszereles/tisztito-gepek/ipari-porszivok/hamu-porszivo': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-funyirok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-fukaszak': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-szegelyvagok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-gyepszelloztetok-talajlazitok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-sovenyvago': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-lancfureszek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-lombszivo-lombfuvok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-rotacioskapak': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-komposztapritok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/elektromos-kerti-gepek/elektromos-ronkhasitok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-funyiro': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-szegelyvagok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-gyepszellozteto-talajlazitok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-funyiro-ollok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-sovenyvagok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-robotfunyirok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-lancfureszek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/akkumulatoros-kerti-gepek/akkumulatoros-lombfuvok-szivok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-funyirok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-fukaszak': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-lancfuresz': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-gyepszellozteto-talajlazitok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-lombszivolombfuvo': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/benzinmotoros-kerti-gepek/benzinmotoros-rotacioskapa': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/kerti-gep-tartozekok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/kerti-gep-tartozekok/funyiro-tartozekok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/kerti-gep-tartozekok/lancfuresz-tartozekok': 6,
    '/kert-barkacs-autofelszereles/kerti-gepek/kerti-gep-tartozekok/munkavedelmi-eszkozok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-keziszerszamok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-keziszerszamok/kertesz-szerszamok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-keziszerszamok/kertesz-szerszamok/tarolo-gyujto': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-keziszerszamok/kis-kerti-szerszamok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-ollok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-ollok/metszoollok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-ollok/sovenyvago-ollok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-ollok/agvago-ollok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kerti-ollok/funyiro-ollok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/balta-fejsze-kesek': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/fureszek': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kezi-szorok-szorokocsik': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kezi-funyirok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/permetezo-eszkozok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/permetezo-eszkozok/kezi-permetezok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/permetezo-eszkozok/hati-permetezok': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/agyaskeretek': 6,
    '/kert-barkacs-autofelszereles/kerti-szerszamok/kesztyuk': 6,
    '/kert-barkacs-autofelszereles/viztechnika': 6,
    '/kert-barkacs-autofelszereles/viztechnika/tomlok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/tomlok/tomloszerelvenyek': 6,
    '/kert-barkacs-autofelszereles/viztechnika/tomlok/kerti-tomlok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/tomlok/tomlokocsik-dobok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/tomlok/locsolok-ontozok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/ontozes': 6,
    '/kert-barkacs-autofelszereles/viztechnika/ontozes/esoztetok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/ontozes/sullyesztett-esoztetok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/ontozes/csepegteto-ontozes': 6,
    '/kert-barkacs-autofelszereles/viztechnika/ontozes/ontozes-vezerles': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/merulo-szivattyu': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/ontozo-szivattyu': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/hazi-vizellato': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/melykutszivattyu': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/benzinmotoros-szivattyuk': 6,
    '/kert-barkacs-autofelszereles/viztechnika/szivattyuk-vizellatok/szivattyu-tartozek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/medencek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/medencek/medencek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/medencek/medence-tartozekok': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/medencek/gyerek-medencek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/faszenes-grillek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/gazgrillek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/pizzakemencek': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/pizzakemence-kiegeszito': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/tuzgyujto-eszkozok': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/sutes-elokeszites': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/grill-bbq/tisztitas-karbantartas': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/kerti-butorok': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/kerti-butorok/kerti-butorok': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/kerti-butorok/butor-kiegeszitok': 6,
    '/kert-barkacs-autofelszereles/grill-medence-kerti-butor/rovar-kisallat-riasztok': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek/apolas': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek/karbantartas': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek/izzok-es-biztositekok': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek/autoszonyegek-huzatok': 6,
    '/kert-barkacs-autofelszereles/jarmuvek-es-kiegeszitok/auto-apolas-tartozek/autos-tartozekok': 6,
    '/kert-barkacs-autofelszereles/navigacio': 6,
    '/kert-barkacs-autofelszereles/navigacio/navigacios-keszulek-terkeppel': 6,
    '/kert-barkacs-autofelszereles/navigacio/navigacios-kiegeszitok': 6,
    '/jatek-sport-szabadido': 7,
    '/jatek-sport-szabadido/szabadido-sport': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/haspadok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/taposogepek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/evezogepek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/fekvotamasz-keret-haskerek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/fitnesz-felszerelesek-regeneracios-eszkozok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/fitnesz-kesztyuk-ruhazat': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/fitnesz-labdak': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/ugralo-kotelek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/egyensulyozo-eszkozok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kardiogepek-fitness-eszkozok/egyeb-felszerelesek': 7,
    '/jatek-sport-szabadido/szabadido-sport/futopadok': 7,
    '/jatek-sport-szabadido/szabadido-sport/szobabiciklik': 7,
    '/jatek-sport-szabadido/szabadido-sport/sulyzok-kettlebell-egyeb-sulyok': 7,
    '/jatek-sport-szabadido/szabadido-sport/fitnesz-sulyok': 7,
    '/jatek-sport-szabadido/szabadido-sport/gumiszalagok-es-kotelek': 7,
    '/jatek-sport-szabadido/szabadido-sport/joga-szonyegek-es-matracok': 7,
    '/jatek-sport-szabadido/szabadido-sport/joga-felszerelesek': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok/kollagen-termekek': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok/testsuly-kontroll-formulak': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok/aminosavak-bcaa': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok/shakerek-sporteszkozok-kiegeszitok': 7,
    '/jatek-sport-szabadido/szabadido-sport/taplalek-kiegeszitok/etel-snack': 7,
    '/jatek-sport-szabadido/szabadido-sport/vitaminok-es-asvanyi-anyagok': 7,
    '/jatek-sport-szabadido/szabadido-sport/feherjek': 7,
    '/jatek-sport-szabadido/szabadido-sport/szeletek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekparok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekparok/futobicikli': 7,
    '/jatek-sport-szabadido/szabadido-sport/e-bike': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/vilagitas': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/kulacsok-kulacstartok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/pumpak': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/lakatok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/sarvedok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-kiegeszitok/edzes-energizalas': 7,
    '/jatek-sport-szabadido/szabadido-sport/sisak-es-vedo-felszerelesek': 7,
    '/jatek-sport-szabadido/szabadido-sport/csomagtartok-es-gyerekulesek': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-computerek': 7,
    '/jatek-sport-szabadido/szabadido-sport/taskak': 7,
    '/jatek-sport-szabadido/szabadido-sport/kerekpar-es-sportszer-szallitas': 7,
    '/jatek-sport-szabadido/szabadido-sport/karbantartas-tisztitas': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/foci-kapuk': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/ping-pong-utok-es-kiegeszitok': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/kosarlabdak': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/amerikai-focilabdak': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/tollaslabda': 7,
    '/jatek-sport-szabadido/szabadido-sport/labdas-jatekok-sportok/egyeb-labdas-jatekok': 7,
    '/jatek-sport-szabadido/szabadido-sport/foci-labdak-es-pumpak': 7,
    '/jatek-sport-szabadido/szabadido-sport/ping-pong-asztalok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kosarlabda-palankok': 7,
    '/jatek-sport-szabadido/szabadido-sport/turazas-es-kemping': 7,
    '/jatek-sport-szabadido/szabadido-sport/turazas-es-kemping/halozsakok': 7,
    '/jatek-sport-szabadido/szabadido-sport/turazas-es-kemping/tabori-felszerelesek': 7,
    '/jatek-sport-szabadido/szabadido-sport/satrak': 7,
    '/jatek-sport-szabadido/szabadido-sport/turafelszerlelesek-turabotok': 7,
    '/jatek-sport-szabadido/szabadido-sport/turahatizsakok': 7,
    '/jatek-sport-szabadido/szabadido-sport/vizisportok': 7,
    '/jatek-sport-szabadido/szabadido-sport/vizisportok/kajak-csonak': 7,
    '/jatek-sport-szabadido/szabadido-sport/vizisportok/egyeb-vizi-sport-eszkozok': 7,
    '/jatek-sport-szabadido/szabadido-sport/sup': 7,
    '/jatek-sport-szabadido/szabadido-sport/kulteri-sportok': 7,
    '/jatek-sport-szabadido/szabadido-sport/kulteri-sportok/gordeszka': 7,
    '/jatek-sport-szabadido/szabadido-sport/kulteri-sportok/roller': 7,
    '/jatek-sport-szabadido/szabadido-sport/kulteri-sportok/egyeb-kulteri-sportok': 7,
    '/jatek-sport-szabadido/szabadido-sport/e-roller': 7,
    '/jatek-sport-szabadido/szabadido-sport/trambulin': 7,
    '/jatek-sport-szabadido/szabadido-sport/egyeb-sport-kiegeszitok': 7,
    '/jatek-sport-szabadido/szabadido-sport/utazas': 7,
    '/jatek-sport-szabadido/szabadido-sport/utazas/poggyaszmerleg': 7,
    '/jatek-sport-szabadido/szabadido-sport/utazas/utazotaskak': 7,
    '/jatek-sport-szabadido/szabadido-sport/borondok': 7,
    '/jatek-sport-szabadido/szabadido-sport/utazasi-kiegeszitok': 7,
    '/jatek-sport-szabadido/jatek': 7,
    '/jatek-sport-szabadido/jatek/lego': 7,
    '/jatek-sport-szabadido/jatek/lego/architecture': 7,
    '/jatek-sport-szabadido/jatek/lego/art': 7,
    '/jatek-sport-szabadido/jatek/lego/boost': 7,
    '/jatek-sport-szabadido/jatek/lego/city': 7,
    '/jatek-sport-szabadido/jatek/lego/classic': 7,
    '/jatek-sport-szabadido/jatek/lego/creator': 7,
    '/jatek-sport-szabadido/jatek/lego/creator-expert': 7,
    '/jatek-sport-szabadido/jatek/lego/dc-comics-super-heroes': 7,
    '/jatek-sport-szabadido/jatek/lego/disney-princess': 7,
    '/jatek-sport-szabadido/jatek/lego/dots': 7,
    '/jatek-sport-szabadido/jatek/lego/duplo': 7,
    '/jatek-sport-szabadido/jatek/lego/friends': 7,
    '/jatek-sport-szabadido/jatek/lego/harry-potter': 7,
    '/jatek-sport-szabadido/jatek/lego/ideas': 7,
    '/jatek-sport-szabadido/jatek/lego/jurassic-world': 7,
    '/jatek-sport-szabadido/jatek/lego/marvel-super-heroes': 7,
    '/jatek-sport-szabadido/jatek/lego/mickey-friends': 7,
    '/jatek-sport-szabadido/jatek/lego/minecraft': 7,
    '/jatek-sport-szabadido/jatek/lego/minions': 7,
    '/jatek-sport-szabadido/jatek/lego/ninjago': 7,
    '/jatek-sport-szabadido/jatek/lego/speed-champions': 7,
    '/jatek-sport-szabadido/jatek/lego/star-wars': 7,
    '/jatek-sport-szabadido/jatek/lego/super-mario': 7,
    '/jatek-sport-szabadido/jatek/lego/technic': 7,
    '/jatek-sport-szabadido/jatek/lego/disney-pixar': 7,
    '/jatek-sport-szabadido/jatek/lego/avatar': 7,
    '/jatek-sport-szabadido/jatek/lego/icons': 7,
    '/jatek-sport-szabadido/jatek/bebijatekok': 7,
    '/jatek-sport-szabadido/jatek/bebijatekok/huzo-es-tolo-jatekok': 7,
    '/jatek-sport-szabadido/jatek/bebijatekok/furdojatekok': 7,
    '/jatek-sport-szabadido/jatek/baba-csorgok-ragokak': 7,
    '/jatek-sport-szabadido/jatek/funkcios-zenelo-bebijatekok': 7,
    '/jatek-sport-szabadido/jatek/jatszo-es-fejleszto-szonyegek': 7,
    '/jatek-sport-szabadido/jatek/babak-kellekek': 7,
    '/jatek-sport-szabadido/jatek/babak-kellekek/pluss-jatekok': 7,
    '/jatek-sport-szabadido/jatek/babak-kellekek/funkcios-pluss-figurak': 7,
    '/jatek-sport-szabadido/jatek/babak-kellekek/funkcios-interaktiv-babak': 7,
    '/jatek-sport-szabadido/jatek/babak-kellekek/babahaz-bababutor': 7,
    '/jatek-sport-szabadido/jatek/csecsemo-es-hajas-babak': 7,
    '/jatek-sport-szabadido/jatek/divat-babak': 7,
    '/jatek-sport-szabadido/jatek/tarsas-jatekok': 7,
    '/jatek-sport-szabadido/jatek/tarsas-jatekok/kartyajatekok': 7,
    '/jatek-sport-szabadido/jatek/tarsas-jatekok/memoria-jatekok': 7,
    '/jatek-sport-szabadido/jatek/tarsas-jatekok/sakk-es-tablajatekok': 7,
    '/jatek-sport-szabadido/jatek/tarsasjatekok': 7,
    '/jatek-sport-szabadido/jatek/puzzle': 7,
    '/jatek-sport-szabadido/jatek/auto-jarmu': 7,
    '/jatek-sport-szabadido/jatek/auto-jarmu/jatek-munkagepek-es-jarmuvek': 7,
    '/jatek-sport-szabadido/jatek/auto-jarmu/jatekvonatok': 7,
    '/jatek-sport-szabadido/jatek/auto-jarmu/jatek-robotok': 7,
    '/jatek-sport-szabadido/jatek/auto-jarmu/rc-autok': 7,
    '/jatek-sport-szabadido/jatek/jatekautok': 7,
    '/jatek-sport-szabadido/jatek/jatek-helikopterek-repulok-es-hajok': 7,
    '/jatek-sport-szabadido/jatek/autopalya-parkolohaz': 7,
    '/jatek-sport-szabadido/jatek/epito-keszletek': 7,
    '/jatek-sport-szabadido/jatek/epito-keszletek/muanyag-epitok': 7,
    '/jatek-sport-szabadido/jatek/epito-keszletek/fem-epitok': 7,
    '/jatek-sport-szabadido/jatek/epito-keszletek/magneses-epitok': 7,
    '/jatek-sport-szabadido/jatek/epito-keszletek/fa-jatekok': 7,
    '/jatek-sport-szabadido/jatek/jatekfigurak-es-szettek': 7,
    '/jatek-sport-szabadido/jatek/jatekfigurak-es-szettek/jatekfigura': 7,
    '/jatek-sport-szabadido/jatek/jatekfigurak-es-szettek/allatfigurak': 7,
    '/jatek-sport-szabadido/jatek/jatekfigurak-es-szettek/jatekfegyverek-es-keszletek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/smink-szepseg-es-tetovalo-szettek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/rajz-es-festo-keszletek-rajztablak': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/kreativ-szettek-gipszkiontok': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/nyomdak-matricak': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/gyurma-es-gyurmazo-keszletek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/tudomanyos-jatekok': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/konyhai-szettek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/takarito-szettek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/orvosi-szettek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/barkacs-keszletek': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/jelmezek-es-maszkok': 7,
    '/jatek-sport-szabadido/jatek/kreativ-es-keszsegfejlesztok/jatek-hangszerek': 7,
    '/jatek-sport-szabadido/jatek/kulteri-jatekok': 7,
    '/jatek-sport-szabadido/jatek/kulteri-jatekok/jatszosator-es-jatszohazak': 7,
    '/jatek-sport-szabadido/jatek/kulteri-jatekok/ugyessegi-jatekok': 7,
    '/jatek-sport-szabadido/jatek/strandjatekok-uszogumik': 7,
    '/otthon': 8,
    '/otthon/otthoni-termekek': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles/hagyomanyos-edenyek-serpenyok': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles/indukcios-edenyek-serpenyok': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles/hagyomanyos-edenyszettek': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles/indukcios-edenyszettek': 8,
    '/otthon/otthoni-termekek/edenyzet-konyhafelszereles/konyhai-kiegeszitok': 8,
    '/otthon/otthoni-termekek/konyhai-eszkozok': 8,
    '/otthon/otthoni-termekek/konyhai-eszkozok/ollok-kesek': 8,
    '/otthon/otthoni-termekek/konyhai-eszkozok/konyhai-eszkozok': 8,
    '/otthon/otthoni-termekek/konyhai-eszkozok/tarolo-dobozok': 8,
    '/otthon/otthoni-termekek/furdoszobai-eszkozok': 8,
    '/otthon/otthoni-termekek/furdoszobai-eszkozok/furdoszoba-kiegeszitok': 8,
    '/otthon/otthoni-termekek/furdoszobai-eszkozok/zuhanyfejek': 8,
    '/otthon/otthoni-termekek/letrak-emelok': 8,
    '/otthon/otthoni-termekek/elemek-akkumulatorok': 8,
    '/otthon/otthoni-termekek/elemek-akkumulatorok/elemek': 8,
    '/otthon/otthoni-termekek/elemek-akkumulatorok/ujratoltheto-elemek': 8,
    '/otthon/otthoni-termekek/elemek-akkumulatorok/ujratoltheto-elemek/akkumulator-tolto': 8,
    '/otthon/otthoni-termekek/orak-ebresztoorak': 8,
    '/otthon/otthoni-termekek/orak-ebresztoorak/ora': 8,
    '/otthon/otthoni-termekek/idojaras-allomasok': 8,
    '/otthon/otthoni-termekek/kisallattartas': 8,
    '/otthon/otthoni-termekek/kisallattartas/jatekok': 8,
    '/otthon/otthoni-termekek/kisallattartas/butor-es-szallito-eszkozok': 8,
    '/otthon/otthoni-termekek/kisallattartas/butor-es-szallito-eszkozok/kisallat-fekvohelyek': 8,
    '/otthon/otthoni-termekek/kisallattartas/butor-es-szallito-eszkozok/szallito-eszkozok': 8,
    '/otthon/otthoni-termekek/kisallattartas/kozmetikum-es-higienia': 8,
    '/otthon/otthoni-termekek/kisallattartas/kiegeszitok': 8,
    '/otthon/otthoni-termekek/kisallattartas/kiegeszitok/eteto-es-itatotalak': 8,
    '/otthon/otthoni-termekek/kisallattartas/kiegeszitok/nyakorvek-porazok-hamok': 8,
    '/otthon/otthoni-termekek/kisallattartas/kutya-macska-kisallat': 8,
    '/otthon/otthoni-termekek/eledelek': 8,
    '/otthon/otthoni-termekek/eledelek/kutya': 8,
    '/otthon/otthoni-termekek/eledelek/kutya/szaraz-eledel': 8,
    '/otthon/otthoni-termekek/eledelek/kutya/alutasakosalutalcas-termekek': 8,
    '/otthon/otthoni-termekek/eledelek/kutya/konzerv': 8,
    '/otthon/otthoni-termekek/eledelek/kutya/jutalomfalat': 8,
    '/otthon/otthoni-termekek/eledelek/macska': 8,
    '/otthon/otthoni-termekek/eledelek/macska/szaraz-eledel': 8,
    '/otthon/otthoni-termekek/eledelek/macska/alutasakosalutalcas-termekek': 8,
    '/otthon/otthoni-termekek/eledelek/macska/jutalomfalat': 8,
    '/otthon/otthoni-termekek/eledelek/macska/kisallat-almok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/dekoracio': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/party-kellekek': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/covid-maszkok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/covid-gel': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/covid-eszkozok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/iratmegsemmisitok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/kaputelefonok-csengok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/co-fust-erzekelok': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/co-fust-erzekelok/szenmonoxid-erzekelo': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/alkoholos-spray': 8,
    '/otthon/otthoni-termekek/otthoni-kiegeszitok-dekoracio/usb-elosztok': 8,
    '/otthon/butorok': 8,
    '/otthon/butorok/iroda-otthoni-munka': 8,
    '/otthon/butorok/iroda-otthoni-munka/irodaszerek-irodai-eszkozok': 8,
    '/otthon/butorok/gyerekeknek': 8,
    '/otthon/butorok/gyerekeknek/furdoszobai-butorok': 8,
    '/otthon/butorok/gyerekeknek/egyeb-butor-kiegeszitok': 8,
    '/otthon/vilagitas': 8,
    '/otthon/vilagitas/belteri-vilagitas': 8,
    '/otthon/vilagitas/belteri-vilagitas/belteri-fali-mennyezeti-lampak': 8,
    '/otthon/vilagitas/belteri-vilagitas/belteri-asztaliiroasztali-lampa': 8,
    '/otthon/vilagitas/belteri-vilagitas/belteri-raepitheto-beepitheto-lampak': 8,
    '/otthon/vilagitas/kulteri-vilagitas': 8,
    '/otthon/vilagitas/kulteri-vilagitas/kulteri-fali-mennyezeti-lampak': 8,
    '/otthon/vilagitas/kulteri-vilagitas/kulteri-allolampa': 8,
    '/otthon/vilagitas/kulteri-vilagitas/kulteri-reflektorok': 8,
    '/otthon/vilagitas/kulteri-vilagitas/kulteri-napelemes-lampak': 8,
    '/otthon/vilagitas/dekor-vilagitas-lampa': 8,
    '/otthon/vilagitas/dekor-vilagitas-lampa/kerti-dekorlampak': 8,
    '/otthon/vilagitas/dekor-vilagitas-lampa/ejszakai-fenyek': 8,
    '/otthon/vilagitas/dekor-vilagitas-lampa/party-fenyek': 8,
    '/otthon/vilagitas/karacsonyi-fenyfuzer': 8,
    '/otthon/vilagitas/karacsonyi-dekoracio': 8,
    '/otthon/vilagitas/halloween-dekoracio': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas/e27-ledek': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas/e14-ledek': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas/gu10-ledek': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas/halogen-izzok': 8,
    '/otthon/vilagitas/led-es-egyeb-vilagitas/egyeb-izzok': 8,
    '/otthon/vilagitas/elektronika': 8,
    '/otthon/vilagitas/elektronika/dugaljak': 8,
    '/otthon/vilagitas/elektronika/halozati-elosztok': 8,
    '/otthon/vilagitas/elektronika/utazo-adapterek': 8,
    '/otthon/vilagitas/elektronika/hosszabbitok': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/elemlampa': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/camping-lampa': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/kerekpar-lampa': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/fejlampa': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/munkalampa': 8,
    '/otthon/vilagitas/hobbi-es-munkalampak/zseblampa': 8,
    '/baba-mama-drogeria': 9,
    '/baba-mama-drogeria/babamama': 9,
    '/baba-mama-drogeria/babamama/pelenkak-es-bugyik': 9,
    '/baba-mama-drogeria/babamama/baba-nedves-torlokendok': 9,
    '/baba-mama-drogeria/babamama/baba-apolas': 9,
    '/baba-mama-drogeria/babamama/gyerek-es-baba-merlegek': 9,
    '/baba-mama-drogeria/babamama/gyerek-inhalatorok-es-tartozekok': 9,
    '/baba-mama-drogeria/babamama/etetes': 9,
    '/baba-mama-drogeria/babamama/cumisuvegek-cumik-es-tartozekok': 9,
    '/baba-mama-drogeria/babamama/bebior': 9,
    '/baba-mama-drogeria/babamama/bebior/bebior': 9,
    '/baba-mama-drogeria/babamama/bebior/baba-mama': 9,
    '/baba-mama-drogeria/babamama/videos-babaorzo': 9,
    '/baba-mama-drogeria/drogeria': 9,
    '/baba-mama-drogeria/drogeria/mosas-es-ruhaapolas': 9,
    '/baba-mama-drogeria/drogeria/mosas-es-ruhaapolas/szaritok-es-szarito-tartozekok': 9,
    '/baba-mama-drogeria/drogeria/mosas-es-ruhaapolas/szennyestartok': 9,
    '/baba-mama-drogeria/drogeria/mosas-es-ruhaapolas/vallfak': 9,
    '/baba-mama-drogeria/drogeria/mosas-es-ruhaapolas/vasalodeszkak': 9,
    '/baba-mama-drogeria/drogeria/mososzerek-mosogelek': 9,
    '/baba-mama-drogeria/drogeria/mosokapszula': 9,
    '/baba-mama-drogeria/drogeria/oblitoszerek': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/padlotisztito-szerek': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/butortisztito-szerek': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/altalanos-tisztitoszerek': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/szivacsok-kendok-kesztyuk': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/szivacsok-kendok-kesztyuk/lakas-tisztitas': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/vizkooldok': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/wc-illatositok': 9,
    '/baba-mama-drogeria/drogeria/tisztito-fertotlenito-szerek/wc-fertotlenitok-tisztitoszerek': 9,
    '/baba-mama-drogeria/drogeria/legfrissitok': 9,
    '/baba-mama-drogeria/drogeria/takarito-eszkozok': 9,
    '/baba-mama-drogeria/drogeria/takarito-eszkozok/monitor-kepernyo-tisztitok': 9,
    '/baba-mama-drogeria/drogeria/takarito-eszkozok/felmosok': 9,
    '/baba-mama-drogeria/drogeria/mosogatoszer': 9,
    '/baba-mama-drogeria/drogeria/mosogatogep-tablettak-oblitok': 9,
    '/baba-mama-drogeria/drogeria/felulettisztito-szerek': 9,
    '/baba-mama-drogeria/drogeria/felulettisztito-szerek/furdoszobai-tisztito-termekek': 9,
    '/baba-mama-drogeria/drogeria/arcapolas': 9,
    '/baba-mama-drogeria/drogeria/arcapolas/arckremek-tisztitok-sminklemosok': 9,
    '/baba-mama-drogeria/drogeria/arcszesz-borotvalkozasi-termekek': 9,
    '/baba-mama-drogeria/drogeria/hajapolas': 9,
    '/baba-mama-drogeria/drogeria/hajapolas/egyeb-hajapolasi-termekek': 9,
    '/baba-mama-drogeria/drogeria/hajsampon-balzsam': 9,
    '/baba-mama-drogeria/drogeria/borapolas-tisztalkodas': 9,
    '/baba-mama-drogeria/drogeria/borapolas-tisztalkodas/testapolo-es-napvedo-termekek': 9,
    '/baba-mama-drogeria/drogeria/szappanok-tusfurdok-habfurdok': 9,
    '/baba-mama-drogeria/drogeria/dezodorok-es-izzadasgatlok': 9,
    '/baba-mama-drogeria/drogeria/szortelenites': 9,
    '/baba-mama-drogeria/drogeria/szortelenites/szortelenites': 9,
    '/baba-mama-drogeria/drogeria/noi-higienia': 9,
    '/baba-mama-drogeria/drogeria/betetek': 9,
    '/baba-mama-drogeria/drogeria/sminkkeszletek': 9,
    '/baba-mama-drogeria/drogeria/korom-es-labapolas': 9,
    '/baba-mama-drogeria/drogeria/korom-es-labapolas/koromvago-ollo-es-csipesz': 9,
    '/baba-mama-drogeria/drogeria/fogkefe-fogkrem': 9,
    '/baba-mama-drogeria/drogeria/korom-es-sarokreszelok': 9,
    '/baba-mama-drogeria/drogeria/egyeb-szajapolasi-termek': 9,
    '/baba-mama-drogeria/drogeria/szajapolas': 9,
    '/baba-mama-drogeria/drogeria/szajapolas/szajviz': 9
}

CATEGORY_FILTER: Dict[int, int] = {}

PREDEFINED_FILTER: Dict[str, int] = {}


INFO_PAGES: List[str] = [
    '/husegkartya',
    '/heti-ajanlatok',
    '/blog/',
    '/jotallas',
    '/szallitasi-informaciok',
    '/b2b-info',
    '/szerviz',
    '/garancia',
    '/aszf',
    '/adatkezelesi-tajekoztato',
    '/elallas',
    '/husegkartya-adatkezelesi-tajekoztato',
    '/husegkartya-reszveteli-szabalyzat',
    '/befektetoi-kapcsolatok',
    '/vasarloi-tajekoztato',
    '/vasarloi-tajekoztato-adattorlo',
    '/green-bond',
    '/aruhazi-hitel',
    '/gyakori-kerdesek',
    '/ugyfelszolgalat'
]


def get_event(item: Dict) -> SessionBodyEvent:
    if item.get('v') == '2':
        return get_event_ga4(item)

    return get_event_ua(item)


def get_event_ga4(item: Dict) -> SessionBodyEvent:
    hit_time: int = int(item.get('_ts', int(dt.now().timestamp())))
    kwargs: Dict[str, Any] = {
        'time': hit_time,
        'referrer': get_referrer(item.get('dr')),
        'tabcount': int(item.get('s_tc')),
        'tabtype': get_tabtype(item.get('s_tt')),
        'navigation': get_navigation(item.get('s_nt')),
        'redirects': int(item.get('s_rc')),
        'title': item.get('dt'),
        'utm_source': get_utm_source(item),
        'utm_medium': item.get('utm_medium', '')
    }
    event_name: str = item.get('en')

    if event_name == 'scroll':
        return ProductPageScrollEvent(**kwargs)

    if event_name == 'add_to_cart':
        delta_count: int = int(item.get('qty'))
        delta_total: int = round(float(item.get('val')), 2)
        return CartModifyEvent(hit_time, delta_count, delta_total)

    if event_name == 'remove_from_cart':
        delta_count: int = -1 * int(item.get('qty'))
        delta_total: int = -1 * round(float(item.get('val')), 2)
        return CartModifyEvent(hit_time, delta_count, delta_total)

    if event_name == 'coupon_offered':
        return CouponOfferedEvent(hit_time, item.get('el'))

    if event_name == 'coupon_accepted':
        return CouponAcceptedEvent(hit_time, item.get('el'))

    if event_name == 'coupon_rejected':
        return CouponRejectedEvent(hit_time, item.get('el'))

    if event_name == 'begin_checkout':
        return CustomerDataEntryBrowsingEvent(**kwargs)

    if event_name == 'add_shipping_info':
        return ShippingMethodBrowsingEvent(**kwargs)

    if event_name == 'add_payment_info':
        return PaymentMethodBrowsingEvent(**kwargs)

    if event_name == 'confirm_checkout':
        return ConfirmationPageBrowsingEvent(**kwargs)

    if event_name == 'purchase':
        return CheckoutSuccessPageBrowsingEvent(**kwargs)

    if event_name == 'view_cart':
        return CartBrowsingEvent(**kwargs)

    parts = urlparse(get_fixed_url(item.get('dl')))
    if event_name == 'view_item':
        kwargs['product_id'] = item.get('pr1id')
        kwargs['category_id'] = -1
        page_path = parts.path[:parts.path.rfind('/')]
        for path, cat in CATEGORY_MAP.items():
            if page_path == path or path.find(page_path) > -1:
                kwargs['category_id'] = cat
                break

        kwargs['price'] = float_or_none(item.get('pr1pr'))
        return ProductPageBrowsingEvent(**kwargs)

    query: Dict[str, str] = parse_query(parts.query)
    if parts.path == '/':
        return MainPageBrowsingEvent(**kwargs)

    if parts.path == '/uzleteink':
        return ShopListBrowsingEvent(**kwargs)

    if parts.path == '/reflexshop-tarsasjatekok':
        return BoardGamesUpdateEvent(**kwargs)

    if parts.path == '/index.php' and query.get('route') == 'wishlist/wishlist':
        return WishListBrowsingEvent(**kwargs)

    if parts.path == '/index.php' and query.get('route', '').startswith('account/'):
        return AccountPageBrowsingEvent(**kwargs)

    # CategoryPage
    for path, category in CATEGORY_MAP.items():
        if parts.path == path or parts.path.find(path) > -1:
            kwargs = {**kwargs, 'category_id': category, **get_pagination(query)}
            return CategoryPageBrowsingEvent(**kwargs)

    # CategoryPage
    if parts.path == '/index.php' and query.get('route') == 'product/list':
        if query.get('keyword') is None and (cat_id := query.get('category_id')):
            category = CATEGORY_FILTER.get(int(cat_id), -1)
            kwargs = {**kwargs, 'category_id': category, **get_pagination(query)}
            return CategoryPageBrowsingEvent(**kwargs)

    # PredefinedFilter -> CategoryPage -> SearchResults
    if parts.path == '/index.php' and query.get('route') == 'filter':
        category = PREDEFINED_FILTER.get(query.get('filter'), -2)
        if category > -2:
            kwargs = {**kwargs, 'category_id': category, **get_pagination(query)}
            return PredefinedFilterBrowsingEvent(**kwargs)

        if query.get('filter', '').startswith('category|') and query.get('keyword') is None:
            numbers = re.findall(r'\d+', query.get('filter'))
            category = CATEGORY_FILTER.get(int(numbers[0]), -2) if numbers else -2
            if category > -2:
                kwargs = {**kwargs, 'category_id': category, **get_pagination(query)}
                return CategoryPageBrowsingEvent(**kwargs)

        kwargs = {**kwargs, **get_pagination(query)}
        return SearchResultsBrowsingEvent(**kwargs)

    # SearchResults
    if parts.path == '/search':
        kwargs = {**kwargs, **get_pagination(query)}
        return SearchResultsBrowsingEvent(**kwargs)

    # InformationPage
    if parts.path in INFO_PAGES or query.get('route') in INFO_PAGES:
        return InformationPageBrowsingEvent(**kwargs)

    return BrowsingEvent(**kwargs)


def float_or_none(value: str):
    try:
        return float(value)
    except:
        return None


def get_event_ua(item: Dict) -> SessionBodyEvent:
    time: int = item.get('_ts', int(dt.now().timestamp()))
    browsing_data = {'time': time,
                     'referrer': get_referrer(item.get(Config.CD_REFERRER)),
                     'tabcount': int(item[Config.CD_TABCOUNT]),
                     'tabtype': get_tabtype(item[Config.CD_TABTYPE]),
                     'navigation': get_navigation(item[Config.CD_NAVIGATION]),
                     'redirects': int(item[Config.CD_REDIRECTS]),
                     'title': item.get('dt'),
                     'utm_source': get_utm_source(item),
                     'utm_medium': item.get('utm_medium', '')}

    if item.get('t') == 'pageview':
        parts = urlparse(get_fixed_url(item.get('dl')))
        query: Dict[str, str] = parse_query(parts.query)
        if parts.path == '/':
            event = MainPageBrowsingEvent(**browsing_data)
            return event
        if item.get('pa') == 'detail':
            browsing_data['product_id'] = item.get('pr1id')
            browsing_data['category_id'] = -1
            for path, cat in CATEGORY_MAP.items():
                if parts.path.startswith(path):
                    browsing_data['category_id'] = cat
                    break

            pr1pr = item.get('pr1pr', 0)
            browsing_data['price'] = int(pr1pr) if pr1pr != 'NaN' else 0
            event = ProductPageBrowsingEvent(**browsing_data)
            return event
        if parts.path == '/szakuzletunk':
            event = ShopListBrowsingEvent(**browsing_data)
            return event
        if parts.path == '/reflexshop-tarsasjatekok':
            event = BoardGamesUpdateEvent(**browsing_data)
            return event
        if parts.path == '/cart':
            event = CartBrowsingEvent(**browsing_data)
            return event
        if parts.path == '/checkout':
            if parts.fragment == '/customerdata/':
                event = CustomerDataEntryBrowsingEvent(**browsing_data)
                return event
            if parts.fragment == '/shippingmethod/':
                event = ShippingMethodBrowsingEvent(**browsing_data)
                return event
            if parts.fragment == '/paymentmethod/':
                event = PaymentMethodBrowsingEvent(**browsing_data)
                return event
            if parts.fragment == '/confirmation/':
                event = ConfirmationPageBrowsingEvent(**browsing_data)
                return event

            event = CheckoutPageBrowsingEvent(**browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route') == 'checkout/success':
            event = CheckoutSuccessPageBrowsingEvent(**browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route') == 'wishlist/wishlist':
            event = WishListBrowsingEvent(**browsing_data)
            return event

        if parts.path == '/index.php' and query.get('route', '').startswith('account/'):
            event = AccountPageBrowsingEvent(**browsing_data)
            return event

        # CategoryPage
        for path, category in CATEGORY_MAP.items():
            if parts.path == path or parts.path.find(path) > -1:
                kwargs = {**browsing_data, 'category_id': category, **get_pagination(query)}
                event = CategoryPageBrowsingEvent(**kwargs)
                return event

        # CategoryPage
        if parts.path == '/index.php' and query.get('route') == 'product/list':
            if query.get('keyword') is None and (cat_id := query.get('category_id')):
                category = CATEGORY_FILTER.get(int(cat_id), -1)
                kwargs = {**browsing_data, 'category_id': category, **get_pagination(query)}
                event = CategoryPageBrowsingEvent(**kwargs)
                return event

        # PredefinedFilter -> CategoryPage -> SearchResults
        if parts.path == '/index.php' and query.get('route') == 'filter':
            category = PREDEFINED_FILTER.get(query.get('filter'), -2)
            if category > -2:
                kwargs = {**browsing_data, 'category_id': category, **get_pagination(query)}
                event = PredefinedFilterBrowsingEvent(**kwargs)
                return event

            if query.get('filter', '').startswith('category|') and query.get('keyword') is None:
                numbers = re.findall(r'\d+', query.get('filter'))
                category = CATEGORY_FILTER.get(int(numbers[0]), -2) if numbers else -2
                if category > -2:
                    kwargs = {**browsing_data, 'category_id': category, **get_pagination(query)}
                    event = CategoryPageBrowsingEvent(**kwargs)
                    return event

            kwargs = {**browsing_data, **get_pagination(query)}
            event = SearchResultsBrowsingEvent(**kwargs)
            return event

        # SearchResults
        if parts.path == '/kereses' or query.get('route') == 'product/list':
            kwargs = {**browsing_data, **get_pagination(query)}
            event = SearchResultsBrowsingEvent(**kwargs)
            return event

        # InformationPage
        if parts.path in INFO_PAGES or query.get('route') in INFO_PAGES:
            event = InformationPageBrowsingEvent(**browsing_data)
            return event

        event = BrowsingEvent(**browsing_data)
        return event

    if item.get('t') == 'event':
        if item.get('ec') == 'Értesítés kérése' and item.get('ea') == 'Értesítés kérése sikeres':
            event = RegistrationEvent(time)
            return event
        if item.get('ec') == 'e-cart' and item.get('ea') == 'update':
            data = json.loads(item.get('el'))
            delta_count = data.get('itemCount')
            delta_total = round(data.get('total'), 2)
            event = CartModifyEvent(time, delta_count, delta_total)
            return event
        if item.get('ec') == 'OptiMonk':
            if item.get('ea') == 'shown':
                event = CouponOfferedEvent(time, item.get('el'))
                return event
            if item.get('ea') == 'filled':
                event = CouponAcceptedEvent(time, item.get('el'))
                return event

    event = SystemEvent(time)
    return event


def get_fixed_url(url: str) -> str:
    p1 = url.find('?')
    p2 = url.find('&')
    if p1 == -1 and p2 > -1:
        return url[:p2] + '?' + url[p2+1:]
    return url[:p2] + url[p1:] + url[p2:p1] if -1 < p2 < p1 else url


def parse_query(query: str) -> Dict[str, str]:
    return {} if query.strip() == '' else {k: v[0] for k, v in parse_qs(unquote(query)).items()}


def get_pagination(query: Dict) -> Dict:
    pagination = {"page": get_page(query.get('page', '1'))}
    if 'filter[order]' in query.keys():
        pagination["sort"] = get_sort(query.get('filter[order]'))
    else:
        pagination["sort"] = get_sort('relevance')
    return pagination
