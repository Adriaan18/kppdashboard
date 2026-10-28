#!/bin/bash
# test-only PostgreSQL 16 (the scratchpad's parent is root-only, so the data dir lives in /var/tmp; removed after the tests)
D=/var/tmp/kpp-pgtest
if [ ! -d $D/data ]; then
  mkdir -p $D && chown postgres:postgres $D
  su postgres -c "/usr/lib/postgresql/16/bin/initdb -D $D/data -U postgres --auth=trust -E UTF8" >/dev/null 2>&1
fi
if ! psql -h /tmp -p 55432 -U postgres -c "select 1" >/dev/null 2>&1; then
  rm -f $D/data/postmaster.pid
  su postgres -c "/usr/lib/postgresql/16/bin/pg_ctl -D $D/data -o '-p 55432 -k /tmp -c timezone=Pacific/Auckland' -l $D/log.txt start -w" >/dev/null 2>&1
fi
psql -h /tmp -p 55432 -U postgres -lqt 2>/dev/null | grep -q "^ kpp " || psql -h /tmp -p 55432 -U postgres -c "CREATE DATABASE kpp" >/dev/null
psql -h /tmp -p 55432 -U postgres -d kpp -Atc "select 'pg up', current_setting('TimeZone')"
