#!/bin/bash

SCRIPT_NAME=`basename $0`
SCRIPT_DIR=$(realpath $(dirname $0))
if [[ -z "$1" ]]; then
	echo "Usage:"
	echo "  ${SCRIPT_NAME} videodb.json"
	exit 1
fi

TMPDIR=$(mktemp -d)
TMPDBJSON="migrate-video.db.json"

# work in TMPDIR
cp "$1" ${TMPDIR}/
pushd ${TMPDIR} > /dev/null
${SCRIPT_DIR}/1-infojson-from-videodb "$1"
${SCRIPT_DIR}/3-create-dbjson *info.json -o ${TMPDBJSON}
${SCRIPT_DIR}/4-migrate-videodb "$1" ${TMPDBJSON}

# copy output (and error logs) to current path
popd > /dev/null
FILE=$(basename "$1")
cp ${TMPDIR}/${TMPDBJSON} "${FILE%.*}.db.json"
cp ${TMPDIR}/[1-9]-failedEntries.json . 2>/dev/null

rm -rf ${TMPDIR}
