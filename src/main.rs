use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugin(DefaultPlugins)
        .add_system(system);
}

fn hello_world() {
    println!("Hello World!");
}