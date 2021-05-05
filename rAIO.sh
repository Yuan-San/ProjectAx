#!/bin/sh

echo "Stashing unsaved local changes"
git stash # Git is naughty

echo "Attempting to pull from https://github.com/Dok4440/KaitoBot"
git pull  # pull from the GitHub (likely fails because it's)

echo
echo RESTARTING
echo
pm2 restart KaitoBot 1>/dev/null 2>&1