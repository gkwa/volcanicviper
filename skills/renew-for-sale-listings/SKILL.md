---
name: renew-for-sale-listings
description: "Check every unsold for-sale item on every selling site (Nextdoor, Craigslist, Facebook Marketplace, eBay) and renew the listings that need it, using the Claude in Chrome browser tools in the user's signed-in Chrome. Skips anything the vault records as sold or given away, and never marks sold or deletes. Use when asked to renew the for sale listings, check that all listings are renewed, keep the listings from expiring, or which listings needed renewal."
---

## Renewing listings on every selling site

The work runs in the user's signed-in Chrome through the `mcp__claude-in-chrome__*` tools, so no credentials are needed and none are ever entered.

Read the claude-in-chrome skill first, then load every browser tool in one ToolSearch call, including get_page_text and find.

Open a new tab rather than reusing one, and close it when finished.

## Which items count

The console is /Users/mtm/Documents/Obsidian Vault/selling stuff management console.md.

Each item has its own note tagged forsale, and its `status` front matter field says listed, pending, or sold.

Only items whose status is listed or pending are renewed, because a pickup can fall through.

Never renew an item whose status is sold, even if a site still shows it live; report that mismatch instead.

The selling sites are the notes with a `selling_url` front matter field, and each site's `selling_url` is where its listings are checked.

Find the items with one rg over the vault root for `^status:` and keep the files that also carry the forsale tag.

## Nextdoor

Follow the nextdoor-renew-listings skill, which renews only listings labeled Expiring.

Also open the Expired tab, because a listing that already expired drops out of Selling.

## Craigslist

The account home page lists every posting with its status, renewed date, and days left in the exp. column.

Always renew with the renew all link rather than renewing postings one at a time.

Before clicking it, check that every Active posting is an unsold item, because renew all renews them all; if a sold item is still Active, report it and do not click.

Afterwards, confirm every Active posting shows today's renewed date.

## Facebook Marketplace

The selling URL redirects to the seller listings table.

A listing that can be renewed shows Renew in its Actions column instead of Promote or View messages.

Click each Renew, which raises no dialog and confirms with a Your listing has been renewed toast, and the button then turns into Promote.

A Messenger chat popup can open in the lower right and cover the Renew buttons, so minimize it with its dash button before clicking, never close or type in it.

Clicking a covered button can hit a link inside the chat and open a stray tab; close that tab and retry.

Confirm afterwards with find that no Renew buttons remain.

## eBay

Good 'Til Cancelled listings show Auto-renews in N on the active page and need nothing.

A listing without that line, or a missing item, is reported rather than relisted.

## The reply

Lead with which listings were renewed, grouped by site, each with its price.

Then say in one line per site that the rest needed nothing.

Report any listing that is live on a site but sold in the vault, or unsold in the vault but missing from a site.

If something seen on a site settles an open checkbox in the console, say so and offer to check it, rather than checking it unasked.
