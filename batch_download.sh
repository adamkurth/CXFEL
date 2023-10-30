#!/bin/bash
# Check if 'wget' is available
if ! command -v wget &> /dev/null
then
    echo "'wget' could not be found. You need to install 'wget' for this script to work."
    exit 1
fi

PROGNAME=$0
BASE_URL="https://files.rcsb.org/downloads"

usage() {
  cat << EOF >&2
Usage: $PROGNAME -f <file> [-o <dir>] [-c] [-p] [-m]

 -f <file>: the input file containing a comma-separated list of PDB IDs
 -o  <dir>: the output dir, default: current dir
 -c       : download a cif.gz file for each PDB ID
 -p       : download a pdb.gz file for each PDB ID (not available for large structures)
 -a       : download a pdb1.gz file (1st bioassembly) for each PDB ID (not available for large structures)
 -x       : download a xml.gz file for each PDB ID
 -s       : download a sf.cif.gz file for each PDB ID (diffraction only)
 -m       : download a mr.gz file for each PDB ID (NMR only)
 -r       : download a mr.str.gz for each PDB ID (NMR only)
 -mtz     : download a mtz file for each PDB ID (if available)
EOF
  exit 1
}

download() {
  url="$BASE_URL/$1"
  out="$2/$1"
  echo "Downloading $url to $out"
  wget -q -O "$out" "$url" || echo "Failed to download $url"
}

listfile=""
outdir="."
cif=false
pdb=false
pdb1=false
xml=false
sf=false
mr=false
mrstr=false
mtz=false
while getopts f:o:cpaxsmrmtz o
do
  case $o in
    (f) listfile=$OPTARG;;
    (o) outdir=$OPTARG;;
    (c) cif=true;;
    (p) pdb=true;;
    (a) pdb1=true;;
    (x) xml=true;;
    (s) sf=true;;
    (m) mr=true;;
    (r) mrstr=true;;
    (mtz) mtz=true;;
    (*) usage
  esac
done
shift "$((OPTIND - 1))"

if [ "$listfile" == "" ]
then
  echo "Parameter -f must be provided"
  exit 1
fi
contents=$(cat $listfile)
# see https://stackoverflow.com/questions/918886/how-do-i-split-a-string-on-a-delimiter-in-bash#tab-top
IFS=',' read -ra tokens <<< "$contents"

for token in "${tokens[@]}"
do
  if [ "$cif" == true ]
  then
    download ${token}.cif.gz $outdir
  fi
  if [ "$pdb" == true ]
  then
    download ${token}.pdb.gz $outdir
  fi
  if [ "$pdb1" == true ]
  then
    download ${token}.pdb1.gz $outdir
  fi
  if [ "$xml" == true ]
  then
    download ${token}.xml.gz $outdir
  fi
  if [ "$sf" == true ]
  then
    download ${token}-sf.cif.gz $outdir
  fi
  if [ "$mr" == true ]
  then
    download ${token}.mr.gz $outdir
  fi
  if [ "$mrstr" == true ]
  then
    download ${token}_mr.str.gz $outdir
  fi
  if [ "$mtz" == true ]
  then
    download ${token}.mtz $outdir
  fi