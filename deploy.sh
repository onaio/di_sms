#!/bin/bash
cd /home/di_sms/app-versioned
. /home/di_sms/di_sms-venv/bin/activate
export TIMESTAMP=`date "+%s"`
git clone git@github.com:onaio/di_sms.git $TIMESTAMP
cd $TIMESTAMP
git checkout origin/$1 || git checkout origin/master
cp /home/di_sms/app/di_sms/local_settings.py di_sms
python manage.py syncdb --settings=di_sms.local_settings --noinput
python manage.py migrate --settings=di_sms.local_settings --noinput
python manage.py collectstatic --settings=di_sms.local_settings --noinput
chown -R di_sms /home/di_sms/app-versioned/$TIMESTAMP
unlink /home/di_sms/app
ln -s /home/di_sms/app-versioned/$TIMESTAMP /home/di_sms/app
restart di_sms
service nginx restart

