# usage:
#	make release tag=v2.7.0

release:
	git status
	echo "Abort now if there are files that needs to be committed"
	sleep 5
	git log
	git tag $(tag)
	# enter "v2.7.0"
	git-cliff -c pyproject.toml > CHANGELOG.md
	#toc -lf .tocfiles
	git tag --delete $(tag)
	git add CHANGELOG.md && git commit -m "minor: updated CHANGELOG.md"
	git tag -fa $(tag)
	git push --follow-tags
