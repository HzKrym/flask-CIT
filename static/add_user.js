const button = document.getElementById('submit_button')

  button.addEventListener('click', async _ => {
    const name_field = document.getElementById('name_field').value
    const fullname_field = document.getElementById('fullname_field').value

    try {
      const response = await fetch('user', {
        method: 'post',
        body: JSON.stringify({
          'name': name_field,
          'fullname': fullname_field
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8'
        }
      })
      const result = await response.json();
      alert(result.message);
  } catch (err) {
    alert(`Error: ${err}`);
  }
})
