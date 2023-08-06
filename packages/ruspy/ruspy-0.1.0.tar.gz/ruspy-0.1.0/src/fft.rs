use crate::array::Array;
use num_complex::Complex;
use pyo3::{
    prelude::{pyfunction, PyResult, Python},
};

#[pyfunction]
pub fn fft(_py: Python, array: &Array) -> PyResult<Array> {
    let mut data = array.data.clone();
    let len = data.len();
    if len == 1 {
        return Ok(Array { data });
    }

    // Check if len is a power of two
    if len & (len - 1) != 0 {
        let next_power_of_two = len.next_power_of_two();
        let padding = next_power_of_two - len;
        for _ in 0..padding {
            data.push(Complex::new(0.0, 0.0));
        }
    }

    let len = data.len();  // Get new length after padding

    let mut even = Vec::new();
    let mut odd = Vec::new();
    for i in 0..len {
        if i % 2 == 0 {
            even.push(data[i]);
        } else {
            odd.push(data[i]);
        }
    }

    let even_array = Array { data: even };
    let odd_array = Array { data: odd };

    let even_fft = fft(_py, &even_array)?;
    let odd_fft = fft(_py, &odd_array)?;

    let half_len = len / 2;
    let mut result = Vec::with_capacity(len);
    for _ in 0..len {
        result.push(Complex::new(0.0, 0.0));
    }

    if len > 1 {
        for i in 0..half_len {
            result[i] = even_fft.data[i] + Complex::new(0.0, -2.0 * std::f64::consts::PI * (i as f64) / (len as f64)).exp() * odd_fft.data[i];
            result[i + half_len] = even_fft.data[i] - Complex::new(0.0, -2.0 * std::f64::consts::PI * (i as f64) / (len as f64)).exp() * odd_fft.data[i];
        }
    }

    Ok(Array { data: result })
}
