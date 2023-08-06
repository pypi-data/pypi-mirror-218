tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

dist:
	rm -rf $@
	python setup.py sdist bdist_wheel

publish-test: dist
	twine upload --repository testpypi dist/*

publish: dist
	twine upload dist/*

test: 
	tox

coverage: test
	coverage report

.PHONY: dist
