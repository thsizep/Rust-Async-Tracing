# os-tracing

[工作计划](./plan.md)

本计划旨在实现对Rust异步函数和 Linux 操作系统的调试跟踪。最终愿景是用户可以在`code-debug` 操作系统调试工具中利用 GDB 跟踪 Linux，利用 eBPF 跟踪Rust 异步函数（这个异步函数可能运行于内核态，也可能运行于用户态）。

async rust 跟踪难点：

  - rust 自身没有支持完整的异步功能，无官方 async runtime。rust 自身只负责处理 async 语法糖（见第三点），具体的调度功能由第三方 runtime (tokio, async-std) 实现
  - gdb 不能跟踪宏，而 runtime 用大量宏，因此很难用 gdb 跟踪异步rust，必须用 eBPF
  - 最末端的 async 函数只有 ready 和 pending 两个状态，嵌套的 async 函数按照 await 被分割成多份，每一份都是一个状态（见 <[https://www.eventhelix.com/rust/rust-to-assembly-async-await/](https://www.eventhelix.com/rust/rust-to-assembly-async-await/)> ）
  
参考对象：

- tokio - console
- [Improving Debugging For *Optimized* Rust Code On Embedded Systems](https://www.diva-portal.org/smash/get/diva2:1720169/FULLTEXT01.pdf)
    - 支持 rust 宏
    - 支持调试优化后的 rust 代码
    - 不支持调试异步函数
- https://www.eventhelix.com/rust/rust-to-assembly-async-await/

## todo

- （1周）调研异步跟踪可以怎么做（读paper）
- 列一个宏观的细化到明年8月底的计划。就像写文献综述那样。包括异步+linux
- 修改编译器/在源代码里添加宏的做法在 release 不能用，因为 release 版编译器会对状态机代码进行 inline

## paper - list

- Automatic Tracing in Task-Based Runtime Systems
- CAT: Context Aware Tracing for Rust Asynchronous Programs