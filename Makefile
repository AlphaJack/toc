# usage:
#	make release tag=2.7.0

#In case a tag has been pushed to GitHub, but the release failed, run `
#	git tag --delete v2.7.0
#	git push --delete origin v2.7.0
# and repeat the steps below

release:
	python -m pytest
	mypy .
	black .
	git status
	grep -q $(tag) pyproject.toml || sed -i pyproject.toml -e "s|version = .*|version = \"$(tag)\"|" && git add pyproject.toml
	echo "Abort now if there are files that needs to be committed"
	sleep 10
	git tag v$(tag) -m "v$(tag)"
	# enter "v2.7.0"
	git-cliff -c pyproject.toml > CHANGELOG.md
	#toc -lf .tocfiles
	git tag --delete v$(tag)
	git add CHANGELOG.md && git commit -m "minor: updated CHANGELOG.md"
	git tag -fa v$(tag) -m "v$(tag)"
	git push --follow-tags
