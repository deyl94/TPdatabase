#Thread.remove
Mark thread as removed

## Supported request methods 
* POST

##Supported formats
* json

##Arguments


###Requried
* thread

   ```int``` thread id of this post


Requesting http://some.host.ru/db/api/s.stupnikov/thread/remove/ with **{'thread': 504}**:
```json
{u'code': 0, u'response': {u'thread': 504}}
```
