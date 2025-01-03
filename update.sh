#!/bin/bash
pushd systeminformer
git fetch
echo "\`\`\`diff" > ../pr-body.md
git diff --exit-code HEAD origin/master -- phnt >> ../pr-body.md
if [ $? -eq 0 ]; then
  echo "[INFO] No changes to commit"
  popd
  exit 0
fi
echo "\`\`\`" >> ../pr-body.md

NEW_HASH=$(git rev-parse --short origin/master)
echo "[INFO] Bumping systeminformer to $NEW_HASH"
git checkout origin/master
popd

echo "[INFO] Checking if bump-$NEW_HASH already exists"
git ls-remote --exit-code --heads origin bump-$NEW_HASH > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "[INFO] Already bumped"
  exit 0
fi

echo "[INFO] Creating pull request"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config user.name "github-actions[bot]"
git checkout -b bump-$NEW_HASH
git commit -am "Bump systeminformer to $NEW_HASH"
git push --set-upstream origin bump-$NEW_HASH
gh pr create --title "Bump systeminformer to $NEW_HASH" --body-file pr-body.md
