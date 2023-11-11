mod data;

use data::{musics_from_json_file, Music};
use leptos::*;

#[component]
fn App(all_musics: Vec<Music>) -> impl IntoView {
    let (musics, set_musics) = create_signal(all_musics.clone());

    println!("{:?}", all_musics);

    view! {
        <For
            each=musics
            key=|state| format!("{} - {}", state.title, state.artist)
            let:music
        >
            <p>{music.title} - {music.artist}</p>
        </For>
    }
}

fn main() {
    let all_musics = musics_from_json_file("musics.json");
    mount_to_body(move || view! { <App  all_musics=all_musics.clone()/> })
}
