from datetime import datetime
from models.LocalTimeZone import LocalTimezone

createdDatetime =datetime.strptime("2019-12-25T17:44:31.202Z","%Y-%m-%dT%H:%M:%S.%fZ")
myTimezone = LocalTimezone()
createdDatetime =createdDatetime.replace(tzinfo=myTimezone)
createdDatetime = myTimezone.fromutc(createdDatetime)