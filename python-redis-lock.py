#!/usr/bin/env/python
#-*- coding:utf-8 -*-
import redis,time
  
rc = redis.Redis(host='localhost',port=6379,db=3)  


LOCK_TIMEOUT = 3
lock = 0
lock_timeout = 0
lock_key = 'lock.foo'

def do_job():
    print "do job"
    time.sleep(2)
    print "job done"

# 获取锁
while lock != 1:
    now = int(time.time())
    lock_timeout = now + LOCK_TIMEOUT + 1
    lock = rc.setnx(lock_key, lock_timeout)
    if lock == 1 or (now > int(rc.get(lock_key))) and now > int(rc.getset(lock_key, lock_timeout)):
        print "get lock"
        break
    else:
        time.sleep(0.001)

# 已获得锁
do_job()

# 释放锁
now = int(time.time())
if now < lock_timeout:
    print "release lock"
    rc.delete(lock_key)
else:
    print "lock timeout"
