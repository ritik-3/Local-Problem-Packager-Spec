use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SchemaVersion {
    pub schema_version: String,
}

pub const CURRENT_SCHEMA_VERSION: &str = "1.0";
