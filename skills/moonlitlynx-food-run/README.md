# moonlitlynx-food-run

Finds untagged/undated media in the digikam grouchygiraffe and shamblingshark collections, classifies food-related content from YAML metadata, and applies digikam tags.

Invoke as a Claude Code skill:

```
/moonlitlynx-food-run
```

```sh
# count files currently in the untagged/undated queue
sqlite3 ~/Pictures/digikam4.db "
SELECT COUNT(*) FROM Images i
JOIN Albums al ON al.id = i.album
JOIN AlbumRoots ar ON ar.id = al.albumRoot
LEFT JOIN ImageInformation ii ON ii.imageid = i.id
WHERE ar.label IN ('grouchygiraffe', 'shamblingshark')
AND i.id NOT IN (
  SELECT imageid FROM ImageTags
  WHERE tagid NOT IN (SELECT id FROM Tags WHERE name LIKE 'Color Label%')
)
AND (ii.creationDate IS NULL OR ii.creationDate < '1904-01-01T00:00:00')"

# list the files
sqlite3 ~/Pictures/digikam4.db "
SELECT i.name, ar.label FROM Images i
JOIN Albums al ON al.id = i.album
JOIN AlbumRoots ar ON ar.id = al.albumRoot
LEFT JOIN ImageInformation ii ON ii.imageid = i.id
WHERE ar.label IN ('grouchygiraffe', 'shamblingshark')
AND i.id NOT IN (
  SELECT imageid FROM ImageTags
  WHERE tagid NOT IN (SELECT id FROM Tags WHERE name LIKE 'Color Label%')
)
AND (ii.creationDate IS NULL OR ii.creationDate < '1904-01-01T00:00:00')
ORDER BY ar.label, i.name"

# read YAML for a shortcode
cat /Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/<shortcode>.yaml

# backup the database before tagging
cp ~/Pictures/digikam4.db ~/Pictures/digikam4.db.bak.$(date +%Y%m%d_%H%M%S)

# verify tags applied to a set of files
sqlite3 ~/Pictures/digikam4.db "
SELECT t.name, COUNT(*) FROM ImageTags it
JOIN Tags t ON t.id = it.tagid
JOIN Images i ON i.id = it.imageid
WHERE i.name IN ('DZY_GI9tCs5.mp4', 'DWMQ8l6x9hu.mp4')
GROUP BY t.name"

# check what tags exist under food
sqlite3 ~/Pictures/digikam4.db "SELECT id, name FROM Tags WHERE pid = 109 ORDER BY name"

# check the noyamldesc tag
sqlite3 ~/Pictures/digikam4.db "SELECT id, name, pid FROM Tags WHERE name = 'noyamldesc'"
```
