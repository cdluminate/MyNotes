Git tips
===

## Automatic pushing after commit

```
vim .git/hooks/post-commit
> git push --mirror origin
chmod +x .git/hooks/post-commit
```

## Completely Remove Files from History

https://help.github.com/en/articles/removing-sensitive-data-from-a-repository

```
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <PATH>" --prune-empty --tag-name-filter cat -- --all
```

## Dealing with annoying windows line ending

https://stackoverflow.com/questions/39076854/why-does-git-keep-messing-with-my-line-endings
