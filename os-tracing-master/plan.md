# Rust异步函数跟踪与操作系统调试 - 详细工作计划

- **总体目标**

  - 跨多个特权级：应用、内核和 **hypervisor**
  - 支持多种高级语言：Rust、C语言（xv6）
  - **支持 Rust 异步跟踪（编译选项，宏，甚至release，其他运行时）**
  - 支持多种操作系统：ArceOS unikernel、**ArceOS宏内核（starry）、Linux**
  - **rust eBPF in Linux => tracing rust program with async**
  - **jtag in openSBI (coprocessor)**
  - 支持多种CPU平台：RISC-V、x86-64
  - 支持多种开发板：QEMU、**x86 物理机（乾云工控机）**、星光2

1) Starry跟踪 + 调试器本身模块化
    - 调试器本身拆分成语言相关（获取信息，信息展示，高级控制命令）和语言无关两个部分
    - 跟踪 Starry
    - 调试工具原则上已经可以调试这个 OS，因此大部分的工作是改调试器本身的配置文件和编译参数
    - 添加工作 1 和工作 2 的人机交互界面

2) 跟踪 Rust 语言的异步函数（11月）
    - 复现论文工作：总结工作内容，分析不足（例如使用场景受限，可跟踪内容有限，需要做过多instrumentation），找到我们可以做的点（2周） uftrace
    - 使用他人论文的思路，支持其他 runtime （全异步OS）的跟踪调试

3) Linux 跟踪，
    - C / Rust 混合。
    - 写一个支持调试 rust 异步函数的 eBPF，代替 Linux 原有的 eBPF
    - 用第一步模块化的成果

4) 写文章 + 基于协处理器的、真实 x86 硬件上的 OS 调试
    - 单核：hypervisor 启动 OS 和 debugger，debugger 通过 hypervisor 的 API 调试 OS
    - 有协处理器：协处理器上跑 debugger ，CPU 上跑 OS，debugger 调试 CPU 上的 OS
    - 让 debugger 支持 JTAG 协议

5) SBI跟踪（后面同学做）
    - 虚拟机上的SBI跟踪
      1. 扩展 GDB，支持文本终端 GDB 上跟踪 SBI 源代码 
        主要工作：建立机器态内存地址和SBI符号表文件的映射关系。
      2. 扩展 `code-debug` 插件的状态机，从而支持 M 态到 S 态的断点组切换

    - 实际硬件上的SBI跟踪：
      - 支持有jtag的硬件
        主要工作：思路和虚拟机相同，工作量主要集中在调整编译参数上
      - 支持没有jtag的硬件（任务2）
        主要工作：在协处理器上跑 修改版 OpenSBI，该修改版 OpenSBI 能够处理jtag调试命令，并调试运行于主处理器上的OS

- **目标（2025年8月）**：

  - 扩展现有的`code-debug`工具，使其具备追踪Rust异步函数和Linux的能力；
  - 撰写并发表一篇关于本项目的学术论文。

