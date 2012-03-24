#coding:utf-8

import settings
from pymongo.collection import Collection
from pymongo.connection import Connection
from pymongo.database import Database
from pymongo import (helpers,
                     message)

class CollectionObject(Collection):
    
    def _get_id(self):
        result = self.database.eval('db.ids.findAndModify({update:{$inc:{id:1}}, query:{name:"%s"}, new:true})'%self.name)
        return int(result['id'])

    def save(self, to_save, manipulate=True, safe=False, **kwargs):
        """Save a document in this collection.

        If `to_save` already has an ``"_id"`` then an :meth:`update`
        (upsert) operation is performed and any existing document with
        that ``"_id"`` is overwritten.  Otherwise an ``"_id"`` will be
        added to `to_save` and an :meth:`insert` operation is
        performed. Returns the ``"_id"`` of the saved document.

        Raises :class:`TypeError` if `to_save` is not an instance of
        :class:`dict`. If `safe` is ``True`` then the save will be
        checked for errors, raising
        :class:`~pymongo.errors.OperationFailure` if one
        occurred. Safe inserts wait for a response from the database,
        while normal inserts do not.

        Any additional keyword arguments imply ``safe=True``, and will
        be used as options for the resultant `getLastError`
        command. For example, to wait for replication to 3 nodes, pass
        ``w=3``.

        :Parameters:
          - `to_save`: the document to be saved
          - `manipulate` (optional): manipulate the document before
            saving it?
          - `safe` (optional): check that the save succeeded?
          - `**kwargs` (optional): any additional arguments imply
            ``safe=True``, and will be used as options for the
            `getLastError` command

        .. versionadded:: 1.8
           Support for passing `getLastError` options as keyword
           arguments.

        .. mongodoc:: insert
        """
        if not isinstance(to_save, dict):
            raise TypeError("cannot save object of type %s" % type(to_save))

        if "id" not in to_save:
            return self.insert(to_save, manipulate, safe, **kwargs)
        else:
            self.update({"id": to_save["id"]}, to_save, True,
                        manipulate, safe, **kwargs)
            return to_save.get("id", None)
    

    def insert(self, doc_or_docs,
               manipulate=True, safe=False, check_keys=True, **kwargs):
        """Insert a document(s) into this collection.

        If `manipulate` is set, the document(s) are manipulated using
        any :class:`~pymongo.son_manipulator.SONManipulator` instances
        that have been added to this
        :class:`~pymongo.database.Database`. Returns the ``"_id"`` of
        the inserted document or a list of ``"_id"`` values of the
        inserted documents.  If the document(s) does not already
        contain an ``"_id"`` one will be added.

        If `safe` is ``True`` then the insert will be checked for
        errors, raising :class:`~pymongo.errors.OperationFailure` if
        one occurred. Safe inserts wait for a response from the
        database, while normal inserts do not.

        Any additional keyword arguments imply ``safe=True``, and
        will be used as options for the resultant `getLastError`
        command. For example, to wait for replication to 3 nodes, pass
        ``w=3``.

        :Parameters:
          - `doc_or_docs`: a document or list of documents to be
            inserted
          - `manipulate` (optional): manipulate the documents before
            inserting?
          - `safe` (optional): check that the insert succeeded?
          - `check_keys` (optional): check if keys start with '$' or
            contain '.', raising :class:`~pymongo.errors.InvalidName`
            in either case
          - `**kwargs` (optional): any additional arguments imply
            ``safe=True``, and will be used as options for the
            `getLastError` command

        .. versionadded:: 1.8
           Support for passing `getLastError` options as keyword
           arguments.
        .. versionchanged:: 1.1
           Bulk insert works with any iterable

        .. mongodoc:: insert
        """
        docs = doc_or_docs
        return_one = False
        if isinstance(docs, dict):
            return_one = True
            if self.name != 'ids':
                docs['id']=self._get_id()
            docs = [docs]

        if manipulate:
            docs = [self.database._fix_incoming(doc, self) for doc in docs]

        if kwargs:
            safe = True
        self.database.connection._send_message(
            message.insert(self.full_name, docs,
                           check_keys, safe, kwargs), safe)

        ids = [doc.get("_id", None) for doc in docs]
        return return_one and ids[0] or ids
    
class DatabaseObject(Database):
    
    def __getattr__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        return CollectionObject(self, name)

    def __getitem__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        return self.__getattr__(name)
#    
#    def _fix_incoming(self, son, collection):
#        super(Database, self)._fix_incoming(son, collection)
    
class ConnectionObject(Connection):
    
    def __getattr__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        return DatabaseObject(self, name)

    def __getitem__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        return self.__getattr__(name)

try:    
    connection = ConnectionObject("mongodb://%s:%s" % (settings.DBHOST, settings.DBPORT))
except Exception, e:
    raise Exception('Can not Connect the database!')

db = DatabaseObject(connection, settings.DBNAME)

def get_col_handler(collection):
    col = CollectionObject(db, collection)
    return col