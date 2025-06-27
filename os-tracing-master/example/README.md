## async tracing utility examples
这是一个用户态的 embassy 例子 （从 复制），用于演示异步跟踪的思路。

### 如何使用
编译运行
```
oslab@oslab-VMware-Virtual-Platform:~/embassy/examples/std$ cargo run --bin tick
   Compiling embassy-time v0.4.0 (/home/oslab/embassy/embassy-time)
   Compiling embassy-net v0.7.0 (/home/oslab/embassy/embassy-net)
   Compiling embassy-std-examples v0.1.0 (/home/oslab/embassy/examples/std)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 5.12s
     Running `target/debug/tick`
[2025-04-29T01:28:14.601388498Z INFO  tick] doing level 0 await
Timer pending: yielded_once=false, expires_at=Instant { ticks: 1000000 }, now=Instant { ticks: 2 }
Timer expired: yielded_once=true, expires_at=Instant { ticks: 1000000 }, now=Instant { ticks: 1000565 }
[2025-04-29T01:28:15.602287808Z INFO  tick] doing level 2 await
Timer pending: yielded_once=false, expires_at=Instant { ticks: 2000731 }, now=Instant { ticks: 1000732 }
Timer expired: yielded_once=true, expires_at=Instant { ticks: 2000731 }, now=Instant { ticks: 2001332 }
[2025-04-29T01:28:16.602997851Z INFO  tick] doing level 1 await
Timer pending: yielded_once=false, expires_at=Instant { ticks: 3001414 }, now=Instant { ticks: 2001415 }
Timer expired: yielded_once=true, expires_at=Instant { ticks: 3001414 }, now=Instant { ticks: 3002066 }
[2025-04-29T01:28:17.603752524Z INFO  tick] finish testing
^C
```
获取符号表
```
./dump.sh
```
利用关键词过滤异步相关的符号
```
./async_function_list.sh 
```

运行 gdb
```
gdb target/debug/tick
```

自动给异步相关的符号打断点
```
(gdb) source async.py
```

运行被调试程序
```
run
```

打印火焰图的json
```
(gdb) dump_async_log
```

在 Perfetto.dev 加载output-directjson.json

通过对比时间戳：





可以确认所有的异步函数都被执行了。


## Running the `embassy-net` examples

First, create the tap99 interface. (The number was chosen to
hopefully not collide with anything.) You only need to do
this once.

```sh
sudo sh tap.sh
```

Second, have something listening there. For example `nc -lp 8000`

Then run the example located in the `examples` folder:

```sh
cd $EMBASSY_ROOT/examples/std/
sudo cargo run --bin net -- --tap tap99 --static-ip
```

gdb
```
sudo -E /home/oslab/.cargo/bin/cargo clean
sudo -E /home/oslab/.cargo/bin/cargo run --bin net -- --tap tap99 --static-ip
sudo gdb --args ./target/debug/net --tap tap99 --static-ip