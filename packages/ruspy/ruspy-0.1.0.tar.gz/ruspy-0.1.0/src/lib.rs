use pyo3::{
    prelude::{pymodule, PyModule, PyResult, Python},
    wrap_pyfunction,
};
mod array;
use array::{array as array_fn, Array};
mod fft;
use fft::{fft as fft_fn};

#[pymodule]
fn ruspy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Array>()?;
    m.add_function(wrap_pyfunction!(array_fn, m)?)?;
    m.add_function(wrap_pyfunction!(fft_fn, m)?)?;
    Ok(())
}
