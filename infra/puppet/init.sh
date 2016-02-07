#/bin/bash

yum install -y puppet3 rubygems git
gem install r10k

git clone https://github.com/bryantrobbins/baseball
mv baseball/infra/puppet .
rm -rf baseball
pushd puppet

r10k puppetfile install -v
puppet apply site.pp
