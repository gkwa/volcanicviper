default:
    just --list

# push to GitHub and update installed skills globally
setup:
    git push
    pnpm dlx skills update --global --yes

# list installed skills to verify deployment
test:
    pnpm dlx skills list

# remove installed volcanicviper skills
teardown:
    pnpm dlx skills remove gkwa/volcanicviper
