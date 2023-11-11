use sycamore::prelude::*;

#[component]
pub fn App<G: Html>(cx: Scope) -> View<G> {
    view! { cx,
        h1 { "guitar music" }
    }
}
