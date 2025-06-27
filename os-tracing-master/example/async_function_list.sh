# cat symbol.sym | grep -E "time" |grep -E "<async_std..task..builder..SupportTaskLocals<.*> as core..future..future..Future>::poll::\{closure.*\}|<core..future..from_generator..GenFuture<.*> as core..future..future..Future>::poll|.*::\{closure.*\}|.*as core..future..future..Future>::poll|executor" | grep -vi "bpf|btree" > async.sym

# cat symbol.sym |grep -E "<async_std..task..builder..SupportTaskLocals<.*> as core..future..future..Future>::poll::\{closure.*\}|<core..future..from_generator..GenFuture<.*> as core..future..future..Future>::poll|.*::\{closure.*\}|.*as core..future..future..Future>::poll|executor" | grep -vi "bpf|btree" > async.sym

# cat symbol.sym |grep -E ".*::\{closure.*\}|.*as core..future..future..Future>::poll" | grep -vi "bpf|btree" > async.sym

# cat symbol.sym |grep -E "closure|poll" | grep -vi "poll@GLIBC" > async.sym

cat symbol.sym |grep -E "poll|notify" | grep -vi "GLIBC" > async.sym
cat async.sym | rustfilt > async_demangled.sym