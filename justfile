default:
    just --list

# push to GitHub and install skills globally
# uses add, not update: update silently skips skills that are not installed yet
setup:
    git push
    pnpm dlx skills add gkwa/volcanicviper --global --yes

# list installed skills to verify deployment
test:
    pnpm dlx skills list

# remove installed volcanicviper skills
teardown:
    pnpm dlx skills remove gkwa/volcanicviper
