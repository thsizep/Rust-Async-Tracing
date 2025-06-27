use embassy_executor::Spawner;
use embassy_time::Timer;
use log::*;

#[inline(never)]
fn level_0_await_notify(){
    info!("doing level 0 await");
}

#[inline(never)]
fn level_1_await_notify() {
    info!("doing level 1 await");
}

#[inline(never)]
fn level_2_await_notify() {
    info!("doing level 2 await");
}

#[inline(never)]
fn finish_testing(){
    info!("finish testing");
}

#[inline(never)]
async fn level_2_await() {
    Timer::after_secs(3).await;
}

#[inline(never)]
async fn inside_await() {
    level_2_await_notify();
    level_2_await().await;
    level_1_await_notify();
    Timer::after_secs(5).await;


}

#[embassy_executor::task]
async fn run() {
    Timer::after_secs(7).await;
    info!("run1 done!");
}

#[embassy_executor::task]
async fn run2() {
    level_0_await_notify();
    Timer::after_secs(2).await;
    inside_await().await;
    finish_testing()
}


#[embassy_executor::main]
async fn main(spawner: Spawner) {
    env_logger::builder()
        .filter_level(log::LevelFilter::Debug)
        .format_timestamp_nanos()
        .init();

    spawner.spawn(run()).unwrap();
    spawner.spawn(run2()).unwrap();
}
