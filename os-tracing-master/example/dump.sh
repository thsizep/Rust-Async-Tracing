# arm-none-eabi-objdump -t target/thumbv7em-none-eabi/debug/blinky | rustfilt > symbol.sym
# nm target/debug/tick | rustfilt > symbol.sym
nm target/debug/tick > symbol.sym