"""
CCN Cheer Competition Map — 2026-27 Season
Production Flask app for Render.com
"""
import os
import json
from flask import Flask, jsonify

# ── Embedded competition data ─────────────────────────────────────────────────
COMPETITIONS = [{"num":1,"brand":"NC","event":"Nation's Choice - Dance Grand Championship & Cheer Showdown","city":"Madison","state":"WI","start":"11/13/2026","end":"11/15/2026","dist":"< 1750 mi","housing":"Housing Rewards","lat":43.0731,"lng":-89.4012,"month":"Nov 2026"},{"num":2,"brand":"GSSA","event":"GSSA - San Mateo - Challenge - DI/DII","city":"San Mateo","state":"CA","start":"11/21/2026","end":"11/21/2026","dist":"< 750 mi","housing":"Housing Offered","lat":37.563,"lng":-122.3255,"month":"Nov 2026"},{"num":3,"brand":"ATC","event":"ATC - Utah - Challenge - DI/DII","city":"Salt Lake City","state":"UT","start":"11/21/2026","end":"11/21/2026","dist":"< 750 mi","housing":"Housing Offered","lat":40.7608,"lng":-111.891,"month":"Nov 2026"},{"num":4,"brand":"GSSA","event":"GSSA - Ontario - Challenge - DI/DII","city":"Ontario","state":"CA","start":"11/21/2026","end":"11/21/2026","dist":"< 1000 mi","housing":"Housing Offered","lat":34.0633,"lng":-117.6509,"month":"Nov 2026"},{"num":5,"brand":"NCA","event":"NCA & NDA - Rockies - Regional","city":"Highlands Ranch","state":"CO","start":"11/21/2026","end":"11/22/2026","dist":"< 1250 mi","housing":"Housing Offered","lat":39.55,"lng":-104.9697,"month":"Nov 2026"},{"num":6,"brand":"ASC","event":"ASC - Twin Cities - Showdown","city":"St Paul","state":"MN","start":"11/21/2026","end":"11/22/2026","dist":"< 1500 mi","housing":"Housing Rewards","lat":44.9537,"lng":-93.09,"month":"Nov 2026"},{"num":7,"brand":"ATH","event":"Athletic Championships - St. Louis - Nationals","city":"St. Louis","state":"MO","start":"11/21/2026","end":"11/21/2026","dist":"< 1750 mi","housing":"Housing Offered","lat":38.627,"lng":-90.1994,"month":"Nov 2026"},{"num":8,"brand":"ACP","event":"Cheer Power - Dayton - Disco Showdown","city":"Dayton","state":"OH","start":"11/21/2026","end":"11/21/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":39.7589,"lng":-84.1916,"month":"Nov 2026"},{"num":9,"brand":"ASC","event":"ASC - Sandusky - Showdown","city":"Sandusky","state":"OH","start":"11/21/2026","end":"11/22/2026","dist":"< 2000 mi","housing":"Housing Required","lat":41.4484,"lng":-82.7079,"month":"Nov 2026"},{"num":10,"brand":"EN","event":"Encore - Atlanta - Showdown - DI/DII","city":"College Park","state":"GA","start":"11/21/2026","end":"11/22/2026","dist":"< 2250 mi","housing":"Housing Offered","lat":33.6534,"lng":-84.4496,"month":"Nov 2026"},{"num":11,"brand":"ALO","event":"Aloha - Trenton - Showdown - DI/DII","city":"Trenton","state":"NJ","start":"11/21/2026","end":"11/21/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":40.2171,"lng":-74.7429,"month":"Nov 2026"},{"num":12,"brand":"ASC","event":"ASC - King of the Jungle - Nashville - Showdown - DI/DII","city":"Lebanon","state":"TN","start":"11/22/2026","end":"11/22/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":36.2081,"lng":-86.2911,"month":"Nov 2026"},{"num":13,"brand":"ASC","event":"ASC - Clash of the Titans - Concord - Showdown - DI/DII","city":"Concord","state":"NC","start":"11/22/2026","end":"11/22/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":35.4088,"lng":-80.5796,"month":"Nov 2026"},{"num":14,"brand":"GRV","event":"WSF - Grand Nationals - DI/DII","city":"Louisville","state":"KY","start":"12/4/2026","end":"12/6/2026","dist":"< 2000 mi","housing":"Housing Required","lat":38.2527,"lng":-85.7585,"month":"Dec 2026"},{"num":15,"brand":"AC","event":"The American Northwest - Portland - Nationals - DI/DII","city":"Portland","state":"OR","start":"12/5/2026","end":"12/6/2026","dist":"< 150 mi","housing":"Housing Rewards","lat":45.5231,"lng":-122.6765,"month":"Dec 2026"},{"num":16,"brand":"ACP","event":"Cheer Power - Holiday - Roseville - Showdown - DI/DII","city":"Roseville","state":"CA","start":"12/5/2026","end":"12/6/2026","dist":"< 750 mi","housing":"Housing Offered","lat":38.7521,"lng":-121.288,"month":"Dec 2026"},{"num":17,"brand":"OU","event":"One Up - SoCal - Nationals - DI/DII","city":"Anaheim","state":"CA","start":"12/5/2026","end":"12/6/2026","dist":"< 1000 mi","housing":"Housing Offered","lat":33.8353,"lng":-117.9145,"month":"Dec 2026"},{"num":18,"brand":"ATC","event":"ATC - Phoenix - Challenge - DI/DII","city":"Phoenix","state":"AZ","start":"12/5/2026","end":"12/5/2026","dist":"< 1250 mi","housing":"Housing Offered","lat":33.4484,"lng":-112.074,"month":"Dec 2026"},{"num":19,"brand":"SCB","event":"Spirit Celebration Christmas Grand Nationals - DI/DII","city":"Dallas","state":"TX","start":"12/5/2026","end":"12/6/2026","dist":"< 1750 mi","housing":"Housing Required","lat":32.7767,"lng":-96.797,"month":"Dec 2026"},{"num":20,"brand":"ACP","event":"Cheer Power - Houston - Christmas Showdown - DI/DII","city":"Rosenberg","state":"TX","start":"12/5/2026","end":"12/5/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":29.5572,"lng":-95.8083,"month":"Dec 2026"},{"num":21,"brand":"UCA","event":"UCA/UDA - Smoky Mountain Championship","city":"Sevierville","state":"TN","start":"12/5/2026","end":"12/6/2026","dist":"< 2250 mi","housing":"Housing Rewards","lat":35.8681,"lng":-83.5618,"month":"Dec 2026"},{"num":22,"brand":"UCA","event":"UCA - Sevierville - Showdown - DI/DII","city":"Sevierville","state":"TN","start":"12/5/2026","end":"12/6/2026","dist":"< 2250 mi","housing":"Housing Rewards","lat":35.8681,"lng":-83.5618,"month":"Dec 2026"},{"num":23,"brand":"CCD","event":"Champion Cheer and Dance - Grand Nationals - DI/DII","city":"Baltimore","state":"MD","start":"12/5/2026","end":"12/6/2026","dist":"< 2500 mi","housing":"Housing Required","lat":39.2904,"lng":-76.6122,"month":"Dec 2026"},{"num":24,"brand":"AB","event":"America's Best - Springfield - Challenge","city":"Springfield","state":"MA","start":"12/5/2026","end":"12/5/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":42.1015,"lng":-72.5898,"month":"Dec 2026"},{"num":25,"brand":"JF","event":"JAMfest - Jackson - Classic - DI/DII","city":"Jackson","state":"MS","start":"12/6/2026","end":"12/6/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":32.2988,"lng":-90.1848,"month":"Dec 2026"},{"num":26,"brand":"CS","event":"CHEERSPORT - Cartersville - Classic - DI/DII","city":"Cartersville","state":"GA","start":"12/6/2026","end":"12/6/2026","dist":"< 2250 mi","housing":"Housing Offered","lat":34.1651,"lng":-84.7999,"month":"Dec 2026"},{"num":27,"brand":"JF","event":"JAMfest - Concord - Classic - DI/DII","city":"Concord","state":"NC","start":"12/6/2026","end":"12/6/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":35.4088,"lng":-80.5796,"month":"Dec 2026"},{"num":28,"brand":"JF","event":"JAMfest - Jacksonville - Classic - DI/DII","city":"Jacksonville","state":"FL","start":"12/6/2026","end":"12/6/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":30.3322,"lng":-81.6557,"month":"Dec 2026"},{"num":29,"brand":"EN","event":"Encore - Lakeland - Showdown","city":"Lakeland","state":"FL","start":"12/6/2026","end":"12/6/2026","dist":"< 2750 mi","housing":"Housing Offered","lat":28.0395,"lng":-81.9498,"month":"Dec 2026"},{"num":30,"brand":"EN","event":"Encore - Grand Nationals - DI/DII","city":"Houston","state":"TX","start":"12/11/2026","end":"12/13/2026","dist":"< 2000 mi","housing":"Housing Required","lat":29.7604,"lng":-95.3698,"month":"Dec 2026"},{"num":31,"brand":"UCA","event":"UCA - Sandy - Fall Classic - DI/DII","city":"Sandy","state":"UT","start":"12/12/2026","end":"12/12/2026","dist":"< 750 mi","housing":"Housing Offered","lat":40.5649,"lng":-111.8389,"month":"Dec 2026"},{"num":32,"brand":"AB","event":"America's Best - Grand Nationals","city":"Kansas City","state":"MO","start":"12/12/2026","end":"12/13/2026","dist":"< 1500 mi","housing":"Housing Required","lat":39.0997,"lng":-94.5786,"month":"Dec 2026"},{"num":33,"brand":"NC","event":"Nation's Choice - Grand Nationals","city":"Wisconsin Dells","state":"WI","start":"12/12/2026","end":"12/13/2026","dist":"< 1750 mi","housing":"Housing Required","lat":43.6275,"lng":-89.7715,"month":"Dec 2026"},{"num":34,"brand":"AB","event":"America's Best - Indy - Challenge","city":"Westfield","state":"IN","start":"12/12/2026","end":"12/12/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":40.0431,"lng":-86.1277,"month":"Dec 2026"},{"num":35,"brand":"CS","event":"CHEERSPORT - Pittsburgh - Classic","city":"Pittsburgh","state":"PA","start":"12/12/2026","end":"12/12/2026","dist":"< 2250 mi","housing":"Housing Offered","lat":40.4406,"lng":-79.9959,"month":"Dec 2026"},{"num":36,"brand":"ALO","event":"Aloha - Gatlinburg - Showdown - DI/DII","city":"Gatlinburg","state":"TN","start":"12/12/2026","end":"12/13/2026","dist":"< 2250 mi","housing":"Housing Offered","lat":35.7143,"lng":-83.5129,"month":"Dec 2026"},{"num":37,"brand":"ASC","event":"ASC - Battle Under the Big Top - Grand Nationals - DI/DII","city":"College Park","state":"GA","start":"12/12/2026","end":"12/13/2026","dist":"< 2250 mi","housing":"Housing Required","lat":33.6534,"lng":-84.4496,"month":"Dec 2026"},{"num":38,"brand":"CS","event":"CHEERSPORT - Fredericksburg - Classic","city":"Fredericksburg","state":"VA","start":"12/12/2026","end":"12/12/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":38.3032,"lng":-77.4605,"month":"Dec 2026"},{"num":39,"brand":"JF","event":"JAMfest - Albany - Classic","city":"Albany","state":"NY","start":"12/12/2026","end":"12/12/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":42.6526,"lng":-73.7562,"month":"Dec 2026"},{"num":40,"brand":"EN","event":"Encore - Philly - Showdown - DI/DII","city":"Philadelphia","state":"PA","start":"12/12/2026","end":"12/13/2026","dist":"< 2500 mi","housing":"Housing Rewards","lat":39.9526,"lng":-75.1652,"month":"Dec 2026"},{"num":41,"brand":"SC","event":"Spirit Cheer - Dance Grand Nationals & Cheer Nationals - DI/DII","city":"Orlando","state":"FL","start":"12/13/2026","end":"12/14/2026","dist":"< 2750 mi","housing":"Housing Required","lat":28.5383,"lng":-81.3792,"month":"Dec 2026"},{"num":42,"brand":"AC","event":"The American Grand - Grand Nationals - DI/DII","city":"Las Vegas","state":"NV","start":"12/18/2026","end":"12/20/2026","dist":"< 1000 mi","housing":"Housing Required","lat":36.1699,"lng":-115.1398,"month":"Dec 2026"},{"num":43,"brand":"ASCS","event":"CHAMPS - Grand Nationals - DI/DII","city":"Aurora","state":"CO","start":"12/19/2026","end":"12/20/2026","dist":"< 1250 mi","housing":"Housing Required","lat":39.7294,"lng":-104.8319,"month":"Dec 2026"},{"num":44,"brand":"GLCC","event":"GLCC - Michigan - Challenge","city":"Grand Rapids","state":"MI","start":"12/19/2026","end":"12/19/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":42.9634,"lng":-85.6681,"month":"Dec 2026"},{"num":45,"brand":"EN","event":"Encore - Virtual Winter II","city":"Louisville","state":"KY","start":"1/7/2027","end":"1/26/2027","dist":"< 2000 mi","housing":"Not Listed","lat":38.2527,"lng":-85.7585,"month":"Jan 2027"},{"num":46,"brand":"ASC","event":"ASC - Return to Atlantis - Salt Lake City - Showdown - DI/DII","city":"Salt Lake City","state":"UT","start":"1/8/2027","end":"1/9/2027","dist":"< 750 mi","housing":"Housing Rewards","lat":40.7608,"lng":-111.891,"month":"Jan 2027"},{"num":47,"brand":"GSSA","event":"GSSA - Grand Nationals - DI/DII","city":"Bakersfield","state":"CA","start":"1/8/2027","end":"1/10/2027","dist":"< 1000 mi","housing":"Housing Required","lat":35.3733,"lng":-119.0187,"month":"Jan 2027"},{"num":48,"brand":"ALO","event":"Aloha - Portland - Showdown - DI/DII","city":"Portland","state":"OR","start":"1/9/2027","end":"1/10/2027","dist":"< 150 mi","housing":"Housing Rewards","lat":45.5231,"lng":-122.6765,"month":"Jan 2027"},{"num":49,"brand":"USA","event":"USA Competition I","city":"Las Vegas","state":"NV","start":"1/9/2027","end":"1/9/2027","dist":"< 1000 mi","housing":"Housing Offered","lat":36.1699,"lng":-115.1398,"month":"Jan 2027"},{"num":50,"brand":"UCA","event":"UCA/UDA - Cactus Cup Challenge","city":"Gilbert","state":"AZ","start":"1/9/2027","end":"1/9/2027","dist":"< 1250 mi","housing":"Housing Offered","lat":33.3528,"lng":-111.789,"month":"Jan 2027"},{"num":51,"brand":"AC","event":"The American Heartland - Council Bluffs - Nationals","city":"Council Bluffs","state":"IA","start":"1/9/2027","end":"1/10/2027","dist":"< 1500 mi","housing":"Housing Rewards","lat":41.2619,"lng":-95.8608,"month":"Jan 2027"},{"num":52,"brand":"ACP","event":"Cheer Power - Cash Bash Showdown - Galveston - DI/DII","city":"Galveston","state":"TX","start":"1/9/2027","end":"1/10/2027","dist":"< 2000 mi","housing":"Housing Rewards","lat":29.3013,"lng":-94.7977,"month":"Jan 2027"},{"num":53,"brand":"CS","event":"CHEERSPORT - Biloxi - Classic - DI/DII","city":"Biloxi","state":"MS","start":"1/9/2027","end":"1/9/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":30.396,"lng":-88.8853,"month":"Jan 2027"},{"num":54,"brand":"SC","event":"Spirit Cheer - Grand Nationals - DI/DII","city":"Atlantic City","state":"NJ","start":"1/9/2027","end":"1/10/2027","dist":"< 2500 mi","housing":"Housing Required","lat":39.3643,"lng":-74.4229,"month":"Jan 2027"},{"num":55,"brand":"ALO","event":"Aloha - Baltimore - Showdown - DI/DII","city":"Baltimore","state":"MD","start":"1/10/2027","end":"1/10/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.2904,"lng":-76.6122,"month":"Jan 2027"},{"num":56,"brand":"GLCC","event":"GLCC - Louisville - Challenge","city":"TBD","state":"KY","start":"1/10/2027","end":"1/10/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":37.8393,"lng":-84.27,"month":"Jan 2027"},{"num":57,"brand":"NCA","event":"NCA & NDA - January Virtual - Regional","city":"Plano","state":"TX","start":"1/13/2027","end":"1/17/2027","dist":"< 1750 mi","housing":"Not Listed","lat":33.0198,"lng":-96.6989,"month":"Jan 2027"},{"num":58,"brand":"OU","event":"One Up - Phoenix - Nationals - DI/DII","city":"Phoenix","state":"AZ","start":"1/16/2027","end":"1/17/2027","dist":"< 1250 mi","housing":"Housing Offered","lat":33.4484,"lng":-112.074,"month":"Jan 2027"},{"num":59,"brand":"JF","event":"JAMfest - Cheer Super Nationals - DI/DII","city":"Indianapolis","state":"IN","start":"1/16/2027","end":"1/17/2027","dist":"< 2000 mi","housing":"Housing Required","lat":39.7684,"lng":-86.1581,"month":"Jan 2027"},{"num":60,"brand":"NCA","event":"NCA - Birmingham - Classic - DI/DII","city":"Birmingham","state":"AL","start":"1/16/2027","end":"1/16/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":33.5186,"lng":-86.8104,"month":"Jan 2027"},{"num":61,"brand":"MGS","event":"Mardi Gras - Grand Nationals - DI/DII","city":"New Orleans","state":"LA","start":"1/16/2027","end":"1/17/2027","dist":"< 2250 mi","housing":"Housing Required","lat":29.9511,"lng":-90.0715,"month":"Jan 2027"},{"num":62,"brand":"ACP","event":"Cheer Power - Rochester - Showdown - DI/DII","city":"Rochester","state":"NY","start":"1/16/2027","end":"1/16/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":43.1566,"lng":-77.6088,"month":"Jan 2027"},{"num":63,"brand":"US","event":"Spirit of Hope - Grand Nationals - DI/DII","city":"Charlotte","state":"NC","start":"1/16/2027","end":"1/17/2027","dist":"< 2500 mi","housing":"Housing Required","lat":35.2271,"lng":-80.8431,"month":"Jan 2027"},{"num":64,"brand":"CS","event":"CHEERSPORT - Oaks - Classic","city":"Oaks","state":"PA","start":"1/16/2027","end":"1/16/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":40.1343,"lng":-75.4527,"month":"Jan 2027"},{"num":65,"brand":"ALO","event":"Aloha - Worcester - Showdown - DI/DII","city":"Worcester","state":"MA","start":"1/16/2027","end":"1/16/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":42.2626,"lng":-71.8023,"month":"Jan 2027"},{"num":66,"brand":"AC","event":"The STATE - Daytona Beach - Nationals - DI/DII","city":"Daytona Beach","state":"FL","start":"1/16/2027","end":"1/17/2027","dist":"< 2750 mi","housing":"Housing Required","lat":29.2108,"lng":-81.0228,"month":"Jan 2027"},{"num":67,"brand":"AC","event":"The American Masterpiece - San Jose - Nationals DI/DII","city":"San Jose","state":"CA","start":"1/17/2027","end":"1/18/2027","dist":"< 750 mi","housing":"Housing Offered","lat":37.3382,"lng":-121.8863,"month":"Jan 2027"},{"num":68,"brand":"FTP","event":"Feel The Power","city":"Brampton","state":"ON","start":"1/22/2027","end":"1/24/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":43.7315,"lng":-79.7624,"month":"Jan 2027"},{"num":69,"brand":"UCA","event":"UCA - Sandy - Spring Classic - DI/DII","city":"Sandy","state":"UT","start":"1/23/2027","end":"1/23/2027","dist":"< 750 mi","housing":"Housing Offered","lat":40.5649,"lng":-111.8389,"month":"Jan 2027"},{"num":70,"brand":"CS","event":"CHEERSPORT - SoCal - Classic - DI/DII","city":"Pomona","state":"CA","start":"1/23/2027","end":"1/23/2027","dist":"< 1000 mi","housing":"Housing Offered","lat":34.0553,"lng":-117.752,"month":"Jan 2027"},{"num":71,"brand":"ATH","event":"Athletic Championships Nationals & Dance Grand Nationals","city":"Columbus","state":"OH","start":"1/23/2027","end":"1/24/2027","dist":"< 2250 mi","housing":"Housing Required","lat":39.9612,"lng":-82.9988,"month":"Jan 2027"},{"num":72,"brand":"ATH","event":"Athletic Championships - Chattanooga - Nationals - DI/DII","city":"Chattanooga","state":"TN","start":"1/23/2027","end":"1/24/2027","dist":"< 2250 mi","housing":"Housing Required","lat":35.0456,"lng":-85.3097,"month":"Jan 2027"},{"num":73,"brand":"UCA","event":"UDA - Magic City Dance Challenge","city":"Alabaster","state":"AL","start":"1/23/2027","end":"1/23/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":33.2345,"lng":-86.8236,"month":"Jan 2027"},{"num":74,"brand":"MGS","event":"Mardi Gras - Biloxi - Showdown - DI/DII","city":"Biloxi","state":"MS","start":"1/23/2027","end":"1/24/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":30.396,"lng":-88.8853,"month":"Jan 2027"},{"num":75,"brand":"SU","event":"SU - Battle at the Boardwalk - Grand Nationals - DI/DII","city":"Atlantic City","state":"NJ","start":"1/23/2027","end":"1/24/2027","dist":"< 2500 mi","housing":"Housing Required","lat":39.3643,"lng":-74.4229,"month":"Jan 2027"},{"num":76,"brand":"ATC","event":"ATC - Grand Nationals","city":"Seattle","state":"WA","start":"1/29/2027","end":"1/31/2027","dist":"< 50 mi","housing":"Housing Required","lat":47.6062,"lng":-122.3321,"month":"Jan 2027"},{"num":77,"brand":"GRV","event":"Spirit Sports - Grand Nationals","city":"Palm Springs","state":"CA","start":"1/29/2027","end":"1/31/2027","dist":"< 1000 mi","housing":"Housing Rewards","lat":33.8303,"lng":-116.5453,"month":"Jan 2027"},{"num":78,"brand":"ACA","event":"ACA Grand Nationals- DI/DII","city":"Fort Worth","state":"TX","start":"1/29/2027","end":"1/31/2027","dist":"< 1750 mi","housing":"Housing Required","lat":32.7555,"lng":-97.3308,"month":"Jan 2027"},{"num":79,"brand":"NCA","event":"NCA - Twin Cities - Classic","city":"St Paul","state":"MN","start":"1/30/2027","end":"1/30/2027","dist":"< 1500 mi","housing":"Housing Offered","lat":44.9537,"lng":-93.09,"month":"Jan 2027"},{"num":80,"brand":"EN","event":"Encore \u2013 Nashville \u2013 Showdown - DI/DII","city":"Nashville","state":"TN","start":"1/30/2027","end":"1/30/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":36.1627,"lng":-86.7816,"month":"Jan 2027"},{"num":81,"brand":"AB","event":"America's Best - Canton - Challenge","city":"Canton","state":"OH","start":"1/30/2027","end":"1/30/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":40.7989,"lng":-81.3784,"month":"Jan 2027"},{"num":82,"brand":"NCA","event":"NCA - Atlanta - Classic - DI/DII","city":"College Park","state":"GA","start":"1/30/2027","end":"1/30/2027","dist":"< 2250 mi","housing":"Not Listed","lat":33.6534,"lng":-84.4496,"month":"Jan 2027"},{"num":83,"brand":"ATH","event":"Athletic Championships - Grand Nationals - DI/DII","city":"Providence","state":"RI","start":"1/30/2027","end":"1/31/2027","dist":"< 2500 mi","housing":"Housing Required","lat":41.824,"lng":-71.4128,"month":"Jan 2027"},{"num":84,"brand":"SS","event":"Spirit Sports - Kissimmee - Nationals - DI/DII","city":"Kissimmee","state":"FL","start":"1/30/2027","end":"1/31/2027","dist":"< 2750 mi","housing":"Housing Offered","lat":28.292,"lng":-81.4079,"month":"Jan 2027"},{"num":85,"brand":"ACP","event":"Cheer Power - Reading - Showdown - DI/DII","city":"Reading","state":"PA","start":"1/31/2027","end":"1/31/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":40.3356,"lng":-75.9269,"month":"Jan 2027"},{"num":86,"brand":"ASC","event":"ASC - Return to Atlantis - Tacoma - Showdown - DI/DII","city":"Tacoma","state":"WA","start":"2/6/2027","end":"2/7/2027","dist":"< 50 mi","housing":"Housing Offered","lat":47.2529,"lng":-122.4443,"month":"Feb 2027"},{"num":87,"brand":"NCA","event":"NCA - Roseville - Showdown","city":"Roseville","state":"CA","start":"2/6/2027","end":"2/7/2027","dist":"< 750 mi","housing":"Housing Offered","lat":38.7521,"lng":-121.288,"month":"Feb 2027"},{"num":88,"brand":"JF","event":"JAMfest - Arizona - Classic","city":"Tempe","state":"AZ","start":"2/6/2027","end":"2/6/2027","dist":"< 1250 mi","housing":"Housing Offered","lat":33.4255,"lng":-111.94,"month":"Feb 2027"},{"num":89,"brand":"CSG","event":"CSG - Grand Nationals - DI/DII","city":"Schaumburg","state":"IL","start":"2/6/2027","end":"2/7/2027","dist":"< 1750 mi","housing":"Housing Required","lat":42.0334,"lng":-88.0834,"month":"Feb 2027"},{"num":90,"brand":"ALO","event":"Aloha - Pittsburgh - Showdown","city":"Moon Township","state":"PA","start":"2/6/2027","end":"2/6/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":40.5076,"lng":-80.212,"month":"Feb 2027"},{"num":91,"brand":"ACP","event":"Cheer Power - Trenton - Showdown - DI/DII","city":"Trenton","state":"NJ","start":"2/6/2027","end":"2/6/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":40.2171,"lng":-74.7429,"month":"Feb 2027"},{"num":92,"brand":"ACDA","event":"ACDA Reach the Beach - All-Star Grand Nationals - DII","city":"Ocean City","state":"MD","start":"2/6/2027","end":"2/7/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":38.3365,"lng":-75.0849,"month":"Feb 2027"},{"num":93,"brand":"ASC","event":"ASC - Return to Atlantis - Worcester - Showdown - DI/DII","city":"Worcester","state":"MA","start":"2/6/2027","end":"2/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":42.2626,"lng":-71.8023,"month":"Feb 2027"},{"num":94,"brand":"ATL","event":"ATL - Atlantic Showdown","city":"Moncton","state":"NB","start":"2/6/2027","end":"2/7/2027","dist":"< 2750 mi","housing":"Housing Offered","lat":46.0878,"lng":-64.7782,"month":"Feb 2027"},{"num":95,"brand":"ALO","event":"Aloha - Concord - Showdown - DI/DII","city":"Concord","state":"NC","start":"2/7/2027","end":"2/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":35.4088,"lng":-80.5796,"month":"Feb 2027"},{"num":96,"brand":"CS","event":"CHEERSPORT - Baltimore - Classic","city":"Baltimore","state":"MD","start":"2/7/2027","end":"2/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.2904,"lng":-76.6122,"month":"Feb 2027"},{"num":97,"brand":"NCA","event":"NCA - Kissimmee - Classic - DI/DII","city":"Kissimmee","state":"FL","start":"2/7/2027","end":"2/7/2027","dist":"< 2750 mi","housing":"Housing Offered","lat":28.292,"lng":-81.4079,"month":"Feb 2027"},{"num":98,"brand":"CS","event":"CHEERSPORT National All Star Cheerleading Championship - DI/DII","city":"Atlanta","state":"GA","start":"2/12/2027","end":"2/14/2027","dist":"< 2250 mi","housing":"Housing Required","lat":33.749,"lng":-84.388,"month":"Feb 2027"},{"num":99,"brand":"ATH","event":"Athletic Championships - Garland - Nationals - DI/DII","city":"Garland","state":"TX","start":"2/13/2027","end":"2/14/2027","dist":"< 1750 mi","housing":"Housing Offered","lat":32.9126,"lng":-96.6389,"month":"Feb 2027"},{"num":100,"brand":"JF","event":"JAMfest - Peoria - Classic","city":"Peoria","state":"IL","start":"2/13/2027","end":"2/13/2027","dist":"< 1750 mi","housing":"Housing Offered","lat":40.6936,"lng":-89.589,"month":"Feb 2027"},{"num":101,"brand":"CS","event":"CHEERSPORT - Sweetheart - Raleigh - Classic - DI/DII","city":"Raleigh","state":"NC","start":"2/13/2027","end":"2/13/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":35.7796,"lng":-78.6382,"month":"Feb 2027"},{"num":102,"brand":"EN","event":"Encore - Foxwoods - Showdown - DI/DII","city":"Mashantucket","state":"CT","start":"2/13/2027","end":"2/14/2027","dist":"< 2500 mi","housing":"Housing Required","lat":41.4676,"lng":-71.9579,"month":"Feb 2027"},{"num":103,"brand":"AC","event":"The American Celebration - Salt Lake City - Nationals - DI/DII","city":"Salt Lake City","state":"UT","start":"2/19/2027","end":"2/20/2027","dist":"< 750 mi","housing":"Housing Rewards","lat":40.7608,"lng":-111.891,"month":"Feb 2027"},{"num":104,"brand":"ASCS","event":"ASCS - Dance Grand Nationals & Cheer Nationals","city":"Wisconsin Dells","state":"WI","start":"2/20/2027","end":"2/21/2027","dist":"< 1750 mi","housing":"Housing Required","lat":43.6275,"lng":-89.7715,"month":"Feb 2027"},{"num":105,"brand":"DDC","event":"Double Down - St. Louis - Nationals","city":"St. Louis","state":"MO","start":"2/20/2027","end":"2/21/2027","dist":"< 1750 mi","housing":"Housing Rewards","lat":38.627,"lng":-90.1994,"month":"Feb 2027"},{"num":106,"brand":"SOU","event":"Southern Grand Nationals - DI/DII","city":"San Antonio","state":"TX","start":"2/20/2027","end":"2/21/2027","dist":"< 2000 mi","housing":"Housing Required","lat":29.4241,"lng":-98.4936,"month":"Feb 2027"},{"num":107,"brand":"CSG","event":"CSG - Canton - Challenge","city":"Canton","state":"OH","start":"2/20/2027","end":"2/20/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":40.7989,"lng":-81.3784,"month":"Feb 2027"},{"num":108,"brand":"ALO","event":"Aloha - York - Showdown - DI/DII","city":"York","state":"PA","start":"2/20/2027","end":"2/20/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9626,"lng":-76.7277,"month":"Feb 2027"},{"num":109,"brand":"CAC","event":"Coastal at the Capitol - Super Nationals - DI/DII","city":"Washington","state":"DC","start":"2/20/2027","end":"2/21/2027","dist":"< 2500 mi","housing":"Housing Required","lat":38.9072,"lng":-77.0369,"month":"Feb 2027"},{"num":110,"brand":"ATH","event":"Athletic Championships - West Palm Beach - Nationals - DI/DII","city":"West Palm Beach","state":"FL","start":"2/20/2027","end":"2/21/2027","dist":"< 2750 mi","housing":"Housing Offered","lat":26.7153,"lng":-80.0534,"month":"Feb 2027"},{"num":111,"brand":"PW","event":"PacWest - Grand Nationals - DI/DII","city":"Portland","state":"OR","start":"2/27/2027","end":"2/28/2027","dist":"< 150 mi","housing":"Housing Required","lat":45.5231,"lng":-122.6765,"month":"Feb 2027"},{"num":112,"brand":"EN","event":"Encore - Las Vegas - Showdown - DI/DII","city":"Las Vegas","state":"NV","start":"2/27/2027","end":"2/28/2027","dist":"< 1000 mi","housing":"Housing Offered","lat":36.1699,"lng":-115.1398,"month":"Feb 2027"},{"num":113,"brand":"CSG","event":"CSG - Des Moines - Challenge","city":"Des Moines","state":"IA","start":"2/27/2027","end":"2/27/2027","dist":"< 1500 mi","housing":"Housing Offered","lat":41.5868,"lng":-93.625,"month":"Feb 2027"},{"num":114,"brand":"JF","event":"JAMfest - Nashville - Classic - DI/DII","city":"Nashville","state":"TN","start":"2/27/2027","end":"2/27/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":36.1627,"lng":-86.7816,"month":"Feb 2027"},{"num":115,"brand":"COA","event":"COA - Grand Nationals","city":"Columbus","state":"OH","start":"2/27/2027","end":"2/28/2027","dist":"< 2250 mi","housing":"Housing Required","lat":39.9612,"lng":-82.9988,"month":"Feb 2027"},{"num":116,"brand":"ALO","event":"Aloha - Daytona Beach - Showdown - DI/DII","city":"Daytona Beach","state":"FL","start":"2/27/2027","end":"2/27/2027","dist":"< 2750 mi","housing":"Housing Rewards","lat":29.2108,"lng":-81.0228,"month":"Feb 2027"},{"num":117,"brand":"AB","event":"America's Best - Bel Air - Challenge","city":"Bel Air","state":"MD","start":"2/28/2027","end":"2/28/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.5357,"lng":-76.3483,"month":"Feb 2027"},{"num":118,"brand":"CS","event":"CHEERSPORT - Virtual Spring II","city":"Louisville","state":"KY","start":"3/4/2027","end":"3/23/2027","dist":"< 2000 mi","housing":"Not Listed","lat":38.2527,"lng":-85.7585,"month":"Mar 2027"},{"num":119,"brand":"ALO","event":"Aloha - Grand Nationals - DI/DII","city":"Phoenix","state":"AZ","start":"3/5/2027","end":"3/7/2027","dist":"< 1250 mi","housing":"Housing Required","lat":33.4484,"lng":-112.074,"month":"Mar 2027"},{"num":120,"brand":"MAC","event":"Mid-Atlantic Championship - Grand Nationals - DI/DII","city":"Wildwood","state":"NJ","start":"3/5/2027","end":"3/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":38.9918,"lng":-74.8127,"month":"Mar 2027"},{"num":121,"brand":"GLCC","event":"GLCC - Grand Nationals","city":"Schaumburg","state":"IL","start":"3/6/2027","end":"3/7/2027","dist":"< 1750 mi","housing":"Housing Required","lat":42.0334,"lng":-88.0834,"month":"Mar 2027"},{"num":122,"brand":"ASC","event":"ASC - Cincy - Showdown","city":"Cincinnati","state":"OH","start":"3/6/2027","end":"3/7/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":39.1031,"lng":-84.512,"month":"Mar 2027"},{"num":123,"brand":"AC","event":"The American Royale - Sevierville - Nationals - DI/DII","city":"Sevierville","state":"TN","start":"3/6/2027","end":"3/7/2027","dist":"< 2250 mi","housing":"Housing Rewards","lat":35.8681,"lng":-83.5618,"month":"Mar 2027"},{"num":124,"brand":"OU","event":"One Up - All Star Prep Nationals - DI/DII","city":"College Park","state":"GA","start":"3/6/2027","end":"3/6/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":33.6534,"lng":-84.4496,"month":"Mar 2027"},{"num":125,"brand":"DDC","event":"Double Down - Concord Nationals - DI/DII","city":"Concord","state":"NC","start":"3/6/2027","end":"3/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":35.4088,"lng":-80.5796,"month":"Mar 2027"},{"num":126,"brand":"ASC","event":"ASC - Clash of the Titans - Baltimore - Showdown - DI/DII","city":"Baltimore","state":"MD","start":"3/6/2027","end":"3/7/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":39.2904,"lng":-76.6122,"month":"Mar 2027"},{"num":127,"brand":"JF","event":"JAMfest - Atlanta - Classic - DI/DII","city":"College Park","state":"GA","start":"3/7/2027","end":"3/7/2027","dist":"< 2250 mi","housing":"Not Listed","lat":33.6534,"lng":-84.4496,"month":"Mar 2027"},{"num":128,"brand":"CS","event":"CHEERSPORT - Reading - Classic","city":"Reading","state":"PA","start":"3/7/2027","end":"3/7/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":40.3356,"lng":-75.9269,"month":"Mar 2027"},{"num":129,"brand":"SF","event":"Spirit Fest - Grand Nationals - DI/DII","city":"Providence","state":"RI","start":"3/12/2027","end":"3/14/2027","dist":"< 2500 mi","housing":"Housing Required","lat":41.824,"lng":-71.4128,"month":"Mar 2027"},{"num":130,"brand":"PW","event":"PacWest - Utah - Challenge - DI/DII","city":"Farmington","state":"UT","start":"3/13/2027","end":"3/13/2027","dist":"< 750 mi","housing":"Housing Offered","lat":40.9805,"lng":-111.8874,"month":"Mar 2027"},{"num":131,"brand":"SS","event":"Spirit Sports - Iowa - Nationals","city":"Coralville","state":"IA","start":"3/13/2027","end":"3/14/2027","dist":"< 1750 mi","housing":"Housing Offered","lat":41.6611,"lng":-91.5799,"month":"Mar 2027"},{"num":132,"brand":"ASC","event":"CSG - Chicago - Showdown","city":"Chicago","state":"IL","start":"3/13/2027","end":"3/14/2027","dist":"< 1750 mi","housing":"Housing Required","lat":41.8781,"lng":-87.6298,"month":"Mar 2027"},{"num":133,"brand":"ACP","event":"Cheer Power - Texas State - Showdown - DI/DII","city":"Galveston","state":"TX","start":"3/13/2027","end":"3/14/2027","dist":"< 2000 mi","housing":"Housing Rewards","lat":29.3013,"lng":-94.7977,"month":"Mar 2027"},{"num":134,"brand":"ACP","event":"Cheer Power - Grand Nationals - DI/DII","city":"Columbus","state":"OH","start":"3/13/2027","end":"3/14/2027","dist":"< 2250 mi","housing":"Housing Required","lat":39.9612,"lng":-82.9988,"month":"Mar 2027"},{"num":135,"brand":"DDC","event":"Double Down - Birmingham - Grand Nationals - DI/DII","city":"Birmingham","state":"AL","start":"3/13/2027","end":"3/14/2027","dist":"< 2250 mi","housing":"Housing Rewards","lat":33.5186,"lng":-86.8104,"month":"Mar 2027"},{"num":136,"brand":"JF","event":"JAMfest - Charlotte - Classic - DI/DII","city":"Charlotte","state":"NC","start":"3/13/2027","end":"3/13/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":35.2271,"lng":-80.8431,"month":"Mar 2027"},{"num":137,"brand":"ALO","event":"Aloha - Richmond - Showdown - DI/DII","city":"Richmond","state":"VA","start":"3/13/2027","end":"3/13/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":37.5407,"lng":-77.436,"month":"Mar 2027"},{"num":138,"brand":"ACP","event":"Cheer Power - Philly - Showdown - DI/DII","city":"Philadelphia","state":"PA","start":"3/13/2027","end":"3/13/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9526,"lng":-75.1652,"month":"Mar 2027"},{"num":139,"brand":"EN","event":"Encore - Louisville - Showdown","city":"TBD","state":"KY","start":"3/13/2027","end":"3/14/2027","dist":"< 2250 mi","housing":"Housing Rewards","lat":37.8393,"lng":-84.27,"month":"Mar 2027"},{"num":140,"brand":"OU","event":"One Up - Bellevue - Nationals - DI/DII","city":"Bellevue","state":"WA","start":"3/20/2027","end":"3/21/2027","dist":"Local (< 50 mi)","housing":"Housing Required","lat":47.6101,"lng":-122.2015,"month":"Mar 2027"},{"num":141,"brand":"CS","event":"CHEERSPORT - Nor Cal - Classic - DI/DII","city":"Davis","state":"CA","start":"3/20/2027","end":"3/20/2027","dist":"< 750 mi","housing":"Housing Offered","lat":38.5449,"lng":-121.7405,"month":"Mar 2027"},{"num":142,"brand":"CS","event":"CHEERSPORT - Phoenix - Classic - DI/DII","city":"Phoenix","state":"AZ","start":"3/20/2027","end":"3/20/2027","dist":"< 1250 mi","housing":"Housing Offered","lat":33.4484,"lng":-112.074,"month":"Mar 2027"},{"num":143,"brand":"ACP","event":"Cheer Power - Canton - Disco Showdown","city":"Canton","state":"OH","start":"3/20/2027","end":"3/20/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":40.7989,"lng":-81.3784,"month":"Mar 2027"},{"num":144,"brand":"ATH","event":"Athletic Championships - Atlanta - Nationals - DI/DII","city":"College Park","state":"GA","start":"3/20/2027","end":"3/21/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":33.6534,"lng":-84.4496,"month":"Mar 2027"},{"num":145,"brand":"ATH","event":"Athletic Championships - Fort Walton Beach - Nationals","city":"Fort Walton Beach","state":"FL","start":"3/20/2027","end":"3/21/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":30.4057,"lng":-86.6188,"month":"Mar 2027"},{"num":146,"brand":"ALO","event":"Aloha - Syracuse - Showdown - DI/DII","city":"Syracuse","state":"NY","start":"3/20/2027","end":"3/20/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":43.0481,"lng":-76.1474,"month":"Mar 2027"},{"num":147,"brand":"CL","event":"CANAM - Grand Nationals - DI/DII","city":"Myrtle Beach","state":"SC","start":"3/20/2027","end":"3/21/2027","dist":"< 2500 mi","housing":"Housing Required","lat":33.689,"lng":-78.8867,"month":"Mar 2027"},{"num":148,"brand":"ACDA","event":"ACDA Reach the Beach - Grand Nationals - DI / Worlds","city":"Ocean City","state":"MD","start":"3/20/2027","end":"3/21/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":38.3365,"lng":-75.0849,"month":"Mar 2027"},{"num":149,"brand":"AC","event":"The American Open - Orlando - Nationals - DI/DII","city":"Orlando","state":"FL","start":"3/20/2027","end":"3/21/2027","dist":"< 2750 mi","housing":"Housing Required","lat":28.5383,"lng":-81.3792,"month":"Mar 2027"},{"num":150,"brand":"GRV","event":"One Up - Grand Nationals - DI/DII","city":"Nashville","state":"TN","start":"4/2/2027","end":"4/4/2027","dist":"< 2000 mi","housing":"Housing Required","lat":36.1627,"lng":-86.7816,"month":"Apr 2027"},{"num":151,"brand":"STS","event":"Sea to Sky - International Cheer Championship","city":"Vancouver","state":"BC","start":"4/3/2027","end":"4/4/2027","dist":"< 150 mi","housing":"Housing Rewards","lat":49.2827,"lng":-123.1207,"month":"Apr 2027"},{"num":152,"brand":"AC","event":"The American Showcase DI & DII","city":"Anaheim","state":"CA","start":"4/3/2027","end":"4/4/2027","dist":"< 1000 mi","housing":"Housing Required","lat":33.8353,"lng":-117.9145,"month":"Apr 2027"},{"num":153,"brand":"CS","event":"CHEERSPORT - Toms River - Classic","city":"Toms River","state":"NJ","start":"4/3/2027","end":"4/3/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9537,"lng":-74.1979,"month":"Apr 2027"},{"num":154,"brand":"CS","event":"CHEERSPORT - Boston - Classic","city":"Boston","state":"MA","start":"4/3/2027","end":"4/3/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":42.3601,"lng":-71.0589,"month":"Apr 2027"},{"num":155,"brand":"ASC","event":"ASC - Clash of the Titans - Tampa - Showdown - DI/DII","city":"Tampa","state":"FL","start":"4/10/2027","end":"4/11/2027","dist":"< 2750 mi","housing":"Housing Rewards","lat":27.9506,"lng":-82.4572,"month":"Apr 2027"},{"num":156,"brand":"NCA","event":"NCA - Daytona Beach - Classic- DI/DII","city":"Daytona Beach","state":"FL","start":"4/11/2027","end":"4/11/2027","dist":"< 2750 mi","housing":"Housing Offered","lat":29.2108,"lng":-81.0228,"month":"Apr 2027"},{"num":157,"brand":"ALO","event":"Aloha - Toronto - Showdown","city":"TBD","state":"NB","start":"TBD","end":"TBD","dist":"< 2750 mi","housing":"Housing Offered","lat":46.5653,"lng":-66.4619,"month":""},{"num":158,"brand":"UCA","event":"UDA - Rocky Mountain Dance Challenge","city":"Broomfield","state":"CO","start":"TBD","end":"TBD","dist":"< 1250 mi","housing":"Housing Offered","lat":39.9205,"lng":-105.0867,"month":""},{"num":159,"brand":"CS","event":"CHEERSPORT - Mississippi - Classic - DI/DII","city":"TBD","state":"MS","start":"TBD","end":"TBD","dist":"< 2250 mi","housing":"Housing Offered","lat":32.3547,"lng":-89.3985,"month":""},{"num":160,"brand":"ALO","event":"Aloha - Indy - Showdown","city":"Indianapolis","state":"IN","start":"TBD","end":"TBD","dist":"< 2000 mi","housing":"Housing Offered","lat":39.7684,"lng":-86.1581,"month":""},{"num":161,"brand":"ACP","event":"Cheer Power - Kansas - Showdown","city":"TBD","state":"OK","start":"TBD","end":"TBD","dist":"< 1750 mi","housing":"Housing Offered","lat":35.4676,"lng":-97.5164,"month":""},{"num":162,"brand":"EN","event":"Encore - Nor Cal - Showdown - DI/DII","city":"TBD","state":"CA","start":"TBD","end":"TBD","dist":"< 1000 mi","housing":"Housing Offered","lat":36.7783,"lng":-119.4179,"month":""},{"num":163,"brand":"UCA/UDA","event":"UCA/UDA - Desert Southwest Regional","city":"Gilbert","state":"AZ","start":"11/14/2026","end":"11/14/2026","dist":"< 1250 mi","housing":"Housing Offered","lat":33.3528,"lng":-111.789,"month":"Nov 2026"},{"num":164,"brand":"NCA","event":"NCA - North Texas Classic - DI/DII","city":"Fort Worth","state":"TX","start":"11/14/2026","end":"11/14/2026","dist":"< 1750 mi","housing":"Housing Offered","lat":32.7555,"lng":-97.3308,"month":"Nov 2026"},{"num":165,"brand":"CSG","event":"CSG - Peoria - Challenge","city":"Peoria","state":"IL","start":"11/7/2026","end":"11/7/2026","dist":"< 1750 mi","housing":"Housing Offered","lat":40.6936,"lng":-89.589,"month":"Nov 2026"},{"num":166,"brand":"CSG","event":"CSG - Indy - Challenge","city":"TBD","state":"IN","start":"11/14/2026","end":"11/14/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":40.2672,"lng":-86.1349,"month":"Nov 2026"},{"num":167,"brand":"ACP","event":"Cheer Power - San Antonio - Halloween - Challenge","city":"San Antonio","state":"TX","start":"10/24/2026","end":"10/24/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":29.4241,"lng":-98.4936,"month":"Oct 2026"},{"num":168,"brand":"UCA/UDA","event":"UCA/UDA - Mid-South Regional","city":"Memphis","state":"TN","start":"10/25/2026","end":"10/25/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":35.1495,"lng":-90.049,"month":"Oct 2026"},{"num":169,"brand":"CS","event":"CHEERSPORT - Memphis - Classic - DI/DII","city":"Southaven","state":"MS","start":"11/8/2026","end":"11/8/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":34.989,"lng":-90.0126,"month":"Nov 2026"},{"num":170,"brand":"NCA","event":"NCA - Lonestar- Classic - DI/DII","city":"Rosenberg","state":"TX","start":"11/14/2026","end":"11/15/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":29.5572,"lng":-95.8083,"month":"Nov 2026"},{"num":171,"brand":"VAR","event":"Varsity - Galveston - Showcase","city":"Galveston","state":"TX","start":"11/7/2026","end":"11/7/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":29.3013,"lng":-94.7977,"month":"Nov 2026"},{"num":172,"brand":"VCS","event":"VCS - Virtual Fall Showcase","city":"Louisville","state":"KY","start":"10/25/2026","end":"11/18/2026","dist":"Virtual","housing":"Not Listed","lat":38.2527,"lng":-85.7585,"month":"Oct 2026"},{"num":173,"brand":"UCA/UDA","event":"UCA/UDA - Magnolia/Mississippi Dance - Regional - DII/Rec","city":"Jackson","state":"MS","start":"11/14/2026","end":"11/14/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":32.2988,"lng":-90.1848,"month":"Nov 2026"},{"num":174,"brand":"ALO","event":"Aloha - Louisiana - Showdown","city":"Baton Rouge","state":"LA","start":"11/14/2026","end":"11/14/2026","dist":"< 2250 mi","housing":"Housing Offered","lat":30.4515,"lng":-91.1871,"month":"Nov 2026"},{"num":175,"brand":"SU","event":"Spirit Unlimited - York - Challenge","city":"York","state":"PA","start":"11/14/2026","end":"11/14/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9626,"lng":-76.7277,"month":"Nov 2026"},{"num":176,"brand":"ACP","event":"Cheer Power - Tulsa - Disco Showdown - DI/DII","city":"TBD","state":"OK","start":"TBD","end":"TBD","dist":"< 1750 mi","housing":"Housing Offered","lat":35.4676,"lng":-97.5164,"month":""},{"num":177,"brand":"CS","event":"CHEERSPORT - Raleigh - Classic - DI/DII","city":"Raleigh","state":"NC","start":"11/8/2026","end":"11/8/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":35.7796,"lng":-78.6382,"month":"Nov 2026"},{"num":178,"brand":"JF","event":"JAMfest Japan - Fall","city":"Tachikawa, Tokyo","state":"nan","start":"11/7/2026","end":"11/8/2026","dist":"< 5000 mi","housing":"Not Listed","lat":35.6938,"lng":139.4185,"month":"Nov 2026"},{"num":179,"brand":"JF","event":"Scottish JAM","city":"Edinburgh","state":"nan","start":"5/15/2027","end":"5/16/2027","dist":"< 4500 mi","housing":"Housing Offered","lat":55.9533,"lng":-3.1883,"month":"May 2027"},{"num":180,"brand":"UCA/UDA","event":"UCA/UDA - Magnolia/Mississippi Dance - Regional - DI","city":"Jackson","state":"MS","start":"11/15/2026","end":"11/15/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":32.2988,"lng":-90.1848,"month":"Nov 2026"},{"num":181,"brand":"JF","event":"JAMfest - San Antonio - Classic - DI/DII","city":"San Antonio","state":"TX","start":"11/21/2026","end":"11/21/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":29.4241,"lng":-98.4936,"month":"Nov 2026"},{"num":182,"brand":"UCA","event":"UCA - Lexington - Classic","city":"Lexington","state":"KY","start":"11/22/2026","end":"11/22/2026","dist":"< 2000 mi","housing":"Housing Offered","lat":38.0406,"lng":-84.5037,"month":"Nov 2026"},{"num":183,"brand":"SS","event":"Spirit Sports - Worcester - Nationals - DI/DII","city":"Worcester","state":"MA","start":"12/12/2026","end":"12/13/2026","dist":"< 2500 mi","housing":"Housing Offered","lat":42.2626,"lng":-71.8023,"month":"Dec 2026"},{"num":184,"brand":"NCA","event":"NCA - Holiday - Classic- DI/DII","city":"Dallas","state":"TX","start":"12/13/2026","end":"12/13/2026","dist":"< 1750 mi","housing":"Housing Rewards","lat":32.7767,"lng":-96.797,"month":"Dec 2026"},{"num":185,"brand":"WSF","event":"WSF - Virtual Winter I","city":"Louisville","state":"KY","start":"12/18/2026","end":"12/18/2026","dist":"Virtual","housing":"Not Listed","lat":38.2527,"lng":-85.7585,"month":"Dec 2026"},{"num":186,"brand":"NCA","event":"NCA - Richmond - Classic","city":"Richmond","state":"VA","start":"1/9/2027","end":"1/9/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":37.5407,"lng":-77.436,"month":"Jan 2027"},{"num":187,"brand":"NCA","event":"NCA - Concord - Classic - DI/DII","city":"Concord","state":"NC","start":"1/9/2027","end":"1/9/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":35.4088,"lng":-80.5796,"month":"Jan 2027"},{"num":188,"brand":"NCA","event":"NCA - Milwaukee - Classic","city":"Milwaukee","state":"WI","start":"1/10/2027","end":"1/10/2027","dist":"< 1750 mi","housing":"Housing Rewards","lat":43.0389,"lng":-87.9065,"month":"Jan 2027"},{"num":189,"brand":"NCA","event":"NCA - Tulsa - Classic- Dl/Dll","city":"Tulsa","state":"OK","start":"TBD","end":"TBD","dist":"< 1750 mi","housing":"Housing Offered","lat":36.154,"lng":-95.9928,"month":""},{"num":190,"brand":"AC","event":"The American Masters - Baltimore - Nationals - DI/DII","city":"Baltimore","state":"MD","start":"1/23/2027","end":"1/24/2027","dist":"< 2500 mi","housing":"Housing Required","lat":39.2904,"lng":-76.6122,"month":"Jan 2027"},{"num":191,"brand":"JF","event":"JAMfest - York - Classic","city":"York","state":"PA","start":"1/23/2027","end":"1/23/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9626,"lng":-76.7277,"month":"Jan 2027"},{"num":192,"brand":"SS","event":"Spirit Sports - Colorado Springs - Nationals - DI/DII","city":"Colorado Springs","state":"CO","start":"1/23/2027","end":"1/24/2027","dist":"< 1250 mi","housing":"Housing Rewards","lat":38.8339,"lng":-104.8214,"month":"Jan 2027"},{"num":193,"brand":"JF","event":"JAMfest - Utah - Classic - DI/DII","city":"Sandy","state":"UT","start":"1/23/2027","end":"1/23/2027","dist":"< 750 mi","housing":"Housing Offered","lat":40.5649,"lng":-111.8389,"month":"Jan 2027"},{"num":194,"brand":"NCA","event":"NCA - Toms River - Classic","city":"Toms River","state":"NJ","start":"1/30/2027","end":"1/30/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.9537,"lng":-74.1979,"month":"Jan 2027"},{"num":195,"brand":"AC","event":"The American Gateway - St. Louis - Nationals","city":"St. Louis","state":"MO","start":"1/30/2027","end":"1/31/2027","dist":"< 1750 mi","housing":"Housing Rewards","lat":38.627,"lng":-90.1994,"month":"Jan 2027"},{"num":196,"brand":"AC","event":"The American Superstarz - Raleigh - Nationals - DI/DII","city":"Raleigh","state":"NC","start":"1/30/2027","end":"2/1/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":35.7796,"lng":-78.6382,"month":"Jan 2027"},{"num":197,"brand":"SS","event":"Spirit Sports - Kansas City - Nationals","city":"Kansas City","state":"MO","start":"2/6/2027","end":"2/7/2027","dist":"< 1500 mi","housing":"Housing Rewards","lat":39.0997,"lng":-94.5786,"month":"Feb 2027"},{"num":198,"brand":"MGS","event":"Mardi Gras - Beaumont - Classic - DI/DII","city":"Beaumont","state":"TX","start":"2/7/2027","end":"2/7/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":30.0802,"lng":-94.1266,"month":"Feb 2027"},{"num":199,"brand":"SU","event":"Spirit Unlimited - Greenbelt - Challenge","city":"Greenbelt","state":"MD","start":"TBD","end":"TBD","dist":"< 2500 mi","housing":"Housing Offered","lat":39.0046,"lng":-76.8755,"month":""},{"num":200,"brand":"JF","event":"JAMfest - Durham - Classic","city":"Durham","state":"NH","start":"2/13/2027","end":"2/13/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":43.134,"lng":-70.9265,"month":"Feb 2027"},{"num":201,"brand":"NCA","event":"NCA - Lexington - Classic","city":"Lexington","state":"KY","start":"2/13/2027","end":"2/13/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":38.0406,"lng":-84.5037,"month":"Feb 2027"},{"num":202,"brand":"JF","event":"JAMfest Rise of the Regions","city":"Telford","state":"nan","start":"2/13/2027","end":"2/14/2027","dist":"< 5000 mi","housing":"Housing Offered","lat":52.6766,"lng":-2.4469,"month":"Feb 2027"},{"num":203,"brand":"NCA","event":"NCA - San Marcos - Classic - DI/DII","city":"San Marcos","state":"TX","start":"2/13/2027","end":"2/13/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":29.8833,"lng":-97.9414,"month":"Feb 2027"},{"num":204,"brand":"SS","event":"Spirit Sports - Hershey - Nationals - DI/DII","city":"Hershey","state":"PA","start":"2/13/2027","end":"2/14/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":40.2862,"lng":-76.6499,"month":"Feb 2027"},{"num":205,"brand":"JF","event":"JAMfest - Springfield - Classic","city":"Springfield","state":"MA","start":"TBD","end":"TBD","dist":"< 2500 mi","housing":"Housing Offered","lat":42.1015,"lng":-72.5898,"month":""},{"num":206,"brand":"SS","event":"Spirit Sports - Canadian Clash","city":"Ottawa","state":"ON","start":"2/20/2027","end":"2/21/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":45.4215,"lng":-75.6972,"month":"Feb 2027"},{"num":207,"brand":"SS","event":"Spirit Sports - Texas - Nationals - DI/DII","city":"TBD","state":"TX","start":"2/27/2027","end":"2/28/2027","dist":"TBD","housing":"Housing Required","lat":31.9686,"lng":-99.9018,"month":"Feb 2027"},{"num":208,"brand":"JF","event":"JAMfest - Fredericksburg - Classic","city":"Fredericksburg","state":"VA","start":"2/27/2027","end":"2/27/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":38.3032,"lng":-77.4605,"month":"Feb 2027"},{"num":209,"brand":"SS","event":"Spirit Sports - Indianapolis - Nationals","city":"Indianapolis","state":"IN","start":"3/6/2027","end":"3/7/2027","dist":"< 2000 mi","housing":"Housing Rewards","lat":39.7684,"lng":-86.1581,"month":"Mar 2027"},{"num":210,"brand":"JF","event":"JAMfest - Fairmont - Classic","city":"Fairmont","state":"WV","start":"3/6/2027","end":"3/6/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":39.4851,"lng":-80.1425,"month":"Mar 2027"},{"num":211,"brand":"OU","event":"One Up - Kenner - Nationals","city":"Kenner","state":"LA","start":"3/6/2027","end":"3/7/2027","dist":"< 2250 mi","housing":"Housing Offered","lat":29.9941,"lng":-90.2417,"month":"Mar 2027"},{"num":212,"brand":"OU","event":"One Up - Oklahoma City - Nationals - DI/DII","city":"Oklahoma City","state":"OK","start":"3/6/2027","end":"3/6/2027","dist":"< 1750 mi","housing":"Housing Offered","lat":35.4676,"lng":-97.5164,"month":"Mar 2027"},{"num":213,"brand":"JF","event":"JAMfest - Northern JAM","city":"Lancashire, England","state":"nan","start":"3/13/2027","end":"3/14/2027","dist":"< 5000 mi","housing":"Housing Offered","lat":53.759,"lng":-2.7044,"month":"Mar 2027"},{"num":214,"brand":"NCA","event":"NCA - All-Star National Championship","city":"Houston","state":"TX","start":"3/19/2027","end":"3/21/2027","dist":"< 2000 mi","housing":"Housing Required","lat":29.7604,"lng":-95.3698,"month":"Mar 2027"},{"num":215,"brand":"OU","event":"One Up - Kansas City - Nationals","city":"Kansas City","state":"KS","start":"3/20/2027","end":"3/20/2027","dist":"< 1500 mi","housing":"Housing Offered","lat":39.1142,"lng":-94.6275,"month":"Mar 2027"},{"num":216,"brand":"SS","event":"Spirit Sports - Pittsburgh - Nationals","city":"Moon Township","state":"PA","start":"3/20/2027","end":"3/21/2027","dist":"< 2250 mi","housing":"Housing Rewards","lat":40.5076,"lng":-80.212,"month":"Mar 2027"},{"num":217,"brand":"CS","event":"CHEERSPORT - Arizona - Classic - DI/DII","city":"TBD","state":"AZ","start":"TBD","end":"TBD","dist":"TBD","housing":"Housing Offered","lat":34.0489,"lng":-111.0937,"month":""},{"num":218,"brand":"SU","event":"Spirit Unlimited - Baltimore - Challenge","city":"Baltimore","state":"MD","start":"3/20/2027","end":"3/20/2027","dist":"< 2500 mi","housing":"Housing Offered","lat":39.2904,"lng":-76.6122,"month":"Mar 2027"},{"num":219,"brand":"VCS","event":"VCS - Virtual Spring Showcase","city":"Louisville","state":"KY","start":"TBD","end":"TBD","dist":"Virtual","housing":"Not Listed","lat":38.2527,"lng":-85.7585,"month":""},{"num":220,"brand":"SS","event":"The Ultimate Battle","city":"Myrtle Beach","state":"SC","start":"4/2/2027","end":"4/2/2027","dist":"< 2500 mi","housing":"Housing Required","lat":33.689,"lng":-78.8867,"month":"Apr 2027"},{"num":221,"brand":"OU","event":"One Up - Houston - Nationals - DI/DII","city":"Rosenberg","state":"TX","start":"4/3/2027","end":"4/3/2027","dist":"< 2000 mi","housing":"Housing Offered","lat":29.5572,"lng":-95.8083,"month":"Apr 2027"},{"num":222,"brand":"SS","event":"Spirit Sports - Myrtle Beach- Nationals - DI/DII","city":"Myrtle Beach","state":"SC","start":"4/3/2027","end":"4/4/2027","dist":"< 2500 mi","housing":"Housing Required","lat":33.689,"lng":-78.8867,"month":"Apr 2027"},{"num":223,"brand":"AC","event":"The American Legacy - Springfield - Nationals - DI/DII","city":"Springfield","state":"MA","start":"4/10/2027","end":"4/11/2027","dist":"< 2500 mi","housing":"Housing Rewards","lat":42.1015,"lng":-72.5898,"month":"Apr 2027"}]

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route("/api/comps")
def api_comps():
    return jsonify(COMPETITIONS)

@app.route("/")
def index():
    return HTML

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CCN Cheer Competitions 2026-27</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css"/>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; display: flex; height: 100vh; overflow: hidden; }

#sidebar {
  width: 300px; min-width: 300px; background: #fff;
  display: flex; flex-direction: column; overflow: hidden;
  box-shadow: 2px 0 12px rgba(0,0,0,.1); z-index: 1000;
}
#sidebar-header {
  background: linear-gradient(135deg, #1e3a5f, #1d4ed8);
  color: #fff; padding: 16px; flex-shrink: 0;
}
#sidebar-header h1 { font-size: 15px; font-weight: 700; }
#sidebar-header p  { font-size: 11px; opacity: .8; margin-top: 3px; }
#count-badge {
  display: inline-block; background: rgba(255,255,255,.2);
  border-radius: 20px; padding: 3px 12px; font-size: 11px;
  font-weight: 600; margin-top: 8px;
}
#sidebar-body { flex: 1; overflow-y: auto; padding: 12px; }
#sidebar-body::-webkit-scrollbar { width: 4px; }
#sidebar-body::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 2px; }

.search-wrap { position: relative; margin-bottom: 12px; }
.search-wrap input {
  width: 100%; border: 1.5px solid #e2e8f0; border-radius: 8px;
  padding: 8px 10px 8px 32px; font-size: 12.5px; outline: none;
  background: #f8fafc; color: #1e293b; transition: border-color .15s;
}
.search-wrap input:focus { border-color: #3b82f6; background: #fff; }
.search-wrap svg {
  position: absolute; left: 9px; top: 50%; transform: translateY(-50%);
  width: 15px; height: 15px; color: #94a3b8; pointer-events: none;
}

.toggle-row {
  display: flex; background: #f1f5f9; border-radius: 8px;
  padding: 3px; margin-bottom: 14px; gap: 3px;
}
.toggle-row button {
  flex: 1; border: none; background: transparent; border-radius: 6px;
  padding: 6px 4px; font-size: 11px; font-weight: 600; cursor: pointer;
  color: #64748b; transition: all .15s;
}
.toggle-row button.active {
  background: #fff; color: #1d4ed8;
  box-shadow: 0 1px 4px rgba(0,0,0,.12);
}

.filter-section { margin-bottom: 14px; }
.filter-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .8px; color: #94a3b8; margin-bottom: 6px;
  display: flex; justify-content: space-between; align-items: center;
}
.clear-btn {
  font-size: 10px; font-weight: 600; color: #3b82f6;
  text-transform: none; letter-spacing: 0;
  padding: 2px 7px; border-radius: 5px; background: #eff6ff; cursor: pointer;
}
.clear-btn:hover { background: #dbeafe; }
.chips { display: flex; flex-wrap: wrap; gap: 5px; }
.chip {
  border: 1.5px solid #e2e8f0; border-radius: 20px; padding: 3px 10px;
  font-size: 11px; font-weight: 500; cursor: pointer; color: #475569;
  background: #fff; user-select: none; white-space: nowrap; transition: all .15s;
}
.chip:hover { border-color: #93c5fd; color: #1d4ed8; background: #eff6ff; }
.chip.on { border-color: transparent; color: #fff; font-weight: 600; }

select.brand-sel {
  width: 100%; border: 1.5px solid #e2e8f0; border-radius: 8px;
  padding: 7px 10px; font-size: 12px; background: #f8fafc;
  color: #1e293b; outline: none; cursor: pointer;
}
select.brand-sel:focus { border-color: #3b82f6; }

.reset-btn {
  width: 100%; margin-top: 4px; padding: 6px;
  border: 1.5px solid #fca5a5; border-radius: 8px; background: #fff;
  color: #dc2626; font-size: 11px; font-weight: 600; cursor: pointer;
}
.reset-btn:hover { background: #fee2e2; }

.legend { border-top: 1px solid #f1f5f9; padding-top: 12px; margin-top: 10px; }
.legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; font-size: 11.5px; color: #475569; }
.legend-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; border: 2px solid rgba(0,0,0,.15); }

#map { flex: 1; }

.leaflet-popup-content-wrapper {
  border-radius: 12px !important; padding: 0 !important;
  overflow: hidden !important; box-shadow: 0 8px 30px rgba(0,0,0,.18) !important;
}
.leaflet-popup-content { margin: 0 !important; }
.leaflet-popup-tip { background: #1e3a5f !important; }
.popup-head {
  background: linear-gradient(135deg, #1e3a5f, #1d4ed8);
  color: #fff; padding: 12px 14px; font-size: 13px; font-weight: 600; line-height: 1.4;
  min-width: 220px; max-width: 280px;
}
.popup-body { padding: 10px 14px 12px; background: #fff; }
.popup-row { display: flex; gap: 7px; margin-bottom: 7px; font-size: 12px; color: #1e293b; align-items: flex-start; }
.popup-row .ico { color: #64748b; flex-shrink: 0; }
.badge {
  display: inline-block; border-radius: 6px; padding: 2px 9px;
  font-size: 11px; font-weight: 600;
}
.req { background: #fee2e2; color: #dc2626; }
.off { background: #dbeafe; color: #1d4ed8; }
.rew { background: #dcfce7; color: #16a34a; }
.not { background: #f1f5f9; color: #6b7280; }
.dist-badge { background: #f1f5f9; color: #1e293b; }
</style>
</head>
<body>

<div id="sidebar">
  <div id="sidebar-header">
    <h1>🏆 CCN Cheer Competitions</h1>
    <p>2026–27 Season &middot; Home: Bellevue, WA</p>
    <div id="count-badge">Showing <span id="vis-count">–</span> of <span id="total-count">–</span></div>
  </div>
  <div id="sidebar-body">

    <div class="search-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
      </svg>
      <input type="text" id="search" placeholder="Search events, cities, brands…" oninput="applyFilters()">
    </div>

    <div class="toggle-row">
      <button id="btn-housing"  class="active" onclick="setMode('housing')">🏨 By Housing</button>
      <button id="btn-distance" onclick="setMode('distance')">📍 By Distance</button>
    </div>

    <div class="filter-section">
      <div class="filter-label">Month <span class="clear-btn" onclick="clearGroup('month')">Clear</span></div>
      <div class="chips" id="month-chips"></div>
    </div>
    <div class="filter-section">
      <div class="filter-label">Distance from Bellevue <span class="clear-btn" onclick="clearGroup('dist')">Clear</span></div>
      <div class="chips" id="dist-chips"></div>
    </div>
    <div class="filter-section">
      <div class="filter-label">Housing <span class="clear-btn" onclick="clearGroup('housing')">Clear</span></div>
      <div class="chips" id="housing-chips"></div>
    </div>
    <div class="filter-section">
      <div class="filter-label">Brand</div>
      <select class="brand-sel" id="brand-sel" onchange="applyFilters()">
        <option value="">All Brands</option>
      </select>
    </div>

    <button class="reset-btn" onclick="resetAll()">↺ Reset All Filters</button>

    <div class="legend">
      <div class="filter-label" style="cursor:default">Legend</div>
      <div id="legend-items"></div>
    </div>
  </div>
</div>

<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<script>
const HOUSING_COLOR = {
  'Housing Required': '#dc2626',
  'Housing Offered':  '#3b82f6',
  'Housing Rewards':  '#16a34a',
  'Not Listed':       '#9ca3af',
};
const HOUSING_LABEL = {
  'Housing Required': '🔴 Stay to Play (Required)',
  'Housing Offered':  '🔵 Housing Offered',
  'Housing Rewards':  '🟢 Housing Rewards',
  'Not Listed':       '⚪ Not Listed',
};
const DIST_ORDER = [
  'Local (< 50 mi)','< 50 mi','< 150 mi','< 750 mi','< 1000 mi','< 1250 mi',
  '< 1500 mi','< 1750 mi','< 2000 mi','< 2250 mi','< 2500 mi','< 2750 mi',
  '< 4500 mi','< 5000 mi','TBD','Virtual'
];
const DIST_COLOR = {
  'Local (< 50 mi)':'#15803d','< 50 mi':'#15803d','< 150 mi':'#16a34a',
  '< 750 mi':'#22c55e','< 1000 mi':'#84cc16','< 1250 mi':'#eab308',
  '< 1500 mi':'#f97316','< 1750 mi':'#f97316','< 2000 mi':'#ef4444',
  '< 2250 mi':'#dc2626','< 2500 mi':'#b91c1c','< 2750 mi':'#991b1b',
  '< 4500 mi':'#7f1d1d','< 5000 mi':'#450a0a','TBD':'#9ca3af','Virtual':'#a855f7'
};
const MONTH_ORDER = [
  'Oct 2026','Nov 2026','Dec 2026','Jan 2027','Feb 2027',
  'Mar 2027','Apr 2027','May 2027'
];

// Map init
const map = L.map('map').setView([38.5, -96], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom: 18
}).addTo(map);

const cluster = L.markerClusterGroup({
  maxClusterRadius: 45,
  iconCreateFunction(c) {
    const n = c.getChildCount(), sz = n < 10 ? 32 : n < 50 ? 38 : 44;
    return L.divIcon({
      html: `<div style="width:${sz}px;height:${sz}px;background:#1d4ed8;border:3px solid #fff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:${sz>36?13:11}px;box-shadow:0 2px 8px rgba(0,0,0,.3)">${n}</div>`,
      className: '', iconSize: [sz, sz], iconAnchor: [sz/2, sz/2]
    });
  }
});
map.addLayer(cluster);

// Home gym marker
const homeIcon = L.divIcon({
  html: '<div style="width:28px;height:28px;background:#fbbf24;border:3px solid #d97706;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 3px 10px rgba(0,0,0,.3)">★</div>',
  className: '', iconSize: [28, 28], iconAnchor: [14, 14], popupAnchor: [0, -16]
});
L.marker([47.6101, -122.2015], { icon: homeIcon, zIndexOffset: 9999 })
  .bindTooltip('<b>🏠 Home Gym — Bellevue, WA</b>', { direction: 'top' })
  .addTo(map);

// State
let ALL = [], colorMode = 'housing';
let selMonths = new Set(), selDist = new Set(), selHousing = new Set();
let selBrand = '', searchVal = '';
let allMarkers = [];

function color(d) {
  return colorMode === 'housing'
    ? (HOUSING_COLOR[d.housing] || '#9ca3af')
    : (DIST_COLOR[d.dist]    || '#9ca3af');
}

function makeIcon(d) {
  const c = color(d);
  return L.divIcon({
    html: `<div style="width:14px;height:14px;background:${c};border:2.5px solid rgba(255,255,255,.9);border-radius:50%;box-shadow:0 1px 5px rgba(0,0,0,.35)"></div>`,
    className: '', iconSize: [14,14], iconAnchor: [7,7], popupAnchor: [0,-9]
  });
}

function popupHtml(d) {
  const hcls = {
    'Housing Required':'req','Housing Offered':'off',
    'Housing Rewards':'rew','Not Listed':'not'
  }[d.housing] || 'not';
  const dates = d.start === d.end ? d.start : `${d.start} – ${d.end}`;
  return `
    <div class="popup-head">${d.event}</div>
    <div class="popup-body">
      <div class="popup-row"><span class="ico">📍</span><div><b>${d.city}, ${d.state}</b></div></div>
      <div class="popup-row"><span class="ico">📅</span><div>${dates}</div></div>
      <div class="popup-row"><span class="ico">🏢</span><div>Brand: <b>${d.brand}</b></div></div>
      <div class="popup-row"><span class="ico">🛣️</span><div><span class="badge dist-badge">${d.dist}</span></div></div>
      <div class="popup-row"><span class="ico">🏨</span><div><span class="badge ${hcls}">${d.housing}</span></div></div>
    </div>`;
}

function buildMarkers() {
  allMarkers = ALL
    .filter(d => d.lat && d.lng && d.lng < 0 && d.lng > -130)
    .map(d => {
      const m = L.marker([d.lat, d.lng], { icon: makeIcon(d) })
        .bindPopup(popupHtml(d), { maxWidth: 300 })
        .bindTooltip(`<b>${d.event}</b><br><span style="color:#64748b">${d.city}, ${d.state}</span>`, { direction: 'top', offset:[0,-8] });
      m._d = d;
      return m;
    });
}

function applyFilters() {
  searchVal = document.getElementById('search').value.toLowerCase();
  selBrand  = document.getElementById('brand-sel').value;

  const visible = allMarkers.filter(m => {
    const d = m._d;
    if (selMonths.size  && !selMonths.has(d.month))   return false;
    if (selDist.size    && !selDist.has(d.dist))       return false;
    if (selHousing.size && !selHousing.has(d.housing)) return false;
    if (selBrand        && d.brand !== selBrand)        return false;
    if (searchVal && !(d.event+d.city+d.state+d.brand).toLowerCase().includes(searchVal)) return false;
    return true;
  });

  visible.forEach(m => m.setIcon(makeIcon(m._d)));
  cluster.clearLayers();
  cluster.addLayers(visible);
  document.getElementById('vis-count').textContent   = visible.length;
}

function setMode(m) {
  colorMode = m;
  document.getElementById('btn-housing').classList.toggle('active',  m === 'housing');
  document.getElementById('btn-distance').classList.toggle('active', m === 'distance');
  buildLegend();
  applyFilters();
}

function toggleChip(set, val, el) {
  set.has(val) ? (set.delete(val), el.classList.remove('on')) : (set.add(val), el.classList.add('on'));
  applyFilters();
}

function clearGroup(g) {
  const map = { month: [selMonths,'#month-chips'], dist: [selDist,'#dist-chips'], housing: [selHousing,'#housing-chips'] };
  const [s, sel] = map[g];
  s.clear();
  document.querySelectorAll(sel + ' .chip').forEach(c => c.classList.remove('on'));
  applyFilters();
}

function resetAll() {
  selMonths.clear(); selDist.clear(); selHousing.clear();
  selBrand = ''; searchVal = '';
  document.getElementById('search').value = '';
  document.getElementById('brand-sel').value = '';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('on'));
  applyFilters();
}

function buildFilters() {
  // months
  const mc = document.getElementById('month-chips');
  MONTH_ORDER.forEach(m => {
    if (!ALL.some(d => d.month === m)) return;
    const c = document.createElement('div');
    c.className = 'chip'; c.textContent = m;
    c.style.setProperty('--on-bg', '#7c3aed');
    c.onclick = () => { toggleChip(selMonths, m, c); };
    c.addEventListener('click', () => c.classList.contains('on') && (c.style.background='#7c3aed', c.style.borderColor='#7c3aed') || (c.style.background='', c.style.borderColor=''));
    mc.appendChild(c);
  });

  // distances
  const dc = document.getElementById('dist-chips');
  DIST_ORDER.forEach(v => {
    if (!ALL.some(d => d.dist === v)) return;
    const c = document.createElement('div');
    c.className = 'chip'; c.textContent = v;
    c.onclick = () => {
      toggleChip(selDist, v, c);
      if (c.classList.contains('on')) { c.style.background = DIST_COLOR[v]||'#64748b'; c.style.borderColor = DIST_COLOR[v]||'#64748b'; }
      else { c.style.background = ''; c.style.borderColor = ''; }
    };
    dc.appendChild(c);
  });

  // housing
  const hc = document.getElementById('housing-chips');
  const housingBg = {
    'Housing Required':'#dc2626','Housing Offered':'#3b82f6',
    'Housing Rewards':'#16a34a','Not Listed':'#9ca3af'
  };
  ['Housing Required','Housing Offered','Housing Rewards','Not Listed'].forEach(h => {
    const c = document.createElement('div');
    c.className = 'chip'; c.textContent = h;
    c.onclick = () => {
      toggleChip(selHousing, h, c);
      if (c.classList.contains('on')) { c.style.background = housingBg[h]; c.style.borderColor = housingBg[h]; }
      else { c.style.background = ''; c.style.borderColor = ''; }
    };
    hc.appendChild(c);
  });

  // brands
  const bs = document.getElementById('brand-sel');
  [...new Set(ALL.map(d => d.brand))].sort().forEach(b => {
    const o = document.createElement('option');
    o.value = b; o.textContent = b;
    bs.appendChild(o);
  });
}

function buildLegend() {
  const el = document.getElementById('legend-items');
  el.innerHTML = '';
  if (colorMode === 'housing') {
    Object.entries(HOUSING_COLOR).forEach(([h, c]) => {
      el.innerHTML += `<div class="legend-item"><div class="legend-dot" style="background:${c}"></div><span>${HOUSING_LABEL[h]}</span></div>`;
    });
  } else {
    [['Local / < 150 mi','#16a34a'],['< 750 mi','#22c55e'],['< 1250 mi','#eab308'],
     ['< 1750 mi','#f97316'],['≥ 2000 mi','#ef4444'],['TBD / Virtual','#9ca3af']
    ].forEach(([lb,c]) => {
      el.innerHTML += `<div class="legend-item"><div class="legend-dot" style="background:${c}"></div><span>${lb}</span></div>`;
    });
  }
  el.innerHTML += `<div class="legend-item"><div style="width:12px;height:12px;background:#fbbf24;border:2px solid #d97706;border-radius:50%;flex-shrink:0"></div><span>🏠 Home Gym (Bellevue, WA)</span></div>`;
}

// Boot
fetch('/api/comps')
  .then(r => r.json())
  .then(data => {
    ALL = data;
    document.getElementById('total-count').textContent = data.length;
    buildFilters();
    buildLegend();
    buildMarkers();
    applyFilters();
  });
</script>
</body>
</html>"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port, debug=False)
