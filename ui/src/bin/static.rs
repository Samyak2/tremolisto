use std::fs;

use guitar_music_ui::App;
use sycamore::prelude::*;

fn main() {
    let rendered_html = sycamore::render_to_string(|cx| {
        view! { cx,
            App {}
        }
    });
    fs::write("../build/index.html", rendered_html).unwrap();
}
