use guitar_music_ui::App;
use sycamore::prelude::*;

fn main() {
    sycamore::hydrate(|cx| {
        view! { cx,
            App {}
        }
    })
}

