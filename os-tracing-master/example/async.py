import json
import gdb
import os
import time # BUG: This is system time, not debugee time!

project_root = "."
result=[] # array of strings
result_object=[] # array of objects
base_addr = int("555555554000", 16)
# result.append("time   thread_id: [entry/exit] FUNCTION_NAME(FUNCTION_ADDR?PC=0x00000000) depth: 0")
# command for logging at function entry
unfinished_async_poll_fn = []


class FunctionEntryLogger(gdb.Command):
    def __init__(self):
        super().__init__("function_entry_logger", gdb.COMMAND_USER)
        self.func_name = "unknown"
        self.depth = -114514
    def invoke(self, arg, from_tty):
        # arg is the function name
        self.func_name = arg
        thread_id = gdb.selected_thread().ptid[1]
        timestamp = time.time()
        frame = gdb.newest_frame()
        self.addr = frame.pc()

        # Get the first function argument named "self"
        try:
            self_arg = frame.read_var("self")
            # Access the '__pointer' member of the 'self' struct
            self_pointer = self_arg['__pointer']
            self_pointer = str(self_pointer)
        except Exception as e:
            self_pointer = None
        
        self.depth = 0
        while frame is not None:
            self.depth += 1
            frame = frame.older()
        # result.append(f"{timestamp:.6f}   {thread_id}: [entry] {self.func_name}({self.addr}) depth: {self.depth}")
        
        result_object.append(
            {
                "time": timestamp,
                "thread_id": thread_id,
                "entry_exit": "entry",
                "fn_name": self.func_name,
                "addr": self.addr,
                "depth": self.depth,
                "self_pointer": self_pointer,
            }
        )

class FunctionReturnBreakpoint(gdb.FinishBreakpoint):
    def __init__(self, func_name):
        super().__init__()
        self.func_name = func_name
        self.depth = -114514
    def stop (self):
        self.log()
        return False
    def out_of_scope(self):
        self.log()
        return
    def log(self):
        thread_id = gdb.selected_thread().ptid[1]
        timestamp = time.time()
        frame = gdb.newest_frame()
        self.addr = frame.pc()

        # Get the first function argument named "self"
        try:
            self_arg = frame.read_var("self")
            # Access the '__pointer' member of the 'self' struct
            self_pointer = self_arg['__pointer']
            self_pointer = str(self_pointer)
        except Exception as e:
            self_pointer = None
        
        self.depth = 0
        while frame is not None:
            self.depth += 1
            frame = frame.older()
        # result.append(f"{timestamp:.6f}   {thread_id}: [exit ] {self.func_name}({self.addr}) depth: {self.depth+1}") # depth + 1 because this is a return breakpoint, you already popped the frame
        result_object.append({
            "time": timestamp,
            "thread_id": thread_id,
            "entry_exit": "exit ",
            "fn_name": self.func_name,
            "addr": self.addr,
            "depth": self.depth+1,
            "self_pointer": self_pointer,
            "return_value": self.return_value,
        })

class RegisterFunctionReturnBreakpoint(gdb.Command):
    def __init__(self):
        super().__init__("register-function-return-breakpoint", gdb.COMMAND_USER)
        self.func_name = "unknown"
    def invoke(self, arg, from_tty):
        # arg is the function name
        self.func_name = arg
        FunctionReturnBreakpoint(self.func_name)


class DumpAsyncLog(gdb.Command):
    def __init__(self):
        super().__init__("dump_async_log", gdb.COMMAND_USER)
    def invoke(self, arg, from_tty):
        print("Dumping async log...")
        trace_events = []
        for entry in result_object:
            ts = entry["time"]
            pid = str(entry["thread_id"])
            tid = f" {entry['thread_id']}"
            name = entry["fn_name"]
            args = {"Function address (For recognizing anonymous type)": f"0x{entry['addr']}"}


            has_self_pointer = False
            has_poll_state = False

            if entry["self_pointer"] is not None:
                has_self_pointer = True
                id_str = entry["self_pointer"]
                # id_str usually looks like "0x555555930118 <tick::run::POOL+64>"
                id = id_str.split("<")[0].strip()
                # turn id into a hex number
                id = int(id, 16)
            
            if "return_value" in entry and entry["return_value"] is not None:
                has_poll_state = True
                poll_state = None
                if entry['return_value'].bytes == b'\x01':
                    poll_state = "Pending"
                elif entry['return_value'].bytes == b'\x00':
                    poll_state = "Ready"
                else:
                    has_poll_state = False

            ph = "B" if entry["entry_exit"] == "entry" else "E"



            is_async_poll = False
            if (ph == "B" and has_self_pointer) or (ph == "E" and has_poll_state): # TODO use the algorithm in the paper to decide if this is async pollx
                is_async_poll = True
                if ph == "B":
                    if id not in unfinished_async_poll_fn:
                        ph = "b" # first poll
                        unfinished_async_poll_fn.append(id)
                    else:
                        ph = "n" # not first poll
                elif ph == "E":
                    if poll_state == "Pending":
                        ph = "n"
                    elif poll_state == "Ready":
                        ph = "e"
                        unfinished_async_poll_fn.remove(id)
                    else:
                        ph = "E"

            trace_event = {
                "ts": ts,
                "ph": ph,
                "pid": pid,
                "tid": tid,
                "name": name,
                "args": args,
            }

            if is_async_poll:
                trace_event["id"] = id
                trace_event["cat"] = "async_poll"
            trace_events.append(trace_event)

        output = {
            "traceEvents": trace_events,
            "displayTimeUnit": "ms"
        }

        with open("output-directjson.json", "w") as json_file:
            json.dump(output, json_file, indent=4)

def get_addr_and_func_name(line:str)->tuple[str, str]:
    parts = line.split()
    if len(parts) >= 2:
        func_addr = "0x"+parts[0]
        func_name = line.strip(parts[0]+" "+parts[1]+" ").strip()
        return func_addr, func_name
    print(f"Invalid line format: {line}")
    return None, None

def register_loggers(symbol_file_path):
    with open(symbol_file_path, "r") as f:
        for line in f:
            (func_addr, func_name) = get_addr_and_func_name(line)
            # gdb.execute(f"""
            #     break *{func_addr}
            #     command
            #     silent
            #     function_entry_logger {func_name}
            #     finish
            #     function_exit_logger {func_name}
            #     continue
            #     end
            # """)
            set_by = "name"
            if set_by == "addr":
                actual_addr = hex(int(func_addr, 16) + base_addr)
                gdb.execute("break *"+actual_addr+"\ncommands\nfunction_entry_logger "+func_name+"\nregister-function-return-breakpoint "+func_name+"\ncontinue\nend")
            elif set_by == "name":
                gdb.execute("break "+func_name+"\ncommands\nfunction_entry_logger "+func_name+"\nregister-function-return-breakpoint "+func_name+"\ncontinue\nend")
            # looks like you can't embed commands in commands, so using finish does not work
            # gdb.execute("break *"+func_addr+"\ncommands\nsilent\nfunction_entry_logger "+func_name+"\nfinish\nfunction_exit_logger "+func_name+"\ncontinue\nend")

FunctionEntryLogger()
RegisterFunctionReturnBreakpoint()
DumpAsyncLog()

register_loggers("async.sym")

