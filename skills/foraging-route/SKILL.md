---
name: foraging-route
description: Solve the shortest walking route from the user's current location through every mapped fruit tree in the vault, and return a map link plus a Google Maps walking link. Use when the user gives coordinates, a Google Maps link, or an address and asks for the route, order, or shortest walk to the apple or plum trees.
---

## Overview

The stops live in the vault note `/Users/mtm/Documents/Obsidian Vault/apples and plums near us.md`, which is the single source of truth for which trees exist.

The route is an open-path travelling salesman problem: start at the user, visit every stop once, and end wherever is shortest.

The public OSRM foot server solves it, and the answer is handed back as links the user can tap on a phone.

This skill reads the vault and writes nothing to it.

Saving a route into a note happens only when the user asks for that separately.

## Step 1: Resolve the start to one decimal position

Turn whatever the user gave into a single `latitude, longitude` pair in decimal degrees.

- Decimal pair such as `47.6204, -122.3112`: use it as given, latitude first.
- Degrees, minutes, seconds such as `47°37'13.4"N 122°18'40.2"W`: convert with degrees + minutes/60 + seconds/3600, and make S latitudes and W longitudes negative.
- Full Google Maps place URL: take the place pin from `!3d<lat>!4d<lon>`, because the `@<lat>,<lon>` segment is only the map's viewport centre and can sit a block away.
- Google Maps URL with no `!3d`/`!4d`: fall back to `@<lat>,<lon>` or a `query=<lat>,<lon>` parameter.
- Short link such as `maps.app.goo.gl/...`: expand it first with `curl --silent --location --output /dev/null --write-out '%{url_effective}' <url>`, then parse the expanded URL as above.
- Street address or place name: geocode it with Nominatim at `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=<address>`, stripping any suite or unit number first because Nominatim fails on them.

Round every coordinate to 6 decimal places, about 4in of precision, and use that same rounded value in the request and in both links.

The step is done when one decimal pair is in hand together with which part of the user's input it came from.

## Step 2: Read the stops from the note

Every `## ` section of the note whose body contains a bare line of the form `<lat>, <lon>` is one stop, named by its heading, and when a section holds more than one such line the first one is the stop.

Sections without such a line, such as Contents, Map, Distances and Best route, are not stops.

Read the note fresh on every run, because trees get added.

The step is done when every stop has a heading and a decimal pair.

OSRM caps a trip at 100 coordinates, so more than 99 stops has to be reported to the user rather than silently truncated.

## Step 3: Call the trip solver

Build one request with the start first and every stop after it, each written longitude first, which is the reverse of how the note and Google write them:

```
https://routing.openstreetmap.de/routed-foot/trip/v1/foot/<start_lon>,<start_lat>;<lon1>,<lat1>;<lon2>,<lat2>?source=first&destination=any&roundtrip=false&overview=false
```

Fetch it with `curl --silent --max-time 20`.

`source=first` pins the walk to the user's position, and dropping it makes the server answer `NotImplemented`, because an open path needs a fixed start.

The routing.openstreetmap.de host serves a real foot profile, while router.project-osrm.org silently answers with driving distances whatever the URL path says.

The step is done when the response has `"code":"Ok"`, and any other code is reported to the user verbatim with the request URL.

## Step 4: Read the visiting order

Parse the JSON with a short script run through `uv run --no-active`, never by eye, and that one throwaway script may also read the note, build the request and build the links in Steps 2 to 5, kept in `$CLAUDE_JOB_DIR/tmp` and never in the vault.

The `waypoints` array stays in the order the coordinates were sent, and each entry's `waypoint_index` is that point's position in the solved walk, so sort by `waypoint_index` to get the order.

`trips[0].legs` holds one leg per consecutive pair in that solved order, and `trips[0].distance` and `trips[0].duration` are the totals in metres and seconds.

Each waypoint's `distance` is how far in metres OSRM snapped that point to the nearest path, and any point, start or stop, snapped more than 15m, about 50ft, gets named in the report because the route then begins or ends somewhere other than the pin.

The step is done when every stop has a position in the order and a leg distance.

## Step 5: Build the links

The map link draws the walk on the OSRM demo frontend, one `loc` per point in solved order, latitude first, with `profile=2` for foot and `center` set to the mean latitude and mean longitude of all the points:

```
https://map.project-osrm.org/?z=14&center=<lat>%2C<lon>&loc=<start_lat>%2C<start_lon>&loc=<lat1>%2C<lon1>&hl=en&alt=0&ly=openstreetmap.de&profile=2
```

The Google Maps link opens turn-by-turn walking directions, with `origin` left out so Maps starts from the phone's live position, the last stop as `destination`, and the stops between as `%7C`-separated `waypoints`, latitude first:

```
https://www.google.com/maps/dir/?api=1&travelmode=walking&destination=<last_lat>,<last_lon>&waypoints=<lat1>,<lon1>%7C<lat2>,<lon2>
```

Leaving `origin` out means Maps walks the solved order from wherever the phone is when the link is opened, so the order is only shortest while the user is still near the start they gave.

Google allows 9 waypoints in the Maps app and only 3 in a mobile browser, so with more than 3 tell the user to open it in the app, and with more than 9 split the walk into consecutive links where each starts at the previous link's last stop.

The step is done when both links are built from the solved order.

## Step 6: Report

Give distances in miles, dividing metres by 1,609.344, rounding to 2 decimal places and writing them squashed like `0.35mi`.

Give the total time rounded to the nearest minute and written compactly like `1h9m`.

Report in this order, one sentence per paragraph:

- the resolved start and which part of the input it came from
- the number of stops read from the note
- the total distance and time, and the stop the walk ends at
- any point snapped more than 15m
- the table of the order
- the app-versus-browser warning when the Google link has more than 3 waypoints
- the map link and the Google Maps link

The legs are rounded one by one, so when they sum to 0.01mi more or less than the total, keep the total computed from the unrounded metres.

| stop | tree | leg |
| --- | --- | --- |
| 1 | <heading> | <miles> |
| total | | <miles> |

Put the map link and the Google Maps link bare on their own lines below the table.
