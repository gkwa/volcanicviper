export const meta = {
  name: 'ingest-new-instagram-recipes',
  description: 'grouchygiraffe-ingest newly archived Instagram posts, deduped against the vault, with serialized Imgur uploads',
  phases: [
    { title: 'Identify', detail: 'recipe lookup + vault dedup per shortcode' },
    { title: 'Upload', detail: 'serialized Imgur upload of local _thumb.jpg' },
    { title: 'Write', detail: 'recipe-cleanup, set pic, commit' },
  ],
}

const DATA = '/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data'
const VAULT = '/Users/mtm/Documents/Obsidian Vault'

const ID_SCHEMA = {
  type: 'object',
  properties: {
    shortcode: { type: 'string' },
    mediaPath: { type: 'string' },
    isRecipe: { type: 'boolean' },
    skipReason: { type: 'string', description: 'why this should not be ingested (not a recipe, or already in the vault as <note>), empty otherwise' },
    recipeName: { type: 'string' },
    authorName: { type: 'string' },
    instagramHandle: { type: 'string' },
    instagramUrl: { type: 'string' },
    recipeUrl: { type: 'string', description: 'direct recipe URL, or the Instagram URL if the recipe lives only in the caption' },
    targetNotePath: { type: 'string', description: 'absolute vault path the note will be written to' },
    existingPic: { type: 'string', description: 'permanent i.imgur.com pic recovered from an existing note or its git history, empty if none' },
  },
  required: ['shortcode', 'isRecipe', 'skipReason', 'recipeName', 'authorName', 'instagramHandle', 'instagramUrl', 'recipeUrl', 'targetNotePath', 'existingPic', 'mediaPath'],
}

const UP_SCHEMA = {
  type: 'object',
  properties: { imgurUrl: { type: 'string' }, error: { type: 'string' } },
  required: ['imgurUrl', 'error'],
}

const OUT_SCHEMA = {
  type: 'object',
  properties: {
    shortcode: { type: 'string' },
    status: { type: 'string', enum: ['written', 'skipped', 'failed'] },
    notePath: { type: 'string' },
    recipeName: { type: 'string' },
    author: { type: 'string' },
    pic: { type: 'string' },
    commit: { type: 'string' },
    notes: { type: 'string' },
  },
  required: ['shortcode', 'status', 'notePath', 'recipeName', 'author', 'pic', 'commit', 'notes'],
}

let chain = Promise.resolve()
function serial(fn) {
  const p = chain.then(fn)
  chain = p.catch(() => null)
  return p
}

const results = await pipeline(
  args,
  code => agent(
    `Identify the grouchygiraffe post with shortcode ${code}. Its files are in ${DATA} (${code}.yaml, ${code}_thumb.jpg, and ${code}.mp4 or ${code}.jpg — list ${DATA}/${code}* to find the media file).
Invoke the grouchygiraffe-recipe-lookup skill on the media file to get the recipe name, author name, Instagram handle, Instagram URL, and direct recipe URL. If the full recipe lives only in the caption, the recipe URL is the Instagram URL.
If the post is not a recipe at all, set isRecipe=false and explain in skipReason.
Then dedup against the vault at ${VAULT}: the shortcode itself is known to be absent, but the same dish by the same creator may already exist from another source (YouTube, their blog, a sibling post). Search by creator handle and dish keywords with rg over *.md filenames and contents. If a note for the same dish by the same creator already exists, set skipReason to 'duplicate of <absolute path>' — do NOT plan an overwrite.
Pick targetNotePath following the vault convention '<handle> <dish name lowercase>.md' (look at existing notes for this creator, e.g. julieandamy notes, for the handle form used). If that path already exists or appears in git history (git log --all --format=%h -- "<name>.md"), read it/its last version and recover any i.imgur.com pic into existingPic.
Do not write or modify any file. Return the structured result.`,
    { label: `identify:${code}`, phase: 'Identify', schema: ID_SCHEMA }
  ),
  id => {
    if (!id || !id.isRecipe || id.skipReason) return id
    if (id.existingPic) return { ...id, pic: id.existingPic }
    return serial(() => agent(
      `Upload the local file ${DATA}/${id.shortcode}_thumb.jpg to Imgur and return the direct i.imgur.com URL. Upload the archived local thumbnail from disk — do not refetch from Instagram. Use the Imgur Client ID from Keychain service "imgur-api" (security find-generic-password -s imgur-api -w), never register or switch Client IDs. POST to https://api.imgur.com/3/image. If that 429s/503s, the block is by egress IP: fall back to the logged-in web upload at https://imgur.com/upload in Chrome (claude-in-chrome tools, file_upload into the type=file input, read the i.imgur.com img src). Verify the resulting URL returns 200 with curl --head. If all fails, return imgurUrl empty and the error. Do not touch any vault file.`,
      { label: `upload:${id.shortcode}`, phase: 'Upload', schema: UP_SCHEMA }
    )).then(u => ({ ...id, pic: u?.imgurUrl || '', uploadError: u?.error || '' }))
  },
  (id, code) => {
    if (!id) return { shortcode: code, status: 'failed', notePath: '', recipeName: '', author: '', pic: '', commit: '', notes: 'identify stage returned nothing' }
    if (!id.isRecipe || id.skipReason) return { shortcode: code, status: 'skipped', notePath: id.targetNotePath, recipeName: id.recipeName, author: id.authorName, pic: '', commit: '', notes: id.skipReason || 'not a recipe' }
    return agent(
      `Write the vault recipe note for grouchygiraffe shortcode ${code} (this is Step 3 of the grouchygiraffe-ingest workflow; Steps 1 and 2 are already done).
Facts from lookup: recipe "${id.recipeName}" by ${id.authorName} (@${id.instagramHandle}); Instagram post ${id.instagramUrl}; recipe source ${id.recipeUrl}; target note ${id.targetNotePath}; archived caption in ${DATA}/${code}.yaml.
Invoke the recipe-cleanup skill with the recipe source URL (if it is the Instagram URL, use the caption in the yaml as the recipe text). Write the note at the target path; if the file already exists, read it first and carry forward its caption/notes rather than blindly overwriting — never overwrite a note for a different recipe.
Set the pic frontmatter field to ${id.pic ? id.pic : "blank (Imgur upload failed: " + id.uploadError + ") — never an expiring Instagram CDN URL"}.
Ensure the note references the Instagram post URL ${id.instagramUrl} so the shortcode ${code} is findable by rg. If recipe-cleanup creates a creator hub note, include it.
Commit each new/changed note: new files need git add -- "<path>" then git commit -- "<path>" -m "<message>"; never a bare git commit (other processes commit to this repo concurrently). If commit says nothing to commit, check git log -1 -- "<path>" — an auto-committer may have swept it, which is fine. Report the commit hash.`,
      { label: `write:${code}`, phase: 'Write', schema: OUT_SCHEMA }
    )
  }
)

return results
