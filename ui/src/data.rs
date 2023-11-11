use std::fs;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Music {
    pub title: String,
    pub artist: String,
    pub url: Option<String>,
    pub parts: Vec<MusicPartWithFile>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MusicPartWithFile {
    pub start: String,
    pub end: String,
    pub typ: String,
    pub extra: String,
}

fn musics_from_json(s: &str) -> Vec<Music> {
    serde_json::from_str(s).unwrap()
}

pub fn musics_from_json_file(filepath: &str) -> Vec<Music> {
    musics_from_json(&fs::read_to_string(filepath).unwrap())
}
