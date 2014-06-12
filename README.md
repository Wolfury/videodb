## videodb

Scripts for creating a database to organize the learning video I've watched.
These scripts requires latest `youtube-dl.py` from http://youtube-dl.org/.

## History

The first version (`create-videodb.py`) was writted in Python, but my Python-fu is elementary and the schema design was a blunder.
The current version is writted in Node and migration scripts are available.

Terminology:
- source
(extractor, video_id) tuple, can be mapped to the clip URL.
- `.info.json`
Description for a video clip created by `youtube-dl.py`.  
It's schema changed so `2-update-infojson` was to update existing `.info.json`.
- `videodb` (`.json`/`videodb.json`)
videodb created by `create-videodb.py`.  
Uses source as key for lookup (which is not orthogonal).
- `dbjson` (`.db.json`)
videodb created by `3-create-dbjson`.

## Scripts

1. download info.json for all videos in videodb
2. update existing info.json
3. convert info.json to dbjson
4. migrate tag and rating from videodb to dbjson

## JSON schema

> corresponding fields in info.json in brackets

```json
{
    [_id]
    video_id (id)
    title
    extractor
    duration
    url (webpage_url)
    uploader (uploader_id)
    upload_date
    thumbnail
    tags
    rating
}
```

## Tags legend

- {presentor/organiztion}
- [playlist/series/conference]
