from ZODB.RelStorage import RelStorage
from ZODB.DB import DB
import transaction

storage = RelStorage('/tmp/Data.fs')
db = DB(storage)
connection = db.open()
root = connection.root()
