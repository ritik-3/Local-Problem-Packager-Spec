use thiserror::Error;

#[derive(Debug, Error)]
pub enum ValidationError {
    #[error("validation rules not yet implemented")]
    NotImplemented,
}

pub fn validate_mcq_manifest(_raw: &str) -> Result<(), ValidationError> {
    Err(ValidationError::NotImplemented)
}
