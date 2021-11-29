import lmdb

with lmdb.open('./test').begin(write=True) as txn:
    txn.put('key'.encode(), 'value'.encode())

