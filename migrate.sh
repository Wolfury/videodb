#!/bin/bash

SCRIPTDIR=$(realpath $(dirname $0))
TMPDIR=$(mktemp -d)

cp "$1" ${TMPDIR}/
pushd ${TMPDIR} > /dev/null
${SCRIPTDIR}/1-infojson-from-videodb "$1"
${SCRIPTDIR}/3-create-dbjson *info.json -o video.db.json
${SCRIPTDIR}/4-migrate-videodb "$1" video.db.json

# copy output (and error log) to current path
popd > /dev/null
FILE=$(basename "$1")
cp ${TMPDIR}/video.db.json "${FILE%.*}.db.json"
cp ${TMPDIR}/[1-9]-failedEntries.json . 2>/dev/null

rm -rf ${TMPDIR}
