skills_dir := env('HOME') / ".agents/skills"

default:
    @just --list
repo_skills := justfile_directory() / "skills"

install:
    mkdir -p {{skills_dir}}
    ln -sf {{repo_skills}}/python-package {{skills_dir}}/python-package
    ln -sf {{repo_skills}}/view-imgur {{skills_dir}}/view-imgur
    ln -sf {{repo_skills}}/write-readme {{skills_dir}}/write-readme

uninstall:
    rm -f {{skills_dir}}/python-package
    rm -f {{skills_dir}}/view-imgur
    rm -f {{skills_dir}}/write-readme
