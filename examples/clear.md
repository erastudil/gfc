# Writing before the ledger

When a database writes a change to disk, it does not immediately update its tables and indexes. Searching a tree and rewriting blocks scattered across storage takes multiple random writes, any of which can fail mid-stride if the power cuts.

Instead, the engine appends the operation to a single contiguous file at the end of the disk. Because appending requires only one sequential write, the system flushes it to physical media in milliseconds. If the machine crashes immediately after, rebooting reads that linear record from the last checkpoint forward, replaying each completed entry to reconstruct the tables.

That sequential append file has a name: the write-ahead log.

A contained picture: an airline flight recorder. It logs every control movement as it happens, not a reconstructed story after landing. The rest of this architecture relies on the log sequence numbers and byte offsets, not the black box.
