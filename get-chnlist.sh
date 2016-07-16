#!/bin/sh
if [ $# -eq 2 ]
then
    SERVER_CONF=$1
    IPSET_CONF=$2
else
    echo "Usage: $0 server.conf ipset.conf"
    exit 1
fi
DNS=114.114.114.114
PORT=53
IPSET=chn
URL='https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf'
TMP_SERVER_CONF=$(mktemp)
TMP_IPSET_CONF=$(mktemp)
echo "# updated on $(date +"%Y-%m-%d %H:%M:%S %Z")"> ${TMP_SERVER_CONF}
curl -s ${URL} |grep -v '^#'|sed -e "s/114.114.114.114/${DNS}#${PORT}/" >> ${TMP_SERVER_CONF}
sed ${TMP_SERVER_CONF} -e "s/server/ipset/" -e "s/${DNS}#${PORT}/${IPSET}/" >> ${TMP_IPSET_CONF}
mv -f ${TMP_SERVER_CONF} ${SERVER_CONF}
mv -f ${TMP_IPSET_CONF} ${IPSET_CONF}
