---
name: instagram-to-imgur
description: Download the thumbnail/cover image from an Instagram post and upload it to Imgur, returning a permanent URL. Use when the user shares an Instagram URL and wants a permanent image link.
---

## Requirements

- `uvx` (comes with `uv`) — used to run `yt-dlp` without installing it
- `IMGUR_CLIENT_ID` environment variable — set in `~/.zshenv`:

```
export IMGUR_CLIENT_ID=your_client_id_here
```

To generate a Client ID, register a new application at https://api.imgur.com/oauth2/addclient

Choose "OAuth 2 authorization without a callback URL" as the authorization type.

The Client ID is shown immediately after registration — no secret is needed for anonymous uploads.

## Instagram to Imgur Workflow

When the user shares an Instagram URL and wants a permanent image URL, follow these steps.

### Step 1: Get the thumbnail URL

```
uvx yt-dlp --get-thumbnail "<instagram_url>"
```

Save the output — it is the expiring CDN URL for the cover image.

### Step 2: Download the image

```
curl -sL "<thumbnail_url>" -o /tmp/image.jpg
```

Verify it is a JPEG:

```
file /tmp/image.jpg
```

If the file is not a JPEG, stop and tell the user what file type was returned.

### Step 3: Upload to Imgur

Requires the `IMGUR_CLIENT_ID` environment variable to be set.

If it is not set, stop and tell the user to add it to `~/.zshenv`:

```
export IMGUR_CLIENT_ID=your_client_id_here
```

Upload:

```
curl -s -X POST -H "Authorization: Client-ID $IMGUR_CLIENT_ID" -F "image=@/tmp/image.jpg" https://api.imgur.com/3/image
```

### Step 4: Extract and return the URL

Parse the JSON response and extract the `link` field.

Print the permanent Imgur URL to the user.

If the upload fails, show the full API response so the user can debug.
