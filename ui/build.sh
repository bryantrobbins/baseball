#!/bin/bash -v

# Add js build steps here (npm, etc.)
npm install
npm run build

zip -j site.zip dist/
